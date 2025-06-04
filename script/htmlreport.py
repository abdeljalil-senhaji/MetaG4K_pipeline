#!/usr/bin/env python3
#coding: utf-8



# Abdeljalil SENHAJI RACHIK
# version  01/03/2023 python3.7+
# Create report  html


import re
import os
import math
import sys
import numpy as np
from jinja2 import Environment, FileSystemLoader
import argparse

class VirusTable:
    def __init__(self,virusid,virusname,verified,rpmverified,coverage,score,genus):
        self.VirusID = virusid
        self.VirusName = virusname
        self.ConservedReads = verified
        self.ConservedRPM = rpmverified
        self.PercentCoverage = coverage
        self.Score = score
        self.Genus = genus

class BacteriaTable:
    def __init__(self,bacteriaid,bacterianame,bacteriagenus,verified,uniqhit,targets):
        self.BacteriaID = bacteriaid
        self.BacteriaName = bacterianame
        self.BacteriaGenus = bacteriagenus
        self.ConservedReads = verified
        self.UniqHit = uniqhit
        self.NbTargets = targets

class MetaphlanTable:
    def __init__(self,metaphlanid,metaphlanname,metaphlangenus,verified,uniqhit,targets):
        self.MetaphlanID = metaphlanid
        self.MetaphlanName = metaphlanname
        self.MetaphlanGenus = metaphlangenus
        self.ConservedReads = verified
        self.UniqHit = uniqhit
        self.NbTargets = targets
class ArgosTable:
    def __init__(self,argosid,argosname,verified,rpmverified,coverage,score,genus):
        self.ArgosID = argosid
        self.ArgosName = argosname
        self.ConservedReads = verified
        self.ConservedRPM = rpmverified
        self.PercentCoverage = coverage
        self.Score = score
        self.Genus = genus

class FungiTable:
    def __init__(self,Fungiid,Funginame,verified,rpmverified,coverage,score,genus,totalnbrcontigs,nbrcontigs):
        self.FungiID = Fungiid
        self.FungiName = Funginame
        self.ConservedReads = verified
        self.ConservedRPM = rpmverified
        self.PercentCoverage = coverage
        self.Score = score
        self.Genus = genus
        self.TotalNbrContigs = totalnbrcontigs
        self.NbrContigs = nbrcontigs

class ParasiteTable:
    def __init__(self,Parasiteid,Parasitename,verified,rpmverified,coverage,score,genus,totalnbrcontigs,nbrcontigs):
        self.ParasiteID = Parasiteid
        self.ParasiteName = Parasitename
        self.ConservedReads = verified
        self.ConservedRPM = rpmverified
        self.PercentCoverage = coverage
        self.Score = score
        self.Genus = genus
        self.TotalNbrContigs = totalnbrcontigs
        self.NbrContigs = nbrcontigs


class InfoTable:
    def __init__(self,totalreads,percentalignment,percentalignmentMS2,percentalignmentT1,nbtotal,preprocess,classified,human,percenthuman,bacteria,percentbacteria,viruses,percentviruses,fungi,percentfungi,parasite,percentparasite):
        self.TotalReads = totalreads
        self.PercentAlignment = percentalignment
        self.PercentAlignmentMS2 = percentalignmentMS2
        self.PercentAlignmentT1 = percentalignmentT1
        self.NbReadsTotal = nbtotal
        self.Preprocess = preprocess
        self.Classified = classified
        self.Human = human
        self.percentHuman = percenthuman
        self.Bacteria = bacteria
        self.percentBacteria = percentbacteria
        self.Viruses = viruses
        self.percentViruses = percentviruses
        self.Fungi = fungi
        self.percentFungi = percentfungi
        self.Parasite = parasite
        self.percentParasite = percentparasite

class GenusTableSum:
    def __init__(self,genusname,readssample):
        self.GenusName = genusname
        self.ReadsSample = readssample

parser=argparse.ArgumentParser(description='Generate HTML report')

