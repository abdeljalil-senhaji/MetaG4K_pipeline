#!/usr/bin/env python3
#coding: utf-8


import pandas as pd
from collections import defaultdict
import argparse

# Fonction pour traiter le fichier BLAST et extraire les informations
def process_blast_output(input_file1, input_file2, output_file):
    # Dictionnaire pour compter les occurrences des contigs
    contig_counts = defaultdict(int)
    
    # Liste pour stocker les resultats
    results = []

    # Lecture du fichier d'entree BLAST
    with open(input_file1, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 8:
                taxid = parts[7]  # 8eme colonne
                name_contig = parts[1]  # 2eme colonne
                
                # Ajout au dictionnaire pour compter les occurrences
                contig_counts[name_contig] += 1
                
                # Stockage des resultats pour le tableau
                results.append((taxid, name_contig))

    # Creation d un DataFrame a partir des resultats
    df = pd.DataFrame(results, columns=['Taxid', 'Name_contigs'])

    # Comptage des occurrences par contig
    occurrence_counts = df.groupby(['Taxid', 'Name_contigs']).size().reset_index(name='nombre_d_occurrence')

    # Lecture du fichier des especes
    #species_df = pd.read_csv(input_file2, sep='\t') 
    species_df = pd.read_csv(input_file2, sep=',', quotechar='"')
    # Conversion des colonnes Taxid et TaxID en chaines de caracteres
    occurrence_counts['Taxid'] = occurrence_counts['Taxid'].astype(str)
    species_df['TaxID'] = species_df['TaxID'].astype(str)

    # Fusionner les deux DataFrames sur TaxID
    merged_df = pd.merge(occurrence_counts, species_df, left_on='Taxid', right_on='TaxID', how='left')

    # Selectionner les colonnes finales
    final_df = merged_df[['Taxid', 'Name_contigs', 'nombre_d_occurrence', 'species', 'Nombre_de_Contigs']]

    # Ecriture des resultats dans le fichier de sortie au format CSV
    final_df.to_csv(output_file, index=False)

# Fonction principale pour gerer les arguments
def main():
    parser = argparse.ArgumentParser(description='Process BLAST output and species information.')
    parser.add_argument('-i1', '--input1', required=True, help='Input BLAST output file')
    parser.add_argument('-i2', '--input2', required=True, help='Input species information file')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')

    args = parser.parse_args()

    # Appel de la fonction avec les arguments
    process_blast_output(args.input1, args.input2, args.output)

# Point d'entree du script
if __name__ == '__main__':
    main()
