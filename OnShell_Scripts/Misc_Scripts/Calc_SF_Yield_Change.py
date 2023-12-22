import ROOT
import sys, os
import numpy as np
from AnalysisTools.Utils import Config
from AnalysisTools.TemplateMaker.Sort_Category import sort_category_systematics
from root_numpy import array2tree, tree2array
from AnalysisTools.Utils.Calc_Weight import Calc_Tree_Weight_2021_gammaH
from AnalysisTools.Utils.OnShell_Category import Tag_Untagged_and_gammaH
from AnalysisTools.data.Photon_Scale_Factor import *
from AnalysisTools.Utils.Helpers import Convert_Final_State_String_To_ZZ_Flav
# Need a path to all of the datafiles to use #

# Arguments should be a path to the directory with all templates #
outputdir = sys.argv[1]
Input_Trees = sys.argv[2:]

# ======== Load up the analysis configuration ======= # 

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics_Photon_Rate")
Production_Modes = Analysis_Config.Production_Modes
Event_Categories = Analysis_Config.Event_Categories
Final_States = Analysis_Config.Final_States
Years = Analysis_Config.Years
# For condor submission setup a few directories etc #
CMSSW_PATH = Analysis_Config.CMSSW_PATH 
Work_Dir = Analysis_Config.Work_Dir

if not outputdir.endswith("/"):
  outputdir = outputdir+"/"

if not os.path.exists(outputdir):
  os.mkdir(outputdir)

def PtEtaPhiMFourVec(Pt,Eta,Phi,Mass):
    TVec = ROOT.Math.PtEtaPhiMVector(Pt,Eta,Phi,Mass)
    return TVec

def separate_by_year(Input_File):
  Files_By_Year = {"2016":[],"2016APV":[],"2017":[],"2018":[],"Run2":[]}
  with open(Input_File) as f:
    for line in f:
      if "16" in line:
        Files_By_Year["2016"].append(line)
        Files_By_Year["Run2"].append(line)
      if "16APV" in line:
        Files_By_Year["2016APV"].append(line)
        Files_By_Year["Run2"].append(line)
      if "17" in line:
        Files_By_Year["2017"].append(line)
        Files_By_Year["Run2"].append(line)
      if "18" in line:
        Files_By_Year["2018"].append(line)
        Files_By_Year["Run2"].append(line)
  return Files_By_Year

def Calculate_New_Yield_SF(tree,year,final_state,Final_State_List,Photon_SF,PhotonPt,PhotonEta,EventTag):
  # Return the fractional change in the gammaH tagged category and the corresponding new yield in Untagged Category
  gammaHTagged  = 9
  #This will not work for 2 < category analysis 
  Scale_Factors = []
  Scale_Factors_Up = []
  Scale_Factors_Down = []

  Nominal_Yields = []

  final_state_num = Convert_Final_State_String_To_ZZ_Flav(final_state)
  print(final_state)
  for i in range(len(EventTag)):
    if EventTag[i] == gammaHTagged and Final_State_List[i] == final_state_num:
      # Calculate the Scale Factor to apply to each event weight for all photons that pass the selection
      Scale_Factors.append(return_Photon_SF(Photon_SF,year,PhotonPt[i][0],PhotonEta[i][0])) # Take only leading photon PT
      Scale_Factors_Up.append(return_Photon_SF_Up(Photon_SF,year,PhotonPt[i][0],PhotonEta[i][0]))
      Scale_Factors_Down.append(return_Photon_SF_Down(Photon_SF,year,PhotonPt[i][0],PhotonEta[i][0]))
      Nominal_Yields.append(Nominal_Event_Weight[i])

  # If there are no event following this criteria scale the yield by 0 #
  if sum(Nominal_Yields) == 0:
    return 1, 1, 1

  Scaled_Yields = []
  Scaled_Yields_ErrUp = []
  Scaled_Yields_ErrDown = []

  for i in range(len(Nominal_Yields)):
    Scaled_Yields.append(Nominal_Yields[i]*Scale_Factors[i])
    Scaled_Yields_ErrUp.append(Nominal_Yields[i]*Scale_Factors_Up[i])
    Scaled_Yields_ErrDown.append(Nominal_Yields[i]*Scale_Factors_Down[i])

  Scaled_Weights = sum(Scaled_Yields)/sum(Nominal_Yields)
  Scaled_Weights_ErrUp = sum(Scaled_Yields_ErrUp)/(Scaled_Weights*sum(Nominal_Yields))
  Scaled_Weights_ErrDown = sum(Scaled_Yields_ErrDown)/(Scaled_Weights*sum(Nominal_Yields))

  Change_In_Yield_gammaH_Tagged = sum(Scaled_Yields)/sum(Nominal_Yields)
  Change_In_Yield_gammaH_Tagged_ErrUp = sum(Scaled_Yields_ErrUp)/sum(Scaled_Yields)
  Change_In_Yield_gammaH_Tagged_ErrDown = sum(Scaled_Yields_ErrDown)/sum(Scaled_Yields)

  return Change_In_Yield_gammaH_Tagged,Change_In_Yield_gammaH_Tagged_ErrUp,Change_In_Yield_gammaH_Tagged_ErrDown

