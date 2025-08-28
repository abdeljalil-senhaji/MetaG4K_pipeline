#!/bin/bash

# Abdeljalil SENHAJI RACHIK
# version Antoine modifiy by Abdeljalil 01/03/2023
# create fasta file with seqkit




# Define the input arguments

#clseqs1="$1"
#clseqs2="$2"
#readnames="$3"
#output="$4"
#output2="$5"

# function help
function display_help {
  echo "Usage: $(basename "$0") -a clseqs1 -b clseqs2 -c readnames -o output"
  echo "  -a: Description de l'option a file R1 classified by kraken2."
  echo "  -b: Description de l'option b file R2 classified by kraken2."
  echo "  -c: Description de l'option c list readname."
  echo "  -o: Description de l'option o file output fq.gz"
  echo "  -h: Show this help and exit."
  exit 0
}

#  argment 
while getopts ":a:b:c:o:h" opt; do
  case $opt in
    a) clseqs1="$OPTARG"
    ;;
    b) clseqs2="$OPTARG"
    ;;
    c) readnames="$OPTARG"
    ;;
    o) output="$OPTARG"
    ;;
    h) display_help
    ;;
    \?) echo "Option invalide: -$OPTARG" >&2
        display_help
    ;;
  esac
done

# check that the required arguments have been passed
if [ -z "$clseqs1" ] || [ -z "$clseqs2" ] || [ -z "$readnames" ] || [ -z "$output" ]
then
  echo "Erreur: Les arguments -a, -b, -c et -o sont requis."
  display_help
fi

# display argment
echo "arg1: $clseqs1"
echo "arg2: $clseqs2"
echo "arg3: $readnames"
echo "arg4: $output"


# Create temporary files
temp_file=$(mktemp)
temp_fasta=$(mktemp)

# Filter the first clseqs file with the read names list
sed -E 's/(@[^ ]+)\/1 /\1 \/1 /' "$clseqs1"  | seqkit grep -f "$readnames" | gzip > "$temp_file" || true

# Convert the filtered clseqs file to fasta format
seqkit fq2fa "$temp_file" -o "$temp_fasta"

# Check if the first filtering and conversion was successful
if [ $? -eq 0 ]; then
  rm "$temp_file"
  if [[ -s "$temp_fasta" ]]; then
    echo "Reads recovered for $clseqs1"
  else
    echo "Reads not recovered for $clseqs1"
  fi
else
  echo "FAIL for $clseqs1"
fi


# Repeat the process for the second clseqs file


temp_file1=$(mktemp)
temp_fasta1=$(mktemp)

sed -E 's/(@[^ ]+)\/2 /\1 \/2 /' "$clseqs2" | seqkit grep -f "$readnames" | gzip > "$temp_file1" || true
seqkit fq2fa "$temp_file1" -o "$temp_fasta1"

if [ $? -eq 0 ]; then
  rm "$temp_file1"
  if [[ -s "$temp_fasta1" ]]; then
    echo "Reads recovered for $clseqs2"
  else
    echo "Reads not recovered for $clseqs2"
  fi
else
  echo "FAIL for $clseqs2"
fi


# Concatenate the recovered reads from both clseqs files into the output file


if [[ -s "$temp_fasta" && -s "$temp_fasta1" ]]; then
  cat "$temp_fasta" "$temp_fasta1" > "$output"
  rm "$temp_fasta"
  rm "$temp_fasta1"
elif [[ ! -s "$temp_fasta" && -s "$temp_fasta1" ]]; then
  mv "$temp_fasta1" "$output"
elif [[ -s "$temp_fasta" && ! -s "$temp_fasta1" ]]; then
  mv "$temp_fasta" "$output"
elif [[ ! -s "$temp_fasta" && ! -s "$temp_fasta1" ]]; then
  touch "$output"
fi

echo "Generation of the fasta file > ...................... DONE !"

