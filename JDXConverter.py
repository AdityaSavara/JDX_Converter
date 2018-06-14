from numpy import array, linspace, amin, amax, alen, append, arange, float64, logical_and, log10
import re
import string
import pdb
from math import log10

'''
JDXConverter.py is a derivative work of JCamp software built by Nathan Hagen and shared on GithHub.
The following License applies only to this file. 

Copyright (c) 2013 Nathan Hagen

LICENSE
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
END OF LICENSE
'''


'''
jcamp.py contains functions useful for parsing JCAMP-DX formatted files containing spectral data. The main
function `JCAMP_reader()` formats the input file into a Python dictionary, while `JCAMP_calc_xsec()`
converts a given JCAMP-style data dictionary from absorption units to cross-section (m^2).
'''

__all__ = ['JCAMP_reader', 'JCAMP_calc_xsec', 'is_float']

##=====================================================================================================
def JCAMP_reader(filename):
    '''
    Read a JDX-format file, and return a dictionary containing the header info, a 1D numpy vectors `x` for
    the abscissa information (e.g. wavelength or wavenumber) and `y` for the ordinate information (e.g.
    transmission).

    Parameters
    ----------
    filename : str
        The JCAMP-DX filename to read.

    Returns
    -------
    jcamp_dict : dict
        The dictionary containing the header and data vectors.
    '''

    f = open(filename, 'r')
    jcamp_dict = {}
    xstart = []
    xnum = []
    y = []
    x = []
    datastart = False
    values_pattern = re.compile('\s*\w\s*')
    jcamp_numbers_pattern = re.compile(r'([+-]?\d+\.\d*)|([+-]?\d+)')

    for line in f:
        if not line.strip(): continue
        if line.startswith('$$'): continue

        ## Lines beginning with '##' are header lines.
        if line.startswith('##'):
            line = line.strip('##')
            (lhs,rhs) = line.split('=', 1)
            lhs = lhs.strip().lower()
            rhs = rhs.strip()
            continuation = rhs.endswith('=')

            if rhs.isdigit():
                jcamp_dict[lhs] = int(rhs)
            elif is_float(rhs):
                jcamp_dict[lhs] = float(rhs)
            else:
                jcamp_dict[lhs] = rhs

            if (lhs in ('xydata','xypoints','peak table')):
                datastart = True
                datatype = rhs
                continue        ## data starts on next line
            elif (lhs == 'end'):
                datastart = False

        if datastart and (datatype == '(X++(Y..Y))'):
            ## If the line does not start with '##' or '$$' then it should be a data line.
            ## The pair of lines below involve regex splitting on floating point numbers and integers. We can't just
            ## split on spaces because JCAMP allows minus signs to replace spaces in the case of negative numbers.
            new = re.split(jcamp_numbers_pattern, line.strip())
            new = [n for n in new if n != '' and n is not None]
            datavals = [n for n in new if n.strip() != '']

            if not all(is_float(datavals)): continue
            xstart.append(float(datavals[0]))
            xnum.append(len(datavals)-1)
            for dataval in datavals[1:]:
                y.append(float(dataval))
        elif datastart and (('xypoints' in jcamp_dict) or ('xydata' in jcamp_dict)) and (datatype == '(XY..XY)'):
            datavals = [v.strip() for v in line.split(',')]     ## split at commas and remove whitespace
            if not all(is_float(datavals)): continue
            datavals = array(datavals)
            x.extend(datavals[0::2])        ## every other data point starting at the zeroth
            y.extend(datavals[1::2])        ## every other data point starting at the first
        elif datastart and ('peak table' in jcamp_dict) and (datatype == '(XY..XY)'):
            line = line.replace(',',' ')
            datavals = [v.strip() for v in line.split(' ') if v]  ## be careful not to allow empty strings
            #datavals = values_pattern.split(line)
            #datavals = [v for v]
            #print('datavals=', datavals)
            if not all(is_float(datavals)): continue
            datavals = array(datavals)
            x.extend(datavals[0::2])        ## every other data point starting at the zeroth
            y.extend(datavals[1::2])        ## every other data point starting at the first

    if ('xydata' in jcamp_dict) and (jcamp_dict['xydata'] == '(X++(Y..Y))'):
        ## You got all of the Y-values. Next you need to figure out how to generate the missing X's...
        ## First look for the "lastx" dictionary entry. You will need that one to finish the set.
        xstart.append(jcamp_dict['lastx'])
        x = array([])
        for n in range(len(xnum)):
            x = append(x, linspace(xstart[n],xstart[n+1],xnum[n]))
        y = array(y)
    else:
        x = array([float(xval) for xval in x])
        y = array([float(yval) for yval in y])

    ## The "xfactor" and "yfactor" variables contain any scaling information that may need to be applied
    ## to the data. Go ahead and apply them.
    if ('xfactor' in jcamp_dict): x = x * jcamp_dict['xfactor']
    if ('yfactor' in jcamp_dict): y = y * jcamp_dict['yfactor']
    jcamp_dict['x'] = x
    jcamp_dict['y'] = y

    return(jcamp_dict)

