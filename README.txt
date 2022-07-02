JDX Converter

**Project Description:
JDX Converter is used to convert JDX spectra (typically obtained from https://webbook.nist.gov/chemistry/) into a more useable delimited formats of the type compatible with MSRESOLVE. 
During 2022, a major upgrade was performed where JDXConverter will now populate the output file with certain metadata (like molecular weight and number of electrons) from online.
In typical usage, a user simply adds a row into MoleculesInfo.tsv using microsoft excel, and then runs JDXConverter.py.

**Installation and dependencies:
JDXConverter has several external dependencies as specified in a requirements.txt file, and also includes an internal dependency of JCampSG.py (which reads JDX files). 
The easiest way get the dependencies is to first install anaconda, then open an anaconda prompt or spyder and use syntax like 'pip install lxml' to install each of the dependencies specified in the requirements file.
Alternatively, download the JDXConverter files, and run 'pip install -r requirements.txt' from that directory.


**Information on File Types***
JDXConverter was also changed to use tab delimited files or  semi-colon delimited files in the inpouts and outputs (.tsv and .skv).
Both of these file types can be opened using microsoft excel.
The main method for entering molecules is to use  MoleculesInfo.tsv or MoleculesInfo.skv. For any entries where there is an empty space (' ') or 'unknown', JDXConverter will attempt to find a value from online.


**Running the Example Set:
Run the JDXConverter.py using (such as from a command prompt or from inside spyder etc.)
Follow the instructions or simply press enter at each question from the program. With the default choices,  ConvertedSpectra1.tab will be generated in the OutputFiles folder.

**Advanced Information:
* There is intentionally no acetone jdx during distribution.
* If you don't need the number of electrons or the molecular mass for your application, enter the value -1 for those values. If you don't know the molecule's ionization factor or ionization type, enter unknown for that molecule.
* If a molecule has multiple ionization types then input each type delimited by a comma (e.g. organic, inorganic)
* To test JDXConverter's ability to fill gaps from online, change the input file to MoleculesInfo_withGaps.skv  by putting "MoleculesInfo_withGaps.skv ;" for the first prompted user input. as the molecule acetaldehdye has gaps in the table.