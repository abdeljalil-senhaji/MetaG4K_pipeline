#!/usr/bin/env python3
# coding: utf-8


# Abdeljalil SENHAJI RACHIK
# version 0.1 python3.7+

import re
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np
from ete3 import NCBITaxa


def listOfSizeN(N):
    return [0] * (N + 1)


def main():
    parser = argparse.ArgumentParser(description='Generate Coverage/Depth plot for Viruses, Parasite, Fungi, silva16S et Argos')

    parser.add_argument('-e', '--inputFile', type=str, nargs=1, required=True,
                        help='extractInfo_vir_fun_par.txt and silva16S, Argos')
    parser.add_argument('-g', '--inputFile1', type=str, nargs=1, required=True,
                        help='_*_count.txt')
    parser.add_argument('-o', '--outputFile', type=str, nargs=1, required=True,
                        help='_*_allInfoCovrage.txt')
    parser.add_argument('-m', '--minimum_reads', type=int, nargs=1, default=[5],
                        help='Minimum number of reads to draw a plot (default=5)')
    parser.add_argument('-n', '--ncbi_taxa', type=str, nargs=1,
                        default=["/data/annotations/Blast/12_08_2019_custom/NCBITaxa/.etetoolkit/taxa.sqlite"],
                        help='Localization of NCBI Taxa database')
    parser.add_argument('-c', '--contigFile', type=str, nargs=1, required=True,
                        help='Fichier CSV contenant le nombre de contigs')

    args = parser.parse_args()

    extractInfoInputPath = args.inputFile[0]
    getNameInputPath = args.inputFile1[0]
    outputPath = args.outputFile[0]
    minReads = args.minimum_reads[0]
    ncbiDB = args.ncbi_taxa[0]
    contigFilePath = args.contigFile[0]

    ncbi = NCBITaxa(dbfile=ncbiDB)

    inputFileV1 = os.path.basename(extractInfoInputPath)
    inputFileV2 = os.path.basename(getNameInputPath)
    outputFile = os.path.basename(outputPath)

    sampleID = inputFileV1.split('_extractInfo')[0]
    folder = extractInfoInputPath[: -len(inputFileV1)]

    # --- Chargement des informations sur les espèces ---
    lineToCopy = []
    dictListSpecies = {}

    with open(getNameInputPath, 'r') as getNameFile:
        for line in getNameFile:
            split = line.strip().split(',')
            if len(split) >= 3:
                taxID = split[0]
                speciesName = split[1]
                countReads = split[2]
                if speciesName != "UNKNOWN":
                    try:
                        taxIDInt = int(taxID)
                        taxNameDic = ncbi.get_taxid_translator([taxIDInt])
                        taxName = taxNameDic.get(taxIDInt, speciesName.replace("/", "_"))
                        dictListSpecies[taxIDInt] = taxName
                    except Exception:
                        # En cas de problème avec taxID, on garde le nom brut
                        dictListSpecies[taxID] = speciesName.replace("/", "_")
                        taxName = speciesName.replace("/", "_")
                    lineToCopy.append(f"{taxID},{taxName},{countReads}")

    # Création du dossier pour les graphiques si nécessaire
    outputGraphFolder = os.path.join(folder, f"Depth_Graphs_{sampleID}")
    if not os.path.exists(outputGraphFolder):
        os.mkdir(outputGraphFolder)

    dictListCoverage = {}
    dictListSizeGenome = {}
    dictListGenus = {}

    # --- Lecture et traitement du fichier extractInfo ---
    with open(extractInfoInputPath, 'r') as extractInfoFile:
        ligne = extractInfoFile.readline()
        while ligne:
            hashed = ligne.strip().split('\t')
            if len(hashed) < 8:
                ligne = extractInfoFile.readline()
                continue  # ignorer les lignes mal formées

            species = hashed[7]
            if species in ('0', ''):
                ligne = extractInfoFile.readline()
                continue

            numContigs = hashed[1].strip()

            try:
                lineage = ncbi.get_lineage(int(species))
            except Exception:
                print(f"Tax ID {species} not found in lineage. Skipping entry.")
                ligne = extractInfoFile.readline()
                continue

            try:
                sizeSubject = int(hashed[6])
            except Exception:
                print(f"Erreur sur la taille du génome pour taxID {species}. Ligne ignorée.")
                ligne = extractInfoFile.readline()
                continue

            coverList = listOfSizeN(sizeSubject)
            coordStart = []
            coordEnd = []

            speciesTick = species

            # Parcours des lignes pour la même espèce
            while ligne and species == speciesTick:
                parts = ligne.strip().split('\t')
                if len(parts) < 8:
                    break  # Ligne mal formée, sortir

                start = min(int(parts[2]), int(parts[3]))
                end = max(int(parts[2]), int(parts[3]))
                coordStart.append(start)
                coordEnd.append(end)

                ligne = extractInfoFile.readline()
                if not ligne:
                    break
                hashed = ligne.strip().split('\t')
                speciesTick = hashed[7] if len(hashed) > 7 else None

            # Mise à jour de la couverture
            for j in range(len(coordStart)):
                start = coordStart[j]
                end = coordEnd[j]
                # Limiter les indices pour éviter les erreurs
                for i in range(start, end + 1):
                    if 0 <= i < len(coverList):
                        coverList[i] += 1

            coveragePercent = round(((len(coverList) - coverList.count(0)) / len(coverList)) * 100, 5)
            dictListCoverage[species] = str(coveragePercent)
            dictListSizeGenome[species] = str(sizeSubject)

            ranks = ncbi.get_rank(lineage)
            genus_taxid = next((taxid for taxid, rank in ranks.items() if rank == 'genus'), None)
            if genus_taxid is not None:
                try:
                    taxid2name = ncbi.get_taxid_translator([genus_taxid])[genus_taxid]
                except Exception:
                    taxid2name = "Genus sp."
                dictListGenus[species] = taxid2name
            else:
                dictListGenus[species] = "Genus sp."

            # Tracer le graphique si nombre de reads >= minReads
            if len(coordStart) >= minReads:
                x = np.arange(len(coverList))
                plt.plot(x, coverList, color="#F44336")
                plt.fill_between(x, 0, coverList, facecolor="#000000")
                plt.xlim(left=0.0, right=len(coverList))
                plt.ylim(bottom=0.0)
                plt.ylabel('Depth')

                try:
                    species_int = int(species)
                    speciesName = dictListSpecies.get(species_int, species).replace("/", "_")
                except Exception:
                    speciesName = species.replace("/", "_")

                xlabel = speciesName
                if genus_taxid is not None:
                    xlabel += f" (genus: {taxid2name})"

                plt.xlabel(xlabel)
                output_file = os.path.join(outputGraphFolder, f"{speciesName}.png")
                plt.savefig(output_file, bbox_inches='tight')
                plt.clf()
                print(f"{speciesName}.png generated")

    # --- Charger les contigs ---
    contigDict = {}
    with open(contigFilePath, 'r') as contigFile:
        _ = contigFile.readline()  # Skip header
        for line in contigFile:
            split = line.strip().split(',')
            if len(split) >= 4:
                taxID = split[2].strip()
                numContigs = split[3].strip()
                contigDict[taxID] = numContigs
                print(f"Contig chargé : {taxID} -> {numContigs}")

    # --- Compter les contigs uniques à partir de extractInfoInputPath ---
    uniqueContigCounts = {}

    with open(extractInfoInputPath, 'r') as extractInfoFile:
        for ligne in extractInfoFile:
            hashed = ligne.strip().split('\t')
            if len(hashed) < 8:
                continue
            species = hashed[7]
            contig_name = hashed[1].strip()
            if species != '0' and species != '':
                if species not in uniqueContigCounts:
                    uniqueContigCounts[species] = set()
                uniqueContigCounts[species].add(contig_name)

    countUniqueContigs = {taxID: len(contigs) for taxID, contigs in uniqueContigCounts.items()}

    # --- Générer le fichier de sortie ---
    with open(outputPath, 'w') as count:
        for line in lineToCopy:
            part1 = line.split(',')[0].strip()
            numContigs = contigDict.get(part1, 'N/A')
            uniqueCount = countUniqueContigs.get(part1, 'N/A')
            coverage = dictListCoverage.get(part1, 'N/A')
            genomeSize = dictListSizeGenome.get(part1, 'N/A')
            genus = dictListGenus.get(part1, 'N/A')
            count.write(f"{line},{coverage},{genomeSize},{genus},{numContigs},{uniqueCount}\n")


if __name__ == "__main__":
    main()
