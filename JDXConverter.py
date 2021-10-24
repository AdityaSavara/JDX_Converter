import JCampSG
import string
import numpy
import csv
import time
import timeit
import math
import sys
from numpy import genfromtxt
import os.path
import httplib2
from bs4 import BeautifulSoup, element , SoupStrainer
import bs4 
import requests 
import pymatgen.core.composition
import urllib.request
import cgi
import httplib2

def getMassSpectrumURL(URL):
    http = httplib2.Http()
    status, response = http.request(URL)

    all_links = BeautifulSoup(response, parse_only=SoupStrainer('a'), features='html.parser')

    for link in all_links:
        if link.has_attr('href'):
            value = link['href']
            if(value.find('#Mass-Spec')>0):
                domain = 'https://webbook.nist.gov'
                mass_spec_url = domain + value
                return mass_spec_url

def getJDXDownloadURL(mass_spectrum_url):
    http = httplib2.Http()
    status, response = http.request(mass_spectrum_url)

    all_links = BeautifulSoup(response, parse_only=SoupStrainer('a'), features='html.parser')

    for link in all_links:
        if link.has_attr('href'):
            value = link['href']
            if(value.find('JCAMP')>0):
                domain = 'https://webbook.nist.gov'
                download_url = domain + value
                return download_url

def getMolecularWeight(URL):
    
    webpage = requests.get(URL) 
    soup = BeautifulSoup(webpage.content, "lxml")

    molecularWeight = soup.find("a", attrs={"title": 'IUPAC definition of relative molecular mass (molecular weight)'}).find_parent().nextSibling
    return float(molecularWeight)

def getMolecularFormula(URL):
    
    webpage = requests.get(URL) 
    soup = BeautifulSoup(webpage.content, "lxml")

    formula_tag = soup.find("a", attrs={"title": 'IUPAC definition of empirical formula'}).find_parent().next_siblings
    formula = ''
    for sib in formula_tag:                                                                                             #sib is the siblings inside formula_tag
        if(type(sib) == bs4.element.Tag):
            formula = formula +sib.text
        else:
            formula = formula + sib

    return formula

def getElectronNumbers(formula):
    comp = pymatgen.core.composition.Composition(formula)
    return comp.total_electrons

def getJDXDownloadURL(mass_spectrum_url):
    http = httplib2.Http()
    status, response = http.request(mass_spectrum_url)

    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features='html.parser'):
        if link.has_attr('href'):
            value = link['href']
            if(value.find('JCAMP')>0):
                domain = 'https://webbook.nist.gov'
                mass_spec_url = domain + value
                return mass_spec_url

def getJDX(URL,molecule_name):
    # URL = "https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C67561&Index=0&Type=Mass"
    remotefile = urllib.request.urlopen(URL)
    remotefileName = remotefile.info()['Content-Disposition']
    value, params = cgi.parse_header(remotefileName)
    outputdirectory = "JDXFiles"
    filename = "%s\\%s" %(outputdirectory,molecule_name+".jdx")
    urllib.request.urlretrieve(URL, filename)
    return filename

def getOverAllArray(listOfFiles):
    OverallArray=[]
    holderArray=[]
    # for i in listOfFiles:
    jcampDict=JCampSG.JCAMP_reader(listOfFiles)
    holderArray=createArray(jcampDict, listOfFiles)
    OverallArray=combineArray(OverallArray, holderArray)
    return OverallArray

#This variable determines the largest fragment size that the program can handle
MaximumAtomicUnit = 300

def createArray(jcampDict, filename):
    DataArray =[]

    counterY=0
    counter =0
    for number in jcampDict['x']:    
        counter = counter +1
        counterY2=0
        while counter != float(number):
        
            DataArray.append(0)
            #fileData.write('%f,'%zero)
            #fileData.write('\n')
            counter = counter +1 

        for number2 in jcampDict['y']:
            if counterY2 == counterY:
                
                DataArray.append(number2) 
                #fileData.write('%f,'%number2)
                #fileData.write('\n')
                #counterY2 =counterY2 + 1
                break
            else:
                counterY2=counterY2 +1  

        counterY= counterY +1

    if len(DataArray) < MaximumAtomicUnit:
        for i in range(len(DataArray), MaximumAtomicUnit):
            DataArray.append(0)
    return DataArray

