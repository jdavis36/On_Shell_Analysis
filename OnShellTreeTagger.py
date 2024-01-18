#!/usr/bin/python3

import importlib.util

if importlib.util.find_spec("numpy") is None: 
    print("\nERROR: Please make sure that numpy is installed via 'pip3 install --user numpy' before running this tool.\n")
    exit()
if importlib.util.find_spec("tqdm") is None: 
    print("\nERROR: Please make sure that tqdm is installed via 'pip3 install --user tqdm' before running this tool.\n")
    exit()
#if importlib.util.find_spec("root_numpy") is None: 
#    print("\nERROR: Please make sure that root_numpy is installed via 'pip3 install --user root_numpy' before running this tool.\n")
#    exit()

import sys, getopt
import os
import glob
import ROOT
from math import sqrt
import time
from pathlib import Path
from tqdm import trange, tqdm
import numpy as np
from array import *
from collections import Counter
from decimal import *
import uproot
from functools import reduce
import itertools 
#from root_numpy import array2tree, tree2array
from AnalysisTools.data import gConstants as gConstants
from AnalysisTools.data import cConstants as cConstants
from AnalysisTools.Utils import Config as Config
from AnalysisTools.Utils import OnShell_Category as OnShell_Category
from AnalysisTools.Utils import Discriminants as Discriminants
from AnalysisTools.Utils import OnShell_Help as OnShell_Help
from AnalysisTools.Utils.Variable_Names_For_Tagging import * 

