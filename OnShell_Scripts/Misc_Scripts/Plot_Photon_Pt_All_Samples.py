import ROOT
import numpy as np 
import sys
import os
from AnalysisTools.Utils.Calc_Weight import *
from AnalysisTools.Utils import Config as Config
from AnalysisTools.Utils import tdr_new
from AnalysisTools.Utils import CMS_lumi
from AnalysisTools.TemplateMaker.Sort_Category import sort_category_templates
from root_numpy import array2tree, tree2array
from scipy.stats import poisson 
from AnalysisTools.Utils import tdr_new
from AnalysisTools.Utils import CMS_lumi
import array 
## Steps to optimize the gammaH cut against SM##
# We need to loop over all of the samples that could be background #
# This includes all SM signal samples and all bkg samples

# Should make a histogram of photon Pt and determine the optimal cut #


ROOT.gROOT.SetBatch(True)
tdr_new.setTDRStyle()

Signal_Trees = sys.argv[1] 
ew_bkg = sys.argv[2]
qq4l_bkg = sys.argv[3]
gg4l_bkg = sys.argv[4]
ZX_bkg = sys.argv[5]
gammaH_tree = sys.argv[6]

# Uncomment for larger pt range #
"""
Pt_Photon_Signals= ROOT.TH1F("Photon Pt","Photon Pt",100,150,800)
Pt_Photon_ew = ROOT.TH1F("Photon Pt","Photon Pt",100,150,800)
Pt_Photon_qq4l = ROOT.TH1F("Photon Pt","Photon Pt",100,150,800)
Pt_Photon_gg4l = ROOT.TH1F("Photon Pt","Photon Pt",100,150,800)
Pt_Photon_ZX = ROOT.TH1F("Photon Pt","Photon Pt",100,150,800)
Pt_Photon_gammaH = ROOT.TH1F("Photon Pt","Photon Pt",100,150,800)
"""

Pt_Photon_Signals= ROOT.TH1F("Photon Pt","Photon Pt",50,0,200)
Pt_Photon_ew = ROOT.TH1F("Photon Pt","Photon Pt",50,0,200)
Pt_Photon_qq4l = ROOT.TH1F("Photon Pt","Photon Pt",50,0,200)
Pt_Photon_gg4l = ROOT.TH1F("Photon Pt","Photon Pt",50,0,200)
Pt_Photon_ZX = ROOT.TH1F("Photon Pt","Photon Pt",50,0,200)
Pt_Photon_gammaH = ROOT.TH1F("Photon Pt","Photon Pt",50,0,200)

#Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics")
Analysis_Config = Config.Analysis_Config("Tree_Level_qqH_Photons_XS")

# Add the signal to the Pt_Histogram #
with open(Signal_Trees) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    print("PROD",prod)
    name = sort_category_templates(Analysis_Config,prod)[0]
    if "2016APV" in line or "16APV" in line:
        name = name +"_2016"
        lumi = 15.9
    if "2016" in line or "16" in line:
        name = name +"_2016"
        lumi = 20.
    elif "2017" in line or "17" in line:
        name = name +"_2017"
        lumi = 41.5
    elif "2018" in line or "18" in line:
        name = name +"_2018"
        lumi = 59.7
    rf = ROOT.TFile(str(sample),'READ')
    t = rf.Get("eventTree")
    rf.ls()
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,True,line) #Tree input as t and the name of the tree should have all info included#
    Photon_Pt = tree2array(tree=t,branches=["PhotonPt"])
    if Analysis_Config.name == "Tree_Level_qqH_Photons_XS":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
    elif Analysis_Config.name == "gammaH_Photons_Decay_Only_Kinematics_Photon_Rate":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedTightID"])
    for event_num in range(len(event_weights)):
      if Photon_Pt[event_num] is not None:
        if len(Photon_Pt[event_num][0]) != 0:
            if (Passed_Cut_Based_ID[event_num][0][0] == True):  
              Pt_Photon_Signals.Fill(Photon_Pt[event_num][0][0],event_weights[event_num]*lumi)
    print(Pt_Photon_Signals.Integral())
    
