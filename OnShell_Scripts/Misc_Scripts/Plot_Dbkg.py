import ROOT
import numpy as np 
import sys
import os
from AnalysisTools.Utils.Calc_Weight import *
from AnalysisTools.Utils import Config as Config
#import AnalysisTools.Utils.stylefunctions as style
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

Signal_Trees = sys.argv[1] 
ew_bkg = sys.argv[2]
qq4l_bkg = sys.argv[3]
gg4l_bkg = sys.argv[4]
ZX_bkg = sys.argv[5]
gammaH_tree = sys.argv[6]

#D_bkg_Signals= ROOT.TH1F("D_bkg","D_bkg",10,0,1)
#D_bkg_ew = ROOT.TH1F("D_bkg","D_bkg",10,0,1)
#D_bkg_qq4l = ROOT.TH1F("D_bkg","D_bkg",10,0,1)
#D_bkg_gg4l = ROOT.TH1F("D_bkg","D_bkg",10,0,1)
#D_bkg_ZX = ROOT.TH1F("D_bkg","D_bkg",10,0,1)
#D_bkg_gammaH = ROOT.TH1F("D_bkg","D_bkg",10,0,1)

D_bkg_Signals= ROOT.TH1F("m4l","m4l",10,0,1)
D_bkg_ZZ_Zy= ROOT.TH1F("m4l","m4l",10,0,1)
D_bkg_ZX = ROOT.TH1F("m4l","m4l",10,0,1)
D_bkg_gammaH = ROOT.TH1F("m4l","m4l",10,0,1)

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics")
#Analysis_Config = Config.Analysis_Config("Tree_Level_qqH_Photons_XS")


