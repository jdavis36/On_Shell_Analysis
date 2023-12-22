import ROOT
import numpy as np 
import sys
import os
from AnalysisTools.Utils.Calc_Weight import *
from AnalysisTools.Utils import Config as Config
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

#m4l_Signals= ROOT.TH1F("m4l","m4l",100,70,170)
#m4l_ew = ROOT.TH1F("m4l","m4l",100,70,170)
#m4l_qq4l = ROOT.TH1F("m4l","m4l",100,70,170)
#m4l_gg4l = ROOT.TH1F("m4l","m4l",100,70,170)
#m4l_ZX = ROOT.TH1F("m4l","m4l",100,70,170)
#m4l_gammaH = ROOT.TH1F("m4l","m4l",100,70,170)

m4l_Signals= ROOT.TH1F("m4l","m4l",50,70,170)
m4l_ZZ_Zy= ROOT.TH1F("m4l","m4l",50,70,170)
m4l_ZX = ROOT.TH1F("m4l","m4l",50,70,170)
m4l_gammaH = ROOT.TH1F("m4l","m4l",50,70,170)

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics")

# Add the signal to the Pt_Histogram #
with open(Signal_Trees) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    if "2016APV" in line or "16APV" in line:
	      name = name+"_2016"
	      lumi = 16.9
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
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,False,line) #Tree input as t and the name of the tree should have all info included#
    m4l = tree2array(tree=t,branches=["ZZMass"])
    for event_num in range(len(event_weights)):
        m4l_Signals.Fill(m4l[event_num][0],event_weights[event_num]*lumi)
    print(m4l_Signals.Integral())
    
# Add the ew_bkg to the Pt_Histogram #
with open(ew_bkg) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    lumi = 0
    if "2016APV" in line or "16APV" in line:
	      name = name+"_2016"
	      lumi = 16.9
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
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,False,line) #Tree input as t and the name of the tree should have all info included#
    m4l = tree2array(tree=t,branches=["ZZMass"])
    for event_num in range(len(event_weights)):
        m4l_ZZ_Zy.Fill(m4l[event_num][0],event_weights[event_num]*lumi)
    print(m4l_ZZ_Zy.Integral())

# Add the qq4l_bkg to the Pt_Histogram #
with open(qq4l_bkg) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    lumi = 0
    if "2016APV" in line or "16APV" in line:
	      name = name+"_2016"
	      lumi = 16.9
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
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,False,line) #Tree input as t and the name of the tree should have all info included#
    m4l = tree2array(tree=t,branches=["ZZMass"])
    for event_num in range(len(event_weights)):
        m4l_ZZ_Zy.Fill(m4l[event_num][0],event_weights[event_num]*lumi)
    print(m4l_ZZ_Zy.Integral())
# Add the gg4l_bkg to the Pt_Histogram #

with open(gg4l_bkg) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    lumi = 0
    if "2016APV" in line or "16APV" in line:
	      name = name+"_2016"
	      lumi = 16.9
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
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,False,line) #Tree input as t and the name of the tree should have all info included#
    m4l = tree2array(tree=t,branches=["ZZMass"])
    for event_num in range(len(event_weights)):
        m4l_ZZ_Zy.Fill(m4l[event_num][0],event_weights[event_num]*lumi)
    print(m4l_ZZ_Zy.Integral())

# Add the ZX_bkg to the Pt_Histogram #

with open(ZX_bkg) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    if "2016APV" in line or "16APV" in line:
	      name = name+"_2016"
	      lumi = 16.9
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
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,False,line) #Tree input as t and the name of the tree should have all info included#
    m4l = tree2array(tree=t,branches=["ZZMass"])
    for event_num in range(len(event_weights)):
        m4l_ZX.Fill(m4l[event_num][0],event_weights[event_num])
    print(m4l_ZX.Integral())

# Add the ew_bkg to the Pt_Histogram #
with open(gammaH_tree) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    name = sort_category_templates(Analysis_Config,prod)[0]
    if "2016APV" in line or "16APV" in line:
	      name = name+"_2016"
	      lumi = 16.9
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
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,False,line) #Tree input as t and the name of the tree should have all info included#
    SM_Like_Decay_Weight = tree2array(tree=t,branches=["p_Gen_Dec_SIG_ghz1_1_JHUGen"])
    m4l = tree2array(tree=t,branches=["ZZMass"])
    # Decide if there will be an extra weight applied as a KFactor for example #
    Extra_Factor = 1
    if Analysis_Config.name == "gammaH_Photons_Decay_Only_Kinematics":
        Extra_Factor = 1.14
    if Analysis_Config.name == "Tree_Level_qqH_Photons_XS":
        Extra_Factor = 100
    for event_num in range(len(event_weights)):
        m4l_gammaH.Fill(m4l[event_num][0],event_weights[event_num]*100*lumi*SM_Like_Decay_Weight[event_num][0]*Extra_Factor)
    print(m4l_gammaH.Integral())