def main(argv):
    inputfile = ''
    outputdir = ''
    branchfile = ''
    retag = False 
    isData = False 
    configname = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:b:d:r:cf",["ifile=","ofile=","bfile=","dfile=","rfile=","config="])
    except getopt.GetoptError:
        print( ' batchTreeTagger.py -i <inputfile> -o <outputdir> -b <branchfile> -d <isData> -r <retag> --config <config name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('batchTreeTagger.py -i <inputfile> -o <outputdir> -b <branchfile> -d <isData> -r <retag> --config <config name>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputdir = arg
        elif opt in ("-b", "--bfile"):
            branchfile = arg
        elif opt in ("-d", "--dfile"):
            isData = arg
        elif opt in ("-r", "--rfile"):
            retag = arg
        elif opt in ("-cf", "--config"):
            configname = arg
            print("ConfigNAME ",configname)
    print([inputfile, outputdir, branchfile, isData, retag, configname])
    if not all([inputfile, outputdir, branchfile, isData, retag, configname]):
        print('batchTreeTagger.py -i <inputfile> -o <outputdir> -b <branchfile> -d <isData> -r <retag> --config <config name>')
        sys.exit(2)

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"
    if isData.upper()=="TRUE":
        isData = True
    elif isData.upper()=="FALSE":
        isData = False
    if retag.upper() == "TRUE":
      retag = True
    elif retag.upper() == "FALSE":
      retag = False
    print("\n================ Reading user input ================\n")

    print("Input CJLST TTree is '{}'".format(inputfile))
    print("Output directory is '{}'".format(outputdir))
    print("Branch list file is '{}'".format(branchfile))
    print("Treat as data: '{}'".format(isData))
    print("\n================ Processing user input ================\n")

    #=============== Load the Analysis Config =================
    cConstants_list = cConstants.init_cConstants()
    gConstants_list = gConstants.init_gConstants()
    Analysis_Config = Config.Analysis_Config(configname)


    #================ Set input file path and output file path ================
    
    filename = inputfile
    branchlistpath = branchfile
    tagtreepath = outputdir

    ind = filename.split("/").index(Analysis_Config.TreeFile)

    tagtreefile = "/".join(filename.split("/")[ind:])
    tagtreefilename = tagtreepath+tagtreefile

    print("Read '"+filename+"'\n")
    print("Write '"+tagtreefilename+"'\n")

    #================ Check existence of output and set up target branches ================

    print("================ Check output location and set up branches ================\n")

    if not Path(filename).exists():
        print("ERROR: \t'" + filename + "' does not exist!\n")
        exit()

    elif Path(tagtreefilename).exists() or glob.glob(tagtreefilename.replace(".root", "_subtree*.root")):
        print("ERROR: \t'" + tagtreefilename + "' or parts of it already exist!\n\tNote that part to all of the final eventTree can be reconstructed from its subtree files if necessary.\n")
        exit()

    else:
        print("Pre-existing output TTree not found --- safe to proceed")
        if not Path("/".join(tagtreefilename.split("/")[:-1])).exists():
            Path("/".join(tagtreefilename.split("/")[:-1])).mkdir(True, True)

        branchlist = []

        with open(branchlistpath) as f:
            blist = [line.rstrip() for line in f]

        if not retag:
          for branch in blist:
            if branch: branchlist.append(branch)

        #f = ROOT.TFile(filename, 'READ')
        with uproot.open(filename) as f:
          fc = ROOT.TFile(filename, 'READ')
          if Analysis_Config.Save_Failed:
            treenames = ["candTree", "candTree_failed"]
          else:
            treenames = ["candTree"]
          #================ Loop over target trees ================

          for tind, tree in enumerate(treenames):
              ftemptree = ROOT.TFile(tagtreefilename.replace(".root", "_subtree"+str(tind)+".root"), "CREATE")

              print("\n================ Reading events from '" + tree + "' and calculating new branches ================\n")
              if Analysis_Config.LHE_Study:
                t=f["eventTree"]
              else:
                if retag:
                  t = f["eventTree"]
                elif not isData and "AllData" in tagtreefilename:
                  #print("here")
                  t = f["CRZLLTree"][tree]
                else:
                  if not retag:
                    t = f["ZZTree"][tree]
                

              if Analysis_Config.LHE_Study:
                tc=fc.Get("eventTree")
              else:
                if retag:
                  tc = fc.Get("eventTree")
                elif not isData and "AllData" in tagtreefilename:
                  print("here")
                  tc = fc.Get("CRZLLTree/"+tree)
                else:
                  if not retag:
                    tc = fc.Get("ZZTree/"+tree)
                

              treebranches = [ x for x in t.keys() ]

              #print(treebranches)
              branchdict = {}
              signfixdict = {}
              # Save any Branch with p_ in the name. This allows for variable branch names in different samples #
              if retag: # retag adds every branch besides Tag to be cloned again
                for branch in treebranches:
                  if (branch not in branchlist) and (branch != "EventTag") and (branch != "Bin40"):
                    branchlist.append(branch)
              else:
                if Analysis_Config.Save_p == True:
                  for branch in treebranches: 
                    if ('p_' in branch) or branch.startswith('p'):
                      branchlist.append(branch)
              for branch in branchlist:
                  if "-" in branch and branch in treebranches:
                      signfixdict[branch.replace("-", "m")] = array('f',[0])
                      t.SetBranchAddress(branch, signfixdict[branch.replace("-", "m")])
                      branchdict[branch.replace("-", "m")] = [] 
                  elif branch not in treebranches:
                      branchdict[branch.replace("-", "m")] = [-999] * t.num_entries
              branchdict["EventTag"] = []
              branchdict["Bin40"] = []
              
              # Load the Disriminants to be saved as branches #
              if not retag:
                for name in Analysis_Config.Discriminants_To_Calculate:
                  branchdict[name] = []
              #for ent in trange(t.GetEntries()):
            
              Needed_Branches = []
              ## Load up all of the needed variables as arrays ##
              if Analysis_Config.TaggingProcess == "Tag_AC_19_Scheme_2": 
                for name in TagAC19():
                  Needed_Branches.append(name)  
              elif Analysis_Config.TaggingProcess == "Tag_Untagged_and_gammaH":
                for name in TagUntagged_Plus_GammaH():
                  Needed_Branches.append(name)
              elif Analysis_Config.TaggingProcess == "Tag_Untagged_and_qq_gammaH":
                for name in TagUntagged_Plus_qqGammaH():
                  Needed_Branches.append(name)
              #Load variables depending on discriminants
              if not retag:
                for name in Return_Needed_From_Discriminants_To_Calculate(Analysis_Config):
                  Needed_Branches.append(name)
                for name in Needed_For_All():
                  Needed_Branches.append(name)
                if not Analysis_Config.LHE_Study:
                  for name in Get_Scale_Values():
                    Needed_Branches.append(name)
                
              if retag:
                Needed_Branches.append("Bin40")
              
              if Analysis_Config.LHE_Study:
                for i in range(len(Needed_Branches)):
                  Needed_Branches[i] = Needed_Branches[i].replace("GG","Gen_GG")
              print("Loading Value Dictionary")
              Needed_Branches = reduce(lambda re, x: re+[x] if x not in re else re, Needed_Branches, [])
              #value_dict = t.arrays(Needed_Branches,library="np")
              Total_Events = t.num_entries
              Total_Run_Over = 0

              for value_dict in t.iterate(Needed_Branches,step_size=10000,library="np"):
                print("Processing",Total_Run_Over,"/",Total_Events," Precentage complete:",float(Total_Run_Over)/float(Total_Events) * 100)
                Total_Run_Over += 10000

                print("Checking for improper naming scheme:")
                bad_names = []
                replacement_names = []
                for name in value_dict.keys():
                  if "Gen_GG" in name:
                    new_name = name.replace("Gen_GG","GG")
                    bad_names.append(name)
                    replacement_names.append(new_name)    

                for bad_name,replacement_name in zip(bad_names,replacement_names):
                  value_dict[replacement_name] = value_dict.pop(bad_name)

                for ent in range(len(value_dict[list(value_dict.keys())[0]])):
                  #================ Loop over events ================#
                  
                  #================ Fill failed events with dummy and skip to loop over branches ================
                  if retag:
                    branchdict["Bin40"].append(value_dict["Bin40"][ent])
                  elif Analysis_Config.LHE_Study:
                    branchdict["Bin40"].append(0)
                  else:
                    branchdict["Bin40"].append(f["ZZTree/Counters"].values(False)[40])
                  if tree == "candTree_failed":
                      branchdict["EventTag"].append(-999)
                      for name in Analysis_Config.Discriminants_To_Calculate:
                        branchdict[name].append(-999)
                      for key in signfixdict.keys():
                          branchdict[key].append(signfixdict[key][0])
                      break
          
                  #================ Tagging event by category ================				
                  if Analysis_Config.TaggingProcess == "Tag_AC_19_Scheme_2":
                    Protect = OnShell_Category.Protect_Category_Against_NAN(value_dict["pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal"][ent],
                                value_dict["pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal"][ent],
                                value_dict["pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal"][ent],
                                value_dict["pConst_JJVBF_BKG_MCFM_JECNominal"][ent],
                                value_dict["pConst_HadZH_BKG_MCFM_JECNominal"][ent],
                                value_dict["pConst_HadWH_BKG_MCFM_JECNominal"][ent],
                                value_dict["pConst_JJQCD_BKG_MCFM_JECNominal"][ent],
                                value_dict["p_HadZH_mavjj_true_JECNominal"][ent],
                                value_dict["p_HadWH_mavjj_true_JECNominal"][ent],
                                value_dict["p_JVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],
                                value_dict["pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],
                                value_dict["p_HadWH_mavjj_JECNominal"][ent],
                                value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],
                                value_dict["p_HadZH_mavjj_JECNominal"][ent],
                                value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"])
                    if Protect:
                      branchdict["EventTag"].append(-999)
                    else:
                      tag = OnShell_Category.Tag_AC_19_Scheme_2( value_dict["nExtraLep"][ent],  
                                                  value_dict["nExtraZ"][ent],
                                                  value_dict["nCleanedJetsPt30"][ent],
                                                  value_dict["nCleanedJetsPt30BTagged_bTagSF"][ent],  
                                                  value_dict["JetQGLikelihood"][ent], 
                                                  value_dict["p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal"][ent],  
                                                  value_dict["p_JQCD_SIG_ghg2_1_JHUGen_JECNominal"][ent],
                                                  value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent], 
                                                  value_dict["p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal"][ent],
                                                  value_dict["p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal"][ent],
                                                  value_dict["p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal"][ent],
                                                  value_dict["p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal"][ent],
                                                  value_dict["p_JVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],
                                                  value_dict["pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],  
                                                  value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],  
                                                  value_dict["p_HadWH_SIG_ghw2_1_JHUGen_JECNominal"][ent],  
                                                  value_dict["p_HadWH_SIG_ghw4_1_JHUGen_JECNominal"][ent],  
                                                  value_dict["p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal"][ent],  
                                                  value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],
                                                  value_dict["p_HadZH_SIG_ghz2_1_JHUGen_JECNominal"][ent],   
                                                  value_dict["p_HadZH_SIG_ghz4_1_JHUGen_JECNominal"][ent],   
                                                  value_dict["p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal"][ent],   
                                                  value_dict["p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal"][ent],  
                                                  value_dict["p_HadWH_mavjj_JECNominal"][ent],  
                                                  value_dict["p_HadWH_mavjj_true_JECNominal"][ent],  
                                                  value_dict["p_HadZH_mavjj_JECNominal"][ent],
                                                  value_dict["p_HadZH_mavjj_true_JECNominal"][ent],  
                                                  value_dict["JetPhi"][ent],  
                                                  value_dict["ZZMass"][ent],  
                                                  value_dict["ZZPt"][ent],  
                                                  value_dict["PFMET"][ent],  
                                                  value_dict["PhotonIsCutBasedLooseID"][ent], 
                                                  value_dict["PhotonPt"][ent], 
                                                  Analysis_Config.useVHMETTagged,  
                                                  Analysis_Config.useQGTagging, 
                                                  cConstants_list, 
                                                  gConstants_list)
                  #================ Saving category tag ================
                      branchdict["EventTag"].append(tag)
                  elif Analysis_Config.TaggingProcess == "Tag_Untagged_and_gammaH":
                    tag = OnShell_Category.Tag_Untagged_and_gammaH(value_dict["PhotonPt"][ent],value_dict["PhotonIsCutBasedLooseID"][ent])
                    branchdict["EventTag"].append(tag)
                  elif Analysis_Config.TaggingProcess == "Tag_Untagged_and_qq_gammaH":
                    tag = OnShell_Category.Tag_Untagged_and_qq_gammaH(value_dict["PhotonPt"][ent],value_dict["PhotonIsCutBasedTightID"][ent])
                    branchdict["EventTag"].append(tag)
                  elif Analysis_Config.TaggingProcess == "Tag_All_Untagged":
                    tag = 0
                    branchdict["EventTag"].append(tag)                   
                  if retag:
                    Do_Retag = True
                  else: # Calculate Discriminants   
                    #============= Save pt_4l discriminants ==============
                    if "Pt4l" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["Pt4l"].append(value_dict["ZZPt"][ent])
                    #===== Calculating Useful Info for OnShell Discriminants ======
                    DoDiJet = False
                    notdijet = None
                    for name in Analysis_Config.Discriminants_To_Calculate:
                      if "VBF" in name or "VH" in name:
                        DoDiJet = True
                    if DoDiJet:
                      notdijet = OnShell_Help.notdijet(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent])
                    #================ Calculating AC discriminants ================
                    if "D_0minus_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_decay"].append(Discriminants.D_0minus_decay(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz4_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_CP_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_decay"].append(Discriminants.D_CP_decay_sub(value_dict["p_GG_SIG_ghg2_1_ghz1_1_ghz4_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz4_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_decay"].append(Discriminants.D_0hplus_decay(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz2_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_int_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_decay"].append(Discriminants.D_int_decay_sub(value_dict["p_GG_SIG_ghg2_1_ghz1_1_ghz2_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz2_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1_decay"].append(Discriminants.D_L1_decay(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1int_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1int_decay"].append(Discriminants.D_L1int_decay_sub(value_dict["p_GG_SIG_ghg2_1_ghz1_1_ghz1prime2_1E4_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zg_decay"].append(Discriminants.D_L1Zg_decay(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1Zgint_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zgint_decay"].append(Discriminants.D_L1Zgint_decay_sub(value_dict["p_GG_SIG_ghg2_1_ghz1_1_ghza1prime2_1E4_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1L1Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1L1Zg_decay"].append(Discriminants.D_L1L1Zg_decay(value_dict["p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1L1Zgint_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1L1Zgint_decay"].append(Discriminants.D_L1L1Zgint_decay_sub(value_dict["p_GG_SIG_ghg2_1_ghz1prime2_1E4_ghza1prime2_1E4_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0minus_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_Zg_decay"].append(Discriminants.D_0minus_Zg_decay(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghza4_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_CP_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_Zg_decay"].append(Discriminants.D_CP_Zg_decay_sub(value_dict["p_GG_SIG_ghg2_1_ghz1_1_ghza4_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghza4_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_Zg_decay"].append(Discriminants.D_0hplus_Zg_decay(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghza2_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_int_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_Zg_decay"].append(Discriminants.D_int_Zg_decay_sub(value_dict["p_GG_SIG_ghg2_1_ghz1_1_ghza2_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghza2_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0minus_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_gg_decay"].append(Discriminants.D_0minus_gg_decay(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_gha4_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_CP_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_gg_decay"].append(Discriminants.D_CP_gg_decay_sub(value_dict["p_GG_SIG_ghg2_1_ghz1_1_gha4_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_gha4_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_gg_decay"].append(Discriminants.D_0hplus_gg_decay(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_gha2_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_int_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_gg_decay"].append(Discriminants.D_int_gg_decay_sub(value_dict["p_GG_SIG_ghg2_1_ghz1_1_gha2_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_GG_SIG_ghg2_1_gha2_1_JHUGen"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    #=============== Calculating VBF Discriminants ================
                    if "D_0minus_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_VBF"].append(Discriminants.D_0minus_VBF(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_CP_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_VBF"].append(Discriminants.D_CP_VBF(value_dict["p_JJVBF_SIG_ghv1_1_ghv4_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_VBF"].append(Discriminants.D_0hplus_VBF(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_int_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_VBF"].append(Discriminants.D_int_VBF(value_dict["p_JJVBF_SIG_ghv1_1_ghv2_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1_VBF"].append(Discriminants.D_L1_VBF(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1int_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1int_VBF"].append(Discriminants.D_L1int_VBF(value_dict["p_JJVBF_SIG_ghv1_1_ghv1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zg_VBF"].append(Discriminants.D_L1Zg_VBF(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1Zgint_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zgint_VBF"].append(Discriminants.D_L1Zgint_VBF(value_dict["p_JJVBF_SIG_ghv1_1_ghza1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0minus_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_Zg_VBF"].append(Discriminants.D_0minus_Zg_VBF(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_CP_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_Zg_VBF"].append(Discriminants.D_CP_Zg_VBF(value_dict["p_JJVBF_SIG_ghv1_1_ghza4_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_Zg_VBF"].append(Discriminants.D_0hplus_Zg_VBF(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_int_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_Zg_VBF"].append(Discriminants.D_int_Zg_VBF(value_dict["p_JJVBF_SIG_ghv1_1_ghza2_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    #=============== Calculating VBF with Decay Discriminants ================
                    if "D_0minus_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_VBFdecay"].append(Discriminants.D_0minus_VBFdecay(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz4_1_JHUGen,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_VBFdecay"].append(Discriminants.D_0hplus_VBFdecay(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz2_1_JHUGen,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1_VBFdecay"].append(Discriminants.D_L1_VBFdecay(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1Zg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zg_VBFdecay"].append(Discriminants.D_L1Zg_VBFdecay(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0minus_Zg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_Zg_VBFdecay"].append(Discriminants.D_0minus_Zg_VBFdecay(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghza4_1_JHUGen,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_Zg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_Zg_VBFdecay"].append(Discriminants.D_0hplus_Zg_VBFdecay(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghza2_1_JHUGen,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0minus_gg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_gg_VBFdecay"].append(Discriminants.D_0minus_gg_VBFdecay(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_JJVBF_SIG_gha4_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_gha4_1_JHUGen,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_gg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_gg_VBFdecay"].append(Discriminants.D_0hplus_gg_VBFdecay(value_dict["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_JJVBF_SIG_gha2_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_gha2_1_JHUGen,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    #=========== Calculating VH Hadronic Discriminants ============
                    WH_scale = 0
                    ZH_scale = 0
                    if not Analysis_Config.LHE_Study:
                      WH_scale = OnShell_Help.HadWH_Scale_Nominal(value_dict["p_HadWH_mavjj_JECNominal"][ent],value_dict["p_HadWH_mavjj_true_JECNominal"][ent],value_dict["pConst_HadWH_SIG_ghw1_1_JHUGen_JECNominal"])
                      ZH_scale = OnShell_Help.HadZH_Scale_Nominal(value_dict["p_HadZH_mavjj_JECNominal"][ent],value_dict["p_HadZH_mavjj_true_JECNominal"][ent],value_dict["pConst_HadZH_SIG_ghz1_1_JHUGen_JECNominal"])
                    if "D_0minus_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_HadVH"].append(Discriminants.D_0minus_HadVH(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadWH_SIG_ghw4_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz4_1_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet,value_dict["ZZMass"][ent],gConstants_list))
                    if "D_CP_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_HadVH"].append(Discriminants.D_CP_HadVH(value_dict["p_HadZH_SIG_ghz1_1_ghz4_1_JHUGen_JECNominal"][ent],value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadWH_SIG_ghw4_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz4_1_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet))
                    if "D_0hplus_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_HadVH"].append(Discriminants.D_0hplus_HadVH(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadWH_SIG_ghw2_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_int_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_HadVH"].append(Discriminants.D_int_HadVH(value_dict["p_HadZH_SIG_ghz1_1_ghz2_1_JHUGen_JECNominal"][ent],value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadWH_SIG_ghw2_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadWH_SIG_ghw2_1_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet))
                    if "D_L1_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1_HadVH"].append(Discriminants.D_L1_HadVH(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet,value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1int_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1int_HadVH"].append(Discriminants.D_L1int_HadVH(value_dict["p_HadWH_SIG_ghw1_1_ghw1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet,value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zg_HadVH"].append(Discriminants.D_L1Zg_HadVH(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,0"][ent],value_dict["p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet,value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1Zgint_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zgint_HadVH"].append(Discriminants.D_L1Zgint_HadVH(value_dict["p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet,value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0minus_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_Zg_HadVH"].append(Discriminants.D_0minus_Zg_HadVH(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,0"][ent],value_dict["p_HadZH_SIG_ghza4_1_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet,value_dict["ZZMass"][ent],gConstants_list))
                    if "D_CP_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_Zg_HadVH"].append(Discriminants.D_CP_Zg_HadVH(value_dict["p_HadZH_SIG_ghz1_1_ghza4_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghza4_1_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet))
                    if "D_0hplus_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_Zg_HadVH"].append(Discriminants.D_0hplus_Zg_HadVH(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,0"][ent],value_dict["p_HadZH_SIG_ghza2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_int_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_Zg_HadVH"].append(Discriminants.D_int_Zg_HadVH(value_dict["p_HadZH_SIG_ghz1_1_ghza2_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghza2_1_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet,value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0minus_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_gg_HadVH"].append(Discriminants.D_0minus_gg_HadVH(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,0"][ent],value_dict["p_HadZH_SIG_gha4_1_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet,value_dict["ZZMass"][ent],gConstants_list))
                    if "D_CP_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_gg_HadVH"].append(Discriminants.D_CP_gg_HadVH(value_dict["p_HadZH_SIG_ghz1_1_gha4_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_gha4_1_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet))
                    if "D_0hplus_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_gg_HadVH"].append(Discriminants.D_0hplus_gg_HadVH(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,0"][ent],value_dict["p_HadZH_SIG_gha2_1_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet,value_dict["ZZMass"][ent],gConstants_list))
                    if "D_int_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_gg_HadVH"].append(Discriminants.D_int_gg_HadVH(value_dict["p_HadZH_SIG_ghz1_1_gha2_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_gha2_1_JHUGen_JECNominal"][ent],WH_scale,ZH_scale,notdijet,value_dict["ZZMass"][ent],gConstants_list))
                    #============== Calculating VH Decay Discriminants ============
                    if "D_0minus_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_HadVHdecay"].append(Discriminants.D_0minus_HadVHdecay(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_HadWH_SIG_ghw4_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz4_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz4_1_JHUGen,WH_scale,ZH_scale,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_HadVHdecay"].append(Discriminants.D_0hplus_HadVHdecay(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_HadWH_SIG_ghw2_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz2_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz2_1_JHUGen,WH_scale,ZH_scale,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1_HadVHdecay"].append(Discriminants.D_L1_HadVHdecay(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,WH_scale,ZH_scale,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_L1Zg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zg_HadVHdecay"].append(Discriminants.D_L1Zg_HadVHdecay(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,WH_scale,ZH_scale,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0minus_Zg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_Zg_HadVHdecay"].append(Discriminants.D_0minus_Zg_HadVHdecay(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_HadZH_SIG_ghza4_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghza4_1_JHUGen,WH_scale,ZH_scale,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_Zg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_Zg_HadVHdecay"].append(Discriminants.D_0hplus_Zg_HadVHdecay(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_HadZH_SIG_ghza2_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghza2_1_JHUGen,WH_scale,ZH_scale,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0minus_gg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_gg_HadVHdecay"].append(Discriminants.D_0minus_gg_HadVHdecay(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_HadZH_SIG_gha4_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_gha4_1_JHUGen,WH_scale,ZH_scale,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    if "D_0hplus_gg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_gg_HadVHdecay"].append(Discriminants.D_0hplus_gg_HadVHdecay(value_dict["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal"][ent],value_dict["p_HadZH_SIG_ghz1_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_HadZH_SIG_gha2_1_JHUGen_JECNominal"][ent],value_dict["p_GG_SIG_ghg2_1_gha2_1_JHUGen,WH_scale,ZH_scale,notdijet"][ent],value_dict["ZZMass"][ent],gConstants_list))
                    #================ Calculating BKG discriminants ===============
                    ZZFlav=value_dict["Z1Flav"][ent]*value_dict["Z2Flav"][ent]
                    if "D_bkg" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_bkg"].append(Discriminants.D_bkg(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_m4l_SIG"][ent],value_dict["p_QQB_BKG_MCFM"][ent],value_dict["p_m4l_BKG"][ent],cConstants_list,ZZFlav,value_dict["ZZMass"][ent]))
                    if "D_bkg_ResUp" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_bkg_ResUp"].append(Discriminants.D_bkg_ResUp(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_m4l_SIG_ResUp"][ent],value_dict["p_QQB_BKG_MCFM"][ent],value_dict["p_m4l_BKG_ResUp"][ent],cConstants_list,ZZFlav,value_dict["ZZMass"][ent]))
                    if "D_bkg_ResDown" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_bkg_ResDown"].append(Discriminants.D_bkg_ResDown(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_m4l_SIG_ResDown"][ent],value_dict["p_QQB_BKG_MCFM"][ent],value_dict["p_m4l_BKG_ResDown"][ent],cConstants_list,ZZFlav,value_dict["ZZMass"][ent]))
                    if "D_bkg_ScaleUp" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_bkg_ScaleUp"].append(Discriminants.D_bkg_ScaleUp(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_m4l_SIG_ScaleUp"][ent],value_dict["p_QQB_BKG_MCFM"][ent],value_dict["p_m4l_BKG_ScaleUp"][ent],cConstants_list,ZZFlav,value_dict["ZZMass"][ent]))
                    if "D_bkg_ScaleDown" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_bkg_ScaleDown"].append(Discriminants.D_bkg_ScaleDown(value_dict["p_GG_SIG_ghg2_1_ghz1_1_JHUGen"][ent],value_dict["p_m4l_SIG_ScaleDown"][ent],value_dict["p_QQB_BKG_MCFM"][ent],value_dict["p_m4l_BKG_ScaleUp"][ent],cConstants_list,ZZFlav,value_dict["ZZMass"][ent]))        
                    if "D_bkg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_bkg_VBFdecay"].append(Discriminants.D_bkg_VBFdecay(value_dict["p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal"][ent],value_dict["p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal"][ent],value_dict["p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal"][ent],value_dict["p_JJVBF_BKG_MCFM_JECNominal"][ent],value_dict["p_HadZH_BKG_MCFM_JECNominal"][ent],value_dict["p_HadWH_BKG_MCFM_JECNominal"][ent],value_dict["p_JJQCD_BKG_MCFM_JECNominal"][ent],value_dict["p_HadZH_mavjj_JECNominal"][ent],value_dict["p_HadZH_mavjj_true_JECNominal"][ent],value_dict["p_HadWH_mavjj_JECNominal"][ent],value_dict["p_HadWH_mavjj_true_JECNominal"][ent],value_dict["pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal"][ent],value_dict["pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal"][ent],value_dict["pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal"][ent],value_dict["pConst_JJVBF_BKG_MCFM_JECNominal"][ent],value_dict["pConst_HadZH_BKG_MCFM_JECNominal"][ent],value_dict["pConst_HadWH_BKG_MCFM_JECNominal"][ent],value_dict["pConst_JJQCD_BKG_MCFM_JECNominal,cConstants_list,ZZFlav"][ent],value_dict["ZZMass"][ent],value_dict["p_m4l_BKG"][ent],value_dict["p_m4l_SIG"][ent],notdijet))
                    if "D_bkg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_bkg_HadVHdecay"].append(Discriminants.D_bkg_HadVHdecay(value_dict["p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal"][ent],value_dict["p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal"][ent],value_dict["p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal"][ent],value_dict["p_JJVBF_BKG_MCFM_JECNominal"][ent],value_dict["p_HadZH_BKG_MCFM_JECNominal"][ent],value_dict["p_HadWH_BKG_MCFM_JECNominal"][ent],value_dict["p_JJQCD_BKG_MCFM_JECNominal"][ent],value_dict["p_HadZH_mavjj_JECNominal"][ent],value_dict["p_HadZH_mavjj_true_JECNominal"][ent],value_dict["p_HadWH_mavjj_JECNominal"][ent],value_dict["p_HadWH_mavjj_true_JECNominal"][ent],value_dict["pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal"][ent],value_dict["pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal"][ent],value_dict["pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal"][ent],value_dict["pConst_JJVBF_BKG_MCFM_JECNominal"][ent],value_dict["pConst_HadZH_BKG_MCFM_JECNominal"][ent],value_dict["pConst_HadWH_BKG_MCFM_JECNominal"][ent],value_dict["pConst_JJQCD_BKG_MCFM_JECNominal,cConstants_list,ZZFlav"][ent],value_dict["ZZMass"][ent],value_dict["p_m4l_BKG"][ent],value_dict["p_m4l_SIG"][ent],notdijet))

                    #================ Calculating EW discriminants ================
                    
                    #================ Calculating gg discriminants ================

                    #================ Saving calculated discriminants ================

                    #================ Saving signed branches ================

                    for key in signfixdict.keys():
                        branchdict[key].append(signfixdict[key][0])
                    #break

              print("\n================ Selecting and cloning branches from '"+tree+"' ================\n")

              for i in trange(len(treebranches)):
                  branch = treebranches[i]
                  if branch not in branchlist or "-" in branch:
                      tc.SetBranchStatus(branch, 0)

              exec("new{} = tc.CloneTree()".format(tree))
              #print(branchdict.keys())
              #print(branchdict)

              # Save the tree without the extra branches #
              print("\n================ Saving processed '"+tree+"' without newly calculated branches ================\n")

              exec("new{}.SetName('eventTree')".format(tree))
              exec("new{}.Write()".format(tree))
              ftemptree.Close()
              #for key in branchdict.keys():
              #    exec("array2tree(np.array(branchdict['{}'], dtype=[('{}', float)]), tree=new{})".format(key, key, tree))

              #print("\n================ Saving processed '"+tree+"' ================\n")

              #exec("new{}.SetName('eventTree')".format(tree))
              #exec("new{}.Write()".format(tree))

              #ftemptree.Close()

              print("Modified '{}' written to '{}'".format(tree, tagtreefilename.replace(".root", "_subtree"+str(tind)+".root")))
              print("\n================ Adding newly calculated branches to '"+tree+"'  ================\n")
              
              ftempfilename_new_branches = tagtreefilename.replace(".root", "_subtree"+str(tind)+"new.root")
              ftempfilename_all_branches = tagtreefilename.replace(".root", "_subtree"+str(tind)+"all.root")
              #print(len(branchdict["D_bkg"]))
              type_dict={}
              for key in branchdict.keys():
                type_dict[key] = np.asarray(branchdict[key]).dtype.type
                branchdict[key] = np.asarray(branchdict[key])
              
              with uproot.recreate(ftempfilename_new_branches) as new_branches:
                new_branches["eventTree"] = branchdict
              saved_old_tree = uproot.open(tagtreefilename.replace(".root", "_subtree"+str(tind)+".root:eventTree"))
              saved_new_tree = uproot.open(tagtreefilename.replace(".root", "_subtree"+str(tind)+"new.root:eventTree"))

              #saved_old_tree_as_np_arrays = saved_old_tree.arrays(saved_old_tree.keys(),library="np")
              #new_dict = saved_old_tree_as_np_arrays | branchdict

              all_keys = saved_old_tree.keys()
              all_keys.extend(list(branchdict.keys()))
              #print(all_keys)

              all_keys_for_new_branches = {}
              
              Total_Merged = 0
              with uproot.recreate(ftempfilename_all_branches) as combined_tree:
                first = True
                for batch1, batch2 in zip(saved_old_tree.iterate(step_size=10000, library="np"),saved_new_tree.iterate(step_size=10000, library="np")):
                  print("Processing",Total_Merged,"/",Total_Events," Precentage complete:",float(Total_Merged)/float(Total_Events) * 100)
                  Total_Merged += 10000
                  merged_dictionary = batch1 | batch2
                  if first:
                    combined_tree["eventTree"] = merged_dictionary
                    first = False
                  else:
                    combined_tree["eventTree"].extend(merged_dictionary)
                #for batch in saved_old_tree.iterate(step_size=1000, library="np"):
                #  combined_tree["eventTree"].extend(batch)
                #for batch in saved_new_tree.iterate(step_size=1000, library="np"):
                #  combined_tree["eventTree"].extend(batch)
              #with uproot.recreate(ftempfilename_all_branches) as combined_tree:
              #  combined_tree["eventTree"] = new_dict
                
              print("Modified '{}' written to '{}'".format(tree, tagtreefilename.replace(".root", "_subtree"+str(tind)+"all.root")))
              
              print("\n Moving '{}' written to '{}'".format(tree, tagtreefilename.replace(".root", "_subtree"+str(tind)+".root")))

              os.system("mv {} {}".format(tagtreefilename.replace(".root", "_subtree"+str(tind)+"all.root"),tagtreefilename.replace(".root", "_subtree"+str(tind)+".root")))
              os.system("rm {}".format(tagtreefilename.replace(".root", "_subtree"+str(tind)+"new.root")))

          print("\n================ Building and saving final merged eventTree ================\n")

          chain = ROOT.TChain("eventTree")
          for i in range(len(treenames)):
              chain.Add(tagtreefilename.replace(".root", "_subtree"+str(i)+".root"))

          chain.Merge(tagtreefilename)
          
          print("Merged eventTree written to '{}'\n".format(tagtreefilename))
          #if Analysis_Config.LHE_Study:
          #  f = ROOT.TFile(tagtreefilename,"Recreate")
          #  f.Print()
          #  AddAliasTree= f.Get("eventTree")
          #  AddAliasTree.SetAlias("ZZMass","M4L")
          #  AddAliasTree.Close

          for i in range(len(treenames)):
              if os.path.exists(tagtreefilename.replace(".root", "_subtree"+str(i)+".root")):
                  os.remove(tagtreefilename.replace(".root", "_subtree"+str(i)+".root"))

          f = ROOT.TFile(tagtreefilename, 'Update')
          t = f.Get("eventTree")
          if Analysis_Config.LHE_Study:
            t.SetAlias("ZZMass","M4L")
            t.SetAlias("Z1Flav","flavdau1*flavdau2")
            t.SetAlias("Z2Flav","flavdau3*flavdau4")
            t.Write()
          f.Close()
          print("")

if __name__ == "__main__":
    main(sys.argv[1:])