def Calculate_New_Yield_SF_Combined(tree_paths,year,final_state,Photon_SF):
  # Return the fractional change in the gammaH tagged category and the corresponding new yield in Untagged Category
  gammaHTagged  = 9

  Nominal_Yields_Comb = []
  Nominal_Event_Weight_Comb = []
  Final_State_List_Comb = []
  Photon_Pt_Comb = []
  Photon_Eta_Comb = []
  Event_Tag_Comb = []

  final_state_num = Convert_Final_State_String_To_ZZ_Flav(final_state)

  for tree in tree_paths:
    f1= ROOT.TFile(tree,"read")
    root_tree = f1.Get("eventTree")
    Event_Tag_Comb.extend(tree2array(tree=root_tree,branches="EventTag"))
    Nominal_Event_Weight_Comb.extend(Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree))
    Photon_Pt_Comb.extend(tree2array(tree=root_tree,branches="PhotonPt"))
    Photon_Eta_Comb.extend(tree2array(tree=root_tree,branches="PhotonEta"))
    Final_State_List_Comb.extend(tree2array(tree=root_tree, branches="Z1Flav * Z2Flav"))

  #This will not work for 2 < category analysis 
  Scale_Factors_Comb = []
  Scale_Factors_Up_Comb = []
  Scale_Factors_Down_Comb = []
  for i in range(len(Event_Tag_Comb)):
    if Event_Tag_Comb[i] == gammaHTagged and Final_State_List_Comb[i] == final_state_num:
      # Calculate the Scale Factor to apply to each event weight for all photons that pass the selection
      Scale_Factors_Comb.append(return_Photon_SF(Photon_SF,year,Photon_Pt_Comb[i][0],Photon_Eta_Comb[i][0])) # Take only leading photon PT
      Scale_Factors_Up_Comb.append(return_Photon_SF_Up(Photon_SF,year,Photon_Pt_Comb[i][0],Photon_Eta_Comb[i][0]))
      Scale_Factors_Down_Comb.append(return_Photon_SF_Down(Photon_SF,year,Photon_Pt_Comb[i][0],Photon_Eta_Comb[i][0]))
      Nominal_Yields_Comb.append(Nominal_Event_Weight_Comb[i])

  # If there are no event following this criteria scale the yield by 0 #
  if sum(Nominal_Yields_Comb) == 0:
    return 1, 1, 1

  Scaled_Yields_Comb = []
  Scaled_Yields_ErrUp_Comb = []
  Scaled_Yields_ErrDown_Comb = []

  for i in range(len(Nominal_Yields_Comb)):
    Scaled_Yields_Comb.append(Nominal_Yields_Comb[i]*Scale_Factors_Comb[i])
    Scaled_Yields_ErrUp_Comb.append(Nominal_Yields_Comb[i]*Scale_Factors_Up_Comb[i])
    Scaled_Yields_ErrDown_Comb.append(Nominal_Yields_Comb[i]*Scale_Factors_Down_Comb[i])

  #Scaled_Weights_Comb = sum(Scaled_Yields_Comb)/sum(Nominal_Yields_Comb)
  #Scaled_Weights_ErrUp_Comb = sum(Scaled_Yields_ErrUp_Comb)/(Scaled_Weights_Comb*sum(Nominal_Yields_Comb))
  #Scaled_Weights_ErrDown_Comb = sum(Scaled_Yields_ErrDown_Comb)/(Scaled_Weights_Comb*sum(Nominal_Yields_Comb))

  Change_In_Yield_gammaH_Tagged = (sum(Scaled_Yields_Comb))/sum(Nominal_Yields_Comb)
  Change_In_Yield_gammaH_Tagged_ErrUp = (sum(Scaled_Yields_ErrUp_Comb))/sum(Scaled_Yields_Comb)
  Change_In_Yield_gammaH_Tagged_ErrDown = (sum(Scaled_Yields_ErrDown_Comb))/sum(Scaled_Yields_Comb)

  return Change_In_Yield_gammaH_Tagged,Change_In_Yield_gammaH_Tagged_ErrUp,Change_In_Yield_gammaH_Tagged_ErrDown

