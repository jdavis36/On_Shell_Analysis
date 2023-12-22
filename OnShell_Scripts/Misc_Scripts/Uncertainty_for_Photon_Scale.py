import ROOT
import numpy as np 
from AnalysisTools.Utils.OnShell_Category import Tag_Untagged_and_gammaH
from AnalysisTools.Utils.Calc_Weight import Calc_Tree_Weight_2021_gammaH
from root_numpy import array2tree, tree2array

# Test this on Zy and yy samples
Zy_Sample_Path = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/Tagged_Signal_Trees/200205_CutBased/gammaH125_0MZy/ZZ4lAnalysis.root"
yy_Sample_Path = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/Tagged_Signal_Trees/200205_CutBased/gammaH125_0Myy/ZZ4lAnalysis.root"

Zy_Sample = ROOT.TFile(Zy_Sample_Path,"read")
yy_Sample = ROOT.TFile(yy_Sample_Path,"read")

Zy_Tree = Zy_Sample.Get("eventTree")
yy_Tree = yy_Sample.Get("eventTree")

Weights_Per_Event_Zy = Calc_Tree_Weight_2021_gammaH(Zy_Tree,"gammaH_2017",True,Zy_Sample_Path)
Weights_Per_Event_yy = Calc_Tree_Weight_2021_gammaH(Zy_Tree,"gammaH_2017",True,Zy_Sample_Path)

# This will return a rescaled Pt branch #
def PtEtaPhiMFourVec(Pt,Eta,Phi,Mass):
    TVec = ROOT.Math.PtEtaPhiMVector(Pt,Eta,Phi,Mass)
    return TVec
def Rescale_Pt_Distribution_Photons(Tree,ScaleName):
    PhotonEnergyPostCorrAll = tree2array(tree=Tree,branches="PhotonEnergyPostCorr") 
    PhiArrayAll = tree2array(tree=Tree,branches="PhotonPhi")
    EtaArrayAll = tree2array(tree=Tree,branches="PhotonEta")
    PtArrayAll = tree2array(tree=Tree,branches="PhotonPt")
    PassIDAll = tree2array(tree=Tree,branches="PhotonIsCutBasedLooseID")
    if ScaleName == "ScaleUp":
        EnergyScale = tree2array(tree=Tree,branches="PhotonScale_Total_Up")
    elif ScaleName == "ScaleDown":
        EnergyScale = tree2array(tree=Tree,branches="PhotonScale_Total_Down")
    elif ScaleName == "SigmaUp":
        EnergyScale = tree2array(tree=Tree,branches="PhotonSigma_Total_Up")
    elif ScaleName == "SigmaDown":
        EnergyScale = tree2array(tree=Tree,branches="PhotonSigma_Total_Down")
    elif ScaleName == "NoScale":
        EnergyScale = 1 
    else:
        raise ValueError("Please Choose a valid scale")
    
    # Sort the calculated photon Pt, only keeping the highest pt by magnitude #
    PhiArray = [] 
    EtaArray = []
    PtArray = []
    PhotonEnergyPostCorrArray = []
    EnergyScaleArray = []
    CorrectedPt = []
    PassID = [] 
    for i in range(len(PtArrayAll)):
        if not isinstance(EnergyScale,int):
          if len(PtArrayAll[i]) != 0:
              index = np.where(PtArrayAll[i] == max((PtArrayAll[i])))
              PtArray.append(PtArrayAll[i][index])
              EtaArray.append(EtaArrayAll[i][index])
              PhiArray.append(PhiArrayAll[i][index])
              PhotonEnergyPostCorrArray.append(PhotonEnergyPostCorrAll[i][index])
              EnergyScaleArray.append(EnergyScale[i][index])
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
              EnergyScaleArray.append(1)
              PassID.append(PassIDAll[i][index][0])
          else:
              PtArray.append(None)
              EtaArray.append(None)
              PhiArray.append(None)
              PhotonEnergyPostCorrArray.append(None)
              EnergyScaleArray.append(None)
              PassID.append(None)
    for i in range(len(PtArray)):
        if not isinstance(EnergyScale,int):
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
                CorrectedPt.append(CorrectedVec.Pt())
            else:
                CorrectedPt.append(None)
    return CorrectedPt, PassID