parser.add_argument('-i', '--inputFile', type=str, nargs=1, help='info.txt file', required=True)
parser.add_argument('-s', '--inputFileStats', type=str, nargs=1, help='stats.txt file', required=True)
parser.add_argument('-s2', '--inputFileStatsMS2', type=str, nargs=1, help='MS2_stats.txt file', required=True)
parser.add_argument('-s1', '--inputFileStatsT1', type=str, nargs=1, help='T1_stats.txt file', required=True)
parser.add_argument('-o', '--outputFile', type=str, nargs=1, help='html file', required=True)
parser.add_argument('-t','--templates_f', type=str, nargs=1, help='Template folder localisation', default="templates")

args = parser.parse_args()

inputPath=args.inputFile[0]
inputPathStats=args.inputFileStats[0]
inputPathStatsMS2=args.inputFileStatsMS2[0]
inputPathStatsT1=args.inputFileStatsT1[0]
outputPath=args.outputFile[0]
templatesFolder=args.templates_f[0]

inputFile=re.split('/',inputPath)[-1]
inputFileStats=re.split('/',inputPathStats)[-1]
inputFileStatsMS2=re.split('/',inputPathStatsMS2)[-1]
inputFileStatsT1=re.split('/',inputPathStatsT1)[-1]
outputFile=re.split('/',outputPath)[-1]

sampleID=re.split('\\.info',inputFile)[0]
folder=re.split(inputFile,inputPath)[0]


VirusesFolder=os.path.join(folder,"Viruses")
BacteriaFolder=os.path.join(folder,"Bacteria")
MetaphlanFolder = os.path.join(BacteriaFolder, "Metaphlan")
ArgosFolder = os.path.join(BacteriaFolder, "Argos")
FungiFolder=os.path.join(folder,"Fungi")
ParasiteFolder=os.path.join(folder,"Parasite")



sampleList=[]
sampleList.append(sampleID)


for sampleName in sampleList:
    with open(inputPath) as Sampleinfo, open(inputPathStats) as AnotherFile, open(inputPathStatsMS2) as AnotherFileMS2, open(inputPathStatsT1) as AnotherFileT1:
        line2=AnotherFile.readlines()
        totalreads_line = line2[0].strip('\n')
        totalreads = totalreads_line.split()[0]
        percentalignment_line = line2[4].strip('\n')
        percentalignment = percentalignment_line.split('(')[1].split(':')[0].strip()
        line3=AnotherFileMS2.readlines()
        percentalignmentMS2_line = line3[4].strip('\n')
        percentalignmentMS2 = percentalignmentMS2_line.split('(')[1].split(':')[0].strip()
        line4=AnotherFileT1.readlines()
        percentalignmentT1_line = line4[4].strip('\n')
        percentalignmentT1 = percentalignmentT1_line.split('(')[1].split(':')[0].strip()
        line=Sampleinfo.readlines()
        nbtotal=line[0].strip('\n')
        preprocess=line[1].strip('\n')
        classified=line[2].strip('\n')
        human=line[3].strip('\n')
        percenthuman=round((int(human)/int(preprocess)*100),3)
        bacteria=line[4].strip('\n')
        percentbacteria=round((int(bacteria)/int(preprocess)*100),3)
        viruses=line[5].strip('\n')
        percentviruses=round((int(viruses)/int(preprocess)*100),3)
        fungi=line[6].strip('\n')
        percentfungi=round((int(fungi)/int(preprocess)*100),3)
        parasite=line[7].strip('\n')
        percentparasite=round((int(parasite)/int(preprocess)*100),3)

        SampleInfoTable=InfoTable(totalreads,percentalignment,percentalignmentMS2,percentalignmentT1,nbtotal,preprocess,classified,human,percenthuman,bacteria,percentbacteria,viruses,percentviruses,fungi,percentfungi,parasite,percentparasite)

