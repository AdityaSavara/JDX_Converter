JDX Converter

**Project Description:
The JDX Converter is used to read spectra reference data (typically obtained from https://webbook.nist.gov/chemistry/) into a useable CSV format. With this module, JDX files can either be converted by providing the molecule data individually or by supplying the converter with a CSV containing all of the molecule information and JDX filenames.
This repository contains JDXConverter.py as the user interface and JCampSG.py as the reader of the JDX files. The repository also contains a template CSV for entering the molecule information and file names (MoleculesInfo.csv) along with example JDX files that can be run (contained in the JDX Files Directory).
JDXConverter.py has two methods of JDX file input: manual and via a csv information file. Manual is useful for going through the molecules one at a time with a smaller number of JDX files to convert. A csv reference file is useful for converting multiple spectra contained in JDX files.

**Installation and dependencies:
The easiest way get the dependencies is to first install anaconda, then open spyder (installed with anaconda).
Download the repository, which includes example files. 
The module does include files which has dependencies on : JCampSG.py (included), and also requires one or more modules from Scipy.

**Running the Example Set:
Run the JDXConverter.py using (such as from a command prompt or from inside spyder etc.)
The example set of molecule files will be converted based to create a mass spectrometry pattern reference file. When prompted to enter if you would like to load references from a csv file, type yes. 
Enter the MoleculesInfo.csv when asked for the reference file name.
When prompted for an output location, use the default location, so simply press enter.
ConvertedSpectra.csv can now be found in the OutputFiles folder.

**Running (beyond the examples):
* If you would like to run multiple spectra using a reference csv file, create a file following the same format as the MoleculesInfo.csv.  If you don't need the number of electrons or the molecular mass for your application, enter the value -1 for those values. If you don't know the molecule's ionization factor or ionization type, enter unknown for that molecule.
* If a molecule has multiple ionization types then input each type delimited by a semicolon (e.g. organic; inorganic)
Open JDXConverter.py on the development environment and select run. 
* The program will print “Would you like to load references from a csv file? Enter ‘yes’ or ‘no’. If not, then you will enter files manually.” If converting spectra using the reference csv file type ‘yes’ otherwise type ‘no’. 
* If yes is selected: The program will prompt you to enter the name of the reference csv. Enter the name (e.g. MoleculesInfo.csv). The JDXConverter will then prompt you to enter an output location. The default location will be the OutputFiles folder. The converted spectra will by default appear as ConvertedSpectra.csv. 
* If no was selected: The program will provide prompts to enter in the individual molecule information and the JDX file name. For manual input, follow the prompts to enter the molecule name, electron number, molecular mass, ionization type, and ionization factor. The JDXConverter will then ask for the JDX filename. If the JDX file is in the same folder as the JDXConverter simply enter filename.jdx (e.g. water.jdx). * If the file is included in a subdirectory, precede the filename with DirectoryName\\ (e.g. JDXFiles\\water.jdx). 
* Finally, the JDXConverter will prompt you to enter an output location or to use the default location. The converted spectra will by default be put into a file named ConvertedSpectra.csv.


Authors:
Savara Group
Acknowledgements:
Nathan Hagen and any other contributors to the original jcamp.py
