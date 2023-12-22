import ROOT
import numpy as np
from AnalysisTools.TemplateMaker.Sort_Category import sort_category_systematics
from AnalysisTools.Utils.OnShell_Category import Tag_Untagged_and_gammaH
from AnalysisTools.Utils.Calc_Weight import Calc_Tree_Weight_2021_gammaH
from root_numpy import array2tree, tree2array
import sys
import os
from AnalysisTools.Utils import Config as Config


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

# This will return a rescaled Pt branch #
def PtEtaPhiMFourVec(Pt,Eta,Phi,Mass):
    TVec = ROOT.Math.PtEtaPhiMVector(Pt,Eta,Phi,Mass)
    return TVec
def Rescale_Pt_Distribution_Photons(PhiArrayAll,EtaArrayAll,PtArrayAll,PassIDAll,PhotonEnergyPostCorrAll,EnergyScaleAll):
    
    # Sort the calculated photon Pt, only keeping the highest pt by magnitude #
    PhiArray = [] 
    EtaArray = []
    PtArray = []
    PhotonEnergyPostCorrArray = []
    EnergyScaleArray = []
    CorrectedPt = []
    PassID = []
    for i in range(len(PtArrayAll)):
        if not isinstance(EnergyScaleAll[i],int):
          if len(PtArrayAll[i]) != 0:
              index = np.where(PtArrayAll[i] == max((PtArrayAll[i])))
              PtArray.append(PtArrayAll[i][index])
              EtaArray.append(EtaArrayAll[i][index])
              PhiArray.append(PhiArrayAll[i][index])
              PhotonEnergyPostCorrArray.append(PhotonEnergyPostCorrAll[i][index])
              EnergyScaleArray.append(EnergyScaleAll[i][index])
              PassID.append(PassIDAll[i][index][0])
          else:
              PtArray.append(None)
              EtaArray.append(None)
              PhiArray.append(None)
              PhotonEnergyPostCorrArray.append(None)
              EnergyScaleArray.append(None)
              PassID.append(None)
        else:
          if len(PtArrayAll[i]) != 0:
              index = np.where(PtArrayAll[i] == max((PtArrayAll[i])))
              PtArray.append(PtArrayAll[i][index])
              EtaArray.append(EtaArrayAll[i][index])
              PhiArray.append(PhiArrayAll[i][index])
              PhotonEnergyPostCorrArray.append(PhotonEnergyPostCorrAll[i][index])
              EnergyScaleArray.append(PhotonEnergyPostCorrAll[i][index])
              PassID.append(PassIDAll[i][index][0])
          else:
              PtArray.append(None)
              EtaArray.append(None)
              PhiArray.append(None)
              PhotonEnergyPostCorrArray.append(None)
              EnergyScaleArray.append(None)
              PassID.append(None)
    for i in range(len(PtArray)):
        if not isinstance(EnergyScaleAll[i],int):
            if PtArray[i] != None:
                Photon4Vec = PtEtaPhiMFourVec(PtArray[i],EtaArray[i],PhiArray[i],0)
                CorrectedVec = Photon4Vec * PhotonEnergyPostCorrArray[i]/Photon4Vec.energy()
                CorrectedVec = Photon4Vec * EnergyScaleArray[i]/CorrectedVec.energy()
                CorrectedPt.append(CorrectedVec.Pt())
            else:
                CorrectedPt.append(None)
        else:
            if PtArray[i] != None:
                Photon4Vec = PtEtaPhiMFourVec(PtArray[i],EtaArray[i],PhiArray[i],0)
                CorrectedVec = Photon4Vec * PhotonEnergyPostCorrArray[i]/Photon4Vec.energy()
                CorrectedVec = Photon4Vec * EnergyScaleArray[i]/CorrectedVec.energy()
                CorrectedPt.append(CorrectedVec.Pt())
                #Photon4Vec = PtEtaPhiMFourVec(PtArray[i],EtaArray[i],PhiArray[i],0)
                #CorrectedVec = Photon4Vec * PhotonEnergyPostCorrArray[i]/Photon4Vec.energy()
                #CorrectedPt.append(CorrectedVec.Pt())
                #CorrectedPt.append(Photon4Vec.Pt())
            else:
                CorrectedPt.append(None)
    return CorrectedPt, PassID