syst_dict=dict()
syst_dict['2016'] = dict()
syst_dict['2016APV'] = dict()
syst_dict['2017'] = dict()
syst_dict['2018'] = dict()
syst_dict['2016']['2e2mu'] = dict()
syst_dict['2016']['4mu'] = dict()
syst_dict['2016']['4e'] = dict()
syst_dict['2016APV']['2e2mu'] = dict()
syst_dict['2016APV']['4mu'] = dict()
syst_dict['2016APV']['4e'] = dict()
syst_dict['2017']['2e2mu'] = dict() 
syst_dict['2017']['4mu'] = dict() 
syst_dict['2017']['4e'] = dict()
syst_dict['2018']['2e2mu'] = dict()
syst_dict['2018']['4mu'] = dict()
syst_dict['2018']['4e'] = dict()

treelist = []
for fin in Input_Trees:

  with open(fin) as f:
    llist = [line.rstrip() for line in f]
        
  for line in llist:
    if os.path.exists(line): 
      treelist.append(line)

yeardict = {}
for numfile in range(0,len(treelist)):
  filename = treelist[numfile]
  ind = filename.split("/").index(Analysis_Config.TreeFile) # ex 200205_CutBased set in Config #
  year = filename.split("/")[ind:][1]
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
  prod, p_sorted = sort_category_systematics(Analysis_Config,prod)
  if prod not in yeardict[year] and p_sorted:
      yeardict[year][prod] = [[]]   #, [], []]
  try:
    yeardict[year][prod][0].append(filename)
  except:
    print("ERROR: Cannot recognize production mode of " + filename + "! Tree not sorted!")
  print("yeardict: ",yeardict)

Scale_Factor_Root_File = init_PhotonSF()
for year in Years:
  for final_state in Final_States:
    if year in yeardict.keys():
      for prod_mode in yeardict[year].keys():
        tree_paths = yeardict[year][prod_mode][0]
        if len(tree_paths) == 1:
          f1= ROOT.TFile(tree_paths[0],"read")
          root_tree = f1.Get("eventTree")
          EventTag = tree2array(tree=root_tree,branches="EventTag")
          Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_paths[0])
          PhotonPt = tree2array(tree=root_tree,branches="PhotonPt")
          PhotonEta = tree2array(tree=root_tree,branches="PhotonEta")
          Final_State_List = tree2array(tree=root_tree, branches="Z1Flav * Z2Flav")
          print("Prod Mode: ",prod_mode)
          New_Yield,Yield_Up,Yield_Down = Calculate_New_Yield_SF(root_tree,year,final_state,Final_State_List,Scale_Factor_Root_File,PhotonPt,PhotonEta,EventTag)
          print("New_Yield: ",New_Yield,"New_Yield_Up: ",Yield_Up,"Yield_Down: ",Yield_Down)
          if prod_mode not in syst_dict[str(year)][final_state].keys():
            syst_dict[str(year)][final_state][prod_mode] = dict()
          syst_dict[str(year)][final_state][prod_mode]["NewYield"]=New_Yield
          syst_dict[str(year)][final_state][prod_mode]["Yield_Uncertainty_Up"]=Yield_Up
          syst_dict[str(year)][final_state][prod_mode]["Yield_Uncertainty_Down"]=Yield_Down
        elif len(tree_paths) > 1:
          New_Yield,Yield_Up,Yield_Down = Calculate_New_Yield_SF_Combined(tree_paths,year,final_state,Scale_Factor_Root_File)
          if prod_mode not in syst_dict[str(year)][final_state].keys():
            syst_dict[str(year)][final_state][prod_mode] = dict()
          syst_dict[str(year)][final_state][prod_mode]["NewYield"]=New_Yield
          syst_dict[str(year)][final_state][prod_mode]["Yield_Uncertainty_Up"]=Yield_Up
          syst_dict[str(year)][final_state][prod_mode]["Yield_Uncertainty_Down"]=Yield_Down
        else:
          raise ValueError("No tree in tree paths")

print(syst_dict)
file_systematics_dict = open(outputdir+"/systematics_dict_"+Analysis_Config.name+".py", "w")
file_systematics_dict.write("Systematics_Dictionary = ")
file_systematics_dict.write(str(syst_dict))
file_systematics_dict.close()