def combineArray(Array1, Array2):
    
    for i in range(MaximumAtomicUnit):
        Array1.append(Array2[i])
    
    
    return Array1

def exportToCSV(filename, OverallArray, MoleculeNames, ENumbers, MWeights, knownMoleculeIonizationTypes, knownIonizationFactorsRelativeToN2, SourceOfFragmentationPatterns, SourceOfIonizationData):
  
    f5 = open(filename, 'w')
    if(len(MoleculeNames) == 1):
        f5.write('#CommentsLine:')
        f5.write(',')
        f5.write('\n')
        
        #write the molecules
        f5.write('Molecules')
        f5.write(',')
        f5.write(MoleculeNames[0])
        f5.write('\n')

        #write the Electron Numbers
        f5.write('Electron Numbers')
        f5.write(',')
        f5.write(str(ENumbers))
        f5.write('\n')
        
        #write the ionization type
        f5.write('knownMoleculesIonizationTypes')
        f5.write(',')
        f5.write(knownMoleculeIonizationTypes)
        f5.write('\n')
        
        #write the ionization factor
        f5.write('knownIonizationFactorsRelativeToN2')
        f5.write(',')
        f5.write(knownIonizationFactorsRelativeToN2)
        f5.write('\n')
        
        #write the header
        f5.write('SourceOfFragmentationPatterns')
        f5.write(',')
        f5.write(SourceOfFragmentationPatterns)
        f5.write('\n')
        
        #write the ionization data source
        f5.write("SourceOfIonizationData")
        f5.write(',')
        f5.write(SourceOfIonizationData)
        f5.write('\n')
        
        #write the molecular weights
        f5.write('Molecular Mass')
        f5.write(',')
        f5.write(str(MWeights))
        f5.write('\n')
    else:
        f5.write('#CommentsLine:')
        for i in range(len(MoleculeNames)):
            f5.write(',')
        f5.write('\n')
        
        #write the molecules
        f5.write('Molecules')
        for i in MoleculeNames:
            f5.write(',%s' %i)
        f5.write('\n')

        #write the Electron Numbers
        f5.write('Electron Numbers')
        # for i in ENumbers:
        #     f5.write(',%f'%(int(i)))
        f5.write(str(ENumbers))
        f5.write('\n')
        
        #write the ionization type
        f5.write('knownMoleculesIonizationTypes')
        for i in knownMoleculeIonizationTypes:
            f5.write(',%s'%i)
        f5.write('\n')
        
        #write the ionization factor
        f5.write('knownIonizationFactorsRelativeToN2')
        for i in knownIonizationFactorsRelativeToN2:
            f5.write(',%s'%i)
        f5.write('\n')
        
        #write the header
        f5.write('SourceOfFragmentationPatterns')
        for i in SourceOfFragmentationPatterns:
            f5.write(',%s' %i)
        f5.write('\n')
        
        #write the ionization data source
        f5.write("SourceOfIonizationData")
        for i in SourceOfIonizationData:
            f5.write(',%s' %i)
        f5.write('\n')
        
        #write the molecular weights
        f5.write('Molecular Mass')
        # for i in MWeights:
        #     f5.write(',%f' %(float(i)))
        f5.write(str(MWeights))
        f5.write('\n')
    
    Array1=OverallArray
    printRow= len(Array1)//MaximumAtomicUnit
    printArray =[]
    zeros = True

    for i in range(1,MaximumAtomicUnit+1):
        print(i)
        zeros = True
        for k in range(printRow):
            if Array1[MaximumAtomicUnit*k +i-1] != 0: #The -1 is for array indexing
                zeros =False                
        if zeros == False:
            f5.write('%d'%(i))    
            for y in range(printRow):    
                f5.write(',%d'%(Array1[MaximumAtomicUnit*y +i-1])) #The -1 is for array indexing
            f5.write('\n')
            
    f5.close()

