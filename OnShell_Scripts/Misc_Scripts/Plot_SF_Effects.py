import ROOT
import numpy as np
from AnalysisTools.TemplateMaker.Sort_Category import sort_category_systematics
from AnalysisTools.Utils.OnShell_Category import Tag_Untagged_and_gammaH
from AnalysisTools.Utils.Calc_Weight import Calc_Tree_Weight_2021_gammaH
from root_numpy import array2tree, tree2array
import sys
import os
from AnalysisTools.Utils import Config as Config
from AnalysisTools.data.Photon_Scale_Factor import *


Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics_Photon_Rate")
Years = Analysis_Config.Years
Input_Trees = sys.argv[1:]

treelist = []
for fin in Input_Trees:

  with open(fin) as f:
    llist = [line.rstrip() for line in f]
        
  for line in llist:
    if os.path.exists(line): 
      treelist.append(line)

print(treelist)
yeardict = {}
for numfile in range(0,len(treelist)):
  filename = treelist[numfile]
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
  prod, p_sorted = sort_category_systematics(Analysis_Config,prod)
  if prod not in yeardict[year] and p_sorted:
      yeardict[year][prod] = [[]]   #, [], []]
  try:
    yeardict[year][prod][0].append(filename)
  except:
    print("ERROR: Cannot recognize production mode of " + filename + "! Tree not sorted!")
  print("yeardict: ",yeardict)


def Calculate_New_Yield_SF(year,Photon_SF,PhotonPt,PhotonEta,EventTag,Nominal_Event_Weight):
  # Now will return the new weight vectors before and after the new yields are applied
  gammaHTagged  = 9
  #This will not work for 2 < category analysis 
  Scale_Factors = []
  Scale_Factors_Up = []
  Scale_Factors_Down = []
  Nominal_Yields = []
  Photon_Pt = []

  for i in range(len(EventTag)):
      # Calculate the Scale Factor to apply to each event weight for all photons that pass the selection
      if len(Photon_Pt_Comb[i]) != 0:
        Scale_Factors.append(return_Photon_SF(Photon_SF,year,PhotonPt[i][0],PhotonEta[i][0])) # Take only leading photon PT
        Scale_Factors_Up.append(return_Photon_SF_Up(Photon_SF,year,PhotonPt[i][0],PhotonEta[i][0]))
        Scale_Factors_Down.append(return_Photon_SF_Down(Photon_SF,year,PhotonPt[i][0],PhotonEta[i][0]))
        Nominal_Yields.append(Nominal_Event_Weight[i])
        Photon_Pt.append(Photon_Pt_Comb[i][0])

  Scaled_Yields = []
  Scaled_Yields_ErrUp = []
  Scaled_Yields_ErrDown = []

  for i in range(len(Nominal_Yields)):
    Scaled_Yields.append(Nominal_Yields[i]*Scale_Factors[i])
    Scaled_Yields_ErrUp.append(Nominal_Yields[i]*Scale_Factors_Up[i])
    Scaled_Yields_ErrDown.append(Nominal_Yields[i]*Scale_Factors_Down[i])

  return Photon_Pt,Scaled_Yields,Scaled_Yields_ErrUp,Scaled_Yields_ErrDown

Event_Tag_Comb = []
Nominal_Event_Weight_Comb = []
Photon_Pt_Comb =[]
Photon_Eta_Comb = []
Final_State_List_Comb = []
Scale_Factor_Root_File = init_PhotonSF()

for year in Years:
  if year in yeardict.keys():
    for prod_mode in yeardict[year]:
        tree_paths = yeardict[year][prod_mode][0]
        for tree in tree_paths:
            f1= ROOT.TFile(tree,"read")
            root_tree = f1.Get("eventTree")
            Nominal_Event_Weight_Comb.extend(Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree))
            Event_Tag_Comb.extend(tree2array(tree=root_tree,branches="EventTag"))
            Photon_Pt_Comb.extend(tree2array(tree=root_tree,branches="PhotonPt"))
            Photon_Eta_Comb.extend(tree2array(tree=root_tree,branches="PhotonEta"))
            Final_State_List_Comb = (tree2array(tree=root_tree, branches="Z1Flav * Z2Flav"))
            Photon_Pt,New_Yield,Yield_Up,Yield_Down = Calculate_New_Yield_SF(year,Scale_Factor_Root_File,Photon_Pt_Comb,Photon_Eta_Comb,Event_Tag_Comb,Nominal_Event_Weight_Comb)

    c1=ROOT.TCanvas('c1','test',200,10,600,600)
    hist_Nominal_Pt = ROOT.TH1F("hist_Nominal_Pt","hist_Nominal_Pt ",20,0,1000)
    hist_Scale_Up_Pt =ROOT.TH1F("hist_Scale_Up_Pt","hist_Scale_Up_Pt",20,0,1000)
    hist_Scale_Down_Pt= ROOT.TH1F("hist_Scale_Down_Pt","hist_Scale_Down_Pt",20,0,1000)

    for i in range(len(Photon_Pt)):
        hist_Nominal_Pt.Fill(Photon_Pt[i],New_Yield[i])
    for i in range(len(Photon_Pt)):
        hist_Scale_Up_Pt.Fill(Photon_Pt[i],Yield_Up[i])
    for i in range(len(Photon_Pt)):
        hist_Scale_Down_Pt.Fill(Photon_Pt[i],Yield_Down[i])

    ROOT.gStyle.SetOptStat(0000000000)
    hist_Nominal_Pt.GetXaxis().SetTitle("Photon p_{T} [GeV]")
    hist_Nominal_Pt.SetTitle("Nominal Scale Factor vs. Scale Factor Up SM signal + Bkg")
    Scale_Up_Ratio = ROOT.TRatioPlot(hist_Nominal_Pt,hist_Scale_Up_Pt)
    Scale_Up_Ratio.Draw()
    c1.Draw()
    c1.SaveAs("RatioPlots/Scale_Factor_Pt_Dist_Up_All"+year+".pdf")
    hist_Nominal_Pt.SetTitle("Nominal Scale Factor vs. Scale Factor Down SM signal + Bkg")
    hist_Nominal_Pt.GetXaxis().SetTitle("Photon p_{T} [GeV]")
    Scale_Down_Ratio = ROOT.TRatioPlot(hist_Nominal_Pt,hist_Scale_Down_Pt)
    Scale_Down_Ratio.Draw()
    c1.Draw()

    c1.SaveAs("RatioPlots/Scale_Factor_Pt_Dist_Down_All_"+year+".pdf")