Nominal_Event_Weight_Comb = []
Photon_Pt_Comb = [] 
Photon_Phi_Comb = [] 
Photon_Eta_Comb = []
Pass_ID_Comb = []
ScaleUp_Comb = []
ScaleDown_Comb = []
SigmaUp_Comb = []
SigmaDown_Comb = []
PhotonEnergyPostCorrAll_Comb = []
for year in Years:
  if year in yeardict.keys():
    for prod_mode in yeardict[year]:
        tree_paths = yeardict[year][prod_mode][0]
        for tree in tree_paths:
            f1= ROOT.TFile(tree,"read")
            root_tree = f1.Get("eventTree")
            Nominal_Event_Weight_Comb.extend(Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree))
            Photon_Pt_Comb.extend(tree2array(tree=root_tree,branches="PhotonPt"))
            Photon_Phi_Comb.extend(tree2array(tree=root_tree,branches="PhotonPhi"))
            Photon_Eta_Comb.extend(tree2array(tree=root_tree,branches="PhotonEta"))
            Pass_ID_Comb.extend(tree2array(tree=root_tree,branches="PhotonIsCutBasedLooseID"))
            ScaleUp_Comb.extend(tree2array(tree=root_tree,branches="PhotonScale_Total_Up"))
            ScaleDown_Comb.extend(tree2array(tree=root_tree,branches="PhotonScale_Total_Down"))
            SigmaUp_Comb.extend(tree2array(tree=root_tree,branches="PhotonSigma_Total_Up"))
            SigmaDown_Comb.extend(tree2array(tree=root_tree,branches="PhotonSigma_Total_Down"))
            PhotonEnergyPostCorrAll_Comb.extend(tree2array(tree=root_tree,branches="PhotonEnergyPostCorr")) 
    
    print(ScaleUp_Comb[0:5])
    print(ScaleDown_Comb[0:5])
    print(SigmaUp_Comb[0:5])
    print(SigmaDown_Comb[0:5])
    print(PhotonEnergyPostCorrAll_Comb[0:5])
