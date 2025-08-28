#!/usr/bin/env python3
#coding: utf-8



# Abdeljalil SENHAJI RACHIK
# VERSION 01/03/2023 python3.7+
#



import re
import os
import math
import sys
import argparse



parser = argparse.ArgumentParser(description='extract info for Blasted sequences depending on Kraken taxonomy')

parser.add_argument('-i', '--inputFile', type=str, nargs=1, help='Blast output (txt)', required=True)
parser.add_argument('-o', '--outputFile', type=str, nargs=1, help='extract info blast or conserved.txt', required=True)

args = parser.parse_args()

inputPath = args.inputFile[0]
outputPath = args.outputFile[0]

inputFile = re.split('/', inputPath)[-1]
outputFile = re.split('/', outputPath)[-1]

sampleID = re.split('\\.blast', inputFile)[0]
folder = re.split(inputFile, inputPath)[0]

conservedSeq = open(outputPath, 'w')

# ==== Compares genus attribution from BLAST and Kraken ====#
with open(inputPath) as blastFile:
    clue = 0
    print("Opened file")
    ligne = blastFile.readline()
    while ligne:
        QtaxID = ''
        queryLigne = len(re.findall("Query: ", ligne))
        if queryLigne == 1:  # Get to lines of interest in the blast file
            QtaxID = re.split("taxid\\|", ligne)[1].strip('\n')  # Save Kraken taxon ID in 'QtaxID'
            isItMate = '0'
            isItMate = re.split("/", re.split(" ", ligne)[3])[1]  # Which mate is read coming from
            if QtaxID != '0':  # Exclude taxID equal to 0
                ligne = blastFile.readline()
                ligne = blastFile.readline()
                ligne = blastFile.readline()
                ligne = blastFile.readline()
                # ajouter de mate pour genere les fichiers fasta
                conservedSeq.write('\t'.join(ligne.split()) + '\t' + QtaxID + '\t' + isItMate + '\n')
            else:
                ligne = blastFile.readline()
        ligne = blastFile.readline()

conservedSeq.close()