# Add the ew_bkg to the Pt_Histogram #
with open(ew_bkg) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    lumi = 0
    print("Name", name)
    if "2016APV" in line or "16APV" in line:
        name = name +"_2016"
        lumi = 15.9
    if "2016" in line or "16" in line:
        name = name +"_2016"
        lumi = 20.
    elif "2017" in line or "17" in line:
        name = name +"_2017"
        lumi = 41.5
    elif "2018" in line or "18" in line:
        name = name +"_2018"
        lumi = 59.7
    rf = ROOT.TFile(str(sample),'READ')
    t = rf.Get("eventTree")
    rf.ls()
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,True,line) #Tree input as t and the name of the tree should have all info included#
    Photon_Pt = tree2array(tree=t,branches=["PhotonPt"])
    if Analysis_Config.name == "Tree_Level_qqH_Photons_XS":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
    elif Analysis_Config.name == "gammaH_Photons_Decay_Only_Kinematics_Photon_Rate":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedTightID"])
    Num_Photons_Passed = 0 
    Num_Events = len(event_weights)
    for event_num in range(len(event_weights)):
      if Photon_Pt[event_num] is not None:
        if len(Photon_Pt[event_num][0]) != 0:
            if (Passed_Cut_Based_ID[event_num][0][0] == True):  
              Num_Photons_Passed += 1 
              Pt_Photon_ew.Fill(Photon_Pt[event_num][0][0],event_weights[event_num]*lumi)
    print(Pt_Photon_ew.Integral()," Num Events: ",Num_Events, " Num Photons Passed: ",Num_Photons_Passed)
# Add the qq4l_bkg to the Pt_Histogram #
with open(qq4l_bkg) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    lumi = 0
    if "2016APV" in line or "16APV" in line:
        name = name +"_2016"
        lumi = 15.9
    if "2016" in line or "16" in line:
        name = name +"_2016"
        lumi = 20.
    elif "2017" in line or "17" in line:
        name = name +"_2017"
        lumi = 41.5
    elif "2018" in line or "18" in line:
        name = name +"_2018"
        lumi = 59.7
    rf = ROOT.TFile(str(sample),'READ')
    t = rf.Get("eventTree")
    rf.ls()
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,True,line) #Tree input as t and the name of the tree should have all info included#
    print(sum(event_weights * lumi))
    Photon_Pt = tree2array(tree=t,branches=["PhotonPt"])
    if Analysis_Config.name == "Tree_Level_qqH_Photons_XS":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
    elif Analysis_Config.name == "gammaH_Photons_Decay_Only_Kinematics_Photon_Rate":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedTightID"])
    for event_num in range(len(event_weights)):
        if(len(Passed_Cut_Based_ID[event_num][0]) != 0):
            Pt_Photon_qq4l.Fill(Photon_Pt[event_num][0][0],event_weights[event_num]*lumi)
    print(Pt_Photon_qq4l.Integral())
# Add the gg4l_bkg to the Pt_Histogram #

with open(gg4l_bkg) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    lumi = 0
    if "2016APV" in line or "16APV" in line:
        name = name +"_2016"
        lumi = 15.9
    if "2016" in line or "16" in line:
        name = name +"_2016"
        lumi = 20.
    elif "2017" in line or "17" in line:
        name = name +"_2017"
        lumi = 41.5
    elif "2018" in line or "18" in line:
        name = name +"_2018"
        lumi = 59.7
    rf = ROOT.TFile(str(sample),'READ')
    t = rf.Get("eventTree")
    rf.ls()
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,True,line) #Tree input as t and the name of the tree should have all info included#
    Photon_Pt = tree2array(tree=t,branches=["PhotonPt"])
    if Analysis_Config.name == "Tree_Level_qqH_Photons_XS":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
    elif Analysis_Config.name == "gammaH_Photons_Decay_Only_Kinematics_Photon_Rate":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedTightID"])
    Num_Photons_Passed = 0 
    Num_Events = len(event_weights)
    for event_num in range(len(event_weights)):
      if Photon_Pt[event_num] is not None:
        if len(Photon_Pt[event_num][0]) != 0:
            if (Passed_Cut_Based_ID[event_num][0][0] == True):  
              Num_Photons_Passed += 1
              Pt_Photon_gg4l.Fill(Photon_Pt[event_num][0][0],event_weights[event_num]*lumi)
    print(Pt_Photon_gg4l.Integral()," Num Events: ",Num_Events, " Num Photons Passed: ",Num_Photons_Passed)

# Add the ZX_bkg to the Pt_Histogram #

with open(ZX_bkg) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    if "2016" in line or "16" in line:
        name = name +"_2016"
    elif "2017" in line or "17" in line:
        name = name +"_2017"
    elif "2018" in line or "18" in line:
        name = name +"_2018"
    rf = ROOT.TFile(str(sample),'READ')
    t = rf.Get("eventTree")
    rf.ls()
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,True,line) #Tree input as t and the name of the tree should have all info included#
    Photon_Pt = tree2array(tree=t,branches=["PhotonPt"])
    if Analysis_Config.name == "Tree_Level_qqH_Photons_XS":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
    elif Analysis_Config.name == "gammaH_Photons_Decay_Only_Kinematics_Photon_Rate":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedTightID"])
    for event_num in range(len(event_weights)):
      if Photon_Pt[event_num] is not None:
        if len(Photon_Pt[event_num][0]) != 0: 
              Pt_Photon_ZX.Fill(Photon_Pt[event_num][0][0],event_weights[event_num])
    print(Pt_Photon_ZX.Integral())