def startCommandLine():

      
    SourceOfFragmentationPattern = ''
    SourceOfFragmentationPatterns = list()
    SourceOfIonizationDatum = ''
    SourceOfIonizationData = list()
    moleculeName=''
    MoleculeNames=list()
    ENumber = 0
    ENumbers =list()
    MWeight =0.0 
    MWeights=list()
    knownMoleculeIonizationType = ''
    knownMoleculeIonizationTypes = list()
    knownIonizationFactorRelativeToN2 = 0.0
    knownIonizationFactorsRelativeToN2 = list()
    filenames=''
    listOfFiles=list()


    fileYorN=''

    print("would you like to load molecular information from a csv file? Enter 'yes' or 'no'. If not, then you will enter files manually.")
    fileYorN=input()


    if (fileYorN =='no'):
        print("Welcome! Enter the name of the molecule, its mass, its ionization factor relative to nitrogen (put unknown if you don't know), its ionization type (put unknown if you don't know), its number of electrons (or the number -1 if you don't need that), and the associated JDX file in order to generate a csv spectrum file")
        print("If a molecule name has a comma in it (e.g. 1,3-pentadiene) or any other input has a comma in it, we recommend using an _ (e.g. 1_3-pentadiene) since this information is stored in a comma separated value file.")
        print("Enter the molecule's Name: ")
        moleculeName = input()



        while moleculeName != 'EXIT':
            MoleculeNames.append(moleculeName)

            print("Retrieve info from NIST webbook?")
            WebbookChoice = input()
            if WebbookChoice.lower() == 'Y'.lower():
                print("WELCOME!")
                molecule_name = input("Enter the name of the Molecule: ")
                url = f'https://webbook.nist.gov/cgi/cbook.cgi?Name={molecule_name}&Units=SI'
                mass_spectrum_url = getMassSpectrumURL(url)
                jdx_download_url = getJDXDownloadURL(mass_spectrum_url)
                jdx_filename = getJDX(jdx_download_url,molecule_name)
                overAllArray = getOverAllArray(jdx_filename)

                molecular_formula = getMolecularFormula(url)
                molecular_weight = getMolecularWeight(url)
                electron_numbers = getElectronNumbers(molecular_formula)
                knownMoleculeIonizationTypes = 'unknown'
                knownIonizationFactorsRelativeToN2 = 'unknown'
                SourceOfFragmentationPatterns = 'unknown'
                SourceOfIonizationData = 'unknown'
            else:
            

                print(" enter the electron Number: ")
                ENumber = input()
                ENumbers.append(ENumber)
                print(" enter the molecule's ionization type (Enter unknown if unknown): ")
                knownMoleculeIonizationType = input()
                knownMoleculeIonizationTypes.append(knownMoleculeIonizationType)
                print(" enter the molecule's ionization factor relative to N2 (Enter a unknown if unknown): ")
                knownIonizationFactorRelativeToN2 = input()
                knownIonizationFactorsRelativeToN2.append(knownIonizationFactorRelativeToN2)
                print(" enter the source of the fragmention pattern: ")
                SourceOfFragmentationPattern = input()
                SourceOfFragmentationPatterns.append(SourceOfFragmentationPattern)
                print(" enter the source of the ionization data: ")
                SourceOfIonizationDatum = input()
                SourceOfIonizationData.append(SourceOfIonizationDatum)
                print(" enter the Molecular Weight:")
                MWeight= input()
                MWeights.append(MWeight)        
                print("enter the file name(EX: oxygen.jdx):")
                print("If the file is in a separate directory, \ninclude the path(EX: JDXFiles\oxygen.jdx):")
                filename=input()
                listOfFiles.append(filename)
                print("Enter the name of the next molecule or type EXIT to finish entering molecules")
                moleculeName=input()

    elif(fileYorN=='yes'):
        fileInputName=''
        print("enter the file input name please:")
        fileInputName=input()
        #input_file ='attempt.csv'
        list_holder=[]
        spamReader = csv.reader(open('%s' %fileInputName), delimiter=',')
        for row in spamReader:
            list_holder.append(row)
            
            
    #The user is provided with the option to direct the functions output as they would like.  
    print("Would you like to specify an output location? If yes, type the path to the location. For default, hit enter.")
    outputDirectory = input()
    #If the user selects default, then the output is piped to "OutputFiles"
    if outputDirectory == "":
        outputDirectory = "OutputFiles"


    #mkaing the directory for exported files, if it isn't already there
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    #only if files exist to draw from
    if fileYorN == 'yes':
    #Checking if a directory exists to be drawn from
        if os.path.isdir("JDXFiles"):
        #This for loop draws from a directory of the user's choice (hard-coded)
            for i in range(1, len(list_holder)):
                
    # The below line has been added to allow the program to draw files from 
    # outside it's own directory.
                list_holder[i][3] = "JDXFiles\\" + list_holder[i][3]
        
                MoleculeNames.append(list_holder[i][0])
                ENumbers.append(list_holder[i][1])
                MWeights.append(list_holder[i][2])
                listOfFiles.append(list_holder[i][3])
                knownMoleculeIonizationTypes.append(list_holder[i][4])
                knownIonizationFactorsRelativeToN2.append(list_holder[i][5])
                SourceOfFragmentationPatterns.append(list_holder[i][6])
                SourceOfIonizationData.append(list_holder[i][7])
                
    #Otherwise, assume that the files are in the directory of the JDXConv-UI
        else:
        
    #This for loop draws files from the current directory
            for i in range(1, len(list_holder)):
                
                MoleculeNames.append(list_holder[i][0])
                ENumbers.append(list_holder[i][1])
                MWeights.append(list_holder[i][2])
                listOfFiles.append(list_holder[i][3])
                knownMoleculeIonizationTypes.append(list_holder[i][4])
                knownIonizationFactorsRelativeToN2.append(list_holder[i][5])
                SourceOfFragmentationPatterns.append(list_holder[i][6])
                SourceOfIonizationData.append(list_holder[i][7])

    OverallArray=[]
    holderArray=[]
    for i in listOfFiles:
        jcampDict=JCampSG.JCAMP_reader(i)
        holderArray=createArray(jcampDict, i)
        OverallArray=combineArray(OverallArray, holderArray)

