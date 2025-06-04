#!/usr/bin/env python3
# coding: utf-8

import sys
import subprocess

fastqfile = sys.argv[1]
report = sys.argv[2]
info = sys.argv[3]

unclassified = 0
classified = 0
humanReads = 0
bacterialReads = 0
viralReads = 0
fungalReads = 0
eucaryotaReads = 0
parasiteReads = 0

with open(report, 'r') as report_file:
    lines = report_file.readlines()
    bacterial_line = None
    Viruses_line = None
    Fungi_line = None
    Eukaryota_line = None
    for line in lines:
        if "Bacteria" in line:
            bacterial_line = line
            break
    if bacterial_line:
        report_line_item = bacterial_line.split("\t")
        bacterialReads = int(report_line_item[1]) * 2
        
    for line in lines:
        if "Viruses" in line:
            Viruses_line = line
            break
    if Viruses_line:
        report_line_item = Viruses_line.split("\t")
        viralReads = int(report_line_item[1]) * 2
        
    for line in lines:
        if "Fungi" in line:
            Fungi_line = line
            break
    if Fungi_line:
        report_line_item = Fungi_line.split("\t")
        fungalReads = int(report_line_item[1]) * 2
        
    for line in lines:
        if "Eukaryota" in line:
            Eukaryota_line = line
            break
    if Eukaryota_line:
        report_line_item = Eukaryota_line.split("\t")
        eucaryotaReads = int(report_line_item[1]) * 2       
        
    for report_line in lines:
        if "unclassified" in report_line:
            report_line_item = report_line.split("\t")
            unclassified = int(report_line_item[1]) * 2
        elif "root" in report_line:
            report_line_item = report_line.split("\t")
            classified = int(report_line_item[1]) * 2
        elif "Homo sapiens" in report_line:
            report_line_item = report_line.split("\t")
            humanReads = int(report_line_item[1]) * 2

parasiteReads = eucaryotaReads - fungalReads

total_reads = int(subprocess.check_output(f"zcat {fastqfile} | grep '^+$' | wc -l", shell=True)) * 2
classified_unclassified = unclassified + classified

with open(info, 'w') as info_file:
    info_file.write(f"{total_reads}\n{classified_unclassified}\n{classified}\n{humanReads}\n{bacterialReads}\n{viralReads}\n{fungalReads}\n{parasiteReads}\n")
    