# Now we need to calculate the scale up and scale down for the combined list of samples we recieved 
    Scale_Up_Pt , Scale_Up_ID = Rescale_Pt_Distribution_Photons(Photon_Phi_Comb,Photon_Eta_Comb,Photon_Pt_Comb,Pass_ID_Comb,PhotonEnergyPostCorrAll_Comb,ScaleUp_Comb)
    Scale_Down_Pt, Scale_Down_ID = Rescale_Pt_Distribution_Photons(Photon_Phi_Comb,Photon_Eta_Comb,Photon_Pt_Comb,Pass_ID_Comb,PhotonEnergyPostCorrAll_Comb,ScaleDown_Comb)
    Sigma_Up_Pt, Sigma_Up_ID = Rescale_Pt_Distribution_Photons(Photon_Phi_Comb,Photon_Eta_Comb,Photon_Pt_Comb,Pass_ID_Comb,PhotonEnergyPostCorrAll_Comb,SigmaUp_Comb)
    Sigma_Down_Pt, Sigma_Down_ID = Rescale_Pt_Distribution_Photons(Photon_Phi_Comb,Photon_Eta_Comb,Photon_Pt_Comb,Pass_ID_Comb,PhotonEnergyPostCorrAll_Comb,SigmaDown_Comb)
    Nominal, Nominal_ID = Rescale_Pt_Distribution_Photons(Photon_Phi_Comb,Photon_Eta_Comb,Photon_Pt_Comb,Pass_ID_Comb,PhotonEnergyPostCorrAll_Comb,[1] * len(Nominal_Event_Weight_Comb))


    c1=ROOT.TCanvas('c1','test',200,10,600,600)
    hist_Nominal_Pt = ROOT.TH1F("hist_Nominal_Pt","hist_Nominal_Pt ",20,0,1000)
    hist_Scale_Up_Pt =ROOT.TH1F("hist_Scale_Up_Pt","hist_Scale_Up_Pt",20,0,1000)
    hist_Scale_Down_Pt= ROOT.TH1F("hist_Scale_Down_Pt","hist_Scale_Down_Pt",20,0,1000)
    hist_Sigma_Up_Pt =ROOT.TH1F("hist_Sigma_Up_Pt","hist_Sigma_Up_Pt",20,0,1000)
    hist_Sigma_Down_Pt= ROOT.TH1F("hist_Sigma_Down_Pt","hist_Sigma_Down_Pt",20,0,1000)
    for i in range(len(Nominal)):
        if Nominal[i] != None and Nominal_ID[i]==True:
            hist_Nominal_Pt.Fill(Nominal[i],Nominal_Event_Weight_Comb[i])
    for i in range(len(Scale_Up_Pt)):
        if Scale_Up_Pt[i] != None and Nominal_ID[i]==True:
            hist_Scale_Up_Pt.Fill(Scale_Up_Pt[i],Nominal_Event_Weight_Comb[i])
    for i in range(len(Scale_Down_Pt)):
        if Scale_Down_Pt[i] != None and Nominal_ID[i]==True:
            hist_Scale_Down_Pt.Fill(Scale_Down_Pt[i],Nominal_Event_Weight_Comb[i])
    for i in range(len(Sigma_Up_Pt)):
        if Sigma_Up_Pt[i] != None and Nominal_ID[i]==True:
            hist_Sigma_Up_Pt.Fill(Sigma_Up_Pt[i],Nominal_Event_Weight_Comb[i])
    for i in range(len(Sigma_Down_Pt)):
        if Sigma_Down_Pt[i] != None and Nominal_ID[i]==True:
            hist_Sigma_Down_Pt.Fill(Sigma_Down_Pt[i],Nominal_Event_Weight_Comb[i])
      
    ROOT.g.GetHistogram().SetStats(0)
    hist_Nominal_Pt.GetXaxis().SetTitle("Nominal vs Scale Up Pt Distribution")
    Scale_Up_Ratio = ROOT.TRatioPlot(hist_Nominal_Pt,hist_Scale_Up_Pt)
    Scale_Up_Ratio.Draw()
    c1.Draw()
    c1.SaveAs("RatioPlots/Scale_Up_"+year+".png")
    hist_Nominal_Pt.GetXaxis().SetTitle("Nominal vs Scale Down Pt Distribution")
    Scale_Down_Ratio = ROOT.TRatioPlot(hist_Nominal_Pt,hist_Scale_Down_Pt)
    Scale_Down_Ratio.Draw()
    c1.Draw()
    c1.SaveAs("RatioPlots/Scale_Down_"+year+".png")
    hist_Nominal_Pt.GetXaxis().SetTitle("Nominal vs Resolution Up Pt Distribution")
    Sigma_Up_Ratio = ROOT.TRatioPlot(hist_Nominal_Pt,hist_Sigma_Up_Pt)
    Sigma_Up_Ratio.Draw()
    c1.Draw()
    c1.SaveAs("RatioPlots/Sigma_Up_"+year+".png")
    hist_Nominal_Pt.GetXaxis().SetTitle("Nominal vs Resolution Down Pt Distribution")
    Sigma_Down_Ratio = ROOT.TRatioPlot(hist_Nominal_Pt,hist_Sigma_Down_Pt)
    Sigma_Down_Ratio.Draw()
    c1.Draw()
    c1.SaveAs("RatioPlots/Sigma_Down_"+year+".png")

    print ("+- 1 sigma gammaH Category:")
    print ("Scale Up:", hist_Scale_Up_Pt.Integral(4,20), "Nominal:",hist_Nominal_Pt.Integral(4,20), "Ratio:",hist_Scale_Up_Pt.Integral(4,20)/hist_Nominal_Pt.Integral(4,20))
    print ("Scale Down:", hist_Scale_Down_Pt.Integral(4,20), "Nominal:",hist_Nominal_Pt.Integral(4,20), "Ratio:",hist_Scale_Down_Pt.Integral(4,20)/hist_Nominal_Pt.Integral(4,20))

    print ("+- 1 sigma Untagged Category:")
    print ("Scale Up:", hist_Scale_Up_Pt.Integral(0,3), "Nominal:",hist_Nominal_Pt.Integral(0,3), "Ratio:",hist_Scale_Up_Pt.Integral(0,3)/hist_Nominal_Pt.Integral(0,3))
    print ("Scale Down:", hist_Scale_Down_Pt.Integral(0,3), "Nominal:",hist_Nominal_Pt.Integral(0,3), "Ratio:",hist_Scale_Down_Pt.Integral(0,3)/hist_Nominal_Pt.Integral(0,3))

    print ("+- 1 sigma gammaH Category:")
    print ("Sigma Up:", hist_Sigma_Up_Pt.Integral(4,20), "Nominal:",hist_Nominal_Pt.Integral(4,20), "Ratio:",hist_Sigma_Up_Pt.Integral(4,20)/hist_Nominal_Pt.Integral(4,20))
    print ("Sigma Down:", hist_Sigma_Down_Pt.Integral(4,20), "Nominal:",hist_Nominal_Pt.Integral(4,20), "Ratio:",hist_Sigma_Down_Pt.Integral(4,20)/hist_Nominal_Pt.Integral(4,20))

    print ("+- 1 sigma Untagged Category:")
    print ("Sigma Up:", hist_Sigma_Up_Pt.Integral(0,3), "Nominal:",hist_Nominal_Pt.Integral(0,3), "Ratio:",hist_Sigma_Up_Pt.Integral(0,3)/hist_Nominal_Pt.Integral(0,3))
    print ("Sigma Down:", hist_Sigma_Down_Pt.Integral(0,3), "Nominal:",hist_Nominal_Pt.Integral(0,3), "Ratio:",hist_Sigma_Down_Pt.Integral(0,3)/hist_Nominal_Pt.Integral(0,3))