##=====================================================================================================
def JCAMP_calc_xsec(jcamp_dict, wavemin=None, wavemax=None, skip_nonquant=True, debug=False):
    '''
    Taking as input a JDX file, extract the spectrum information and transform the absorption spectrum
    from existing units to absorption cross-section.

    This function also corrects for unphysical data (such as negative transmittance values, or
    transmission above 1.0), and calculates absorbance if transmittance given. Instead of a return
    value, the function inserts the information into the input dictionary.

    Parameters
    ----------
    jcamp_dict : dict
        A JCAMP spectrum dictionary.
    wavemin : float, optional
        The shortest wavelength in the spectrum to limit the calculation to.
    wavemax : float, optional
        The longest wavelength in the spectrum to limit the calculation to.
    skip_nonquant: bool
        If True then return "None" if the spectrum is missing quantitative data. If False, then try \
        to fill in missing quantitative values with defaults.
    '''

    x = jcamp_dict['x']
    y = jcamp_dict['y']

    T = 296.0            ## the temperature (23 degC) used by NIST when collecting spectra
    R = 1.0355E-25       ## the constant for converting data (includes the gas constant)

    ## Note: normally when we convert from wavenumber to wavelength units, the ordinate must be nonuniformly
    ## rescaled in order to compensate. But this is only true if we resample the abscissa to a uniform sampling
    ## grid. In this case here, we keep the sampling grid nonuniform in wavelength space, such that each digital
    ## bin retains its proportionality to energy, which is what we want.
    if (jcamp_dict['xunits'].lower() in ('1/cm','cm-1','cm^-1')):
        jcamp_dict['wavenumbers'] = array(x)            ## note that array() always performs a copy
        x = 10000.0 / x
        jcamp_dict['wavelengths'] = x
    elif (jcamp_dict['xunits'].lower() in ('micrometers','um','wavelength (um)')):
        jcamp_dict['wavelengths'] = x
        jcamp_dict['wavenumbers'] = 10000.0 / x
    elif (jcamp_dict['xunits'].lower() in ('nanometers','nm','wavelength (nm)')):
        x = x * 1000.0
        jcamp_dict['wavelengths'] = x
        jcamp_dict['wavenumbers'] = 10000.0 / x
    else:
        raise ValueError('Don\'t know how to convert the spectrum\'s x units ("' + jcamp_dict['xunits'] + '") to micrometers.')

    ## Correct for any unphysical negative values.
    y[y < 0.0] = 0.0

    ## Make sure "y" refers to absorbance.
    if (jcamp_dict['yunits'].lower() == 'transmittance'):
        ## If in transmittance, then any y > 1.0 are unphysical.
        y[y > 1.0] = 1.0

        ## convert to absorbance
        y = log10(1.0 / y)

        jcamp_dict['absorbance'] = y
    elif (jcamp_dict['yunits'].lower() == 'absorbance'):
        pass
    elif (jcamp_dict['yunits'].lower() == '(micromol/mol)-1m-1 (base 10)'):
        jcamp_dict['yunits'] = 'xsec (m^2))'
        jcamp_dict['xsec'] = y
    else:
        raise ValueError('Don\'t know how to convert the spectrum\'s y units ("' + jcamp_dict['yunits'] + '") to absorbance.')


    ## Determine the effective path length "ell" of the measurement chamber, in meters.
    if ('path length' in jcamp_dict):
        (val,unit) = jcamp_dict['path length'].lower().split()[0:2]
        if (unit == 'cm'):
            ell = float(val) / 100.0
        elif (unit == 'm'):
            ell = float(val)
        elif (unit == 'mm'):
            ell = float(val) / 1000.0
        else:
            ell = 0.1
    else:
        if skip_nonquant: return({'info':None, 'x':None, 'xsec':None, 'y':None})
        ell = 0.1
        if debug: print('Path length variable not found. Using 0.1m as a default ...')

    assert(alen(x) == alen(y))

    if ('npoints' in jcamp_dict):
        if (alen(x) != jcamp_dict['npoints']):
            npts_retrieved = str(alen(x))
            msg = '"' + jcamp_dict['title'] + '": Number of data points retrieved (' + npts_retrieved + \
                  ') does not equal the expected length (npoints = ' + str(jcamp_dict['npoints']) + ')!'
            raise ValueError(msg)

    ## For each gas, manually define the pressure "p" at which the measurement was taken (in units of mmHg).
    ## These values are obtained from the NIST Infrared spectrum database, which for some reason did not
    ## put the partial pressure information into the header.
    if ('partial_pressure' in jcamp_dict):
        p = float(jcamp_dict['partial_pressure'].split()[0])
        p_units = jcamp_dict['partial_pressure'].split()[1]
        if (p_units.lower() == 'mmhg'):
            pass
        elif (p_units.lower() == 'ppm'):
            p = p * 759.8 * 1.0E-6       ## scale PPM units at atmospheric pressure to partial pressure in mmHg
    else:
        if debug: print(('No pressure "p" value entry for ' + jcamp_dict['title'] + '. Using the default p = 150.0 mmHg ...'))
        if skip_nonquant: return({'info':None, 'x':None, 'xsec':None, 'y':None})
        p = 150.0
        if debug: print('Partial pressure variable not found. Using 150mmHg as a default ...')

    ## Convert the absorbance units to cross-section in meters squared per molecule.
    xsec = y * T * R / (p * ell)

    ## With a third-party-spectrometer, I've found convincing evidence that the NIST spectra for propane and butane have
    ## an artificial DC baseline (and one that the PNNL data also do not have). So let's just subtract it here.
    if (jcamp_dict['title'].lower() in ('propane','n_butane','butane')):
        okay = logical_and(jcamp_dict['wavelengths'] >= 8.0, jcamp_dict['wavelengths'] <= 12.0)
        minvalue = amin(xsec[okay])
        #print('Subtracting a baseline of %g from %s' % (minvalue, jcamp_dict['title']))
        xsec = xsec - minvalue

    ## Add the "xsec" values to the data dictionary.
    jcamp_dict['xsec'] = xsec

    return