#-----------------------------Viruses----------------------------#


    SampleVirusTable=[]
    GenusTableVir=[]
    GenusVirusTable={}
    with open(os.path.join(VirusesFolder,sampleName)+"_Viruses_allInfoCovrage.txt") as SamplecountVir:
        line = SamplecountVir.readline()
        while line:
            split=re.split(",",line)
            id=split[0]
            name=split[1]
            genus=split[5].strip("\n")
            verified=split[2]
            if int(verified) >= 5:
                rpmverified=round((int(split[2])/int(SampleInfoTable.Preprocess)*1000000),3)
                coverage=float(split[3])
                rpkm=(int(split[2])/int(SampleInfoTable.Preprocess)*1000000)/int(split[4].strip("/n"))
                score=np.log(rpmverified*coverage)
                VirusToAdd=VirusTable(id,name,verified,rpmverified,coverage,score,genus)
                SampleVirusTable.append(VirusToAdd)
                if genus in GenusVirusTable:
                    GenusVirusTable[genus]+=int(verified)
                else:
                    GenusVirusTable[genus]=int(verified)
            line = SamplecountVir.readline()
    for genusRow in GenusVirusTable:
        genusName=genusRow
        genusReads=GenusVirusTable[genusRow]
        genusTableRow=GenusTableSum(genusName,genusReads)
        GenusTableVir.append(genusTableRow)


#----------------------------- Fungi ----------------------------#


    SampleFungiTable=[]
    GenusTableFungi=[]
    GenusFungiTable={}
    with open(os.path.join(FungiFolder,sampleName)+"_Fungi_allInfoCovrage_test.txt") as SamplecountFungi:
        line = SamplecountFungi.readline()
        while line:
            split=re.split(",",line)
            id=split[0]
            name=split[1]
            genus=split[5]
            verified=split[2]
            nbrcontigs=split[7].strip("\n")
            totalnbrcontigs=split[6]
            if int(verified) >= 5:
                rpmverified=round((int(split[2])/int(SampleInfoTable.Preprocess)*1000000),3)
                coverage=float(split[3])
                rpkm=(int(split[2])/int(SampleInfoTable.Preprocess)*1000000)/int(split[4].strip("/n"))
                score=np.log(rpmverified*coverage)
                FungiToAdd=FungiTable(id,name,verified,rpmverified,coverage,score,genus,totalnbrcontigs,nbrcontigs)
                SampleFungiTable.append(FungiToAdd)
                if genus in GenusFungiTable:
                    GenusFungiTable[genus]+=int(verified)
                else:
                    GenusFungiTable[genus]=int(verified)
            line = SamplecountFungi.readline()
    for genusRow in GenusFungiTable:
        genusName=genusRow
        genusReads= GenusFungiTable[genusRow]
        genusTableRow=GenusTableSum(genusName,genusReads)
        GenusTableFungi.append(genusTableRow)


#------------------------------- Parasite --------------------------------#


    SampleParasiteTable=[]
    GenusTablePara=[]
    GenusParasiteTable={}
    with open(os.path.join(ParasiteFolder,sampleName)+"_Parasite_allInfoCovrage_test.txt") as SamplecountPara:
        line = SamplecountPara.readline()
        while line:
            split=re.split(",",line)
            id=split[0]
            name=split[1]
            genus=split[5]
            verified=split[2]
            nbrcontigs=split[7].strip("\n")
            totalnbrcontigs=split[6]
            if int(verified) >= 5:
                rpmverified=round((int(split[2])/int(SampleInfoTable.Preprocess)*1000000),3)
                coverage=float(split[3])
                rpkm=(int(split[2])/int(SampleInfoTable.Preprocess)*1000000)/int(split[4].strip("/n"))
                score=np.log(rpmverified*coverage)
                ParasiteToAdd=ParasiteTable(id,name,verified,rpmverified,coverage,score,genus,totalnbrcontigs,nbrcontigs)
                SampleParasiteTable.append(ParasiteToAdd)
                if genus in GenusParasiteTable:
                    GenusParasiteTable[genus]+=int(verified)
                else:
                    GenusParasiteTable[genus]=int(verified)
            line = SamplecountPara.readline()
    for genusRow in GenusParasiteTable:
        genusName=genusRow
        genusReads=GenusParasiteTable[genusRow]
        genusTableRow=GenusTableSum(genusName,genusReads)
        GenusTablePara.append(genusTableRow)

