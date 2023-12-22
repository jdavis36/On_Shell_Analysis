import ROOT
import sys
import os
from AnalysisTools.Utils.ReWeightSample import *
from AnalysisTools.Utils import Config as Config
from root_numpy import array2tree, tree2array

ROOT.gROOT.SetBatch(True)
Input_Tree = sys.argv[1]
Input_Probabilities = sys.argv[3]
OutputDir = sys.argv[2]

if not os.path.isdir(OutputDir):
  os.mkdir(OutputDir)

DoInterf = False

f1 = ROOT.TFile(Input_Tree, 'READ')
t1 = f1.Get("eventTree")

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics_Photon_Rate")

branchnames = [ x.GetName() for x in t1.GetListOfBranches() ]

Discriminant_Names=[]
for name in branchnames:
  if name.startswith("D_") and not "Gen" in name:
    Discriminant_Names.append(name)

Discriminant_Names.append("Z2Mass")
Discriminant_Names.append("Z1Mass")

# Read input Probabilities #
Probability_Names = [] 
with open(Input_Probabilities,'r') as p_list:
  for p in p_list:
    Probability_Names.append(p.rstrip('\n'))

#Make Plots#
D_bkg = tree2array(tree=t1,branches=["D_bkg"]).astype(float)
for P_name in Probability_Names:
  for D_name in Discriminant_Names:
    print(D_name,P_name)
    # Format the Output Name and directory #
    # Make the subdirectory for the Probabilitiy name #
    if not os.path.isdir(OutputDir+"/"+P_name):
      os.mkdir(OutputDir+"/"+P_name)
    c1=ROOT.TCanvas('c1','test',200,10,600,600)
    if "int" in D_name or "CP" in D_name and not "bkg" in D_name:
      DP=ROOT.TH1F(P_name,P_name,100,-1,1)
      SM=ROOT.TH1F("SM","SM",100,-1,1)
    if "Z2Mass" in D_name or "Z1Mass" in D_name:
      DP=ROOT.TH1F(P_name,P_name,100,0,120)
      SM=ROOT.TH1F("SM","SM",100,0,120)
    else:
      DP=ROOT.TH1F(P_name,P_name,100,0,1)
      SM=ROOT.TH1F("SM","SM",100,-1,1)
    Discriminants = tree2array(tree=t1,branches=[D_name]).astype(float)
    Probability = tree2array(tree=t1,branches=[P_name]).astype(float)
    ProbabilitySM = tree2array(tree=t1,branches=["p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen"]).astype(float)
    for i in range(len(Discriminants)):
      if D_bkg[i] > 0 and Discriminants[i] != -999:
        #print(Discriminants[i],Probability[i])
        DP.Fill(Discriminants[i],Probability[i])
        SM.Fill(Discriminants[i],ProbabilitySM[i])
    DP.SetStats(False)
    DP.GetXaxis().SetTitle(D_name)
    DP.GetXaxis().CenterTitle()
    DP.SetMarkerStyle(1)
    DP.SetMarkerColor(1)
    DP.SetLineColor(1)
    DP.Scale(1/DP.Integral(),"width")
    DP.Draw("HIST")
    SM.Scale(1/SM.Integral(),"width")
    SM.SetMarkerStyle(2)
    SM.SetMarkerColor(2)
    SM.SetLineColor(2)
    SM.Draw("Hist Same")
    c1.SaveAs(OutputDir+"/"+P_name+"/"+D_name+".png")