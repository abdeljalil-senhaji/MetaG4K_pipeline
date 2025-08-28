#!/bin/bash

# Abdeljalil SENHAJI RACHIK
# version
# Sort an input file, count the occurrences of values in the eighth column, and save the sorted result in an output file.


# Analyser les options de la ligne de commande
while getopts "i:o:" option; do
  case "${option}" in
    i)
      extractInfo="${OPTARG}"
      ;;
    o)
      output="${OPTARG}"
      ;;
    *)
      echo "Usage: $0 -i <extractInfo_file> -o <output_file>"
      exit 1
      ;;
  esac
done

# Verifier si les fichiers d'entree existent et ne sont pas vides
if [ ! -s "$extractInfo" ]; then
  touch "$output"  # Creer un fichier de sortie vide
else
  # Trier le fichier extractInfo et sauvegarder le resultat dans un fichier temporaire
  sort -n "$extractInfo" -k8 > "${extractInfo%.*}.sorted.txt"
  mv "${extractInfo%.*}.sorted.txt" "$extractInfo"

  # Effectuer les operations de comptage
  cut -f8 "$extractInfo" | uniq -c | awk '{print $2, $1}' > "${extractInfo%.*}.temp1.txt"

  # Effectuer la jointure et le tri final, puis sauvegarder le resultat dans le fichier de sortie
  sort -k2,2 -gr "${extractInfo%.*}.temp1.txt" > "$output"

  # Supprimer les fichiers temporaires
  rm "${extractInfo%.*}.temp1.txt"
fi

echo "Commande executee : $0 $"
