#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import re
import argparse
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ete3 import NCBITaxa

def main():
    parser = argparse.ArgumentParser(description='Generate Coverage/Depth plot for Viruses, Parasite, Fungi, silva16S et Argos')
    parser.add_argument('-e', '--inputFile', type=str, required=True, help='extractInfo_vir_fun_par.txt')
    parser.add_argument('-g', '--inputFile1', type=str, required=True, help='_count.txt')
    parser.add_argument('-o', '--outputFile', type=str, required=True, help='_allInfoCovrage.txt')
    parser.add_argument('-m', '--minimum_reads', type=int, default=5, help='Minimum reads to draw plot')
    parser.add_argument('-n', '--ncbi_taxa', type=str, default="/data/annotations/Blast/12_08_2019_custom/NCBITaxa/.etetoolkit/taxa.sqlite", help='Path to NCBI taxa DB')
    parser.add_argument('-c', '--contigFile', type=str, required=True, help='CSV with contig counts')

    args = parser.parse_args()

    extractInfoInputPath = args.inputFile
    getNameInputPath = args.inputFile1
    outputPath = args.outputFile
    minReads = args.minimum_reads
    ncbiDB = args.ncbi_taxa
    contigFilePath = args.contigFile

    # Vérifier l'existence des fichiers
    for f in [extractInfoInputPath, getNameInputPath, contigFilePath]:
        if not os.path.exists(f):
            raise FileNotFoundError(f"Fichier introuvable : {f}")

    ncbi = NCBITaxa(dbfile=ncbiDB)

    inputFileV1 = os.path.basename(extractInfoInputPath)
    sampleID = inputFileV1.split('_extractInfo')[0]
    folder = os.path.dirname(extractInfoInputPath)
    outputGraphFolder = os.path.join(folder, f"Depth_Graphs_{sampleID}")

    if not os.path.exists(outputGraphFolder):
        os.makedirs(outputGraphFolder)

    lineToCopy = []
    dictListSpecies = {}

    # Charger les espèces depuis _count.txt
    with open(getNameInputPath) as getNameFile:
        for line in getNameFile:
            split = line.strip().split(',')
            if len(split) >= 3:
                taxID, speciesName, countReads = split[0], split[1], split[2]
                if speciesName != "UNKNOWN":
                    try:
                        name = ncbi.get_taxid_translator([taxID]).get(taxID, speciesName.replace("/", "_"))
                        dictListSpecies[taxID] = name
                        lineToCopy.append(f"{taxID},{name},{countReads}")
                    except KeyError:
                        continue

    dictListCoverage = {}
    dictListSizeGenome = {}
    dictListGenus = {}

    current_species = None
    coverList = []
    sizeSubject = 0
    coordStart = []
    coordEnd = []

    # Traiter le fichier extractInfo
    with open(extractInfoInputPath) as extractInfoFile:
        for ligne in extractInfoFile:
            hashed = ligne.strip().split('\t')
            if len(hashed) < 8:
                continue

            species = hashed[7].strip()
            if species == '0':
                continue

            if species != current_species:
                if current_species and len(coverList) > minReads:
                    coveragePercent = round(((len(coverList) - coverList.count(0)) / len(coverList) * 100), 5)
                    dictListCoverage[current_species] = str(coveragePercent)
                    dictListSizeGenome[current_species] = str(sizeSubject)

                    try:
                        lineage = ncbi.get_lineage(current_species)
                        ranks = ncbi.get_rank(lineage)
                        genus_taxid = next((tid for tid in lineage if ranks.get(tid) == 'genus'), None)
                        genus_name = ncbi.get_taxname_from_taxid(genus_taxid) if genus_taxid else "unclassified"
                    except Exception as e:
                        genus_name = "unclassified"

                    dictListGenus[current_species] = genus_name

                    x = np.arange(len(coverList))
                    plt.figure(figsize=(10, 4))
                    plt.plot(x, coverList, color="#F44336")
                    plt.fill_between(x, 0, coverList, facecolor="#000000", alpha=0.3)
                    plt.xlim(left=0, right=len(coverList))
                    plt.ylim(bottom=0)
                    plt.ylabel('Depth')
                    plt.xlabel(f"{dictListSpecies.get(current_species, 'Unknown')} (genus: {genus_name})", fontsize=10)
                    plt.tight_layout()
                    plt.savefig(os.path.join(outputGraphFolder, f"{dictListSpecies.get(current_species, 'Unknown')}.png"), dpi=100)
                    plt.close()

                current_species = species
                sizeSubject = int(hashed[6])
                coverList = [0] * (sizeSubject + 1)

            coordStart_temp = min(int(hashed[2]), int(hashed[3]))
            coordEnd_temp = max(int(hashed[2]), int(hashed[3]))

            if coordEnd_temp >= len(coverList):
                coordEnd_temp = len(coverList) - 1

            for i in range(coordStart_temp, coordEnd_temp + 1):
                coverList[i] += 1

        # Dernière espèce
        if current_species and len(coverList) > minReads:
            coveragePercent = round(((len(coverList) - coverList.count(0)) / len(coverList) * 100), 5)
            dictListCoverage[current_species] = str(coveragePercent)
            dictListSizeGenome[current_species] = str(sizeSubject)

    # Charger les contigs
    contigDict = {}
    with open(contigFilePath) as contigFile:
        contigFile.readline()  # sauter l'en-tête
        for line in contigFile:
            split = line.strip().split(',')
            if len(split) >= 4:
                contigDict[split[2].strip()] = split[3].strip()

    # Compter les contigs uniques
    uniqueContigCounts = {}
    with open(extractInfoInputPath) as extractInfoFile:
        for ligne in extractInfoFile:
            hashed = ligne.strip().split('\t')
            if len(hashed) < 8:
                continue
            species = hashed[7].strip()
            if species != '0':
                if species not in uniqueContigCounts:
                    uniqueContigCounts[species] = set()
                uniqueContigCounts[species].add(hashed[1])

    countUniqueContigs = {k: len(v) for k, v in uniqueContigCounts.items()}

    # Générer la sortie
    with open(outputPath, 'w') as out_file:
        for line in lineToCopy:
            parts = line.strip().split(',')
            if len(parts) < 3:
                continue
            taxID = parts[0]
            numContigs = contigDict.get(taxID, 'N/A')
            uniqueCount = countUniqueContigs.get(taxID, 'N/A')
            genus = dictListGenus.get(taxID, 'N/A')
            out_file.write(f"{line},{dictListCoverage.get(taxID, 'N/A')},{dictListSizeGenome.get(taxID, 'N/A')},{genus},{numContigs},{uniqueCount}\n")

if __name__ == "__main__":
    main()
