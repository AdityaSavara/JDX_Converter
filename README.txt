JDX Converter

Project Description:
The JDX Converter is used to read spectra reference data obtained from NIST into a useable CSV format. NIST stores reference data in JDX files, but these are not widely read by software, making a conversion to a different format necessary. JDX files can either be converted by providing the molecule data individually or by supplying the converter with a CSV containing all of the molecule information and JDX filenames.
This repository contains JDXConverter.py as the user interface and JCampSG.py as the reader of the JDX files. The repository also contains a template CSV for entering the molecule information and file names (MoleculesInfo.csv) along with example JDX files that can be run (contained in the JDX Files Directory).
JDXConverter.py has two methods of JDX file input: manual and via a csv information file. Manual is useful for going through the molecules one at a time with a smaller number of JDX files to convert. A csv reference file is useful for converting multiple spectra contained in JDX files.

Prerequisites:
JDX files for reference spectra can be downloaded from https://webbook.nist.gov/chemistry/ .
The program requires an executable Python development environment such as Anaconda and Spyder. Additionally, it requires the JDX files to be converted, JCampSG.py, JDXConverter.py, and MoleculesInfo.csv (if used). The JDX Files can be contained in the same directory as the JDXConverter.py or in the subdirectory called JDXFiles.
Regardless of the input method for the JDX files, molecule information must be provided. This information includes the molecule name, the number of electrons, and the molecular mass.

Installing:
Download the repository containing JDXConverter.py, JCampSG.py, the desired JDX files, and MoleculesInfo.csv (if converting multiple spectra at once). JDX files should be in the subdirectory: JDXFiles if running a reference csv or in either the JDXFiles subdirectory or the same folder as the JDXConverter.

Running the Example Set:
Open the JDXConverter in the Python Development Environment and select run.
The example set will run using a reference csv file. When prompted to enter if you would like to load references from a csv file, type yes. 
Enter the MoleculesInfo.csv when asked for the reference file name.
When prompted for an output location, use the default location, so simply press enter.
ConvertedSpectra.csv can now be found in the OutputFiles folder.

Running:
If you would like to run multiple spectra using a reference csv file, create a file following the same format as the MoleculesInfo.csv.
Open JDXConverter.py on the development environment and select run. 
The program will print “Would you like to load references from a csv file? Enter ‘yes’ or ‘no’. If not, then you will enter files manually.” If converting spectra using the reference csv file type ‘yes’ otherwise type ‘no’. 
If no was selected:
The program will provide prompts to enter in the individual molecule information and the JDX file name. For manual input, follow the prompts to enter the molecule name, electron number and molecular mass. The JDXConverter will then ask for the JDX filename. If the JDX file is in the same folder as the JDXConverter simply enter filename.jdx (e.g. water.jdx). If the file is included in the JDXFiles subdirectory, precede the filename with JDXFiles\\ (e.g. JDXFiles\\water.jdx). When finished entering molecule JDX files to convert, enter EXIT when prompted. 
The JDXConverter will then prompt you to enter an output location if desired. Enter the output location if wanted, or press enter. The default location will be the OutputFiles folder. The converted spectra will appear as ConvertedSpectra.csv.

If yes was selected:
The program will prompt you to enter the name of the reference csv. Enter the name (e.g. MoleculesInfo.csv). The JDXConverter will then prompt you to enter an output location if desired. Enter the output location if wanted, or press enter. The default location will be the OutputFiles folder. The converted spectra will appear as ConvertedSpectra.csv.


Authors:
Savara Group
Acknowledgements:
Nathan Hagen for providing the original jcamp.py
