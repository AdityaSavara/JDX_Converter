import JDXConverter
import string
import numpy
import csv
import time
import timeit
import math
import sys
from numpy import genfromtxt



def createArray(jcampDict, filename):
	DataArray =[]

	counterY=0
	counter =0
	for number in jcampDict['x']:	
		counter = counter +1
		counterY2=0
		while counter != float(number):
		
			#print float(number)
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
				break;
			else:
				counterY2=counterY2 +1  


		counterY= counterY +1


	if len(DataArray) < 100:
		for i in range(len(DataArray), 100):
			DataArray.append(0)
			#print i

	return DataArray

def combineArray(Array1, Array2):
	
	for i in range(100):
		Array1.append(Array2[i])
	
	
	return Array1

def exportToCSV(filename, OverallArray, listOfFiles, MoleculeNames, ENumbers, MWeights):

	f5 = open(filename, 'wb')

	#write the molecues
	f5.write('Information/Notes: ')
	f5.write('\n')
	f5.write('Molecues,')
	for i in MoleculeNames:
		f5.write('%s,' %i)
		#print i
	f5.write('\n')

	#write the Electron Numbers
	f5.write('Electron number,')
	for i in ENumbers:
		f5.write('%f,'%(int(i)))
		#print i
	f5.write('\n')

	f5.write('Molecular Weight,')
	for i in MWeights:
		f5.write('%f,' %(float(i)))
		#print i
	f5.write('\n')

	Array1=OverallArray
	printRow= len(Array1)/100
	printArray =[]
	zeros = True


	
	for i in range(100):
		zeros = True
		for k in range(printRow):
			if Array1[100*k +i] != 0:
				zeros =False				
		if zeros == False:
			f5.write('%d,'%(i))	
			for y in range(printRow):	
				f5.write('%d,'%(Array1[100*y +i]))
			f5.write('\n')
		

moleculeName=''
MoleculeNames=list()
ENumber = 0
ENumbers =list()
MWeight =0.0 
MWeights=list()
filenames=''
listOfFiles=list()


fileYorN=''

print "would you like to load references from a csv file? Enter 'yes' or 'no'. If not then you will enter files manually."
fileYorN=raw_input()


if (fileYorN =='no'):
	print "Welcome! Enter the name of the molecule, it's mass, it's electron number and the associated JDX file in order to generate your raw data fields"
	print "Enter the molecule's Name: "
	moleculeName = raw_input()



	while moleculeName != 'EXIT':
		MoleculeNames.append(moleculeName)
		print " enter the electron Number: "
		ENumber = raw_input()
		ENumbers.append(ENumber)
		print " enter the Molecular Weight:"
		MWeight= raw_input()
		MWeights.append(MWeight)
		print "enter the file name(EX: oxygenMass.jdx): "
		filename=raw_input()
		listOfFiles.append(filename)
		print "Enter the name of the next molecule or type EXIT to finish entering molecules"
		moleculeName=raw_input()

elif(fileYorN=='yes'):
	fileInputName=''
	print "enter the file input name please:"
	fileInputName=raw_input()
	#input_file ='attempt.csv'
	list_holder=[]
	spamReader = csv.reader(open('%s' %fileInputName), delimiter=',')
	for row in spamReader:
		list_holder.append(row)


	for i in range(1, len(list_holder)):

		MoleculeNames.append(list_holder[i][0])
		ENumbers.append(list_holder[i][1])
		MWeights.append(list_holder[i][2])
		listOfFiles.append(list_holder[i][3])
		



OverallArray=[]
holderArray=[]
for i in listOfFiles:
	jcampDict=JDXConverter.JCAMP_reader(i)
	holderArray=createArray(jcampDict, i)
	OverallArray=combineArray(OverallArray, holderArray)

exportToCSV("RawData.csv", OverallArray, listOfFiles, MoleculeNames, ENumbers, MWeights)