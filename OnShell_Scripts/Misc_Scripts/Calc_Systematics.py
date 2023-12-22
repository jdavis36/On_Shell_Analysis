import ROOT
import sys, os
import numpy as np
from AnalysisTools.Utils import Config
from AnalysisTools.TemplateMaker.Sort_Category import sort_category_systematics
from root_numpy import array2tree, tree2array
from AnalysisTools.Utils.Calc_Weight import Calc_Tree_Weight_2021_gammaH
from AnalysisTools.Utils.OnShell_Category import Tag_Untagged_and_gammaH

# Need a path to all of the datafiles to use #

# Arguments should be a path to the directory with all templates #
outputdir = sys.argv[1]
MakePlots = sys.argv[2]
Input_Trees = sys.argv[3:]

# ======== Load up the analysis configuration ======= # 

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Kinematics_Photon_Rate")
Production_Modes = Analysis_Config.Production_Modes
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

def PtEtaPhiMFourVec(Pt,Eta,Phi,Mass):
    TVec = ROOT.Math.PtEtaPhiMVector(Pt,Eta,Phi,Mass)
    return TVec

def separate_by_year(Input_File):
  Files_By_Year = {"2016":[],"2016APV":[],"2017":[],"2018":[],"Run2":[]}
  with open(Input_File) as f:
    for line in f:
      if "16APV" in line:
        Files_By_Year["2016APV"].append(line)
        Files_By_Year["Run2"].append(line)
      elif "16" in line:
        Files_By_Year["2016"].append(line)
        Files_By_Year["Run2"].append(line)
      elif "17" in line:
        Files_By_Year["2017"].append(line)
        Files_By_Year["Run2"].append(line)
      elif "18" in line:
        Files_By_Year["2018"].append(line)
        Files_By_Year["Run2"].append(line)
      else:
        raise ValueError("DATASET does not correspond to valid year")
  return Files_By_Year

def return_systematics_per_production_mode_year_and_final_state(production_mode,year,final_state):
  print("Return Syst Production Modes", production_mode)
  if any(x in production_mode for x in ["ggH"]):
    #systematics = ["QCDscale_muF_ggH","QCDscale_muR_ggH","pdf_Higgs_gg","CMS_res_"+final_state,"CMS_scale_"+final_state,"CMS_scale_j","hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu","ecal_scale"]
    systematics = ["QCDscale_muF_ggH","QCDscale_muR_ggH","pdf_Higgs_gg","CMS_res_"+final_state,"CMS_scale_"+final_state,"CMS_scale_j","hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu"]
    if year != 2016:
      systematics.append("CMS_pythia_scale")
      systematics.append("pdf_As_Higgs_gg")
      print("Skip")
    template_string = "ggH" 
  elif any(x in production_mode for x in ["VBFH","qqH"]):
    #systematics = ["QCDscale_muF_qqH","QCDscale_muR_qqH","pdf_Higgs_qqbar","CMS_res_"+final_state,"CMS_scale_"+final_state,"CMS_scale_j","hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu","ecal_scale"]
    systematics = ["QCDscale_muF_qqH","QCDscale_muR_qqH","pdf_Higgs_qqbar","CMS_res_"+final_state,"CMS_scale_"+final_state,"CMS_scale_j","hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu"]
    if year != 2016:
      systematics.append("CMS_pythia_scale")
      systematics.append("pdf_As_Higgs_qqbar")
    template_string = "qqH" 
  elif any(x in production_mode for x in ["VH","WplusH","WminusH","ZH"]):
    #systematics = ["QCDscale_muF_VH","QCDscale_muR_VH","pdf_Higgs_qqbar","CMS_res_"+final_state,"CMS_scale_"+final_state,"CMS_scale_j","hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu","ecal_scale"]
    systematics = ["QCDscale_muF_VH","QCDscale_muR_VH","pdf_Higgs_qqbar","CMS_res_"+final_state,"CMS_scale_"+final_state,"CMS_scale_j","hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu"]
    if year != 2016:
      systematics.append("pdf_As_Higgs_qqbar")
    template_string = "VH" 
  elif any(x in production_mode for x in ["ttH"]):
    #systematics = ["QCDscale_muF_ttH","QCDscale_muR_ttH","pdf_Higgs_gg","CMS_res_"+final_state,"CMS_scale_"+final_state,"CMS_scale_j","hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu","ecal_scale"]
    systematics = ["QCDscale_muF_ttH","QCDscale_muR_ttH","pdf_Higgs_gg","CMS_res_"+final_state,"CMS_scale_"+final_state,"CMS_scale_j","hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu"]
    if year != 2016:
      systematics.append("CMS_pythia_scale")
      systematics.append("pdf_As_Higgs_gg")  
    template_string = "ttH" 
  elif any(x in production_mode for x in ["bbH"]):
    #systematics = ["CMS_scale_j","hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu","ecal_scale"]
    systematics = ["CMS_scale_j","hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu"]
    template_string = "bbH" 
  elif any(x in production_mode for x in ["gammaH"]):
    systematics = ["CMS_res_"+final_state,"CMS_scale_"+final_state,"hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu","ecal_scale"]
    #systematics = ["CMS_res_"+final_state,"CMS_scale_"+final_state,"hzz_br","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu"]
    template_string = "gammaH"
  elif any(x in production_mode for x in ["bkg_qqzz","qqZZ"]):
    #systematics = ["QCDscale_muF_VV","QCDscale_muR_VV","EWcorr_qqZZ","pdf_qqbar","pdf_As_qqbar","CMS_scale_j","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu","ecal_scale"]
    systematics = ["QCDscale_muF_VV","QCDscale_muR_VV","EWcorr_qqZZ","pdf_qqbar","pdf_As_qqbar","CMS_scale_j","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu"]
    template_string = "bkg_qqzz" 
  elif any(x in production_mode for x in ["bkg_ggzz","ggZZ"]):
    #systematics = ["QCDscale_muF_ggH","QCDscale_muR_ggH","pdf_Higgs_gg","CMS_scale_j","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu","ecal_scale"]
    systematics = ["QCDscale_muF_ggH","QCDscale_muR_ggH","pdf_Higgs_gg","CMS_scale_j","lumi_13TeV_"+str(year),"CMS_eff_e","CMS_eff_mu"]
    if year != 2016:
      systematics.append("pdf_As_Higgs_gg") 
    template_string = "bkg_ggzz" 
  elif any(x in production_mode for x in ["bkg_zjets","ZX"]):
    #systematics = ["zjet_"+final_state+"_"+year,"ecal_scale"]
    systematics = ["zjet_"+final_state+"_"+year]
    template_string = "bkg_zjets"
  elif any(x in production_mode for x in ["bkg_ew","ew_bkg"]):
    systematics = []      
    template_string = "bkg_ew"
  else:
    raise ValueError ("Did not use valid production mode in return_systematics")
  return template_string, systematics

