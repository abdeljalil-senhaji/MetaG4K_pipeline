#!/usr/bin/env python3
#coding: utf-8

# Abdeljalil senhaji rachik
# version.0.1  01/03/2023 python3.7+
# Recover read names of a specific taxonomic Group


import re
import os
import sys
import argparse


parser = argparse.ArgumentParser(description='Recover read names of a specific taxonomic group')

parser.add_argument('-r', '--inputReport', type=str, nargs=1, help='Kraken report.txt', required=True)
parser.add_argument('-k', '--inputKraken', type=str, nargs=1, help='Kraken output.txt', required=True)
parser.add_argument('-o', '--outputFile', type=str, nargs=1, help='Readnames list', required=True)
parser.add_argument('-l', '--listTaxIdNcbi', type=str, nargs=1, help='Viruses/Bacteria/Fungi/Eukaryota', required=True)

args = parser.parse_args()

inputReport = args.inputReport[0]
inputKraken = args.inputKraken[0]
outputPath = args.outputFile[0]
listTaxIdNcbi = args.listTaxIdNcbi[0]

#--------------------------------------------------


listTaxIdNcbiName = os.path.splitext(os.path.basename(listTaxIdNcbi))[0]

def compare_taxids(report_file, ncbi_taxid_file):
    try:
        with open(ncbi_taxid_file) as f:
            all_taxids = set([int(line.strip()) for line in f])
            print("TaxId number in the NCBI list",  listTaxIdNcbiName + " : ", + len(all_taxids))
    except FileNotFoundError:
        print(f"Error: {ncbi_taxid_file} not found")
        sys.exit(1)

    subset_taxids = set()
    with open(report_file) as f:
        for line in f:
            fields = line.strip().split('\t')
            taxid = int(fields[4])
            score = int(fields[2])
            if score > 0 and taxid in all_taxids:
                subset_taxids.add(taxid)

    return subset_taxids

#--------------------------------------------------

try:
    subset_taxids = compare_taxids(inputReport, listTaxIdNcbi)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

print("Generation of the TaxIdList: ...................... DONE !")
listreadName = []

try:
    with open(outputPath, 'w') as outputFile, open(inputKraken) as clseqFile:
        ligne = clseqFile.readline()
        while ligne:
            TaxID = re.split("\t", ligne)[2]
            ReadName = re.split("\t", ligne)[1]
            if int(TaxID) in subset_taxids:
                listreadName.append(ReadName)
                outputFile.write(ReadName + "\n")
            ligne = clseqFile.readline()
except FileNotFoundError:
    print(f"Error: {inputKraken} not found")
    sys.exit(1)
print("TaxId number in the sample list",  listTaxIdNcbiName + " : ", + len(listreadName))
print("Generation of the ReadsList: ...................... DONE !")
