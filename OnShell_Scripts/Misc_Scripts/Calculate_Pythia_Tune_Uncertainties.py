import ROOT
import sys, os
import numpy as np
from AnalysisTools.Utils import Config
from AnalysisTools.TemplateMaker.Sort_Category import sort_category_systematics
from root_numpy import array2tree, tree2array
from AnalysisTools.Utils.Calc_Weight import Calc_Tree_Weight_2021_gammaH

# Need a path to all of the datafiles to use #

# Arguments should be a path to the directory with all templates #
outputdir = sys.argv[1]
Input_Trees = sys.argv[2]

# ======== Load up the analysis configuration ======= # 

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics_Photon_Rate")
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

# Here we need to sort all of the input trees by year and tune #

treelist = []

with open(Input_Trees) as f:
    llist = [line.rstrip() for line in f]
        
for line in llist:
  if os.path.exists(line): 
    treelist.append(line)

yeardict = {}
print(Input_Trees,treelist)
for numfile in range(0,len(treelist)):
  filename = treelist[numfile]
  print(filename)
  ind = filename.split("/").index(Analysis_Config.TreeFile) # ex 200205_CutBased set in Config #
  year = filename.split("/")[ind:][1]
  ## Allow for strings in the year##
  if "16" in year:
    year = "2016"
  elif "17" in year:
    year = "2017"
  elif "18" in year:
    year = "2018"
  if year not in yeardict.keys():
    yeardict[year] = {}
  # Set the Production Method #
  prod = filename.split("/")[ind:][2]
  #Before overwriting check the tunes on the samples#
  tune = None 
  if "tuneup" in prod:
    tune = "up"
  elif "tunedown" in prod:
    tune = "down"
  else:
    tune = "nominal"
  prod, p_sorted = sort_category_systematics(Analysis_Config,prod)
  if prod not in yeardict[year] and p_sorted:
      yeardict[year][prod] = {}  #, [], []]
  if tune not in yeardict[year][prod]:
    yeardict[year][prod][tune] = [] 
  try:
    yeardict[year][prod][tune].append(filename)
  except:
    print("ERROR: Cannot recognize production mode of " + filename + "! Tree not sorted!")
  #print("yeardict: ",yeardict)

#print(yeardict)

# Function for comparing yeilds when passed three root files #
def Compare_Categorization(Nominal_Event_Weight,Alternative_Event_Weight,Event_Category,Tag_List_Nominal,Tag_List_Alternative,Final_State,Final_State_List_Nominal,Final_State_List_Alternative):
  if Event_Category == "Untagged":
    Tag = 0
  elif Event_Category == "VBF1jTagged":
    Tag = 1
  elif Event_Category == "VBF2jTagged":
    Tag = 2
  elif Event_Category == "VHLeptTagged":
    Tag  = 3
  elif Event_Category == "VHHadrTagged":
    Tag  = 4
  elif Event_Category == "ttHLeptTagged":
    Tag  = 5
  elif Event_Category == "ttHHadrTagged":
    Tag  = 6
  elif Event_Category == "VHMETTagged":
    Tag  = 7
  elif Event_Category == "Boosted":
    Tag  = 8
  elif Event_Category == "gammaH":
    Tag  = 9
  else:
    raise ValueError ("Invalid Event Category! in Calc_Systematics!")
  
  if Final_State == "4e":
    Final_State_Check = 11**2 * 11**2
  elif Final_State == "4mu":
    Final_State_Check = 13**2 * 13**2
  elif Final_State == "2e2mu":
    Final_State_Check = 11**2 * 13**2
  else:
    raise ValueError ("Invalid Final State in Calc_Systematics")
  Sum_Nominal = 0
  Sum_Alternative = 0
  for i in range(len(Nominal_Event_Weight)):
    if Tag_List_Nominal[i] == Tag and Final_State_List_Nominal[i] == Final_State_Check:
      Sum_Nominal += Nominal_Event_Weight[i]
  for i in range(len(Alternative_Event_Weight)):
    if Tag_List_Alternative[i] == Tag and Final_State_List_Alternative[i] == Final_State_Check:
      Sum_Alternative += Alternative_Event_Weight[i]  
  
  print(Sum_Nominal,Sum_Alternative)
  if Sum_Nominal == 0:
    return 1
  Ratio = Sum_Alternative/Sum_Nominal
  return Ratio 

