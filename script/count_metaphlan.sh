#!/bin/bash



# Abdeljalil SENHAJI RACHIK
# version
# Analyze the command-line options, and if the input file is not empty, sort the input file, count the occurrences of values in the eighth column. part metaphlan



# Initialiser les variables des fichiers d'entree et sortie
conserved=""
counting=""
sorteds=""
genesMetaphlan=""

# Analyser les options de la ligne de commande
while getopts "i:o:g:" option; do
  case "${option}" in
    i)
      conserved="${OPTARG}"
      ;;
    o)
      counting="${OPTARG}"
      sorteds="${counting%.*}.sorted.txt"
      ;;
    g)
      genesMetaphlan="${OPTARG}"
      ;;
    *)
      echo "Usage: $0 -i <conserved_file> -g <genesMetaphlan_file> -o <counting_file>"
      exit 1
      ;;
  esac
done


if [ ! -s "$conserved" ]; then
  touch "$counting"
  touch "$sorteds"
else
  # Trier le fichier conserved etians le fichier sorted
  sort -n "$conserved" -k8 > "$sorteds"

  cut -f8 "$sorteds" | uniq -c | sort -k2,2 -g > "${counting%.*}.temp1.txt"

  cut -f2,8 "$sorteds" | sort -k1,1 | uniq | cut -f2 | sort -g | uniq -c > "${counting%.*}.temp2.txt"

  join -1 2 -2 2 "${counting%.*}.temp1.txt" "${counting%.*}.temp2.txt" | sort -k1,1b > "${counting%.*}.temp3.txt"

  join -1 1 -2 1 "${counting%.*}.temp3.txt" "$genesMetaphlan" | sort -k2,2 -gr > "$counting"

  # Supprimer les fichiers temporaires
  rm "${counting%.*}.sorted.txt"
  rm "${counting%.*}.temp1.txt"
  rm "${counting%.*}.temp2.txt"
  rm "${counting%.*}.temp3.txt"
fi

# Enregistrer
echo "Dooooooonnneeeeeee >>>> Commande excutee: $0 $@"