def Rescale_Weights_QCD_Scale(Tree,Nominal_Event_Weights):
  wsystu = tree2array(tree=Tree,branches="KFactor_QCD_ggZZ_QCDScaleUp")
  wsystdn = tree2array(tree=Tree,branches="KFactor_QCD_ggZZ_QCDScaleDn")
  Nominal_KFactor = tree2array(tree=Tree,branches="KFactor_QCD_ggZZ_Nominal")
  KFactor_Up = [wsystu[i]/Nominal_KFactor[i] for i in range(len(Nominal_KFactor))]
  KFactor_Down = [wsystdn[i]/Nominal_KFactor[i] for i in range(len(Nominal_KFactor))]
  Weights_Up = [KFactor_Up[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down = [KFactor_Down[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  
  return Weights_Up, Weights_Down

def Rescale_Weights_As_Scale_GluGlu(Tree,Nominal_Event_Weights):
  wsystu = tree2array(tree=Tree,branches="KFactor_QCD_ggZZ_AsUp")
  wsystdn = tree2array(tree=Tree,branches="KFactor_QCD_ggZZ_AsDn")
  Nominal_KFactor = tree2array(tree=Tree,branches="KFactor_QCD_ggZZ_Nominal")
  KFactor_Up = [wsystu[i]/Nominal_KFactor[i] for i in range(len(Nominal_Event_Weights))]
  KFactor_Down = [wsystdn[i]/Nominal_KFactor[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Up = [KFactor_Up[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down = [KFactor_Down[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  return Weights_Up, Weights_Down

def Rescale_Weights_Pdf_Scale_GluGlu(Tree,Nominal_Event_Weights):
  wsystu = tree2array(tree=Tree,branches="KFactor_QCD_ggZZ_PDFScaleUp")
  wsystdn = tree2array(tree=Tree,branches="KFactor_QCD_ggZZ_PDFScaleDn")
  Nominal_KFactor = tree2array(tree=Tree,branches="KFactor_QCD_ggZZ_Nominal")
  KFactor_Up = [wsystu[i]/Nominal_KFactor[i] for i in range(len(Nominal_Event_Weights))]
  KFactor_Down = [wsystdn[i]/Nominal_KFactor[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Up = [KFactor_Up[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down = [KFactor_Down[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  return Weights_Up, Weights_Down

def Rescale_Weights_As_Scale_qqbar(Tree,Nominal_Event_Weights):
  wsystu = tree2array(tree=Tree,branches="LHEweight_AsMZ_Up")
  wsystdn = tree2array(tree=Tree,branches="LHEweight_AsMZ_Dn")
  Weights_Up = [wsystu[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down = [wsystdn[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  return Weights_Up, Weights_Down

def Rescale_Weights_Pdf_Scale_qqbar(Tree,Nominal_Event_Weights):
  wsystu = tree2array(tree=Tree,branches="LHEweight_PDFVariation_Up")
  wsystdn = tree2array(tree=Tree,branches="LHEweight_PDFVariation_Dn")
  Weights_Up = [wsystu[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down = [wsystdn[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  return Weights_Up, Weights_Down

def Rescale_Weights_As_Scale_ttH(Tree,Nominal_Event_Weights):
  wsystu = tree2array(tree=Tree,branches="LHEweight_AsMZ_Up")
  wsystdn = tree2array(tree=Tree,branches="LHEweight_AsMZ_Dn")
  Weights_Up = [wsystu[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down = [wsystdn[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  return Weights_Up, Weights_Down

def Rescale_Weights_Pdf_Scale_ttH(Tree,Nominal_Event_Weights):
  wsystu = tree2array(tree=Tree,branches="LHEweight_PDFVariation_Up")
  wsystdn = tree2array(tree=Tree,branches="LHEweight_PDFVariation_Dn")
  Weights_Up = [wsystu[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down = [wsystdn[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  return Weights_Up, Weights_Down

def Rescale_Weights_Pythia_Scale(Tree,Nominal_Event_Weights):
  wpfu = tree2array(tree=Tree,branches="PythiaWeight_fsr_muR4/PythiaWeight_isr_muRoneoversqrt2")
  wpiu = tree2array(tree=Tree,branches="PythiaWeight_isr_muR4/PythiaWeight_isr_muRoneoversqrt2")
  wpfd = tree2array(tree=Tree,branches="PythiaWeight_fsr_muR0p25/PythiaWeight_isr_muRoneoversqrt2")
  wpid = tree2array(tree=Tree,branches="PythiaWeight_isr_muR0p25/PythiaWeight_isr_muRoneoversqrt2")

  wsystu = [wpfu[i]/wpiu[i] for i in range(len(wpfu))]
  wsystdn = [wpfd[i]/wpid[i] for i in range(len(wpfd))]
  
  Weights_Up = [wsystu[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down = [wsystdn[i]*Nominal_Event_Weights[i] for i in range(len(Nominal_Event_Weights))]
  
  return Weights_Up, Weights_Down

def Rescale_Weights_muR_Scale(Tree,Nominal_Event_Weights):
  wsystu = tree2array(tree=Tree,branches="LHEweight_QCDscale_muR2_muF1")
  wsystdn = tree2array(tree=Tree,branches="LHEweight_QCDscale_muR0p5_muF1")
  Weights_Up =  [Nominal_Event_Weights[i]*wsystu[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down =  [Nominal_Event_Weights[i]*wsystdn[i] for i in range(len(Nominal_Event_Weights))]
  return Weights_Up, Weights_Down

def Rescale_Weights_muF_Scale(Tree,Nominal_Event_Weights):
  wsystu = tree2array(tree=Tree,branches="LHEweight_QCDscale_muR1_muF2")
  wsystdn = tree2array(tree=Tree,branches="LHEweight_QCDscale_muR1_muF0p5")
  Weights_Up = [Nominal_Event_Weights[i]*wsystu[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down = [Nominal_Event_Weights[i]*wsystdn[i] for i in range(len(Nominal_Event_Weights))]
  return Weights_Up, Weights_Down

def Rescale_EWcorr(Tree,Nominal_Event_Weights):
  KFactor_unc = tree2array(tree=Tree,branches="KFactor_EW_qqZZ_unc")
  wsystu = [1.0 + KFactor_unc[i] for i in range(len(Nominal_Event_Weights))]
  wsystdn = [1.0 - KFactor_unc[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Up = [Nominal_Event_Weights[i]*wsystu[i] for i in range(len(Nominal_Event_Weights))]
  Weights_Down = [Nominal_Event_Weights[i]*wsystdn[i] for i in range(len(Nominal_Event_Weights))]
  return Weights_Up, Weights_Down

def Return_CMS_Res_Scale():
  return 1

def Return_hzz_br():
  return 1.02

def Return_Lumi_Uncertainty(Year):
  Lumi_Up,Lumi_Down = 0 , 0
  if Year == "2016" or Year == "2016APV":
    Lumi_Up = 1.025
    Lumi_Down = 0.975
  elif Year == "2017":
    Lumi_Up = 1.023
    Lumi_Down = 0.977
  elif Year == "2018":
    Lumi_Up = 1.025
    Lumi_Down = 0.975
  else:
    raise ValueError("Invalid Year for Lumi Systematics")
  return Lumi_Up, Lumi_Down

def Return_CMS_eff_e(year,final_state):
  if year == "2016" or year == "2016APV":
    if final_state == "2e2mu":
      return "1.039/0.975"
    elif final_state == "4e":
      return "1.082/0.914"
  elif year == "2017":
    if final_state == "2e2mu":
      return "1.058/0.939"
    elif final_state == "4e":
      return "1.125/0.862"
  elif year == "2018":
    if final_state == "2e2mu":
      return "1.074"
    elif final_state == "4e":
      return "1.161"      
  else:
    raise ValueError("Invalid Year or final state for eff_e Systematics")
  

def Return_CMS_eff_mu(year,final_state):
  if year == "2016" or year == "2016APV":
    if final_state == "2e2mu":
      return "1.025/0.975"
    elif final_state == "4mu":
      return "1.046/0.953"
  elif year == "2017":
    if final_state == "2e2mu":
      return "1.03/0.968"
    elif final_state == "4mu":
      return "1.056/0.937"
  elif year == "2018":
    if final_state == "2e2mu":
      return "1.011/0.992"
    elif final_state == "4mu":
      return "1.016/0.978"      
  else:
    raise ValueError("Invalid Year or final state for eff_mu Systematics")
  
def Return_zjets(year,final_state):
  zjet_up, zjet_down = 0,0 
  if year == "2016" or year == "2016APV":
    if final_state == "2e2mu":
      zjet_up = 1.152
      zjet_down = 0.868
    elif final_state == "4e":
      zjet_up = 1.314
      zjet_down = 0.728
    elif final_state == "4mu":
      zjet_up = 1.104
      zjet_down = 0.899
  elif year == "2017":
    if final_state == "2e2mu":
      zjet_up = 1.33
      zjet_down = 0.67
    elif final_state == "4e":
      zjet_up = 1.38
      zjet_down = 0.64
    elif final_state == "4mu":
      zjet_up = 1.32
      zjet_down = 0.68
  elif year == "2018":
    if final_state == "2e2mu":
      zjet_up = 1.3
      zjet_down = 0.7
    elif final_state == "4e":
      zjet_up = 1.37
      zjet_down = 0.63
    elif final_state == "4mu":
      zjet_up = 1.24
      zjet_down = 0.76 
  else:
    raise ValueError("Invalid Year or final state for eff_e Systematics")
  return zjet_up, zjet_down

def Rescale_Pt_Distribution_Photons_Arrays_Only(PhotonEnergyPostCorrAll,PhiArrayAll,EtaArrayAll,PtArrayAll,PassIDAll,Scale_Array):
    
    # Sort the calculated photon Pt, only keeping the highest pt by magnitude #
    PhiArray = [] 
    EtaArray = []
    PtArray = []
    PhotonEnergyPostCorrArray = []
    EnergyScaleArray = []
    CorrectedPt = []
    PassID = [] 
    for i in range(len(PtArrayAll)):
        if not isinstance(Scale_Array,int):
          if len(PtArrayAll[i]) != 0:
              PtArray.append(PtArrayAll[i])
              EtaArray.append(EtaArrayAll[i])
              PhiArray.append(PhiArrayAll[i])
              PhotonEnergyPostCorrArray.append(PhotonEnergyPostCorrAll[i])
              EnergyScaleArray.append(Scale_Array[i])
              PassID.append(PassIDAll[i])
          else:
              PtArray.append(None)
              EtaArray.append(None)
              PhiArray.append(None)
              PhotonEnergyPostCorrArray.append(None)
              EnergyScaleArray.append(None)
              PassID.append(None)
        else:
          if len(PtArrayAll[i]) != 0:
              PtArray.append(PtArrayAll[i])
              EtaArray.append(EtaArrayAll[i])
              PhiArray.append(PhiArrayAll[i])
              PhotonEnergyPostCorrArray.append(PhotonEnergyPostCorrAll[i])
              EnergyScaleArray.append(1)
              PassID.append(PassIDAll[i])
          else:
              PtArray.append(None)
              EtaArray.append(None)
              PhiArray.append(None)
              PhotonEnergyPostCorrArray.append(None)
              EnergyScaleArray.append(None)
              PassID.append(None)
    for i in range(len(PtArray)):
        if not isinstance(Scale_Array,int):
            if PtArray[i] is not None:
              Pt_New_Array = [] 
              for j in range(len(PtArray[i])):
                Photon4Vec = PtEtaPhiMFourVec(PtArray[i][j],EtaArray[i][j],PhiArray[i][j],0)
                CorrectedVec = Photon4Vec * PhotonEnergyPostCorrArray[i][j]/Photon4Vec.energy()
                CorrectedVec = Photon4Vec * EnergyScaleArray[i][j]/CorrectedVec.energy()
                Pt_New_Array.append(CorrectedVec.Pt())
              CorrectedPt.append(Pt_New_Array)
            else:
                CorrectedPt.append(None)
        else:
            if PtArray[i] is not None:
              Pt_New_Array = []
              for j in len(range(PtArray[i])):
                Photon4Vec = PtEtaPhiMFourVec(PtArray[i],EtaArray[i],PhiArray[i],0)
                CorrectedVec = Photon4Vec * PhotonEnergyPostCorrArray[i]/Photon4Vec.energy()
                CorrectedPt.append(CorrectedVec.Pt())
            else:
                CorrectedPt.append(None)
    return CorrectedPt, PassID
    

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
              PtArray.append(PtArrayAll[i])
              EtaArray.append(EtaArrayAll[i])
              PhiArray.append(PhiArrayAll[i])
              PhotonEnergyPostCorrArray.append(PhotonEnergyPostCorrAll[i])
              EnergyScaleArray.append(EnergyScale[i])
              PassID.append(PassIDAll[i])
          else:
              PtArray.append(None)
              EtaArray.append(None)
              PhiArray.append(None)
              PhotonEnergyPostCorrArray.append(None)
              EnergyScaleArray.append(None)
              PassID.append(None)
        else:
          if len(PtArrayAll[i]) != 0:
              PtArray.append(PtArrayAll[i])
              EtaArray.append(EtaArrayAll[i])
              PhiArray.append(PhiArrayAll[i])
              PhotonEnergyPostCorrArray.append(PhotonEnergyPostCorrAll[i])
              EnergyScaleArray.append(1)
              PassID.append(PassIDAll[i])
          else:
              PtArray.append(None)
              EtaArray.append(None)
              PhiArray.append(None)
              PhotonEnergyPostCorrArray.append(None)
              EnergyScaleArray.append(None)
              PassID.append(None)
    for i in range(len(PtArray)):
        if not isinstance(EnergyScale,int):
            if PtArray[i] is not None:
              Pt_New_Array = [] 
              for j in range(len(PtArray[i])):
                Photon4Vec = PtEtaPhiMFourVec(PtArray[i][j],EtaArray[i][j],PhiArray[i][j],0)
                CorrectedVec = Photon4Vec * PhotonEnergyPostCorrArray[i][j]/Photon4Vec.energy()
                CorrectedVec = Photon4Vec * EnergyScaleArray[i][j]/CorrectedVec.energy()
                Pt_New_Array.append(CorrectedVec.Pt())
              CorrectedPt.append(Pt_New_Array)
            else:
                CorrectedPt.append(None)
        else:
            if PtArray[i] is not None:
              Pt_New_Array = []
              for j in len(range(PtArray[i])):
                Photon4Vec = PtEtaPhiMFourVec(PtArray[i],EtaArray[i],PhiArray[i],0)
                CorrectedVec = Photon4Vec * PhotonEnergyPostCorrArray[i]/Photon4Vec.energy()
                CorrectedPt.append(CorrectedVec.Pt())
            else:
                CorrectedPt.append(None)
    return CorrectedPt, PassID
    

def Get_gammaH_Categorization_Uncertainty_Ecal_Scale_From_Arrays(Nominal_Event_Weight,Event_Category,Nominal_Tag_List,Final_State,Final_State_List,PhotonEnergyPostCorrAll,PhiArrayAll,EtaArrayAll,PtArrayAll,PassIDAll,ScaleUpArray,ScaleDownArray):
  print("Calculating the Uncertainty")
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
  
  print("Rescaling the Pt Up")
  CorrectedPt, PassID = Rescale_Pt_Distribution_Photons_Arrays_Only(PhotonEnergyPostCorrAll,PhiArrayAll,EtaArrayAll,PtArrayAll,PassIDAll,ScaleUpArray)
  print("Done rescaling the Pt Up")
  Scaled_Tag_List_Up = []
  for i in range(len(Nominal_Tag_List)):
    Scaled_Tag_List_Up.append(Tag_Untagged_and_gammaH(CorrectedPt[i],PassID[i]))

  print("Rescaling the Pt Down")
  CorrectedPt, PassID = Rescale_Pt_Distribution_Photons_Arrays_Only(PhotonEnergyPostCorrAll,PhiArrayAll,EtaArrayAll,PtArrayAll,PassIDAll,ScaleDownArray)
  print("Done rescaling the Pt Down")
  Scaled_Tag_List_Down = []
  for i in range(len(Nominal_Tag_List)):
    Scaled_Tag_List_Down.append(Tag_Untagged_and_gammaH(CorrectedPt[i],PassID[i]))
  
  Sum_Nominal = 0
  Sum_Up = 0
  for i in range(len(Nominal_Event_Weight)):
    if Nominal_Tag_List[i] == Tag and Final_State_List[i] == Final_State_Check:
      Sum_Nominal += Nominal_Event_Weight[i]
  for i in range(len(Nominal_Event_Weight)):
    if Scaled_Tag_List_Up[i] == Tag and Final_State_List[i] == Final_State_Check:
      Sum_Up += Nominal_Event_Weight[i]  
  
  Sum_Nominal = 0
  Sum_Down = 0
  for i in range(len(Nominal_Event_Weight)):
    if Nominal_Tag_List[i] == Tag and Final_State_List[i] == Final_State_Check:
      Sum_Nominal += Nominal_Event_Weight[i]
  for i in range(len(Nominal_Event_Weight)):
    if Scaled_Tag_List_Down[i] == Tag and Final_State_List[i] == Final_State_Check:
      Sum_Down += Nominal_Event_Weight[i]  

  Ratio_Up = Sum_Up/Sum_Nominal
  Ratio_Down = Sum_Down/Sum_Nominal

  return Ratio_Up, Ratio_Down

def Get_gammaH_Categorization_Uncertainty_Ecal_Scale(tree,Nominal_Event_Weight,Event_Category,Nominal_Tag_List,Final_State,Final_State_List):
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

  CorrectedPt, PassID = Rescale_Pt_Distribution_Photons(tree,"ScaleUp")
  Scaled_Tag_List_Up = []
  for i in range(len(Nominal_Tag_List)):
    Scaled_Tag_List_Up.append(Tag_Untagged_and_gammaH(CorrectedPt[i],PassID[i]))
  CorrectedPt, PassID = Rescale_Pt_Distribution_Photons(tree,"ScaleDown")
  Scaled_Tag_List_Down = []
  for i in range(len(Nominal_Tag_List)):
    Scaled_Tag_List_Down.append(Tag_Untagged_and_gammaH(CorrectedPt[i],PassID[i]))
  
  Sum_Nominal = 0
  Sum_Up = 0
  for i in range(len(Nominal_Event_Weight)):
    if Nominal_Tag_List[i] == Tag and Final_State_List[i] == Final_State_Check:
      Sum_Nominal += Nominal_Event_Weight[i]
  for i in range(len(Nominal_Event_Weight)):
    if Scaled_Tag_List_Up[i] == Tag and Final_State_List[i] == Final_State_Check:
      Sum_Up += Nominal_Event_Weight[i]  
  
  Sum_Nominal = 0
  Sum_Down = 0
  for i in range(len(Nominal_Event_Weight)):
    if Nominal_Tag_List[i] == Tag and Final_State_List[i] == Final_State_Check:
      Sum_Nominal += Nominal_Event_Weight[i]
  for i in range(len(Nominal_Event_Weight)):
    if Scaled_Tag_List_Down[i] == Tag and Final_State_List[i] == Final_State_Check:
      Sum_Down += Nominal_Event_Weight[i]  

  Ratio_Up = Sum_Up/Sum_Nominal
  Ratio_Down = Sum_Down/Sum_Nominal

  return Ratio_Up, Ratio_Down

def Compare_Categorization(Nominal_Event_Weight,Alternative_Event_Weight,Event_Category,Tag_List,Final_State,Final_State_List):
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
  #print(Tag,Final_State_Check)
  for i in range(len(Nominal_Event_Weight)):
    if Tag_List[i] == Tag and Final_State_List[i] == Final_State_Check:
      Sum_Nominal += Nominal_Event_Weight[i]
  for i in range(len(Alternative_Event_Weight)):
    if Tag_List[i] == Tag and Final_State_List[i] == Final_State_Check:
      Sum_Alternative += Alternative_Event_Weight[i]  
  
  if Sum_Nominal == 0:
    return 1
  Ratio = Sum_Alternative/Sum_Nominal
  return Ratio

syst_dict=dict()
syst_dict['2016APV'] = dict()
syst_dict['2016'] = dict()
syst_dict['2017'] = dict()
syst_dict['2018'] = dict()
syst_dict['2016APV']['2e2mu'] = dict()
syst_dict['2016APV']['4mu'] = dict()
syst_dict['2016APV']['4e'] = dict()
syst_dict['2016']['2e2mu'] = dict()
syst_dict['2016']['4mu'] = dict()
syst_dict['2016']['4e'] = dict()
syst_dict['2017']['2e2mu'] = dict() 
syst_dict['2017']['4mu'] = dict() 
syst_dict['2017']['4e'] = dict()
syst_dict['2018']['2e2mu'] = dict()
syst_dict['2018']['4mu'] = dict()
syst_dict['2018']['4e'] = dict()

def Fill_Systematic_Dict(tree,fs,Production_Mode,Event_Categories,Nominal_Event_Weight,Tag_List,Final_State_List,syst,year,syst_dict):
          if "QCDScale" in syst:
              QCD_Scale_Up, QCD_Scale_Down = Rescale_Weights_QCD_Scale(tree,Nominal_Event_Weight)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,QCD_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,QCD_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "As" in syst and "_gg" in syst and "ttH" != Production_Mode:
              AS_Scale_Up, AS_Scale_Down = Rescale_Weights_As_Scale_GluGlu(tree,Nominal_Event_Weight)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,AS_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,AS_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "As" in syst and "_gg" in syst and "ttH" == Production_Mode:
              AS_Scale_Up, AS_Scale_Down = Rescale_Weights_As_Scale_ttH(tree,Nominal_Event_Weight)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,AS_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,AS_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "As" in syst and "_qqbar" in syst:
              AS_Scale_Up, AS_Scale_Down = Rescale_Weights_As_Scale_qqbar(tree,Nominal_Event_Weight)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,AS_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,AS_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "pdf" in syst and "_gg" in syst and Production_Mode != "ttH":
              PDF_Scale_Up, PDF_Scale_Down = Rescale_Weights_Pdf_Scale_GluGlu(tree,Nominal_Event_Weight)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,PDF_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,PDF_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "pdf" in syst and "_gg" in syst and Production_Mode == "ttH":
              PDF_Scale_Up, PDF_Scale_Down = Rescale_Weights_Pdf_Scale_ttH(tree,Nominal_Event_Weight)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,PDF_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,PDF_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)            
          elif "pdf" in syst and "_qqbar" in syst:
              PDF_Scale_Up, PDF_Scale_Down = Rescale_Weights_Pdf_Scale_qqbar(tree,Nominal_Event_Weight)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,PDF_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,PDF_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)       
          elif "pythia_scale" in syst:
              Pythia_Scale_Up, Pythia_Scale_Down = Rescale_Weights_Pythia_Scale(tree,Nominal_Event_Weight)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,Pythia_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,Pythia_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)       
          elif "muR" in syst:
              muR_Scale_Up, muR_Scale_Down = Rescale_Weights_muR_Scale(tree,Nominal_Event_Weight)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,muR_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,muR_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)       
          elif "muF" in syst:
              muF_Scale_Up, muF_Scale_Down = Rescale_Weights_muF_Scale(tree,Nominal_Event_Weight)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,muF_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,muF_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "lumi" in syst:
              Plus1_Sigma, Minus1_Sigma = Return_Lumi_Uncertainty(year)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "ecal_scale" in syst:
            for EventTag in Event_Categories:
              Plus1_Sigma, Minus1_Sigma = Get_gammaH_Categorization_Uncertainty_Ecal_Scale(tree,Nominal_Event_Weight,EventTag,Tag_List,fs,Final_State_List)
              if EventTag not in syst_dict[str(year)][fs].keys():
                syst_dict[str(year)][fs][EventTag] = dict()
              if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
              syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "eff_e" in syst:
            for EventTag in Event_Categories:
              if fs == "4mu": continue
              else:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = Return_CMS_eff_e(year,fs)
          elif "eff_mu" in syst:
            for EventTag in Event_Categories:
              if fs == "4e": continue
              else:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = Return_CMS_eff_mu(year,fs) 
          elif "CMS_res" in syst or "CMS_scale" in syst:
            for EventTag in Event_Categories:
              if EventTag not in syst_dict[str(year)][fs].keys():
                syst_dict[str(year)][fs][EventTag] = dict()
              if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
              syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = "1"
          elif "EWcorr_qqZZ" in syst:
            for EventTag in Event_Categories:
              EWcorr_Scale_Up, EWcorr_Scale_Down = Rescale_EWcorr(tree,Nominal_Event_Weight)
              if EventTag not in syst_dict[str(year)][fs].keys():
                syst_dict[str(year)][fs][EventTag] = dict()
              if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
              Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight,EWcorr_Scale_Up,EventTag,Tag_List,fs,Final_State_List)
              Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight,EWcorr_Scale_Down,EventTag,Tag_List,fs,Final_State_List)
              syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "hzz_br" in syst:
            for EventTag in Event_Categories:
              if EventTag not in syst_dict[str(year)][fs].keys():
                syst_dict[str(year)][fs][EventTag] = dict()
              if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()   
              syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Return_hzz_br())
          elif "zjet" in syst:
            for EventTag in Event_Categories:
              zjets_Up, zjets_Down = Return_zjets(year,fs)
              if EventTag not in syst_dict[str(year)][fs].keys():
                syst_dict[str(year)][fs][EventTag] = dict()
              if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()   
              syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(zjets_Up) + "/" +str(zjets_Down)
            
              

#Sorry in advance for making a separate combination method
def Fill_Systematic_Dict_Combined(tree_paths,fs,Production_Mode,Event_Categories,syst,year,syst_dict):
          Nominal_Event_Weight_Comb = []
          Tag_Comb = []
          Final_State_List_Comb = []
          for tree_path in tree_paths:
            f1= ROOT.TFile(tree_path,"read")
            root_tree = f1.Get("eventTree")
            Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_path)
            Tag = tree2array(tree=root_tree,branches="EventTag")
            Final_State_List = tree2array(tree=root_tree, branches="Z1Flav * Z2Flav")
            Nominal_Event_Weight_Comb.extend(Nominal_Event_Weight)
            Tag_Comb.extend(Tag)
            Final_State_List_Comb.extend(Final_State_List)
          if "QCDScale" in syst:
              QCD_Scale_Down_Comb = []
              QCD_Scale_Up_Comb = []
              for tree_path in tree_paths:
                f1= ROOT.TFile(tree,"read")
                root_tree = f1.Get("eventTree")
                Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_path)
                QCD_Scale_Up, QCD_Scale_Down = Rescale_Weights_QCD_Scale(root_tree,Nominal_Event_Weight)
                QCD_Scale_Down_Comb.extend(QCD_Scale_Down)
                QCD_Scale_Up_Comb.extend(QCD_Scale_Up)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,QCD_Scale_Up_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,QCD_Scale_Down_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "As" in syst and "_gg" in syst:
              AS_Scale_Up_Comb = []
              AS_Scale_Down_Comb = []
              for tree_path in tree_paths:
                f1= ROOT.TFile(tree_path,"read")
                root_tree = f1.Get("eventTree")
                Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_path)
                AS_Scale_Up, AS_Scale_Down = Rescale_Weights_As_Scale_GluGlu(root_tree,Nominal_Event_Weight)
                AS_Scale_Down_Comb.extend(AS_Scale_Down)
                AS_Scale_Up_Comb.extend(AS_Scale_Up)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,AS_Scale_Up_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,AS_Scale_Down_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)         
          elif "As" in syst and "_qqbar" in syst:
              AS_Scale_Up_Comb = []
              AS_Scale_Down_Comb = []
              for tree_path in tree_paths:
                f1= ROOT.TFile(tree_path,"read")
                root_tree = f1.Get("eventTree")
                Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_path)
                AS_Scale_Up, AS_Scale_Down = Rescale_Weights_As_Scale_qqbar(root_tree,Nominal_Event_Weight)
                AS_Scale_Down_Comb.extend(AS_Scale_Down)
                AS_Scale_Up_Comb.extend(AS_Scale_Up)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,AS_Scale_Up_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,AS_Scale_Down_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)        
          elif "pdf" in syst and "_gg" in syst:
              PDF_Scale_Up_Comb = []
              PDF_Scale_Down_Comb = []
              for tree_path in tree_paths:
                f1= ROOT.TFile(tree_path,"read")
                root_tree = f1.Get("eventTree")
                Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_path)
                PDF_Scale_Up, PDF_Scale_Down = Rescale_Weights_Pdf_Scale_GluGlu(root_tree,Nominal_Event_Weight)
                PDF_Scale_Down_Comb.extend(PDF_Scale_Down)
                PDF_Scale_Up_Comb.extend(PDF_Scale_Up)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,PDF_Scale_Up_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,PDF_Scale_Down_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "pdf" in syst and "_qqbar" in syst:
              PDF_Scale_Up_Comb = []
              PDF_Scale_Down_Comb = []
              for tree_path in tree_paths:
                f1= ROOT.TFile(tree_path,"read")
                root_tree = f1.Get("eventTree")
                Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_path)
                PDF_Scale_Up, PDF_Scale_Down = Rescale_Weights_Pdf_Scale_qqbar(root_tree,Nominal_Event_Weight)
                PDF_Scale_Down_Comb.extend(PDF_Scale_Down)
                PDF_Scale_Up_Comb.extend(PDF_Scale_Up)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,PDF_Scale_Up_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,PDF_Scale_Down_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "pythia_scale" in syst:
              Pythia_Scale_Up_Comb = []
              Pythia_Scale_Down_Comb = []
              for tree_path in tree_paths:
                f1= ROOT.TFile(tree_path,"read")
                root_tree = f1.Get("eventTree")
                Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_path)
                Pythia_Scale_Up, Pythia_Scale_Down = Rescale_Weights_Pythia_Scale(root_tree,Nominal_Event_Weight)
                Pythia_Scale_Down_Comb.extend(Pythia_Scale_Down)
                Pythia_Scale_Up_Comb.extend(Pythia_Scale_Up)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,Pythia_Scale_Up_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,Pythia_Scale_Down_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "muR" in syst:
              muR_Scale_Up_Comb = []
              muR_Scale_Down_Comb = []
              for tree_path in tree_paths:
                f1= ROOT.TFile(tree_path,"read")
                root_tree = f1.Get("eventTree")
                Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_path)
                muR_Scale_Up, muR_Scale_Down = Rescale_Weights_muR_Scale(root_tree,Nominal_Event_Weight)
                muR_Scale_Down_Comb.extend(muR_Scale_Down)
                muR_Scale_Up_Comb.extend(muR_Scale_Up)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,muR_Scale_Up_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,muR_Scale_Down_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "muF" in syst:
              muF_Scale_Up_Comb = []
              muF_Scale_Down_Comb = []
              for tree_path in tree_paths:
                f1= ROOT.TFile(tree_path,"read")
                root_tree = f1.Get("eventTree")
                Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_path)
                muF_Scale_Up, muF_Scale_Down = Rescale_Weights_muF_Scale(root_tree,Nominal_Event_Weight)
                muF_Scale_Down_Comb.extend(muF_Scale_Down)
                muF_Scale_Up_Comb.extend(muF_Scale_Up)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                Plus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,muF_Scale_Up_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                Minus1_Sigma = Compare_Categorization(Nominal_Event_Weight_Comb,muF_Scale_Down_Comb,EventTag,Tag_Comb,fs,Final_State_List_Comb)
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "lumi" in syst:
              Plus1_Sigma, Minus1_Sigma = Return_Lumi_Uncertainty(year)
              for EventTag in Event_Categories:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "ecal_scale" in syst:   
            for EventTag in Event_Categories:
                Nominal_Event_Weight_Comb = []
                Nominal_Tag_List_Comb = []
                Final_State_List_Comb = []
                PhotonEnergyPostCorrAll = []
                PhiArrayAll = []
                EtaArrayAll = [] 
                PtArrayAll = [] 
                PassIDAll = [] 
                EnergyScaleUp = []
                EnergyScaleDown = []
                for tree_path in tree_paths:
                    f1= ROOT.TFile(tree_path,"read")
                    root_tree = f1.Get("eventTree")
                    Nominal_Tag_List_Comb = np.concatenate((Nominal_Tag_List_Comb, tree2array(tree=root_tree,branches="EventTag")), axis=None) 
                    Final_State_List_Comb = np.concatenate((Final_State_List_Comb,tree2array(tree=root_tree, branches="Z1Flav * Z2Flav")), axis=None)
                    PhotonEnergyPostCorrAll =  np.concatenate((PhotonEnergyPostCorrAll,tree2array(tree=root_tree,branches="PhotonEnergyPostCorr")), axis=None) 
                    PhiArrayAll = np.concatenate((PhiArrayAll,tree2array(tree=root_tree,branches="PhotonPhi")), axis=None) 
                    EtaArrayAll = np.concatenate((EtaArrayAll,tree2array(tree=root_tree,branches="PhotonEta")), axis=None) 
                    PtArrayAll = np.concatenate((PtArrayAll,tree2array(tree=root_tree,branches="PhotonPt")), axis=None) 
                    PassIDAll = np.concatenate((PassIDAll,tree2array(tree=root_tree,branches="PhotonIsCutBasedLooseID")), axis=None) 
                    EnergyScaleUp = np.concatenate((EnergyScaleUp,tree2array(tree=root_tree,branches="PhotonScale_Total_Up")), axis=None) 
                    EnergyScaleDown = np.concatenate((EnergyScaleDown,tree2array(tree=root_tree,branches="PhotonScale_Total_Down")), axis=None) 
                    Nominal_Event_Weight_Comb = np.concatenate((Nominal_Event_Weight_Comb,Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_path)), axis=None)
                print("Calculting Ecal Scales Now. Final State: ",fs,"EventTag: ",EventTag)     
                Plus1_Sigma, Minus1_Sigma = Get_gammaH_Categorization_Uncertainty_Ecal_Scale_From_Arrays(Nominal_Event_Weight_Comb,EventTag,Nominal_Tag_List_Comb,fs,Final_State_List_Comb,PhotonEnergyPostCorrAll,PhiArrayAll,EtaArrayAll,PtArrayAll,PassIDAll,EnergyScaleUp,EnergyScaleDown)
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Plus1_Sigma) + "/" + str(Minus1_Sigma)
          elif "eff_e" in syst:
            for EventTag in Event_Categories:
              if fs == "4mu": continue
              else:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = Return_CMS_eff_e(year,fs)
          elif "eff_mu" in syst:
            for EventTag in Event_Categories:
              if fs == "4e": continue
              else:
                if EventTag not in syst_dict[str(year)][fs].keys():
                  syst_dict[str(year)][fs][EventTag] = dict()
                if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                  syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
                syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = Return_CMS_eff_mu(year,fs) 
          elif "CMS_res" in syst or "CMS_scale" in syst:
            for EventTag in Event_Categories:
              if EventTag not in syst_dict[str(year)][fs].keys():
                syst_dict[str(year)][fs][EventTag] = dict()
              if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()
              syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = "1"
          elif "hzz_br" in syst:
            for EventTag in Event_Categories:
             if EventTag not in syst_dict[str(year)][fs].keys():
               syst_dict[str(year)][fs][EventTag] = dict()
             if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
               syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()   
             syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(Return_hzz_br())
          elif "zjets" in syst:
            for EventTag in Event_Categories:
              zjets_Up, zjets_Down = Return_zjets(year,final_state)
              if EventTag not in syst_dict[str(year)][fs].keys():
                syst_dict[str(year)][fs][EventTag] = dict()
              if Production_Mode not in syst_dict[str(year)][fs][EventTag].keys():
                syst_dict[str(year)][fs][EventTag][Production_Mode] = dict()   
              syst_dict[str(year)][fs][EventTag][Production_Mode][syst] = str(zjets_Up) + "/" +str(zjets_Down)

for fin in Input_Trees:

  treelist = []

  with open(fin) as f:
    llist = [line.rstrip() for line in f]
        
  for line in llist:
    if os.path.exists(line): 
      treelist.append(line)

  yeardict = {}
  for numfile in range(0,len(treelist)):
    filename = treelist[numfile]
    ind = filename.split("/").index(Analysis_Config.TreeFile) # ex 200205_CutBased set in Config #
    year = filename.split("/")[ind:][1]
    ## Allow for strings in the year##
    if "16APV" in year:
      year = "2016APV"
    elif "16" in year:
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

  if "SIGNAL" in fin.upper():
    for year in Years:
      for fs in Final_States:
        if year in yeardict.keys():
          for prod_mode in yeardict[year].keys():
            template_string, syst_list = return_systematics_per_production_mode_year_and_final_state(prod_mode,year,fs)
            tree_paths = yeardict[year][prod_mode][0]
            if len(tree_paths) == 1:
              f1= ROOT.TFile(tree_paths[0],"read")
              root_tree = f1.Get("eventTree")
              Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_paths[0])
              Tag = tree2array(tree=root_tree,branches="EventTag")
              Final_State_List = tree2array(tree=root_tree, branches="Z1Flav * Z2Flav")
              for syst in syst_list:
                Fill_Systematic_Dict(root_tree,fs,prod_mode,Event_Categories,Nominal_Event_Weight,Tag,Final_State_List,syst,year,syst_dict)
            elif len(tree_paths) > 1:
              for syst in syst_list:
                Fill_Systematic_Dict_Combined(tree_paths,fs,prod_mode,Event_Categories,syst,year,syst_dict)
            else:
              raise ValueError("No tree in tree paths")
  elif "EW_BKG" in fin.upper():
    print("EW background does not have any relevant systematics")
  elif "GG4L_BKG" in fin.upper():
    prod_mode = "bkg_ggzz"
    for year in Years:
      for fs in Final_States:
        if year in yeardict.keys():
          for prod_mode in yeardict[year].keys():
            template_string, syst_list = return_systematics_per_production_mode_year_and_final_state(prod_mode,year,fs)
            tree_paths = yeardict[year][prod_mode][0]
            if len(tree_paths) == 1:
              f1= ROOT.TFile(tree_paths[0],"read")
              root_tree = f1.Get("eventTree")
              Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_paths[0])
              Tag = tree2array(tree=root_tree,branches="EventTag")
              Final_State_List = tree2array(tree=root_tree, branches="Z1Flav * Z2Flav")
              for syst in syst_list:
                Fill_Systematic_Dict(root_tree,fs,prod_mode,Event_Categories,Nominal_Event_Weight,Tag,Final_State_List,syst,year,syst_dict)
            elif len(tree_paths) > 1:
              for syst in syst_list:
                Fill_Systematic_Dict_Combined(tree_paths,fs,prod_mode,Event_Categories,syst,year,syst_dict)
            else:
              raise ValueError("No tree in tree paths")
  elif "QQ4L_BKG" in fin.upper():
    prod_mode = "bkg_qqzz"
    for year in Years:
      for fs in Final_States:
        if year in yeardict.keys():
          for prod_mode in yeardict[year].keys():
            template_string, syst_list = return_systematics_per_production_mode_year_and_final_state(prod_mode,year,fs)
            tree_paths = yeardict[year][prod_mode][0]
            if len(tree_paths) == 1:
              f1= ROOT.TFile(tree_paths[0],"read")
              root_tree = f1.Get("eventTree")
              Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_paths[0])
              Tag = tree2array(tree=root_tree,branches="EventTag")
              Final_State_List = tree2array(tree=root_tree, branches="Z1Flav * Z2Flav")
              for syst in syst_list:
                Fill_Systematic_Dict(root_tree,fs,prod_mode,Event_Categories,Nominal_Event_Weight,Tag,Final_State_List,syst,year,syst_dict)
            elif len(tree_paths) > 1:
              for syst in syst_list:
                Fill_Systematic_Dict_Combined(tree_paths,fs,prod_mode,Event_Categories,syst,year,syst_dict)
            else:
              raise ValueError("No tree in tree paths")
  elif "ZX" in fin.upper():
    prod_mode = "bkg_zjets"
    for year in Years:
      for fs in Final_States:
        if year in yeardict.keys():
          for prod_mode in yeardict[year].keys():
            template_string, syst_list = return_systematics_per_production_mode_year_and_final_state(prod_mode,year,fs)
            tree_paths = yeardict[year][prod_mode][0]
            if len(tree_paths) == 1:
              f1= ROOT.TFile(tree_paths[0],"read")
              root_tree = f1.Get("eventTree")
              Nominal_Event_Weight = Calc_Tree_Weight_2021_gammaH(root_tree,prod_mode+str(year),True,tree_paths[0])
              Tag = tree2array(tree=root_tree,branches="EventTag")
              Final_State_List = tree2array(tree=root_tree, branches="Z1Flav * Z2Flav")
              for syst in syst_list:
                Fill_Systematic_Dict(root_tree,fs,prod_mode,Event_Categories,Nominal_Event_Weight,Tag,Final_State_List,syst,year,syst_dict)
            elif len(tree_paths) > 1:
              for syst in syst_list:
                Fill_Systematic_Dict_Combined(tree_paths,fs,prod_mode,Event_Categories,syst,year,syst_dict)
            else:
              raise ValueError("No tree in tree paths")
  else:
    raise ValueError("I do not recognize this type of input tree")

print(syst_dict)

### Dump out the dictionary to a file ####
file_systematics_dict = open(outputdir+"/systematics_dict_"+Analysis_Config.name+".py", "w")
file_systematics_dict.write("Systematics_Dictionary = ")
file_systematics_dict.write(str(syst_dict))
file_systematics_dict.close()

if str(MakePlots).upper():
  for year in syst_dict.keys():
    if not os.path.exists(outputdir+"/"+year):
        os.mkdir(outputdir+"/"+year)
    for fs in syst_dict[year].keys():
      if not os.path.exists(outputdir+"/"+year+"/"+fs):
        os.mkdir(outputdir+"/"+year+"/"+fs)
      current_directory_for_plots = outputdir+"/"+year+"/"+fs 
      for syst in syst_dict[year][fs].keys():
        for Category in syst_dict[year][fs][syst].keys(): 
          output_plot = current_directory_for_plots+"syst_"+syst+"_"+Category+".png"