##=====================================================================================================
def is_float(s):
    '''
    Test if a string, or list of strings, contains a numeric value(s).

    Parameters
    ----------
    s : str, or list of str
        The string or list of strings to test.

    Returns
    -------
    is_float_bool : bool or list of bool
        A single boolean or list of boolean values indicating whether each input can be converted into a float.
    '''

    if isinstance(s,tuple) or isinstance(s,list):
        if not all(isinstance(i,str) for i in s): raise TypeError("Input 's' is not a list of strings")
        if len(s) == 0:
            try:
                temp = float(i)
            except ValueError:
                return(False)
        else:
            bool = list(True for i in range(0,len(s)))
            for i in range(0,len(s)):
                try:
                    temp = float(s[i])
                except ValueError:
                    bool[i] = False
        return(bool)
    else:
        if not isinstance(s,str): raise TypeError("Input 's' is not a string")
        try:
            temp = float(s)
            return(True)
        except ValueError:
            return(False)

## =================================================================================================
## =================================================================================================

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    filename = './infrared_spectra/methane.jdx'
    jcamp_dict = JCAMP_reader(filename)
    plt.plot(jcamp_dict['x'], jcamp_dict['y'])
    plt.title(filename)
    plt.xlabel(jcamp_dict['xunits'])
    plt.ylabel(jcamp_dict['yunits'])

    JCAMP_calc_xsec(jcamp_dict, skip_nonquant=False, debug=True)
    plt.figure()
    plt.plot(jcamp_dict['wavelengths'], jcamp_dict['xsec'])
    plt.title(filename)
    plt.xlabel('um')
    plt.ylabel('Cross-section (m^2)')

    filename = './uvvis_spectra/toluene.jdx'
    plt.figure()
    jcamp_dict = JCAMP_reader(filename)
    plt.plot(jcamp_dict['x'], jcamp_dict['y'], 'r-')
    plt.title(filename)
    plt.xlabel(jcamp_dict['xunits'])
    plt.ylabel(jcamp_dict['yunits'])

    filename = './mass_spectra/ethanol_ms.jdx'
    jcamp_dict = JCAMP_reader(filename)
    plt.figure()
    for n in arange(alen(jcamp_dict['x'])):
        plt.plot((jcamp_dict['x'][n],jcamp_dict['x'][n]), (0.0, jcamp_dict['y'][n]), 'm-', linewidth=2.0)
    plt.title(filename)
    plt.xlabel(jcamp_dict['xunits'])
    plt.ylabel(jcamp_dict['yunits'])

    filename = './raman_spectra/tannic_acid.jdx'
    jcamp_dict = JCAMP_reader(filename)
    plt.figure()
    plt.plot(jcamp_dict['x'], jcamp_dict['y'], 'k-')
    plt.title(filename)
    plt.xlabel(jcamp_dict['xunits'])
    plt.ylabel(jcamp_dict['yunits'])

    plt.show()