def executeForSingleMolecule():
    print("WELCOME!")
    molecule_name = input("Enter the name of the Molecule: ")
    url = f'https://webbook.nist.gov/cgi/cbook.cgi?Name={molecule_name}&Units=SI'

    mass_spectrum_url = getMassSpectrumURL(url)
    jdx_download_url = getJDXDownloadURL(mass_spectrum_url)
    jdx_filename = getJDX(jdx_download_url,molecule_name)
    overAllArray = getOverAllArray(jdx_filename)

    molecular_formula = getMolecularFormula(url)
    molecular_weight = getMolecularWeight(url)
    electron_numbers = getElectronNumbers(molecular_formula)
    knownMoleculeIonizationTypes = 'unknown'
    knownIonizationFactorsRelativeToN2 = 'unknown'
    SourceOfFragmentationPatterns = 'unknown'
    SourceOfIonizationData = 'unknown'

    filename = molecule_name+".csv"
    outputDirectory = "OutputSingleCSVFiles"

    Molecules = []
    Molecules.append(molecule_name)
    exportToCSV("%s\\%s" %(outputDirectory,filename), overAllArray, Molecules, electron_numbers, molecular_weight, knownMoleculeIonizationTypes, knownIonizationFactorsRelativeToN2, SourceOfFragmentationPatterns, SourceOfIonizationData)

# exportToCSV("%s\\ConvertedSpectra.csv" %outputDirectory, OverallArray,  MoleculeNames, ENumbers, MWeights, knownMoleculeIonizationTypes, knownIonizationFactorsRelativeToN2, SourceOfFragmentationPatterns, SourceOfIonizationData)
executeForSingleMolecule()