# Add the ew_bkg to the Pt_Histogram #

with open(gammaH_tree) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    if "2016APV" in line or "16APV" in line:
        name = name +"_2016"
        lumi = 15.9
    if "2016" in line or "16" in line:
        name = name +"_2016"
        lumi = 20.
    elif "2017" in line or "17" in line:
        name = name +"_2017"
        lumi = 41.5
    elif "2018" in line or "18" in line:
        name = name +"_2018"
        lumi = 59.7
    rf = ROOT.TFile(str(sample),'READ')
    t = rf.Get("eventTree")
    rf.ls()
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,True,line) #Tree input as t and the name of the tree should have all info included#
    Photon_Pt = tree2array(tree=t,branches=["PhotonPt"])
    SM_Like_Decay_Weight = tree2array(tree=t,branches=["p_Gen_Dec_SIG_ghz1_1_JHUGen"])
    if Analysis_Config.name == "Tree_Level_qqH_Photons_XS":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
    elif Analysis_Config.name == "gammaH_Photons_Decay_Only_Kinematics_Photon_Rate":
        Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedTightID"])
    for event_num in range(len(event_weights)):
      if Photon_Pt[event_num] is not None:
        if len(Photon_Pt[event_num][0]) != 0:
          if (Passed_Cut_Based_ID[event_num][0][0] == True):  
            Pt_Photon_gammaH.Fill(Photon_Pt[event_num][0][0],event_weights[event_num]*5000*lumi*SM_Like_Decay_Weight[event_num][0])

c1=ROOT.TCanvas('c1','test',200,10,600,600)
#===============================================#
Pt_stack = ROOT.THStack("Pt","")
Pt_Photon_Signals.SetLineColor(1)
Pt_Photon_Signals.SetMarkerColor(1)
Pt_Photon_Signals.SetFillColor(1)
Pt_stack.Add(Pt_Photon_Signals)
Pt_Photon_ew.SetLineColor(2)
Pt_Photon_ew.SetMarkerColor(2)
Pt_Photon_ew.SetFillColor(2)
Pt_stack.Add(Pt_Photon_ew)
Pt_Photon_qq4l.SetLineColor(3)
Pt_Photon_qq4l.SetMarkerColor(3)
Pt_Photon_qq4l.SetFillColor(3)
Pt_stack.Add(Pt_Photon_qq4l)
Pt_Photon_gg4l.SetLineColor(4)
Pt_Photon_gg4l.SetMarkerColor(4)
Pt_Photon_gg4l.SetFillColor(4)
Pt_stack.Add(Pt_Photon_gg4l)
Pt_Photon_ZX.SetLineColor(5)
Pt_Photon_ZX.SetMarkerColor(5)
Pt_Photon_ZX.SetFillColor(5)
Pt_stack.Add(Pt_Photon_ZX)
Pt_Photon_gammaH.SetLineColor(6)
Pt_Photon_gammaH.SetMarkerColor(6)
Pt_Photon_gammaH.SetFillColor(6)
Pt_stack.Add(Pt_Photon_gammaH)
Pt_stack.Draw("hist")

Pt_stack.GetXaxis().SetTitle("p_{t} #gamma [GeV]")
Pt_stack.GetYaxis().SetTitle("Events / 6.5 GeV")

legend = ROOT.TLegend(0.8,0.7,0.34,0.9)
legend.SetBorderSize(0)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)

legend.AddEntry(Pt_Photon_Signals,"H production (ggH+VBF+VH+qqH)","f")
legend.AddEntry(Pt_Photon_ew,"Ew_bkg","f")
legend.AddEntry(Pt_Photon_qq4l,"qq4l bkg","f")
legend.AddEntry(Pt_Photon_gg4l,"gg4l","f")
legend.AddEntry(Pt_Photon_ZX,"ZX bkg","f")
legend.AddEntry(Pt_Photon_gammaH,"#gammaH #rightarrow 4l (51.17 fb)","f")

legend.Draw()


CMS_lumi.CMS_lumi(c1,4,0)
c1.Draw()
c1.SaveAs("Photon_Pt_qqH.png")
c1.SaveAs("Photon_Pt_qqH.pdf")
