# MetaG4K_pipeline

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Snakemake](https://img.shields.io/badge/snakemake-%20≥7.0-brightgreen.svg)](https://snakemake.readthedocs.io)
[![Status](https://img.shields.io/badge/status-active-brightgreen)](#)

> **Clinical Metagenomics Pipeline**

##  Description

> **A robust Snakemake pipeline for clinical metagenomic analysis**  
> Written in Snakemake, this pipeline supports the complete metagenomic analysis of Illumina short-read sequencing data. It performs dual analyses — classification and taxonomic assignment — and synthesizes the results into a clear and concise HTML report. Task scheduling is optimized through the use of the Godocker cluster.

---

## Table of Contents
- [1. Context and Objectives](#-context-and-objectives)
- [2. Key Features](#-key-features)
- [3. Project Structure](#-project-structure)
- [4. Prerequisites and Installation](#-prerequisites-and-installation)
- [5. Configuration](#-configuration)
- [6. Usage](#-usage)
- [7. Error Handling](#-error-handling)
- [8. Output Report](#-output-report)
- [9. Deployment](#-deployment)
- [10. License](#-license)


---

##  1. Context and Objectives

**MetaG4K_pipeline** is a bioinformatics pipeline designed for **high-throughput clinical metagenomics**. It is specifically optimized to:
- Identify microorganisms present in a sample (bacteria, viruses, fungi, parasites),
- Remove human sequences and contaminants,
- Generate interpretable reports for biologists and clinicians.

Built on **Snakemake**, it runs on a cluster (Godocker) and ensures full traceability of analyses.

---

## 2. Key Features

- ✅ **Multi-kingdom detection**: Bacteria, Viruses, Fungi, Parasite  
- ✅ **Rigorous filtering**: removal of human reads, duplicates, and short sequences  
- ✅ **Taxonomic classification**: via Kraken2 and targeted BLAST alignment  
- ✅ **Automated HTML reporting**: statistics, plots, taxon lists  
- ✅ **Automatic resume**: restarts from the last completed step after interruption  
- ✅ **Compatible with G-route**: for routine use in clinical settings  

---

##  3. Project Structure

```bash
MetaG4K_pipeline/
├── Snakefile                     # Main workflow (Snakemake)
├── config.json                   # Global configuration (paths, samples, parameters)
├── cluster.json                  # Resource configuration (Godocker, memory, threads)
├── main/                         # Main pipeline scripts (Python/Bash)
├── script/                       # Utility scripts (extraction, filtering, taxid mapping)
├── Snakemake-rules/              # Modular Snakemake rules per analysis step
├── graph_dotRule/                # Workflow graphs in DOT format
├── data/                         # Input: raw FASTQ files (to be placed here)
├── results/                      # Output: reports, contigs, taxonomic lists
├── bases/                        # Local databases (Kraken2, BLAST, NCBI taxdump)
├── clean.sh                      # Cleans temporary and cache files
├── save.sh                       # Backs up results to external storage
├── commandLine.sh                # Launches the full pipeline from command line
├── commandLine_rerun-incomplete.sh # Restarts pipeline from last incomplete step
├── script_git.sh                 # Git management scripts (optional)
└── README.md                     # Project documentation
```
##  Note

The `data/`, `results/`, and `bases/` directories must be created or configured according to your environment.  The `bases/` directory is implied by the requirement for pre-downloaded Kraken2 and BLAST databases, and should contain those databases.

---

##  4. Prerequisites and Installation

### Prerequisites

- [x] **Snakemake** ≥ 7.0: `conda install -c conda-forge snakemake`
- [x] **Python** ≥ 3.8 (with modules: `ete3`, `pandas`, `matplotlib`)
- [x] **Godocker** or access to the Moabi cluster
- [x] Installed tools: `kraken2`, `bowtie2`, `samtools`, `makeblastdb`, `blastn`, `fastp`
- [x] Pre-downloaded Kraken2 and BLAST databases

### Installation

```bash
git clone https://github.com/abdeljalil-senhaji/MetaG4K_pipeline.git
cd MetaG4K_pipeline
```

Configure the paths in config.json according to your environment.


##  5. Configuration

The config.json file centralizes all parameters:
```bash
{
  "prefix": "/scratch/",
  "data_dir": "data",
  "results_dir": "results",
  "kraken_db": "/shared/databases/kraken2/pluspf",
  "blast_db": "/shared/databases/blast/nt",
  "taxdump": "/shared/databases/ncbi_taxdump",
  "threads": 16,
  "samples": ["sample1", "sample2"]
}
```

##  6. Usage

On the command line (Moabi):
```bash
# 1. Clean old files
bash clean.sh

# 2. Place FASTQ files in data/
# Example: sample1_R1.fastq.gz, sample1_R2.fastq.gz

# 3. Run the pipeline
bash commandLine.sh

# 4. In case of interruption, resume here:
bash commandLine_rerun-incomplete.sh
```

##  7. Error Handling
Common errors:

* Incorrectly named FASTQ files: must follow the format _R1_001.fastq.gz or _R1.fastq.gz
* Missing R1 or R2 files
* Cluster overload → restart with commandLine_rerun-incomplete.sh

Diagnostics:

* Via Go-docker: search for the job by ID → god.err file
* On the command line: ```bash godfile download <job-id> god.err```

## 8. Output Report

At the end of the pipeline, an HTML report is generated in:

```bash results/{sample}/report_{sample}.html```

It contains :

*  Mapping and classification statistics
*  Interactive taxonomic tree
*  Tables of dominant taxa by kingdom
*  Links to extracted contigs and reads

> The pipeline is designed to be modular, reproducible, and traceable.


##  9. Deployment

* In production: via  [G-route]()
* In development: local execution or on the Moabi cluster
* Job monitoring: [Go-docker]()



## 10. License

Distributed under the MIT License.

See the [LICENSE]() file for more details. (In progress)

