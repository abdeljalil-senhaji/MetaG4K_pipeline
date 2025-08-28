#!/usr/bin/env python3
#coding: utf-8

# Abdeljalil SENHAJI RACHIK
# version.0.1 python3.7+

import re
import os
import math
import sys
import argparse
import matplotlib
matplotlib.use('Agg')  # Important pour les environnements sans affichage
import matplotlib.pyplot as plt
import numpy as np
from ete3 import NCBITaxa


parser=argparse.ArgumentParser(description='Generate Coverage/Depth plot for Viruses, Parasite, Fungi, silva16S et Argos')

parser.add_argument('-e', '--inputFile', type=str, nargs=1, help='extractInfo_vir_fun_par.txt and silva16S, Argos', required=True)
parser.add_argument('-g', '--inputFile1', type=str, nargs=1, help='_*_count.txt', required=True)
parser.add_argument('-o', '--outputFile', type=str, nargs=1, help='_*_allInfoCovrage.txt', required=True)
parser.add_argument('-m','--minimum_reads', type=int, nargs=1, help='Minimum number of reads to draw a plot (default=5)', default=5)
parser.add_argument('-n','--ncbi_taxa', type=str, nargs=1, help='Localization of NCBI Taxa database', default="/data/annotations/Blast/12_08_2019_custom/NCBITaxa/.etetoolkit/taxa.sqlite")
parser.add_argument('-c', '--contigFile', type=str, nargs=1, help='Fichier CSV contenant le nombre de contigs', required=True)

args = parser.parse_args()

extractInfoInputPath=args.inputFile[0]
getNameInputPath=args.inputFile1[0]
outputPath=args.outputFile[0]
minReads=args.minimum_reads[0]
ncbiDB=args.ncbi_taxa[0]
contigFilePath = args.contigFile[0]

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

# Lire les informations sur les especes
lineToCopy = []
dictListSpecies = {}
with open(getNameInputPath) as getNameFile:
    for line in getNameFile:
        split = re.split(',', line)
        if len(split) >= 3:
            taxID = split[0]
            speciesName = split[1]
            countReads = split[2].strip('\n')
            if speciesName != "UNKNOWN":
                try:
                    taxNameDic = ncbi.get_taxid_translator([taxID])
                    dictListSpecies.update(taxNameDic)
                    taxName = taxNameDic.get(taxID, speciesName.replace("/", "_"))
                    lineToCopy.append(f"{taxID},{taxName},{countReads}")
                except KeyError as e:
                    print(f"TaxID {taxID} not found in NCBI database: {e}")
                    continue

# Creer le dossier pour les graphiques si necessaire
outputGraphFolder = folder + "/Depth_Graphs_" + sampleID
if not os.path.exists(outputGraphFolder):
    os.mkdir(outputGraphFolder)

# Lire et traiter le fichier d'extraction
dictListCoverage = {}
dictListSizeGenome = {}
dictListGenus = {}
uniqueContigCounts = {}

# Dictionnaire pour stocker le nombre de contigs par TaxID
contigDict = {}

with open(extractInfoInputPath) as extractInfoFile:
    #ligne = extractInfoFile.readline()
    #while ligne:
    for ligne in extractInfoFile: # Utiliser une boucle for pour une meilleure gestion de la mémoire
        hashed = re.split(r'\t', ligne)
        species = hashed[7].strip('\n')
        numContigs = hashed[1].strip()  # Utiliser la deuxieme colonne pour le nombre de contigs
        speciesTick = species
        
        if species != '0' and speciesTick != '0':
            try:
                lineage = ncbi.get_lineage(species)
            except ValueError:
                print(f"Tax ID {species} not found in lineage. Skipping entry.")
                #ligne = extractInfoFile.readline()
                continue
            
            sizeSubject = int(hashed[6])
            coverList = listOfSizeN(sizeSubject)
            coordStart = []
            coordEnd = []

            # Traiter les coordonnees directement dans la boucle, sans stocker toutes les coordonnees en memoire
            while species == speciesTick:
                coordStart_temp = min(int(hashed[2]), int(hashed[3]))
                coordEnd_temp = max(int(hashed[2]), int(hashed[3]))
                
                for i in range(coordStart_temp, coordEnd_temp + 1):
                    try:
                        coverList[i] += 1
                    except IndexError:
                        print("A bad allocation")

                #ligne = extractInfoFile.readline()
                try:
                    ligne = next(extractInfoFile)
                    hashed = re.split(r'\t', ligne)
                    speciesTick = hashed[7].strip('\n')
                except StopIteration:
                    speciesTick = -1
                    break # Sortir de la boucle while si on atteint la fin du fichier
            
            coveragePercent = str(round(((len(coverList) - coverList.count(0)) / len(coverList) * 100), 5))
            dictListCoverage[species] = coveragePercent
            dictListSizeGenome[species] = str(sizeSubject)
            ranks = ncbi.get_rank(lineage)
            genus = next((k for k in ranks if ranks[k] == 'genus'), -1)
            if genus != -1:
                taxid2name = ncbi.get_taxid_translator([genus])[genus]
                dictListGenus[species] = taxid2name
            else:
                dictListGenus[species] = "Genus sp."

            if len(coverList) >= minReads: #Verifier la longueur de coverList au lieu de coordStart
                x = np.arange(len(coverList))
                plt.plot(x, coverList, color="#F44336")
                plt.fill_between(x, 0, coverList, facecolor="#000000")
                plt.xlim(left=0.0, right=len(coverList))
                plt.ylim(bottom=0.0)
                plt.ylabel('Depth')
                speciesName = dictListSpecies[int(species)].replace("/", "_")
                taxid2name = dictListGenus.get(species, "Genus sp.")
                plt.xlabel(f"{speciesName} (genus: {taxid2name})" if genus != -1 else speciesName)
                plt.savefig(outputGraphFolder + "/" + speciesName + ".png", bbox_inches='tight')
                plt.clf()
                print(f"{speciesName}.png generated")

            # Supprimer coverList pour liberer de la memoire
            del coverList
            del coordStart
            del coordEnd

        #else:
            #ligne = extractInfoFile.readline()

# Ajouter les informations sur les contigs
with open(contigFilePath) as contigFile:
    contigFile.readline() 
    for line in contigFile:
        split = line.strip().split(',') 
        if len(split) >= 4:
            taxID = split[2].strip() 
            numContigs = split[3].strip()  # Normalisation
            contigDict[taxID] = numContigs
            print(f"Contig charge : {taxID} -> {numContigs}")

# Compter les contigs uniques a partir de extractInfoInputPath
uniqueContigCounts = {}

with open(extractInfoInputPath) as extractInfoFile:
    for ligne in extractInfoFile:
        hashed = re.split(r'\t', ligne)
        species = hashed[7].strip('\n')
        if species != '0':
            if species not in uniqueContigCounts:
                uniqueContigCounts[species] = set()
            uniqueContigCounts[species].add(hashed[1].strip())  

# Compter les contigs uniques pour chaque taxID
countUniqueContigs = {taxID: len(contigNames) for taxID, contigNames in uniqueContigCounts.items()}

# Generer le fichier de sortie
with open(outputPath, 'w') as count:
    for line in lineToCopy:
        part1 = re.split(',', line)[0].strip()
        numContigs = contigDict.get(part1, 'N/A')  
        uniqueCount = countUniqueContigs.get(part1, 'N/A')  
        count.write(f"{line},{dictListCoverage.get(part1, 'N/A')},{dictListSizeGenome.get(part1, 'N/A')},{dictListGenus.get(part1, 'N/A')},{numContigs},{uniqueCount}\n")