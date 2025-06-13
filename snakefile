import os



#=============== CONFIG FILES AND GENERAL PATHS ==================#

rulePath = config["general_path"]["RULE_PATH"]
workdir:  config["general_path"]["OUTPUT_PATH"]
output_path = config["general_path"]["OUTPUT_PATH"]


#======================== RULES ==============================#
 
include: rulePath+"/iget_samples_rule"
include: rulePath+"/dedupe_rule"
include: rulePath+"/trimmomatic_rule"
include: rulePath+"/bwa_mem_rule"
include: rulePath+"/samtools_flagstat_rule"
include: rulePath+"/samtools_process_rule"
include: rulePath+"/samtools_get_unmapped_rule"

include: rulePath+"/bwa_mem_T1_rule"
include: rulePath+"/samtools_process_T1_rule"
include: rulePath+"/samtools_flagstat_T1_rule"

include: rulePath+"/bwa_mem_MS2_rule"
include: rulePath+"/samtools_process_MS2_rule"
include: rulePath+"/samtools_flagstat_MS2_rule"

include: rulePath+"/samtools_merge_rule"
include: rulePath+"/samtools_get_unmapped_2_rule"

include: rulePath+"/kraken2_rule"
include: rulePath+"/iget_listTaxId_rule"
include: rulePath+"/iget_readNames_list_rule"
include: rulePath+"/seqkit_rule"
include: rulePath+"/iget_db_bacteria_rule"
include: rulePath+"/bacteria_blast_rule"
include: rulePath+"/extract_info_rule"
include: rulePath+"/extract_info_bact_rule"
include: rulePath+"/vir_fun_par_blast_rule"
include: rulePath+"/get_fasta_final_rule"
include: rulePath+"/get_fasta_final_bac_rule"
include: rulePath+"/infofile_rule"
include: rulePath+"/count_info_metaphlan_rule"
include: rulePath+"/getNames_metaphlan_rule"
include: rulePath+"/create_tab_info_contigs_rule"
include: rulePath+"/count_info_argos_silva_rule"
include: rulePath+"/getNames_argos_silva_rule"
include: rulePath+"/coverage_Argos_info_rule"
include: rulePath+"/count_info_rule"
include: rulePath+"/getNames_rule"
include: rulePath+"/coverage_Fungi_Parasite_info_rule"
include: rulePath+"/coverage_Viruses_info_rule"
include: rulePath+"/reportHtml_rule"
#============================= RECUP SAMPLES INFORMATIOS =================================#

mate_ids = ["R1","R2"]
kingdom_ids = ["Viruses","Bacteria","Fungi","Parasite"]
bac_kingdom_ids = ["Viruses","Fungi","Parasite"]
dbnames_ids = ["Argos","Metaphlan"]
argosSilva_ids = ["Argos"]
fungi_parasite_ids = ["Fungi","Parasite"]
Viruses_ids =  ["Viruses"]


sample_ids = []
directory = '/scratch/recherche/asenhaji/v10_pipMeta_4Kingdoms/data'
for sample_id in os.listdir(directory) :
        sample = os.path.basename(sample_id)
        for r in (('_R2_001.fastq.gz', ''), ('_R1_001.fastq.gz', ''), ('_R2.fastq.gz', ''), ('_R1.fastq.gz', '')):
              sample = sample.replace(*r)
        sample_ids.append(sample)


#=================================================== Output name ==================================================#

