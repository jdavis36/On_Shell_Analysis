import ROOT
import numpy as np
import os 
import sys
from AnalysisTools.Utils.Calc_Weight import *
from AnalysisTools.Utils import Config as Config
from AnalysisTools.Utils import tdr_new
from AnalysisTools.Utils import CMS_lumi
from AnalysisTools.TemplateMaker.Sort_Category import sort_category_templates
from AnalysisTools.Utils.root_numpy import tree2array
from scipy.stats import poisson 
from AnalysisTools.Utils import tdr_new
from AnalysisTools.Utils import CMS_lumi
import array 

ROOT.gROOT.SetBatch(True)
#tdr_new.setTDRStyle()

Input_Trees = sys.argv[1]
output_directory =sys.argv[2]

if not os.path.isdir(output_directory):
  os.mkdir(output_directory)

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics_Photon_Rate")


with open(Input_Trees) as f:
  for line in f:
    sample = line.strip('\n')
    prod = sample.split("/")[-2]
    print("PROD",prod)
    name = sort_category_templates(Analysis_Config,prod)[0]
    if "2016APV" in line or "16APV" in line:
        name = name +"_2016"
        lumi = 15.9
    elif "2016" in line or "16" in line:
        name = name +"_2016"
        lumi = 20.
    elif "2017" in line or "17" in line:
        name = name +"_2017"
        lumi = 41.5
    elif "2018" in line or "18" in line:
        name = name +"_2018"
        lumi = 59.7
    event_weights = Calc_Tree_Weight_2021_gammaH(sample,name,True,"eventTree")
    PU_Up = tree2array(tree=sample,branches=["PUWeight_Up/PUWeight"],top_branch_name="eventTree")
    PU_Dn = tree2array(tree=sample,branches=["PUWeight_Dn/PUWeight"],top_branch_name="eventTree")
    PU = tree2array(tree=sample,branches=["PUWeight"],top_branch_name="eventTree")
    L1_Up = tree2array(tree=sample,branches=["L1prefiringWeightUp/L1prefiringWeight"],top_branch_name="eventTree")
    L1_Dn = tree2array(tree=sample,branches=["L1prefiringWeightDn/L1prefiringWeight"],top_branch_name="eventTree")
    D_bkg = tree2array(tree=sample,branches=["D_bkg"],top_branch_name="eventTree")

    # Convert the weights to be up and down #
    PU_Up = PU_Up * event_weights
    PU_Dn = PU_Dn * event_weights
    L1_Up = L1_Up * event_weights
    L1_Dn = L1_Dn * event_weights

    print(PU)

    c1=ROOT.TCanvas('c1','test',600,10,1000,600)

    hist_Nominal_PU = ROOT.TH1F("hist_Nominal_PU","hist_Nominal_PU ",10,0,1)
    hist_Scale_Up_PU = ROOT.TH1F("hist_PU_Up","hist_PU_Up",10,0,1)
    hist_Scale_Down_PU= ROOT.TH1F("hist_PU_Dn","hist_PU_Dn",10,0,1)
    hist_Nominal_L1 = ROOT.TH1F("hist_Nominal_L1","hist_Nominal_L1",10,0,1)
    hist_Scale_Up_L1 =ROOT.TH1F("hist_L1_Up","hist_L1_Up",10,0,1)
    hist_Scale_Down_L1= ROOT.TH1F("hist_L1_Dn","hist_L1_Dn",10,0,1)    

    for event_num in range(len(event_weights)):
        hist_Nominal_PU.Fill(D_bkg[event_num],event_weights[event_num]*lumi)
        hist_Scale_Up_PU.Fill(D_bkg[event_num],PU_Up[event_num]*lumi)
        hist_Scale_Down_PU.Fill(D_bkg[event_num],PU_Dn[event_num]*lumi)
        hist_Nominal_L1.Fill(D_bkg[event_num],event_weights[event_num]*lumi)
        hist_Scale_Up_L1.Fill(D_bkg[event_num],L1_Up[event_num]*lumi)
        hist_Scale_Down_L1.Fill(D_bkg[event_num],L1_Dn[event_num]*lumi)

    ROOT.gStyle.SetOptStat(0)

    hist_Nominal_PU.GetXaxis().SetTitle("D_{Bkg}")
    hist_Nominal_PU.GetYaxis().SetTitle("Nominal PU Factor vs. Scale PU Up")
    Scale_Up_Ratio_PU = ROOT.TRatioPlot(hist_Nominal_PU,hist_Scale_Up_PU)
    Scale_Up_Ratio_PU
    c1.Draw()
    Scale_Up_Ratio_PU.Draw()
    c1.SaveAs(output_directory+"/{}".format(prod)+"_PU_Up.pdf")

    hist_Nominal_PU.GetXaxis().SetTitle("D_{Bkg}")
    hist_Nominal_PU.SetTitle("Nominal PU Factor vs. Scale PU Dn")
    Scale_Down_Ratio_PU = ROOT.TRatioPlot(hist_Nominal_PU,hist_Scale_Down_PU)
    Scale_Down_Ratio_PU.GetLowYaxis().SetNdivisions(505)
    Scale_Down_Ratio_PU.Draw()
    c1.Draw()
    c1.SaveAs(output_directory+"/{}".format(prod)+"_PU_Down.pdf")

    hist_Nominal_L1.GetXaxis().SetTitle("D_{Bkg}")
    hist_Nominal_L1.SetTitle("Nominal L1 Factor vs. Scale L1 Up")
    Scale_Up_Ratio_L1 = ROOT.TRatioPlot(hist_Nominal_L1,hist_Scale_Up_L1)
    Scale_Up_Ratio_L1.Draw()
    c1.Draw()
    c1.SaveAs(output_directory+"/{}".format(prod)+"_L1_Up.pdf")

    hist_Nominal_L1.GetXaxis().SetTitle("D_{Bkg}")
    hist_Nominal_L1.SetTitle("Nominal L1 Factor vs. Scale L1 Up")
    Scale_Down_Ratio_L1 = ROOT.TRatioPlot(hist_Nominal_L1,hist_Scale_Down_L1)
    Scale_Down_Ratio_L1.Draw()
    c1.Draw()
    c1.SaveAs(output_directory+"/{}".format(prod)+"_L1_Dn.pdf")