Categories= [0]
for Category in Categories:
  # Add the signal to the Pt_Histogram #
  with open(Signal_Trees) as f:
    for line in f:
      sample = line.strip('\n')
      prod = sample.split("/")[-2]
      print("PROD",prod)
      name = sort_category_templates(Analysis_Config,prod)[0]
      if "2016APV" in line or "16APV" in line:
          name = name+"_2016"
          lumi = 16
      elif "2016" in line or "16" in line:
          name = name +"_2016"
          lumi = 20
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
      D_bkg = tree2array(tree=t,branches=["D_bkg"])
      Event_Tag = tree2array(tree=t,branches=["EventTag"])
      for event_num in range(len(event_weights)):
        if Event_Tag[event_num][0] == Category:
          D_bkg_Signals.Fill(D_bkg[event_num][0],event_weights[event_num]*lumi)
      print(D_bkg_Signals.Integral())
      
  # Add the ew_bkg to the Pt_Histogram #
  with open(ew_bkg) as f:
    for line in f:
      sample = line.strip('\n')
      prod = sample.split("/")[-2]
      name = sort_category_templates(Analysis_Config,prod)[0]
      lumi = 0
      print("Name", name)
      if "2016APV" in line or "16APV" in line:
          name = name+"_2016"
          lumi = 16
      elif "2016" in line or "16" in line:
          name = name +"_2016"
          lumi = 20
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
      D_bkg = tree2array(tree=t,branches=["D_bkg"])
      Event_Tag = tree2array(tree=t,branches=["EventTag"])
      for event_num in range(len(event_weights)):
        if Event_Tag[event_num][0] == Category:
          D_bkg_ZZ_Zy.Fill(D_bkg[event_num][0],event_weights[event_num]*lumi)
      print(D_bkg_ZZ_Zy.Integral())
  # Add the qq4l_bkg to the Pt_Histogram #
  with open(qq4l_bkg) as f:
    for line in f:
      sample = line.strip('\n')
      prod = sample.split("/")[-2]
      name = sort_category_templates(Analysis_Config,prod)[0]
      lumi = 0
      if "2016APV" in line or "16APV" in line:
          name = name+"_2016"
          lumi = 16
      elif "2016" in line or "16" in line:
          name = name +"_2016"
          lumi = 20
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
      D_bkg = tree2array(tree=t,branches=["D_bkg"])
      Event_Tag = tree2array(tree=t,branches=["EventTag"])
      for event_num in range(len(event_weights)):
        if Event_Tag[event_num][0] == Category:
          D_bkg_ZZ_Zy.Fill(D_bkg[event_num][0],event_weights[event_num]*lumi)
      print(D_bkg_ZZ_Zy.Integral())
  # Add the gg4l_bkg to the Pt_Histogram #

  with open(gg4l_bkg) as f:
    for line in f:
      sample = line.strip('\n')
      prod = sample.split("/")[-2]
      name = sort_category_templates(Analysis_Config,prod)[0]
      lumi = 0
      if "2016APV" in line or "16APV" in line:
          name = name+"_2016"
          lumi = 16
      elif "2016" in line or "16" in line:
          name = name +"_2016"
          lumi = 20
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
      D_bkg = tree2array(tree=t,branches=["D_bkg"])
      Event_Tag = tree2array(tree=t,branches=["EventTag"])
      for event_num in range(len(event_weights)):
        if Event_Tag[event_num][0] == Category:
          D_bkg_ZZ_Zy.Fill(D_bkg[event_num][0],event_weights[event_num]*lumi)
      print(D_bkg_ZZ_Zy.Integral())

  # Add the ZX_bkg to the Pt_Histogram #

  with open(ZX_bkg) as f:
    for line in f:
      sample = line.strip('\n')
      prod = sample.split("/")[-2]
      name = sort_category_templates(Analysis_Config,prod)[0]
      if "2016APV" in line or "16APV" in line:
          name = name+"_2016"
          lumi = 16
      elif "2016" in line or "16" in line:
          name = name +"_2016"
          lumi = 20
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
      D_bkg = tree2array(tree=t,branches=["D_bkg"])
      Event_Tag = tree2array(tree=t,branches=["EventTag"])
      for event_num in range(len(event_weights)):
        if Event_Tag[event_num][0] == Category:
          D_bkg_ZX.Fill(D_bkg[event_num][0],event_weights[event_num])
      print(D_bkg_ZX.Integral())

  # Add the ew_bkg to the Pt_Histogram #
  with open(gammaH_tree) as f:
    for line in f:
      sample = line.strip('\n')
      prod = sample.split("/")[-2]
      name = sort_category_templates(Analysis_Config,prod)[0]
      if "2016APV" in line or "16APV" in line:
          name = name+"_2016"
          lumi = 16
      elif "2016" in line or "16" in line:
          name = name +"_2016"
          lumi = 20
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
      D_bkg = tree2array(tree=t,branches=["D_bkg"])
      SM_Like_Decay_Weight = tree2array(tree=t,branches=["p_Gen_Dec_SIG_ghz1_1_JHUGen"])
      # Decide if there will be an extra weight applied as a KFactor for example #
      Extra_Factor = 1
      if Analysis_Config.name == "gammaH_Photons_Decay_Only_Kinematics":
        Extra_Factor = 1.14
      if Analysis_Config.name == "Tree_Level_qqH_Photons_XS":
        Extra_Factor = 100
      for event_num in range(len(event_weights)):
        if Event_Tag[event_num][0] == Category:
          D_bkg_gammaH.Fill(D_bkg[event_num][0],event_weights[event_num]*lumi*100*SM_Like_Decay_Weight[event_num][0]*Extra_Factor)
      print(D_bkg_gammaH.Integral())


  c1=ROOT.TCanvas('c1','test',200,10,600,600)
  #===============================================#
  #===============================================#
  D_bkg_stack = ROOT.THStack("D_bkg","")
  D_bkg_Signals.SetLineColor(ROOT.TColor.GetColor("#ff9b9b"))
  D_bkg_Signals.SetFillColor(ROOT.TColor.GetColor("#ff9b9b"))
  D_bkg_ZZ_Zy.SetFillColor(ROOT.TColor.GetColor("#99ccff")) #kAzure + 6)
  D_bkg_ZZ_Zy.SetLineColor(ROOT.TColor.GetColor("#99ccff")) #kAzure + 6)
  D_bkg_ZX.SetLineColor(ROOT.TColor.GetColor("#669966"))
  D_bkg_ZX.SetFillColor(ROOT.TColor.GetColor("#669966")) 
  D_bkg_gammaH.SetLineColor(ROOT.kRed)
  D_bkg_gammaH.SetFillColor(ROOT.kRed)
  D_bkg_gammaH.SetFillColorAlpha(ROOT.kRed,0)

 
 # Load order of the plots #
  D_bkg_stack.Add(D_bkg_ZX)
  D_bkg_stack.Add(D_bkg_ZZ_Zy)
  D_bkg_stack.Add(D_bkg_Signals)
  D_bkg_stack.Add(D_bkg_gammaH)

  D_bkg_stack.Draw("hist")
  D_bkg_stack.GetXaxis().SetTitle("D_{bkg}")
  D_bkg_stack.GetYaxis().SetTitle("Events / bin")

 
  legend = ROOT.TLegend(0.9,0.7,0.48,0.9)
  legend.SetBorderSize(0)
  legend.SetBorderSize(0)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetTextFont(42)
  legend.SetTextSize(0.035)
  legend.AddEntry(D_bkg_Signals,"SM H","f")
  legend.AddEntry(D_bkg_ZZ_Zy,"ZZ/Z#gamma^{*}","f")
  legend.AddEntry(D_bkg_ZX,"Z+X","f")
  legend.AddEntry(D_bkg_gammaH,"#gamma H (1 fb)","l")

  legend.Draw()

  #style.applycanvasstyle(c1)
  
  #style.applyaxesstyle(D_bkg_stack)
  CMS_lumi.CMS_lumi(c1,4,0)

  c1.Draw()
  if Category == 0:
    c1.SaveAs("Dbkg_Untagged_KFactor.png")
    c1.SaveAs("Dbkg_Untagged_KFactor.pdf")
  if Category == 9:
    c1.SaveAs("Dbkg_gammaH_KFactor.png")
    c1.SaveAs("Dbkg_gammaH_KFactor.pdf")
