# -*- coding: utf-8 -*-
import re
import os
import argparse
from ete3 import NCBITaxa

parser = argparse.ArgumentParser(description='Add names of species to the final "count" file')
parser.add_argument('-i', '--inputFile', type=str, nargs=1, help='_count.txt file', required=True)
parser.add_argument('-o', '--outputFile', type=str, nargs=1, help='_NameVirFunPar.txt file', required=True)
parser.add_argument('-n', '--ncbi_taxa', type=str, nargs=1, help='Localization of NCBI Taxa database', required=True)
args = parser.parse_args()

inputPath = args.inputFile[0]
outputPath = args.outputFile[0]
ncbiDB = args.ncbi_taxa[0]
ncbi = NCBITaxa(dbfile=ncbiDB)

# Ouvre le fichier de sortie
with open(outputPath, 'w') as count:
    with open(inputPath) as countFile:
        line = countFile.readline()
        while line:
            line = line.strip()
            if not line:  # Ignore les lignes vides
                line = countFile.readline()
                continue

            split = re.split(r'\s+', line)  # Utilise un regex pour separer par espaces
            if len(split) < 2:  
                print(f"Ligne ignoree (trop courte) : {line.strip()}")
                line = countFile.readline()
                continue

            taxID = split[0].strip('\n')
            countReads = split[1]

            if taxID != 'N/A' and taxID != '0':
                # Tente de convertir taxID en entier
                try:
                    taxID_int = int(taxID)  # Essaie de convertir en entier
                    taxNameDic = ncbi.get_taxid_translator([taxID_int])
                    if taxNameDic:
                        taxName = taxNameDic[list(taxNameDic.keys())[0]]
                    else:
                        taxName = "UNKNOWN"
                    count.write(f"{taxID},{taxName.replace(',', '_')},{countReads}\n")
                except ValueError:
                    print(f"TaxID non valide (non entier) : {taxID}")  # Affiche un message d'erreur

            line = countFile.readline()

print("Traitement termine. ")
