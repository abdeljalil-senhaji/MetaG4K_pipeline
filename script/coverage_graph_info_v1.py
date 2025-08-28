#!/usr/bin/env python3
#coding: utf-8

# Abdeljalil senhaji rachik
# version.0.1  01/03/2023 python3.7+
# script 



import re
import os
import math
import sys
import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from ete3 import NCBITaxa
#from exceptions import ValueError

parser=argparse.ArgumentParser(description='Generate Coverage/Depth plot for Viruses, Parasite, Fungi, silva16S et Argos')

parser.add_argument('-e', '--inputFile', type=str, nargs=1, help='extractInfo_vir_fun_par.txt and silva16S, Argos', required=True)
parser.add_argument('-g', '--inputFile1', type=str, nargs=1, help='_*_count.txt', required=True)
parser.add_argument('-o', '--outputFile', type=str, nargs=1, help='_*_allInfoCovrage.txt', required=True)
parser.add_argument('-m','--minimum_reads', type=int, nargs=1, help='Minimum number of reads to draw a plot (default=5)', default=5)
parser.add_argument('-n','--ncbi_taxa', type=str, nargs=1, help='Localization of NCBI Taxa database', default="/data/annotations/Blast/12_08_2019_custom/NCBITaxa/.etetoolkit/taxa.sqlite")

args = parser.parse_args()

extractInfoInputPath=args.inputFile[0]
getNameInputPath=args.inputFile1[0]
outputPath=args.outputFile[0]
minReads=args.minimum_reads[0]
ncbiDB=args.ncbi_taxa[0]

ncbi = NCBITaxa(dbfile=ncbiDB)


inputFileV1=re.split('/',extractInfoInputPath)[-1]
inputFileV2=re.split('/',getNameInputPath)[-1]
outputFile=re.split('/',outputPath)[-1]

sampleID=re.split('\\_extractInfo',inputFileV1)[0]
folder=re.split(inputFileV1,extractInfoInputPath)[0]

#===== This function can be used to initialize a list of specific size with default values, such as zeros.

def listOfSizeN(N):
    cover=[0]*(N+1)
    return cover


#===== For each taxonID, gets corresponding name of species + Creates first part of the output =====#
lineToCopy = []
with open(getNameInputPath) as getNameFile:
    dictListSpecies = {}
    line = getNameFile.readline()
    while line:
        split = re.split(',', line)
        if len(split) >= 3:
            taxID = split[0]
            speciesName = split[1]
            countReads = split[2].strip('\n')
            if speciesName != "UNKNOWN":
                taxNameDic = ncbi.get_taxid_translator([taxID])
                dictListSpecies.update(taxNameDic)
                if taxNameDic:
                    taxName = taxNameDic[list(taxNameDic.keys())[0]]
                else:
                    taxName = ""
                taxName = speciesName.replace("/", "_")
                lineToCopy.append(taxID + ',' + taxName + ',' + countReads)
        line = getNameFile.readline()

#===== For each specie, create a list of all coordinates of alignment, and draw the plot based on this list =====#
dictListCoverage = {}
dictListSizeGenome = {}
dictListGenus = {}
if not os.path.exists(folder + "/Depth_Graphs_" + sampleID):  # Creates graph folder if it doesn't exist
    os.mkdir(folder + "/Depth_Graphs_" + sampleID)

with open(extractInfoInputPath) as extractInfoFile:
    ligne = extractInfoFile.readline()
    while ligne:
        if not ligne.strip():  # Ignore les lignes vides
            ligne = extractInfoFile.readline()
            continue
        
        hashed = re.split(r'\t', ligne)
        if len(hashed) > 7:  # Verifie le nombre de colonnes
            species = hashed[7].strip('\n')
            speciesTick = hashed[7].strip('\n')

            if species != '0' and speciesTick != '0':
                try:
                    lineage = ncbi.get_lineage(species)
                except ValueError:
                    print("Tax ID {} not found in lineage. Skipping entry.".format(species))
                    ligne = extractInfoFile.readline()
                    continue  # Ignore cette entree et passee la suivante

                sizeSubject = int(hashed[6])
                coverList = listOfSizeN(sizeSubject)  # List of set size filled with 0
                coordStart = []
                coordEnd = []

                while species == speciesTick:  # For each read of the same specie, memorize the coordinates of alignment
                    coordStart.append(min(int(hashed[2]), int(hashed[3])))
                    coordEnd.append(max(int(hashed[2]), int(hashed[3])))
                    ligne = extractInfoFile.readline()
                    hashed = re.split(r'\t', ligne)

                    if len(hashed) > 7:  # Verifie a nouveau le nombre de colonnes
                        speciesTick = hashed[7].strip('\n')
                    else:
                        speciesTick = -1

                for j in range(len(coordStart)):  # List of 0 is being incremented according to previously memorized coordinate
                    for i in range(coordStart[j], coordEnd[j] + 1):
                        try:
                            coverList[i] += 1
                        except:
                            print("A bad allocation")

                coveragePercent = str(round(((len(coverList) - coverList.count(0)) / len(coverList) * 100), 5))
                dictListCoverage.update({species: coveragePercent})
                dictListSizeGenome.update({species: str(sizeSubject)})
                ranks = ncbi.get_rank(lineage)
                genus = -1

                for k in ranks:
                    if ranks[k] == 'genus':
                        genus = k

                if genus != -1:
                    taxid2name = ncbi.get_taxid_translator([genus])[genus]
                    dictListGenus.update({species: taxid2name})
                else:
                    dictListGenus.update({species: "Genus sp."})

                if len(coordStart) >= minReads:  # Draw the depth/coverage plot following the list
                    x = np.arange(len(coverList))
                    plt.plot(x, coverList, color="#F44336")
                    plt.fill_between(x, 0, coverList, facecolor="#000000")
                    plt.xlim(left=0.0, right=len(coverList))
                    plt.ylim(bottom=0.0)
                    plt.ylabel('Depth')
                    speciesName = dictListSpecies[int(species)]
                    speciesName = speciesName.replace("/", "_")
                    if genus != -1:
                        plt.xlabel(speciesName + " (genus:" + taxid2name + ")")
                        plt.savefig(folder + "/Depth_Graphs_" + sampleID + "/" + speciesName + ".png", bbox_inches='tight')
                    else:
                        plt.xlabel(speciesName)
                        plt.savefig(folder + "/Depth_Graphs_" + sampleID + "/" + speciesName + ".png", bbox_inches='tight')
                    plt.clf()
                    print(speciesName + ".png generated")
            else:
                ligne = extractInfoFile.readline()
        else:
            print("Line does not contain enough columns:", ligne)
            ligne = extractInfoFile.readline()

#===== Generate the ***.coverage_info.txt, summary of all important informations =====#
count=open(outputPath,'w')
for line in lineToCopy:
    part1=re.split(',',line)[0]
    count.write(line+','+dictListCoverage[part1]+','+dictListSizeGenome[part1]+','+dictListGenus[part1]+'\n')
count.close()