#iget_samples = expand((output_path+"/{sample_id}/{sample_id}.R1.fastq.gz", output_path+"/{sample_id}/{sample_id}.R2.fastq.gz"), sample_id=sample_ids)
#dedupe = expand((output_path + "/{sample_id}/{sample_id}.R1_dedupe.fastq.gz",output_path + "/{sample_id}/{sample_id}.R2_dedupe.fastq.gz"),sample_id = sample_ids)
#trimmomatic = expand((output_path + "/{sample_id}/{sample_id}R1_paired.fq.gz",output_path + "/{sample_id}/{sample_id}R2_paired.fq.gz",output_path + "/{sample_id}/{sample_id}R1_unpaired.fq.gz",output_path + "/{sample_id}/{sample_id}R2_unpaired.fq.gz"),sample_id = sample_ids)
#kraken2 = expand((output_path + "/{sample_id}/{sample_id}.report.txt",output_path + "/{sample_id}/{sample_id}.output.txt",output_path + "/{sample_id}/{sample_id}.clseqs_1.fastq",output_path + "/{sample_id}/{sample_id}.clseqs_2.fastq"),sample_id = sample_ids)
#iget_readNames_list =  expand(output_path + "/{sample_id}/{kingdom_id}/{sample_id}_readNames_list.txt", sample_id = sample_ids, kingdom_id = kingdom_ids)
#seqkit = expand(output_path + "/{sample_id}/{kingdom_id}/{sample_id}_seqfa.fasta", sample_id = sample_ids, kingdom_id = kingdom_ids)
#blast = expand((output_path + "/{sample_id}/{kingdom_id}/{sample_id}_blast.txt"), sample_id = sample_ids, kingdom_id = kingdom_ids),
#samtools_get_unmapped = expand((output_path+"/{sample_id}/{sample_id}_not_hg38.R1.fastq.gz", output_path+"/{sample_id}/{sample_id}_not_hg38.R2.fastq.gz") ,sample_id = sample_ids)
#bacteria_blast = expand(output_path + "/{sample_id}/Bacteria/{dbnames_id}/{sample_id}_{dbnames_id}_blast.txt", sample_id = sample_ids, dbnames_id = dbnames_ids),
#extract_info_bact = expand(output_path + "/{sample_id}/Bacteria/{dbnames_id}/{sample_id}_{dbnames_id}_extractInfo_blast.txt", sample_id = sample_ids, dbnames_id = dbnames_ids),
#vir_fun_par_blast = expand((output_path + "/{sample_id}/{bac_kingdom_id}/{sample_id}_{bac_kingdom_id}_blast.txt"), sample_id = sample_ids, bac_kingdom_id = bac_kingdom_ids)
#extract_info = expand((output_path + "/{sample_id}/{bac_kingdom_id}/{sample_id}_{bac_kingdom_id}_extractInfo_vir_fun_par.txt"), sample_id = sample_ids, bac_kingdom_id = bac_kingdom_ids),
#infofile = expand(output_path + "/{sample_id}/{sample_id}.info.txt", sample_id = sample_ids),
#sort_blast = expand((output_path + "/{sample_id}/{bac_kingdom_id}/{sample_id}.conserved.txt",output_path + "/{sample_id}/{bac_kingdom_id}/{sample_id}.notconserved.txt"),sample_id = sample_ids, bac_kingdom_id = bac_kingdom_ids)
#sort_blast_Bacteria = expand((output_path + "/{sample_id}/Bacteria/{dbnames_id}/{sample_id}.conserved.txt",output_path + "/{sample_id}/Bacteria/{dbnames_id}/{sample_id}.notconserved.txt"),sample_id = sample_ids, dbnames_id = dbnames_ids)
#blast_bacteria = expand((output_path + "/{sample_id}/Bacteria/{sample_id}_blast.txt"), sample_id = sample_ids)
#count_info_metaphlan = expand(output_path + "/{sample_id}/Bacteria/Metaphlan/{sample_id}_Metaphlan_count.metaphlan.txt", sample_id = sample_ids),
#getNames_metaphlan = expand(output_path + "/{sample_id}/Bacteria/Metaphlan/{sample_id}_Metaphlan_NameBact.txt", sample_id = sample_ids),
#count_info_argos_silva = expand(output_path + "/{sample_id}/Bacteria/{argosSilva_id}/{sample_id}_{argosSilva_id}_count.txt", sample_id = sample_ids, argosSilva_id = argosSilva_ids),
#getNames_argos_silva = expand(output_path + "/{sample_id}/Bacteria/{argosSilva_id}/{sample_id}_{argosSilva_id}_NameArgosSilva16S.txt", sample_id = sample_ids, argosSilva_id = argosSilva_ids),
#coverage_Argos_info =expand(output_path + "/{sample_id}/Bacteria/{argosSilva_id}/{sample_id}_{argosSilva_id}_allInfoCovrage.txt", sample_id = sample_ids, argosSilva_id = argosSilva_ids),
#count_info = expand(output_path + "/{sample_id}/Viruses/{sample_id}_Viruses_count.txt", sample_id = sample_ids, bac_kingdom_id = bac_kingdom_ids),
#getNames = expand(output_path + "/{sample_id}/{bac_kingdom_id}/{sample_id}_{bac_kingdom_id}_NameVirFunPar.txt", sample_id = sample_ids, bac_kingdom_id = bac_kingdom_ids),
#coverage_Viruses_info = expand(output_path + "/{sample_id}/{Viruses_id}/{sample_id}_{Viruses_id}_allInfoCovrage.txt", sample_id = sample_ids, Viruses_id = Viruses_ids),
#coverage_Fungi_Parasite_info = expand(output_path + "/{sample_id}/{fungi_parasite_id}/{sample_id}_{fungi_parasite_id}_allInfoCovrage_test.txt", sample_id = sample_ids, fungi_parasite_id = fungi_parasite_ids),

