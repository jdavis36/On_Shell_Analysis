import ROOT
import numpy as np 
import sys
import os
from AnalysisTools.Utils.Calc_Weight import *
from AnalysisTools.Utils import Config as Config
from AnalysisTools.TemplateMaker.Sort_Category import sort_category_templates
from root_numpy import array2tree, tree2array
from scipy.stats import poisson 
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

Pt_Photon_Signals= ROOT.TH1F("Photon Pt","Photon Pt",100,0,800)
Pt_Photon_ew = ROOT.TH1F("Photon Pt","Photon Pt",100,0,800)
Pt_Photon_qq4l = ROOT.TH1F("Photon Pt","Photon Pt",100,0,800)
Pt_Photon_gg4l = ROOT.TH1F("Photon Pt","Photon Pt",100,0,800)
Pt_Photon_ZX = ROOT.TH1F("Photon Pt","Photon Pt",100,0,800)
Pt_Photon_gammaH = ROOT.TH1F("Photon Pt","Photon Pt",100,0,800)

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics")

# Add the signal to the Pt_Histogram #
with open(Signal_Trees) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    print("PROD",prod)
    name = sort_category_templates(Analysis_Config,prod)[0]
    if "2016" in line or "16" in line:
        name = name +"_2016"
        lumi = 35.9
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
    Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
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
    if "2016" in line or "16" in line:
        name = name +"_2016"
        lumi = 35.9
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
    Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
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
    if "2016" in line or "16" in line:
        name = name +"_2016"
        lumi = 35.9
    if "2017" in line or "17" in line:
        name = name +"_2017"
        lumi = 41.5
    if "2018" in line or "18" in line:
        name = name +"_2018"
        lumi = 59.7
    rf = ROOT.TFile(str(sample),'READ')
    t = rf.Get("eventTree")
    rf.ls()
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,True,line) #Tree input as t and the name of the tree should have all info included#
    print(sum(event_weights * lumi))
    Photon_Pt = tree2array(tree=t,branches=["PhotonPt"])
    Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
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
    if "2016" in line or "16" in line:
        name = name +"_2016"
        lumi = 35.9
    if "2017" in line or "17" in line:
        name = name +"_2017"
        lumi = 41.5
    if "2018" in line or "18" in line:
        name = name +"_2018"
        lumi = 59.7
    rf = ROOT.TFile(str(sample),'READ')
    t = rf.Get("eventTree")
    rf.ls()
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,True,line) #Tree input as t and the name of the tree should have all info included#
    Photon_Pt = tree2array(tree=t,branches=["PhotonPt"])
    Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
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
    if "2017" in line  or "17" in line:
        name = name +"_2017"
    if "2018" in line  or "18" in line:
        name = name +"_2018"
    rf = ROOT.TFile(str(sample),'READ')
    t = rf.Get("eventTree")
    rf.ls()
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,True,line) #Tree input as t and the name of the tree should have all info included#
    Photon_Pt = tree2array(tree=t,branches=["PhotonPt"])
    Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
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
    if "2016" or "16" in line:
        name = name +"_2016"
    if "2017" or "17" in line:
        name = name +"_2017"
    if "2018" or "18" in line:
        name = name +"_2018"
    rf = ROOT.TFile(str(sample),'READ')
    t = rf.Get("eventTree")
    rf.ls()
    event_weights = Calc_Tree_Weight_2021_gammaH(t,name,True,line) #Tree input as t and the name of the tree should have all info included#
    Photon_Pt = tree2array(tree=t,branches=["PhotonPt"])
    Passed_Cut_Based_ID = tree2array(tree=t,branches=["PhotonIsCutBasedLooseID"])
    for event_num in range(len(event_weights)):
      if Photon_Pt[event_num] is not None:
        if len(Photon_Pt[event_num][0]) != 0:
            if (Passed_Cut_Based_ID[event_num][0][0] == True):  
              Pt_Photon_gammaH.Fill(Photon_Pt[event_num][0][0],event_weights[event_num]*50000*lumi)

# Calculate the Most Efficient cut for a discovery#
# Basically if I put a selection cut at X-GEV how many events do I need to measure to claim discovery ?#

