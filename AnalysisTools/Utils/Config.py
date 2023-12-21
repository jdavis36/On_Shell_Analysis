import os

class Analysis_Config:
  def __init__(self,name):
    if name == "OnShell_HVV_Photons_2021": # HVV Couplings and Photons
      self.name = "OnShell_HVV_Photons_2021"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.TaggingProcess = "Tag_AC_19_Scheme_2"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "200205_CutBased"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      # Discriminants and couplings for OnShell Analysis #
      self.Coupling_Name = 'a3'
      self.Hypothesis_List = ['SM','g4','fa30.5-interf']
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay",
                                         "D_0minus_VBF","D_CP_VBF","D_0hplus_VBF","D_int_VBF","D_L1_VBF","D_L1int_VBF","D_L1Zg_VBF","D_L1Zgint_VBF","D_0minus_Zg_VBF","D_CP_Zg_VBF","D_0hplus_Zg_VBF","D_int_Zg_VBF",
                                         "D_0minus_VBFdecay","D_0hplus_VBFdecay","D_L1_VBFdecay","D_L1Zg_VBFdecay","D_0minus_Zg_VBFdecay","D_0hplus_Zg_VBFdecay","D_0minus_gg_VBFdecay", "D_0hplus_gg_VBFdecay",
                                         "D_0minus_HadVHdecay","D_0hplus_HadVHdecay","D_L1_HadVHdecay","D_L1Zg_HadVHdecay","D_0minus_Zg_HadVHdecay","D_0hplus_Zg_HadVHdecay","D_0minus_gg_HadVHdecay", "D_0hplus_gg_HadVHdecay",
                                         "D_0minus_HadVH","D_CP_HadVH","D_0hplus_HadVH","D_int_HadVH","D_L1_HadVH","D_L1int_HadVH","D_L1Zg_HadVH","D_L1Zgint_HadVH","D_0minus_Zg_HadVH", "D_CP_Zg_HadVH","D_0hplus_Zg_HadVH","D_int_Zg_HadVH", "D_0minus_gg_HadVH","D_CP_gg_HadVH","D_0hplus_gg_HadVH","D_int_gg_HadVH",
                                         "D_bkg","D_bkg_VBFdecay","D_bkg_HadVHdecay",
                                         "Pt4l"]
      self.lumi = {'2016':35.9,'2017':41.5,'2018':59.7}
      self.VBF1jTagged_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,1000]}
      self.VBF2jTagged_Discriminants = {"D_bkg_VBFdecay":[0,.33,.66,1],"D_0hplus_VBFdecay":[0,.33,.66,1],"D_0minus_VBFdecay":[0,.33,.66,1],"D_L1_VBFdecay":[0,.33,.66,1],"D_L1Zg_VBFdecay":[0,.33,.66,1],"D_int_VBF":[-1,.33,.66,1],"D_CP_VBF":[0,.33,.66,1]}
      self.VHLeptTagged_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,1000]}
      self.VHHadrTagged_Discriminants = {"D_bkg_HadVHdecay":[0,.33,.66,1],"D_0hplus_HadVHdecay":[0,.33,.66,1],"D_0minus_HadVHdecay":[0,.33,.66,1],"D_L1_HadVHdecay":[0,.33,.66,1],"D_L1Zg_HadVHdecay":[0,.33,.66,1],"D_int_HadVH":[-1,.33,.66,1],"D_CP_HadVH":[0,.33,.66,1]}
      self.ttHLeptTagged_Discriminants = {}
      self.ttHHadrTagged_Discriminants = {}
      self.VHMETTagged_Discriminants = {}
      self.Boosted_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,1000]}
      self.Untagged_Discriminants = {"D_bkg":[0,.33,.66,1],"D_CP_decay":[-1,0,.66,1],"D_0hplus_decay":[0,.33,.66,1],"D_0minus_decay":[0,.33,.66,1],"D_L1_decay":[0,.33,.66,1],"D_L1Zg_decay":[0,.33,.66,1],"D_int_decay":[0,.33,.66,1]}
      # This section should be a list of tags and signal types to use to make cards #
      #self.Production_Modes=["ggH","VBF","Wplus","Wminus","ZH","bbH","ttH","tH"]
      self.Production_Modes=["WplusH","WminusH","bbH","ttH"]
      self.Event_Categories=["Untagged","VBF1jTagged","VBF2jTagged","VHLeptTagged","VHHadrTagged","Boosted"]
      self.Final_States=["4l"]
      self.Years=["2016"]

    if name == "gammaH_Cross_Section_Measurement": # Setup to Measure SM production of Higgs in association with SM 
      self.name = "gammaH_Cross_Section_Measurement"
      self.CMSSW_PATH = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/CMSSW_12_2_0/src"
      self.Work_Dir = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.DoMassFilter = True
      self.TaggingProcess = "Tag_Untagged_and_gammaH"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "200205_CutBased"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      # Use Heshy Optimal Binning #
      self.UseOptimal = {"Untagged":False,"gammaH":False}
      self.PathToPickle = None
      self.Optimal_Discriminants = None # This is a list of the most optimal discriminants
      self.Combine_Production_Mode = "Sum"
      # Discriminants and couplings for OnShell Analysis #
      self.Coupling_Name = 'XS_Measurement'
      self.Hypothesis_List = {"Hypothesis":['g1'],"Options":"None"}
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay",
                                         "D_bkg","D_bkg_kin",
                                         "Pt4l"]
      self.lumi = {'2016':35.9,'2017':41.5,'2018':59.7}
      self.gammaH_Discriminants = {"D_bkg":[0,.2,.5,.7,.85,1]}
      self.Untagged_Discriminants = {"D_bkg":[0,.2,.5,.7,.85,1]}
      self.Production_Modes=["ggH","gammaH"]
      self.Event_Categories=["Untagged","gammaH"]
      self.Final_States=["4e","2e2mu","4mu"]
      self.Years=["2016","2017","2018"]

    if name == "gammaH_Photons_Decay_Only": # HVV Couplings and Photons
      self.name = "gammaH_Photons_Decay_Only"
      self.CMSSW_PATH = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/CMSSW_12_2_0/src"
      self.Work_Dir = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.DoMassFilter = True
      self.TaggingProcess = "Tag_Untagged_and_gammaH"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "200205_CutBased"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      # Use Heshy Optimal Binning #
      self.UseOptimal = {"Untagged":False,"gammaH":False}
      self.PathToPickle = None
      self.Optimal_Discriminants = None # This is a list of the most optimal discriminants
      # Discriminants and couplings for OnShell Analysis #
      self.Coupling_Name = 'a2a3L1'
      self.Hypothesis_List = {"Hypothesis":['g1','g2','g4','g1prime2','ghzgs1prime2','g2gg','g4gg','g2Zg','g4Zg'],"Options":"HZZ_Only"}
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay",
                                         "D_bkg","D_bkg_kin",
                                         "Pt4l"]
      self.lumi = {'2016':35.9,'2017':41.5,'2018':59.7}
      self.gammaH_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,200,300,400,500,600,700,1000]}
      self.Untagged_Discriminants = {"D_bkg":[0,.2,.7,1],"D_CP_decay":[-1,0,1],"D_0hplus_decay":[0,.5,.7,1],"D_0minus_decay":[0,.33,.66,1],"D_L1_decay":[0,.55,.8,1],"D_L1Zg_decay":[0,.4,.55,1],"D_int_decay":[-1,.8,1]}
      # This section should be a list of tags and signal types to use to make cards #
      #self.Production_Modes=["ggH","VBF","Wplus","Wminus","ZH","bbH","ttH"]
      self.Production_Modes=["ggH"]
      self.Event_Categories=["Untagged","gammaH"]
      self.Final_States=["4e","2e2mu","4mu"]
      self.Years=["2016","2017","2018"]

    if name == "gammaH_Photons_Decay_Only_Optimal_Binning": # HVV Couplings and Photons
      self.name = "gammaH_Photons_Decay_Only_Optimal_Binning"
      self.CMSSW_PATH = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/CMSSW_12_2_0/src"
      self.Work_Dir = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.DoMassFilter = True
      self.TaggingProcess = "Tag_Untagged_and_gammaH"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "200205_CutBased"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      # Use Heshy Optimal Binning #
      self.UseOptimal = {"Untagged":True,"gammaH":False}
      self.Optimal_Discriminants_Untagged = {"Path_To_Pickle":"/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/HexUtils/AnalysisTools/Utils/pkl/mergedbins1234prime_6bins_raw.pkl","nbins":20,"D_0hplus_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_0minus_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_L1_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_L1Zg_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1]} # This is a list of the most optimal discriminants
      # Discriminants and couplings for OnShell Analysis #
      #self.Coupling_Name = 'a2a3L1L1Zg'
      self.Coupling_Name = 'a2a3L1'
      self.Hypothesis_List = {"Hypothesis":['g1','g2','g4','g1prime2','ghzgs1prime2',"g2gg","g4gg","g2Zg","g4Zg"],"Options":"SM+AC_Only HZZ_Only"}
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay",
                                         "D_bkg",
                                         "Pt4l"]
      self.lumi = {'2016':35.9,'2017':41.5,'2018':59.7}
      self.gammaH_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,200,300,400,500,600,700,1000]}
      self.Untagged_Discriminants = {"D_bkg":[0,.2,.7,1],"D_CP_decay":[-1,0,1],"D_0hplus_decay":[0,.5,.7,1],"D_0minus_decay":[0,.33,.66,1],"D_L1_decay":[0,.55,.8,1],"D_L1Zg_decay":[0,.4,.55,1],"D_int_decay":[-1,.8,1]}
      # This section should be a list of tags and signal types to use to make cards #
      #self.Production_Modes=["ggH","VBF","Wplus","Wminus","ZH","bbH","ttH"]
      self.Production_Modes=["ggH"]
      self.Event_Categories=["Untagged","gammaH"]
      self.Final_States=["4e","2e2mu","4mu"]
      self.Years=["2016","2017","2018"]

    if name == "gammaH_Photons_Decay_Only_Kinematics": # HVV Couplings and Photons
      self.name = "gammaH_Photons_Decay_Only_Kinematics"
      self.CMSSW_PATH = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/CMSSW_12_2_0/src"
      self.Work_Dir = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.DoMassFilter = True
      self.TaggingProcess = "Tag_Untagged_and_gammaH"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "200205_CutBased"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      self.Combine_Production_Mode = "Average"
      # Use Heshy Optimal Binning #
      self.UseOptimal = {"Untagged":False,"gammaH":False}
      self.Optimal_Discriminants_Untagged = {"Path_To_Pickle":"/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/HexUtils/AnalysisTools/Utils/pkl/mergedbins1234prime_6bins_raw.pkl","nbins":20,"D_0hplus_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_0minus_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_L1_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_L1Zg_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1]} # This is a list of the most optimal discriminants
      # Discriminants and couplings for OnShell Analysis #
      self.Coupling_Name = '8AC_Decay_Only'
      #self.Hypothesis_List = {"Hypothesis":['g1','g2','g4','g1prime2','ghzgs1prime2','g2gg','g4gg','g2Zg','g4Zg'],"Options":"SM+AC_Only"}
      self.Hypothesis_List = {"Hypothesis":['g1','g2','g4','g1prime2','ghzgs1prime2','g2gg','g4gg','g2Zg','g4Zg'],"Options":""}
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay",
                                         "D_bkg",
                                         "Pt4l"]
      self.lumi = {'2016':35.9,'2017':41.5,'2018':59.7}
      self.gammaH_Discriminants = {"D_bkg":[0,.33,.66,1],"Z1Mass":[0,60,85,120],"Z2Mass":[0,20,40,70],"helcosthetaZ1":[-1,-0.8,0.8,1],"helcosthetaZ2":[-1,-0.8,0.8,1],"helphi":[-3.14,-1.57,1.57,3.14]}
      self.Untagged_Discriminants = {"D_bkg":[0,.33,.66,1],"Z1Mass":[0,60,85,120],"Z2Mass":[0,20,40,70],"helcosthetaZ1":[-1,-0.8,0.8,1],"helcosthetaZ2":[-1,-0.8,0.8,1],"helphi":[-3.14,-1.57,1.57,3.14]}
      # This section should be a list of tags and signal types to use to make cards #
      #self.Production_Modes=["ggH","VBF","Wplus","Wminus","ZH","bbH","ttH"]
      self.Production_Modes=["ggH","gammaH"]
      self.Event_Categories=["Untagged","gammaH"]
      self.Final_States=["4e","2e2mu","4mu"]
      self.Years=["2016","2017","2018"]

    if name == "gammaH_Photons_Decay_Only_Kinematics_Photon_Rate": # HVV Couplings and Photons
      self.name = "gammaH_Photons_Decay_Only_Kinematics_Photon_Rate"
      self.CMSSW_PATH = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/CMSSW_12_2_0/src"
      self.Work_Dir = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.DoMassFilter = True
      self.TaggingProcess = "Tag_Untagged_and_gammaH"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "Run2UL_22_apr23"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      self.Do_Shape_Systematics = True
      self.Combine_Production_Mode = "Average"
      # Use Heshy Optimal Binning #
      #self.UseOptimal = {"Untagged":True,"gammaH":True}
      self.UseOptimal = {"Untagged":False,"gammaH":False}
      self.Optimal_Discriminants_Untagged = {"Path_To_Pickle":"/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/AnalysisTools/Utils/pkl/result_1000_0.001_7_0.001_0-_raw.pkl","nbins":20,"Z1Mass":[0, 40.9, 66.8, 81.2, 86.5, 89.4, 91.4, 120.0],"Z2Mass":[0,15.1,21.1,26.1,28.1,31.1,35.4,120],"helcosthetaZ1":[-1,-.774,-.594,-0.334,0.192,0.532,0.828,1.0],"helcosthetaZ2":[-1,-0.648,-0.318,0.208,0.42,0.602,0.77,1.0],"helphi":[-3.142,3.1415927410125732,-2.3624776754995245,-1.3320352851220723,-0.5529203070318034,0.8293804605477058,2.0923007072908026,2.632654643708247,3.142]} # This is a list of the most optimal discriminants
      self.Optimal_Discriminants_gammaH = {"Path_To_Pickle":"/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/AnalysisTools/Utils/pkl/result_1000_10_allwithSM_raw.pkl","nbins":20,"D_0minus_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_0hplus_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_L1_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_L1Zg_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1]}
      # Discriminants and couplings for OnShell Analysis #
      self.Coupling_Name = '8AC_Decay_Only'
      #self.Hypothesis_List = {"Hypothesis":['g1','g2','g4','g1prime2','ghzgs1prime2','g2gg','g4gg','g2Zg','g4Zg'],"Options":"SM+AC_Only"}
      #self.Hypothesis_List = {"Hypothesis":['g1','g2','g4','g1prime2','ghzgs1prime2','g2gg','g4gg','g2Zg','g4Zg'],"Options":"gammaH_XS_Only Decay_Only"}
      self.Hypothesis_List = {"Hypothesis":['g1','g2gg','g4gg','g2Zg','g4Zg'],"Options":"gammaH_XS_Only FixDecaygammaH Photons_Only Prod_Only"}
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay","D_int_gg_decay",
                                         "D_bkg","D_bkg_ResUp","D_bkg_ResDown","D_bkg_ScaleUp","D_bkg_ScaleDown",
                                         "Pt4l"]
      self.lumi = {'2016':20,'2016APV':15.9,'2017':41.5,'2018':59.7}
      #self.gammaH_Discriminants = {"D_bkg":[0,.2,.7,1],"D_CP_decay":[-1,0,1],"D_0minus_decay":[0,.33,.66,1],"D_0hplus_decay":[0,.5,.7,1],"D_L1_decay":[0,.55,.8,1],"D_L1Zg_decay":[0,.4,.55,1]}
      #self.Untagged_Discriminants = {"D_bkg":[0,.2,.7,1],"D_CP_decay":[-1,0,1],"D_0minus_decay":[0,.33,.66,1],"D_0hplus_decay":[0,.5,.7,1],"D_L1_decay":[0,.55,.8,1],"D_L1Zg_decay":[0,.4,.55,1]}
      #self.Untagged_Discriminants = {"D_bkg":[0,0.2,0.7,1],"D_0hplus_decay":[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]}
      #self.gammaH_Discriminants = {"D_bkg":[0,0.2,0.7,1],"D_0hplus_decay":[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]}
      #self.Untagged_Discriminants = {"D_bkg":[0,0.2,0.7,1],"Z1Mass":[0,60,85,120],"Z2Mass":[0,20,40,70],"helcosthetaZ1":[-1,-0.8,0.8,1],"helcosthetaZ2":[-1,-0.8,0.8,1],"helphi":[-3.14,-1.57,1.57,3.14]}
      self.Untagged_Discriminants = {"D_bkg":[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]}
      self.gammaH_Discriminants = {"D_bkg":[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]}
      # This section should be a list of tags and signal types to use to make cards #
      self.Production_Modes=["ggH","VBFH","WplusH","WminusH","ZH","bbH","ttH","gammaH"]
      #self.Production_Modes=["ggH","gammaH"]
      self.Event_Categories=["Untagged","gammaH"]
      #self.Event_Categories=["Untagged"]
      self.Final_States=["4e","2e2mu","4mu"]
      self.Years=["2016","2016APV","2017","2018"]

    if name == "Tree_Level_qqH_Photons_XS": # HVV Couplings and Photons
      self.name = "Tree_Level_qqH_Photons_XS"
      self.CMSSW_PATH = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/CMSSW_12_2_0/src"
      self.Work_Dir = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.DoMassFilter = True
      self.TaggingProcess = "Tag_Untagged_and_qq_gammaH"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "Run2UL_22_apr23"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      self.Combine_Production_Mode = "Average"
      self.Do_Shape_Systematics = False # Shape systematics for the cms res and scale
      # Use Heshy Optimal Binning #
      #self.UseOptimal = {"Untagged":True,"gammaH":True}
      self.UseOptimal = {"Untagged":False,"gammaH":False}
      self.Optimal_Discriminants_Untagged = {"Path_To_Pickle":"/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/AnalysisTools/Utils/pkl/result_1000_0.001_7_0.001_0-_raw.pkl","nbins":20,"Z1Mass":[0, 40.9, 66.8, 81.2, 86.5, 89.4, 91.4, 120.0],"Z2Mass":[0,15.1,21.1,26.1,28.1,31.1,35.4,120],"helcosthetaZ1":[-1,-.774,-.594,-0.334,0.192,0.532,0.828,1.0],"helcosthetaZ2":[-1,-0.648,-0.318,0.208,0.42,0.602,0.77,1.0],"helphi":[-3.142,3.1415927410125732,-2.3624776754995245,-1.3320352851220723,-0.5529203070318034,0.8293804605477058,2.0923007072908026,2.632654643708247,3.142]} # This is a list of the most optimal discriminants
      self.Optimal_Discriminants_gammaH = {"Path_To_Pickle":"/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/AnalysisTools/Utils/pkl/result_1000_10_allwithSM_raw.pkl","nbins":20,"D_0minus_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_0hplus_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_L1_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1],"D_L1Zg_decay":[0,1./6.,2./6.,3/.6,4./6,5./6,1]}
      # Discriminants and couplings for OnShell Analysis #
      self.Coupling_Name = '8AC_Decay_Only'
      #self.Hypothesis_List = {"Hypothesis":['g1','g2','g4','g1prime2','ghzgs1prime2','g2gg','g4gg','g2Zg','g4Zg'],"Options":"SM+AC_Only"}
      #self.Hypothesis_List = {"Hypothesis":['g1','g2','g4','g1prime2','ghzgs1prime2','g2gg','g4gg','g2Zg','g4Zg'],"Options":"gammaH_XS_Only Decay_Only"}
      self.Hypothesis_List = {"Hypothesis":['g1','wCuu','wCdd','wCss','wCcc'],"Options":"qq_gammaH_XS_Only"}
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay","D_int_gg_decay",
                                         "D_bkg","D_bkg_ResUp","D_bkg_ResDown","D_bkg_ScaleUp","D_bkg_ScaleDown",
                                         "Pt4l"]
      self.lumi = {'2016':20,'2016APV':15.9,'2017':41.5,'2018':59.7}
      #self.gammaH_Discriminants = {"D_bkg":[0,.2,.7,1],"D_CP_decay":[-1,0,1],"D_0minus_decay":[0,.33,.66,1],"D_0hplus_decay":[0,.5,.7,1],"D_L1_decay":[0,.55,.8,1],"D_L1Zg_decay":[0,.4,.55,1]}
      #self.Untagged_Discriminants = {"D_bkg":[0,.2,.7,1],"D_CP_decay":[-1,0,1],"D_0minus_decay":[0,.33,.66,1],"D_0hplus_decay":[0,.5,.7,1],"D_L1_decay":[0,.55,.8,1],"D_L1Zg_decay":[0,.4,.55,1]}
      #self.Untagged_Discriminants = {"D_bkg":[0,0.2,0.7,1],"D_0hplus_decay":[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]}
      #self.gammaH_Discriminants = {"D_bkg":[0,0.2,0.7,1],"D_0hplus_decay":[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]}
      #self.Untagged_Discriminants = {"D_bkg":[0,0.2,0.7,1],"Z1Mass":[0,60,85,120],"Z2Mass":[0,20,40,70],"helcosthetaZ1":[-1,-0.8,0.8,1],"helcosthetaZ2":[-1,-0.8,0.8,1],"helphi":[-3.14,-1.57,1.57,3.14]}
      self.Untagged_Discriminants = {"D_bkg":[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]}
      self.gammaH_Discriminants = {"D_bkg":[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]}
      # This section should be a list of tags and signal types to use to make cards #
      self.Production_Modes=["ggH","VBFH","WplusH","WminusH","ZH","bbH","ttH","uuH","ddH","ssH","ccH"]
      #self.Production_Modes=["ggH","gammaH"]
      self.Event_Categories=["Untagged","gammaH"]
      #self.Event_Categories=["Untagged"]
      self.Final_States=["4e","2e2mu","4mu"]
      self.Years=["2016","2016APV","2017","2018"]



    if name == "Test_Optimal_Binning_All_Untagged": # HVV Couplings and Photons
      self.name = "Test_Optimal_Binning_All_Untagged"
      self.CMSSW_PATH = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils/CMSSW_13_3_0/src"
      self.Work_Dir = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/New_Git/HexUtils"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.DoMassFilter = True
      self.TaggingProcess = "Tag_All_Untagged"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "Run2UL_22_apr23"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      self.Do_Shape_Systematics = False
      self.Combine_Production_Mode = "Average"
      # Use Heshy Optimal Binning #
      self.UseOptimal = {"Untagged":False}
      self.Optimal_Discriminants_Untagged = {"Name":"Analytic","nbins":20,"Observables_For_Optimal":["Z1Mass","Z2Mass","helcosthetaZ1","helcosthetaZ2","helphi"]} # This is a list of the most optimal discriminants
      # Discriminants and couplings for OnShell Analysis #
      self.Coupling_Name = '8AC_Decay_Only'
      #self.Hypothesis_List = {"Hypothesis":['g1','g2','g4','g1prime2','ghzgs1prime2',"g2gg","g4gg","g2Zg","g4Zg"],"Options":"SM+AC_Only HZZ_Only"}
      self.Hypothesis_List = {"Hypothesis":['g1','g2',"g2gg","g4gg","g2Zg","g4Zg"],"Options":"SM+AC_Only HZZ_Only"}
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay",
                                         "D_bkg",
                                         "Pt4l"]
      self.lumi = {'2016':35.9,'2017':41.5,'2018':59.7}
      #self.Untagged_Discriminants={"Z1Mass":[0,60,85,120],"Z2Mass":[0,20,40,70],"helcosthetaZ1":[-1,-0.8,0.8,1],"helcosthetaZ2":[-1,-0.8,0.8,1],"helphi":[-3.14,-1.57,1.57,3.14]}
      self.Untagged_Discriminants={"D_bkg":[0,0.33,0.66,1],"Z1Mass":[0,60,85,120],"Z2Mass":[0,20,40,70]}
      # This section should be a list of tags and signal types to use to make cards #
      #self.Production_Modes=["ggH","VBF","Wplus","Wminus","ZH","bbH","ttH"]
      self.Production_Modes=["ggH"]
      self.Event_Categories=["Untagged"]
      self.Final_States=["4e","2e2mu","4mu"]
      self.Years=["2016","2016APV","2017","2018"]