# Now compare the yields for each category of each sample #
tune_dictionary = dict()
tune_dictionary['2016'] = dict()
tune_dictionary['2017'] = dict()
tune_dictionary['2018'] = dict()
tune_dictionary['2016']['2e2mu'] = dict()
tune_dictionary['2016']['4mu'] = dict()
tune_dictionary['2016']['4e'] = dict()
tune_dictionary['2017']['2e2mu'] = dict()
tune_dictionary['2017']['4mu'] = dict()
tune_dictionary['2017']['4e'] = dict()
tune_dictionary['2018']['2e2mu'] = dict()
tune_dictionary['2018']['4mu'] = dict()
tune_dictionary['2018']['4e'] = dict()
Production_Modes = yeardict
for year in yeardict.keys():
  for prod_mode in yeardict[year].keys():
      print("Prod Mode: ",prod_mode)
      tree_path_nominal = yeardict[year][prod_mode]["nominal"][0]
      tree_path_tuneup = yeardict[year][prod_mode]["up"][0]
      tree_path_tunedown = yeardict[year][prod_mode]["down"][0]
      print("Tree Paths: ",tree_path_nominal,tree_path_tuneup,tree_path_tunedown)
      nominal = ROOT.TFile(tree_path_nominal,"read")
      tune_up = ROOT.TFile(tree_path_tuneup,"read")
      tune_down = ROOT.TFile(tree_path_tunedown,"read")
      root_tree_nominal = nominal.Get("eventTree")
      root_tree_tune_up = tune_up.Get("eventTree")
      root_tree_tune_down = tune_down.Get("eventTree")
      Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree_nominal,prod_mode+str(year),True,tree_path_nominal)
      TuneUp_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree_tune_up,prod_mode+str(year),True,tree_path_tuneup)
      TuneDown_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree_tune_down,prod_mode+str(year),True,tree_path_tunedown)
      Tag_Nominal = tree2array(tree=root_tree_nominal,branches="EventTag")
      Tag_TuneUp = tree2array(tree=root_tree_tune_up,branches="EventTag")
      Tag_TuneDown = tree2array(tree=root_tree_tune_down,branches="EventTag")
      Final_State_List_Nominal = tree2array(tree=root_tree_nominal, branches="Z1Flav * Z2Flav")
      Final_State_List_TuneUp = tree2array(tree=root_tree_tune_up, branches="Z1Flav * Z2Flav")
      Final_State_List_TuneDown = tree2array(tree=root_tree_tune_down, branches="Z1Flav * Z2Flav")
      for fs in Final_States:
        for category in Analysis_Config.Event_Categories:
          print("Category: ", category)
          SystUp = Compare_Categorization(Nominal_Event_Weight,TuneUp_Event_Weight,category,Tag_Nominal,Tag_TuneUp,fs,Final_State_List_Nominal,Final_State_List_TuneUp)
          SystDown = Compare_Categorization(Nominal_Event_Weight,TuneDown_Event_Weight,category,Tag_Nominal,Tag_TuneDown,fs,Final_State_List_Nominal,Final_State_List_TuneDown)
          if category not in tune_dictionary[year][fs].keys():
            tune_dictionary[str(year)][fs][category] = dict()
          tune_dictionary[year][fs][category][prod_mode]=str(SystUp)+"/"+str(SystDown)


file_systematics_dict = open(outputdir+"/pythia_tune_dict_"+Analysis_Config.name+".py", "w")
file_systematics_dict.write("Systematics_Dictionary = ")
file_systematics_dict.write(str(tune_dictionary))
file_systematics_dict.close()
print(tune_dictionary)