Events_Needed_For_Discovery = array.array('f')
#Extra for CS Discovery Sensitivity#
CS_For_Discovery_Zy = array.array('f')
Expected_300fb_Events = 0.7861
CS_for_Expected_300fb_Events = 37.287412 #fb
CS_For_Discovery_X2 = array.array('f')
Pt_Cut = array.array('f')
xbins = Pt_Photon_Signals.GetNbinsX()
# Calculate the chisquare for the bins remaining above the pt cut #
'''
for x in range(1,xbins+1):
    observed_data = []
    expected_data = []
    bkg = 0
    signal = 0
    for xx in range(x,xbins+1):
       bkg = Pt_Photon_Signals.GetBinContent(xx) + Pt_Photon_ew.Integral(x,xbins+1) + Pt_Photon_qq4l.Integral(x,xbins+1) + Pt_Photon_gg4l.Integral(x,xbins+1)
'''

# Null Hypothesis is the Background events above a certain cut #
for x in range (1,xbins+1):
  binx_c = Pt_Photon_gammaH.GetXaxis().GetBinCenter(x)
  Bkg_Expectation_Above_Cut = 0
  Bkg_Expectation_Above_Cut += Pt_Photon_Signals.Integral(x,xbins+1)
  Bkg_Expectation_Above_Cut += Pt_Photon_ew.Integral(x,xbins+1)
  Bkg_Expectation_Above_Cut += Pt_Photon_qq4l.Integral(x,xbins+1)
  Bkg_Expectation_Above_Cut += Pt_Photon_gg4l.Integral(x,xbins+1)
  Bkg_Expectation_Above_Cut += Pt_Photon_ZX.Integral(x,xbins+1)
  Fraction_gammaH_Above_Cut = Pt_Photon_gammaH.Integral(x,xbins+1)/Pt_Photon_gammaH.Integral()
  pvalue = 1
  N_events = 0 
  while pvalue > 3E-7:
    pvalue = 1 - poisson.cdf(N_events, Bkg_Expectation_Above_Cut, loc=0)
    N_events += 1
  CS_For_Discovery_Zy.append((N_events/(Expected_300fb_Events*Fraction_gammaH_Above_Cut)) * CS_for_Expected_300fb_Events)
  Events_Needed_For_Discovery.append(N_events)
  Pt_Cut.append(binx_c)

c1=ROOT.TCanvas('c1','test',200,10,600,600)
XS_Graph = ROOT.TGraph(xbins,Pt_Cut,CS_For_Discovery_Zy)
XS_Graph.SetTitle("XS for 5 sigma;Pt_cut;XS [fb]")
XS_Graph.Draw("AC*")
c1.Draw()
c1.SaveAs("XS_Significance.png")

c1=ROOT.TCanvas('c1','test',200,10,600,600)
Significance_Graph = ROOT.TGraph(xbins,Pt_Cut,Events_Needed_For_Discovery)
Significance_Graph.GetYaxis().SetRange(0,150)
Significance_Graph.SetTitle("Number for 5 sigma;Pt_cut;N_events")
Significance_Graph.Draw("AC*")
c1.SetLogy()
c1.Draw()
c1.SaveAs("Pt_Significance.png")
#=====================================================================================#
# Calculate the Most Efficient cut for sensitivity#
# Plot signal to background for each cut#

Signal_Bkg_Ratio = array.array('f')
Pt_Cut = array.array('f')
c1=ROOT.TCanvas('c1','test',200,10,600,600)

# Null Hypothesis is the Background events above a certain cut #
xbins = Pt_Photon_Signals.GetNbinsX()
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

legend = ROOT.TLegend(0.9,0.7,0.48,0.9)
legend.AddEntry(Pt_Photon_Signals,"H production (ggH+VBF+VH+qqH)","lep")
legend.AddEntry(Pt_Photon_ew,"Ew_bkg","lep")
legend.AddEntry(Pt_Photon_qq4l,"qq4l bkg","lep")
legend.AddEntry(Pt_Photon_gg4l,"gg4l","lep")
legend.AddEntry(Pt_Photon_ZX,"ZX bkg","lep")
legend.AddEntry(Pt_Photon_gammaH,"gammaH signal","lep")

legend.Draw()
c1.Draw()
c1.SaveAs("Pt_Cut_Plot.png")