#------------------------------- Argos --------------------------------#


    SampleArgosTable=[]
    GenusTableArgos=[]
    GenusArgosTable={}
    with open(os.path.join(ArgosFolder,sampleName)+"_Argos_allInfoCovrage.txt") as SamplecountArgos:
        line = SamplecountArgos.readline()
        while line:
            split=re.split(",",line)
            id=split[0]
            name=split[1]
            genus=split[5].strip("\n")
            verified=split[2]
            if id == "1773" or int(verified) >= 5:
                rpmverified=round((int(split[2])/int(SampleInfoTable.Preprocess)*1000000),3)
                coverage=float(split[3])
                rpkm=(int(split[2])/int(SampleInfoTable.Preprocess)*1000000)/int(split[4].strip("/n"))
                score=np.log(rpmverified*coverage)
                ArgosToAdd=ArgosTable(id,name,verified,rpmverified,coverage,score,genus)
                SampleArgosTable.append(ArgosToAdd)
                if genus in GenusArgosTable:
                    GenusArgosTable[genus]+=int(verified)
                else:
                    GenusArgosTable[genus]=int(verified)
            line = SamplecountArgos.readline()
    for genusRow in GenusArgosTable:
        genusName=genusRow
        genusReads=GenusArgosTable[genusRow]
        genusTableRow=GenusTableSum(genusName,genusReads)
        GenusTableArgos.append(genusTableRow)


#-----------------------------Bacteria (Metaphlan)----------------------------#


    SampleMetaphlanTable=[]
    GenusTable=[]
    try:
        GenusMetaphlanTable={}
        with open(os.path.join(MetaphlanFolder,sampleName)+"_Metaphlan_NameBact.txt") as SamplecountBac:
            line = SamplecountBac.readline()
            while line:
                split=re.split(",",line)
                id=split[0]
                name=split[1]
                genus=re.split(" ",name)[0]
                verified=split[2]
                if id == "1773" or int(verified) >= 5:
                    uniqhit=split[3]
                    targets=split[4].strip("\n")
                    MetaphlanToAdd=MetaphlanTable(id,name,genus,verified,uniqhit,targets)
                    SampleMetaphlanTable.append(MetaphlanToAdd)
                    if genus in GenusMetaphlanTable:
                        GenusMetaphlanTable[genus]+=int(verified)
                    else:
                        GenusMetaphlanTable[genus]=int(verified)
                line = SamplecountBac.readline()
        for genusRow in GenusMetaphlanTable:
            genusName=genusRow
            genusReads=GenusMetaphlanTable[genusRow]
            genusTableRow=GenusTableSum(genusName,genusReads)
            GenusTable.append(genusTableRow)

    except:
        print("No bacteria analysis")
#-------------------------------------------------------------------------------#

    file_loader = FileSystemLoader(templatesFolder)
    env = Environment(loader=file_loader)
    template =env.get_template('html_page.html')
    output = template.render(sampleName=sampleName,listOfVirusesToShow=SampleVirusTable,listOfFungiToShow=SampleFungiTable,listOfParasiteToShow=SampleParasiteTable,listOfBacteriaToShow=SampleMetaphlanTable,listOfArgosToShow=SampleArgosTable,Table1Fill=SampleInfoTable,GenusTable=GenusTable,GenusTableVir=GenusTableVir,GenusTableFungi=GenusTableFungi,GenusTablePara=GenusTablePara,GenusTableArgos=GenusTableArgos)
    Page2=open(outputPath,"w")
    Page2.write(output)
    Page2.close()
    print("DOOOONEEEEE")
