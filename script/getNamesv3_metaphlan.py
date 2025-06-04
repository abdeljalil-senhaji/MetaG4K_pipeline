#!/usr/bin/env python3
# coding: utf-8


# Abdeljalil SENHAJI RACHIK
# version
# Reads a count file, retrieves species names from the NCBI Taxa database based on taxonomic IDs, and writes the results to a specified output file.


import re
import os
import math
import sys
import argparse
from ete3 import NCBITaxa

parser=argparse.ArgumentParser(description='Add names of species to the final "count" file')
parser.add_argument('-i', '--inputFile', type=str, nargs=1, help='countbis.txt file', required=True)
parser.add_argument('-o', '--outputFile', type=str, nargs=1, help='count.txt file', required=True)
parser.add_argument('-n','--ncbi_taxa', type=str, nargs=1, help='Localization of NCBI Taxa database', default="/v3_pipMeta_4Kingdoms/db/NCBITaxa/.etetoolkit/taxa.sqlite")
args = parser.parse_args()

inputPath=args.inputFile[0]
outputPath=args.outputFile[0]
ncbiDB=args.ncbi_taxa[0]
ncbi = NCBITaxa(dbfile=ncbiDB)

#==== Adds the name of bacterial species, and write it in "count.txt" file ====#

count=open(outputPath,'w')
with open(inputPath) as countFile:
    line = countFile.readline()
    while line:
        split=re.split(' ',line.strip(' '))
        taxID=split[0].strip('\n')
        if taxID != 'N/A':
            if len(split) >= 4:
                countReads=split[1]+','+split[2]+','+split[3]
            else:
                countReads = "UNKNOWN"
            taxNameDic=ncbi.get_taxid_translator([int(taxID)])
            if taxNameDic:
                taxName=taxNameDic[list(taxNameDic.keys())[0]]
            else:
                taxName = "UNKNOWN"
        else:
            countReads = "UNKNOWN"
            taxName = "UNKNOWN"
        count.write(taxID+','+taxName.replace(",","_")+','+countReads)
        line = countFile.readline()
count.close()