Zy_Scale_Up_Pt , Zy_Scale_Up_ID = Rescale_Pt_Distribution_Photons(Zy_Tree,"ScaleUp")
Zy_Scale_Down_Pt, Zy_Scale_Down_ID = Rescale_Pt_Distribution_Photons(Zy_Tree,"ScaleDown")
Zy_Sigma_Up_Pt, Zy_Sigma_Up_ID = Rescale_Pt_Distribution_Photons(Zy_Tree,"SigmaUp")
Zy_Sigma_Down_Pt, Zy_Sigma_Down_ID = Rescale_Pt_Distribution_Photons(Zy_Tree,"SigmaDown")
Zy_Nominal, Zy_Nominal_ID = Rescale_Pt_Distribution_Photons(Zy_Tree,"NoScale")
#for i in range(len(Zy_Nominal)):
#   if Zy_Nominal[i] != None:
#     print(Zy_Nominal[i] - Zy_Scale_Up_Pt[i],Zy_Nominal[i] - Zy_Scale_Down_Pt[i])

c1=ROOT.TCanvas('c1','test',200,10,600,600)
hist_Nominal_Pt = ROOT.TH1F("hist_Nominal_Pt","hist_Nominal_Pt ",20,0,1000)
hist_Scale_Up_Pt =ROOT.TH1F("hist_Scale_Up_Pt","hist_Scale_Up_Pt",20,0,1000)
hist_Scale_Down_Pt= ROOT.TH1F("hist_Scale_Down_Pt","hist_Scale_Down_Pt",20,0,1000)
hist_Sigma_Up_Pt =ROOT.TH1F("hist_Sigma_Up_Pt","hist_Sigma_Up_Pt",20,0,1000)
hist_Sigma_Down_Pt= ROOT.TH1F("hist_Sigma_Down_Pt","hist_Sigma_Down_Pt",20,0,1000)
for i in range(len(Zy_Nominal)):
    if Zy_Nominal[i] != None and Zy_Nominal_ID[i]==True:
        hist_Nominal_Pt.Fill(Zy_Nominal[i],Weights_Per_Event_Zy[i])
for i in range(len(Zy_Scale_Up_Pt)):
    if Zy_Scale_Up_Pt[i] != None and Zy_Nominal_ID[i]==True:
        hist_Scale_Up_Pt.Fill(Zy_Scale_Up_Pt[i],Weights_Per_Event_Zy[i])
for i in range(len(Zy_Scale_Down_Pt)):
    if Zy_Scale_Down_Pt[i] != None and Zy_Nominal_ID[i]==True:
        hist_Scale_Down_Pt.Fill(Zy_Scale_Down_Pt[i],Weights_Per_Event_Zy[i])
for i in range(len(Zy_Sigma_Up_Pt)):
    if Zy_Sigma_Up_Pt[i] != None and Zy_Nominal_ID[i]==True:
        hist_Sigma_Up_Pt.Fill(Zy_Sigma_Up_Pt[i],Weights_Per_Event_Zy[i])
for i in range(len(Zy_Sigma_Down_Pt)):
    if Zy_Sigma_Down_Pt[i] != None and Zy_Nominal_ID[i]==True:
        hist_Sigma_Down_Pt.Fill(Zy_Sigma_Down_Pt[i],Weights_Per_Event_Zy[i])

print(hist_Sigma_Down_Pt.GetBinContent(3),hist_Sigma_Up_Pt.GetBinContent(3))
hist_Nominal_Pt.GetXaxis().SetTitle("Nominal vs Scale Up Pt Distribution")
Scale_Up_Ratio = ROOT.TRatioPlot(hist_Nominal_Pt,hist_Scale_Up_Pt)
Scale_Up_Ratio.Draw()
c1.Draw()
c1.SaveAs("RatioPlots/Scale_Up.png")
Scale_Down_Ratio = ROOT.TRatioPlot(hist_Nominal_Pt,hist_Scale_Down_Pt)
Scale_Down_Ratio.Draw()
c1.Draw()
c1.SaveAs("RatioPlots/Scale_Down.png")
Sigma_Up_Ratio = ROOT.TRatioPlot(hist_Nominal_Pt,hist_Sigma_Up_Pt)
Sigma_Up_Ratio.Draw()
c1.Draw()
c1.SaveAs("RatioPlots/Sigma_Up.png")
Sigma_Down_Ratio = ROOT.TRatioPlot(hist_Nominal_Pt,hist_Sigma_Down_Pt)
Sigma_Down_Ratio.Draw()
c1.Draw()
c1.SaveAs("RatioPlots/Sigma_Down.png")


# Calculate Difference in Integrals of Pt Spectrum for All Photons #

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