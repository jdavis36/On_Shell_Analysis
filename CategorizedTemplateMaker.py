#!/usr/bin/env python
# convert jupyter to python get_ipython().system('jupyter nbconvert --to script CategorizedTemplateMake-Parts.ipynb')

import os
import glob
import ROOT as ROOT
from math import sqrt
import time
import getopt
#from pathlib import Path
import re
#from tqdm import trange, tqdm
import numpy as np
import copy
from array import *
from AnalysisTools.TemplateMaker.GetSyst import getsyst
from AnalysisTools.TemplateMaker.Sort_Category import sort_category_templates
from AnalysisTools.TemplateMaker.OnShell_Template import FillHistOnShell
from AnalysisTools.TemplateMaker.Unroll_gen import Unroll_1D_OnShell, Unroll_2D_OnShell, Unroll_3D_OnShell
from AnalysisTools.Utils import Config as Config
import sys

def main(argv):
    treelistpath = ''
    production = ''
    category = ''
    final_state = ''
    inputyear = ''
    outputdir = ''
    try:
        opts, args = getopt.getopt(argv,"hi:p:c:f:y:o:",["ifile=","pfile=","cfile=","ffile=","yfile=","ofile="])
    except getopt.GetoptError:
        print('CategorizedTemplateMaker.py -i <treelistpath> -p <production> -c <category> -f <final_state> -y <year> -o <output_directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('CategorizedTemplateMaker.py -i <treelistpath> -p <production> -c <category> -f <final_state> -y <year> -o <output_directory>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            treelistpath = arg
        elif opt in ("-p", "--pfile"):
            production = arg
        elif opt in ("-c", "--cfile"):
            category = arg
        elif opt in ("-f", "--ffile"):
            final_state = arg
        elif opt in ("-y", "--yfile"):
            inputyear = arg
        elif opt in ("-o", "--ofile"):
            outputdir = arg
    if not all([treelistpath, production, category, final_state, inputyear, outputdir]):
        print('CategorizedTemplateMaker.py -i <treelistpath> -p <production> -c <category> -fs <final_state> -y <year> -o <output_dir>')
        sys.exit(2)
    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"

    print("\n================ Reading user input ================\n")

    print("Input CJLST TTree is '{}'".format(treelistpath))
    print("Production mode is '{}'".format(production))
    print("Category is '{}'".format(category))
    print("Year is '{}'".format(inputyear))
    print("Final state is '{}'".format(final_state))
    print("Output Directory is '{}'".format(outputdir))

    print("\n================ Processing user input ================\n")
    
    if not os.path.exists(outputdir):
      os.mkdir(outputdir) 
    unrolled_dir = outputdir+"unrolled/"
    rolled_dir = outputdir+"rolled/"
    if not os.path.exists(unrolled_dir):
      os.mkdir(unrolled_dir)
    if not os.path.exists(rolled_dir):
      os.mkdir(rolled_dir)


    print("\n=============== Loading Analysis Config ===============\n")
    #====== Load Analysis Config =====#
    #Analysis_Config = Config.Analysis_Config("OnShell_HVV_Photons_2021")
    #Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only")
    #Analysis_Config = Config.Analysis_Config("gammaH_Cross_Section_Measurement")
    #Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics_Photon_Rate")
    #Analysis_Config = Config.Analysis_Config("Tree_Level_qqH_Photons_XS")    
    Analysis_Config = Config.Analysis_Config("Test_Optimal_Binning_All_Untagged")    
    
    lumi = Analysis_Config.lumi

    if Analysis_Config.Variable_Edges == True:
      medges = Analysis_Config.medges  
      d1edges = Analysis_Config.d1edges
      d2edges = ReweightingSamplePlus
      print("medges", len(medges))
      print("medges", (medges))
      print("d1edges", len(d1edges))
      print("d1edges", (d1edges))
      print("d2edges", len(d2edges))
      print("d2edges", (d2edges))

    Combine_Mode= Analysis_Config.Combine_Production_Mode

    treelist = []

    with open(treelistpath) as f:
      llist = [line.rstrip() for line in f]
        
    for line in llist:
      if os.path.exists(line): 
        treelist.append(line)

    yeardict = {}
    print(treelistpath,treelist)
    for numfile in range(0,len(treelist)):
      filename = treelist[numfile]
      print("reading in:" , filename)
      ind = filename.split("/").index(Analysis_Config.TreeFile) # ex 200205_CutBased set in Config #
      year = filename.split("/")[ind:][1]
      print(year)
      ## Allow for strings in the year##
      if "16APV" in year:
        year = "2016APV"
      elif "16" in year:
        year = "2016"
      elif "17" in year:
        year = "2017"
      elif "18" in year:
        year = "2018"
      if year not in yeardict.keys():
        yeardict[year] = {}
      # Set the Production Method #
      prod = filename.split("/")[ind:][2]
      # Easy fix for allowing Data Templates to Be Made#
      if production == "Data":
        prod = "Data"
        p_sorted = True
      else:
        prod, p_sorted = sort_category_templates(Analysis_Config,prod)
      print(prod)
      if prod not in yeardict[year] and p_sorted:
          yeardict[year][prod] = [[]]   #, [], []]
      try:
        yeardict[year][prod][0].append(filename)
      except:
        print("ERROR: Cannot recognize production mode of " + filename + "! Tree not sorted!")
    #print("yeardict: ",yeardict)

    hlist = []
    print(production,category,hlist,yeardict,inputyear,final_state)
    foutName = FillHistOnShell(production,category,hlist,yeardict,Analysis_Config,inputyear,final_state,Combine_Production_Mode = Combine_Mode,Do_Systematics = True) # Store the Histrograms before unrolling
    fout = ROOT.TFile(rolled_dir+foutName,"recreate")
    fout.cd()

    for hist in hlist: 
      print ("writing :",hist.GetName(),hist.Integral())
      hist.Write()
    fout.Close()

    fout = ROOT.TFile(unrolled_dir+foutName,"recreate")
    fout.cd()
    # Unroll and save the unrolled histograms #
     
    for hist in hlist:
      if type(hist) == type(ROOT.TH3F()):
        Temp_Neg, Temp_Pos = Unroll_3D_OnShell(hist)
        Temp_Neg.Write()
        Temp_Pos.Write()
      if type(hist) == type(ROOT.TH2F()):
        Temp_Neg, Temp_Pos = Unroll_2D_OnShell(hist)
        Temp_Neg.Write()
        Temp_Pos.Write()
      if type(hist) == type(ROOT.TH1F()):
        Temp_Neg, Temp_Pos = Unroll_1D_OnShell(hist)
        Temp_Neg.Write()
        Temp_Pos.Write()

if __name__ == "__main__":
    main(sys.argv[1:])