#=====================================================================================#
# Calculate the Most Efficient cut for sensitivity#
# Plot signal to background for each cut#

Signal_Bkg_Ratio = array.array('f')
Pt_Cut = array.array('f')
c1=ROOT.TCanvas('c1','test',200,10,600,600)

# Null Hypothesis is the Background events above a certain cut #
'''xbins = m4l_Signals.GetNbinsX()
for x in range (1,xbins+1):
  binx_c = Pt_Photon_gammaH.GetXaxis().GetBinCenter(x)
  Bkg_Expectation_Above_Cut = 0
  Bkg_Expectation_Above_Cut += Pt_Photon_Signals.Integral(x,xbins+1)
  Bkg_Expectation_Above_Cut += Pt_Photon_ew.Integral(x,xbins+1)
  Bkg_Expectation_Above_Cut += Pt_Photon_qq4l.Integral(x,xbins+1)
  Bkg_Expectation_Above_Cut += Pt_Photon_gg4l.Integral(x,xbins+1)
  Bkg_Expectation_Above_Cut += Pt_Photon_ZX.Integral(x,xbins+1)
  Signal = Pt_Photon_gammaH.Integral(x,xbins+1)
  Signal_Bkg_Ratio.append(Signal/Bkg_Expectation_Above_Cut)
  Pt_Cut.append(binx_c)

Signal_Bkg_Graph = ROOT.TGraph(xbins,Pt_Cut,Signal_Bkg_Ratio)
Signal_Bkg_Graph.SetTitle("Signal_To_Bkg_Ratio;Pt_cut;S/B")
Signal_Bkg_Graph.Draw("AC*")
c1.Draw()
c1.SaveAs("Signal_Bkg_Ratio.png")
'''
c1=ROOT.TCanvas('c1','test',200,10,800,600)
#===============================================#
m4l_stack = ROOT.THStack("m4l","")
m4l_Signals.SetLineColor(ROOT.TColor.GetColor("#ff9b9b"))
m4l_Signals.SetFillColor(ROOT.TColor.GetColor("#ff9b9b"))
m4l_ZZ_Zy.SetFillColor(ROOT.TColor.GetColor("#99ccff")) #kAzure + 6)
m4l_ZZ_Zy.SetLineColor(ROOT.TColor.GetColor("#99ccff")) #kAzure + 6)
m4l_ZX.SetLineColor(ROOT.TColor.GetColor("#669966"))
m4l_ZX.SetFillColor(ROOT.TColor.GetColor("#669966")) 
m4l_gammaH.SetLineColor(ROOT.kRed)
m4l_gammaH.SetFillColor(ROOT.kRed)
m4l_gammaH.SetFillColorAlpha(ROOT.kRed,0)


# Load order of the plots #
m4l_stack.Add(m4l_ZX)
m4l_stack.Add(m4l_ZZ_Zy)
m4l_stack.Add(m4l_Signals)
m4l_stack.Add(m4l_gammaH)

# Set THstack #
m4l_stack.Draw("hist")
m4l_stack.GetXaxis().SetTitle("m_{4l} [GeV]")
m4l_stack.GetYaxis().SetTitle("Events / 2 GeV")

legend = ROOT.TLegend(0.9,0.7,0.7,0.9)
legend.SetBorderSize(0)
legend.SetBorderSize(0)
legend.SetFillColor(0) 
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)

legend.AddEntry(m4l_Signals,"SM H","f")
legend.AddEntry(m4l_ZZ_Zy,"ZZ/Z#gamma^{*}","f")
legend.AddEntry(m4l_ZX,"Z+X","f")
legend.AddEntry(m4l_gammaH,"#gamma H (1 fb)","l")

legend.Draw()

CMS_lumi.CMS_lumi(c1,4,0)

c1.Draw()
c1.SaveAs("m4l_KFactor.png")
c1.SaveAs("m4l_KFactor.pdf")