samtools_flagstat = expand(output_path+"/{sample_id}/{sample_id}.txt", sample_id=sample_ids),
samtools_flagstat_MS2 = expand(output_path+"/{sample_id}/{sample_id}_MS2.txt", sample_id=sample_ids),
samtools_flagstat_T1 = expand(output_path+"/{sample_id}/{sample_id}_T1.txt", sample_id=sample_ids),
iget_listTaxId =  expand(output_path + "/{sample_id}/{kingdom_id}/{kingdom_id}_taxids.txt", sample_id = sample_ids, kingdom_id = kingdom_ids),
iget_db_bacteria =  expand(output_path + "/{sample_id}/Bacteria/{dbnames_id}/{sample_id}_bacteria_seqfa.fasta", sample_id = sample_ids, dbnames_id = dbnames_ids),
get_fasta_final =  expand((output_path + "/{sample_id}/{bac_kingdom_id}/{sample_id}_{bac_kingdom_id}.fastarecupDone"),sample_id = sample_ids,bac_kingdom_id = bac_kingdom_ids),
get_fasta_final_bac =  expand((output_path + "/{sample_id}/Bacteria/{dbnames_id}/{sample_id}_{dbnames_id}.fastarecupDone"),sample_id = sample_ids,dbnames_id = dbnames_ids),
create_tab_info_contigs = expand((output_path + "/{sample_id}/{fungi_parasite_id}/{sample_id}_{fungi_parasite_id}_tab_info_contigs.csv"), sample_id = sample_ids, fungi_parasite_id = fungi_parasite_ids),
reportHtml = expand((output_path + "/{sample_id}/{sample_id}.html"), sample_id = sample_ids)
#=================================================== Rule all ==================================================#

rule all:
    input:
#       repair,
#       kraken2,
#       iget_readNames_list,
#       seqkit,
#       blast,
#       samtools_get_unmapped,
#       bacteria_blast,
#       viruses_blast,
#       fungi_blast,
#       parasite_blast,
#       extract_info_bact,
#       extract_info,
#       vir_fun_par_blast,
#       infofile,
#       count_info_metaphlan,
#       getNames_metaphlan,
#       count_info_argos_silva,
#       getNames_argos_silva,
#       coverage_Argos_info,
#       coverage_Fungi_Parasite_info,
#       count_info,
#       getNames,
#       coverage_Viruses_info
        samtools_flagstat,
        samtools_flagstat_MS2,
        samtools_flagstat_T1,
        iget_listTaxId,
        iget_db_bacteria,
        get_fasta_final,
        get_fasta_final_bac,
        create_tab_info_contigs,
        reportHtml
    shell:
        "touch "+output_path+"/done"
