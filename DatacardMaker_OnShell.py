import os,glob
import sys
import ROOT
import copy
from AnalysisTools.Utils.Addsyst_functions_Onshell import *
from AnalysisTools.data.On_Shell_Systematics.pythia_tune_dict_gammaH_Photons_Decay_Only_Kinematics_Photon_Rate import Return_Tune_Dictionary
from AnalysisTools.data.On_Shell_Systematics.systematics_dict_gammaH_Photons_Decay_Only_Kinematics_Photon_Rate import Return_Systematics_Dictionary,Return_Photon_SF_Scale_Dictionary
# Expected input is a root file with the extension .input.root #
# This script will parse out the histograms in this root file 
# The output we expect is a text file for input into combine 

Input_Dir = sys.argv[1]
output_dir = sys.argv[1]

Systematics_Dictionary = Return_Systematics_Dictionary()
Pythia_Tune_Dictionary = Return_Tune_Dictionary()
Photon_SF_Scale_Dictionary = Return_Photon_SF_Scale_Dictionary()

Add_Systematics = False

Apply_Photon_Scale_Factors = False

def Init_Yield_Change_Dict():
  Change_In_gammaH_Yield_With_SF_applied = {}
  Change_In_gammaH_Yield_With_SF_applied["2016"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2017"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2018"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2016"]["2e2mu"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2017"]["2e2mu"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2018"]["2e2mu"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2016"]["4e"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2017"]["4e"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2018"]["4e"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2016"]["4mu"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2017"]["4mu"] = {}
  Change_In_gammaH_Yield_With_SF_applied["2018"]["4mu"] = {}
  return Change_In_gammaH_Yield_With_SF_applied

def Yield_Change_Pull_Up():
  Yield_Change_Pull_Up = {}
  Yield_Change_Pull_Up["2016"] = {}
  Yield_Change_Pull_Up["2017"] = {}
  Yield_Change_Pull_Up["2018"] = {}
  Yield_Change_Pull_Up["2016"]["2e2mu"] = {}
  Yield_Change_Pull_Up["2017"]["2e2mu"] = {}
  Yield_Change_Pull_Up["2018"]["2e2mu"] = {}
  Yield_Change_Pull_Up["2016"]["4e"] = {}
  Yield_Change_Pull_Up["2017"]["4e"] = {}
  Yield_Change_Pull_Up["2018"]["4e"] = {}
  Yield_Change_Pull_Up["2016"]["4mu"] = {}
  Yield_Change_Pull_Up["2017"]["4mu"] = {}
  Yield_Change_Pull_Up["2018"]["4mu"] = {}
  return Yield_Change_Pull_Up

def Yield_Change_Pull_Down():
  Yield_Change_Pull_Down = {}
  Yield_Change_Pull_Down["2016"] = {}
  Yield_Change_Pull_Down["2017"] = {}
  Yield_Change_Pull_Down["2018"] = {}
  Yield_Change_Pull_Down["2016"]["2e2mu"] = {}
  Yield_Change_Pull_Down["2017"]["2e2mu"] = {}
  Yield_Change_Pull_Down["2018"]["2e2mu"] = {}
  Yield_Change_Pull_Down["2016"]["4e"] = {}
  Yield_Change_Pull_Down["2017"]["4e"] = {}
  Yield_Change_Pull_Down["2018"]["4e"] = {}
  Yield_Change_Pull_Down["2016"]["4mu"] = {}
  Yield_Change_Pull_Down["2017"]["4mu"] = {}
  Yield_Change_Pull_Down["2018"]["4mu"] = {}
  return Yield_Change_Pull_Down

def sort_templates(name):
  if "gammaH" in name.split("/")[-1]:
    return 1
  else:
    return 2

# function to make a somewhat uniform order of output in the datacards
def sort_name(name):
  if "ggH" in name[0]:
    return 1
  elif "qqH" in name[0]:
    return 2
  elif "VH" in name[0]:
    return 3
  elif "ttH" in name[0]:
    return 4
  elif "bbH" in name[0]:
    return 5
  elif "gammaH" in name[0]:
    return 6
  elif "bkg_zjets" in name[0]:
    return 7
  elif "bkg_ggzz" in name[0]:
    return 8
  elif "bkg_qqzz" in name[0]:
    return 9
  elif "bkg_ew" in name[0]:
    return 10


if not os.path.exists(output_dir):
  os.mkdir(output_dir)
List_Of_Input_Root_Trees = []
for filename in glob.iglob(Input_Dir+'/**', recursive=True):
  if os.path.isfile(filename) and ('.root' in filename):
    List_Of_Input_Root_Trees.append(filename)

# Sort so that the gammaH tagged trees are read in first
Sorted_List_Of_Input_Root_Trees = sorted(List_Of_Input_Root_Trees,key = sort_templates)

# Inti the scale factor yield change dictionary 
Change_In_gammaH_Yield_With_SF_applied = Init_Yield_Change_Dict()
Yield_Change_Pull_Up = Yield_Change_Pull_Up()
Yield_Change_Pull_Down = Yield_Change_Pull_Down()


for filename in Sorted_List_Of_Input_Root_Trees:
    #print("Reading in ROOT File: ",filename)
    # Need to extract Final State, Year, and Categorization of each input root file
    # Extracting the Year #
    year = None
    if "2016" in filename:
      year = "2016"
    elif "2017" in filename:
      year = "2017"
    elif "2018" in filename:
      year = "2018"
    else:
      raise ValueError("DataCard Maker did not parse valid year in Input_Root " + filename)
    # Extracting the Final_State #
    final_state = None
    if "2e2mu" in filename:
      final_state = "2e2mu"
    elif "4mu" in filename:
      final_state = "4mu"
    elif "4e" in filename:
      final_state = "4e"
    else:
      raise ValueError("DataCard Maker did not parse valid final state in Input_Root " + filename)
    # Extracting the Category #
    Event_Tag = ""
    if "Untagged" in filename:
      Event_Tag = "Untagged"
    elif "gammaH" in filename:
      Event_Tag = "gammaH"
    else:
      raise ValueError("DataCard Maker did not parse valid Category in Input_Root " + filename)
    nm = filename
    filename_no_path = nm
    if "/" in filename:
      filename_no_path = nm.split("/")[-1]
    # Remove the any potential filepath #
    fin = ROOT.TFile.Open(nm,"UPDATE")
    print("Reading in: ",fin)
    this_key_list = copy.deepcopy(fin.GetListOfKeys())
    # What is done here is now we will scale each histogram by the Photon SF adjustment
    Photon_SF_Dictionary = Return_Photon_SF_Scale_Dictionary()
    for key in this_key_list:
      if "TH1F" in key.GetClassName():
        h_name = key.GetName()
        print("Looking at: ",h_name)
        hist = fin.Get(h_name)
        proc_yield = hist.Integral()
        if Apply_Photon_Scale_Factors:
          if "zjets" not in h_name and "data" not in h_name:
            process = h_name
            if "bkg" not in h_name:
              process = h_name.split("_")[0]
            print("Rescaling: ",process, "File: ",nm)
            gammaH_Yield_Scale_Factor = Return_Yield_Scale_Photon_Scale_Factors_gammaH(year,final_state,process,Photon_SF_Dictionary)
            Prior_Area = hist.Integral()
            if Event_Tag == "gammaH":
              hist.Scale((gammaH_Yield_Scale_Factor))
              Change_In_gammaH_Yield_With_SF_applied[year][final_state][h_name] = hist.Integral() - Prior_Area
              Yield_Change_Pull_Up[year][final_state][h_name] = hist.Integral() *  Return_Yield_ScaleUp_Photon_Scale_Factors_gammaH(year,final_state,process,Photon_SF_Dictionary) - hist.Integral()
              Yield_Change_Pull_Down[year][final_state][h_name] = hist.Integral() *  Return_Yield_ScaleDown_Photon_Scale_Factors_gammaH(year,final_state,process,Photon_SF_Dictionary) - hist.Integral()

            elif Event_Tag == "Untagged":
              # Need to scale the yield to match the change in yield from the gammaH category
              try:
                New_Scale_Factor = 1 - (Change_In_gammaH_Yield_With_SF_applied[year][final_state][h_name]/Prior_Area)
              except:
                New_Scale_Factor = 1 
              hist.Scale(New_Scale_Factor)
            else:
              raise ValueError("Warning: I am not currently sure about how to correctly scale this Event Category with Photon SF")
            Final_Area = hist.Integral()
            #print("Category: ", Event_Tag, " Template Name: ", h_name, " Original Area: ", Prior_Area, " Rescaled Area: ", Final_Area)
        hist.Write("",ROOT.TObject.kOverwrite)

    fin.Close()
    processes      =[]
    rate           =[]
    shapesyst      =[]
    applyshapesyst =[]
    procsyst       =[]
    fin = ROOT.TFile.Open(nm)
    obs = 0
    #print(Yield_Change_Pull_Up)
    for key in fin.GetListOfKeys():
        if "TH1F" in key.GetClassName():
            h_name = key.GetName()
            if "Up" not in h_name and "Down" not in h_name and "data" not in h_name: #Up and Down are for tune up tune down QCD stuff
                  hist = fin.Get(h_name)
                  hrate = hist.Integral()
                  processes.append(h_name)
                  rate.append(hrate)
                  h_temp = fin.Get(h_name)  
            elif "data" not in h_name:
                hnml = h_name.split("_")
                syst_name = hnml[2]
                for iel,el  in enumerate(hnml):
                    if iel> 2: 
                        syst_name = syst_name +"_"+el 
                syst_name = syst_name.replace("Down","")        
                syst_name = syst_name.replace("Up","")        
                syst_name = syst_name.replace("_positive","")        
                syst_name = syst_name.replace("_negative","")
                if syst_name not in applyshapesyst : applyshapesyst.append(syst_name)
                psyst = h_name.replace("Down","")
                psyst = psyst.replace("Up","")
                if psyst not in procsyst : procsyst.append(psyst)
                #print (h_name)
            else :
                hist = fin.Get(h_name)
                hrate = hist.Integral()
                obs = hrate
                #print ("data :",obs)
    print("processes:",processes)
    proc_and_rate = [(processes[i], rate[i]) for i in range(0, len(processes))]
    sorted_proc_and_rate = sorted(proc_and_rate, key=sort_name)
    processes, rate = zip(*sorted_proc_and_rate)

    print("Systematics: ",procsyst)
                
    '''
    
    '''
    
    #Write output datacard
    
    proc = len(processes)
    category = filename_no_path.replace("input.root","onshell.txt")
    chanel = category.replace(".onshell.txt","")
    #print("here",category)
    f = open(output_dir+"/"+category, "w")
    
    f.write("imax 1\n")
    f.write("jmax "+str(proc -1)+"\n")
    f.write("kmax *\n")
    f.write("------------\n")
    f.write("shapes * * $CHANNEL.input.root $PROCESS $PROCESS_$SYSTEMATIC\n")
    f.write("------------\n")
    f.write("bin "+str(chanel)+"\n")
    f.write("observation "+ str(obs)+"\n")
    f.write("------------\n")
    
    line= "bin"
    line_p = "process"
    line_rate = "rate"
    line_indx = "process"
    
    #construct shapy syst lines
    lineSHsyst= []
    for isyst,syst in enumerate(applyshapesyst):
        lineSHsyst.append(syst)
        lineSHsyst[isyst] = lineSHsyst[isyst] + " shape1 "
        for proc in processes :
          pas = False
          for procs in procsyst :
              if syst in procs :
                  if proc+"_"+syst == procs:
                    pas = True
                    break
                  else:
                    pas =  False  
          if pas :
              lineSHsyst[isyst] = lineSHsyst[isyst] + " 1"
          else :     
              lineSHsyst[isyst] = lineSHsyst[isyst] + " -"
    
    scale_syst = []
    
    if Add_Systematics:
      # QCDScales muF #
      addQCDscale_muF_ggH(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      addQCDscale_muF_qqH(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      addQCDscale_muF_VH(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      addQCDscale_muF_ttH(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      addQCDscale_muF_VV(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      # QCDScales muR #
      addQCDscale_muR_ggH(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      addQCDscale_muR_qqH(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      addQCDscale_muR_VH(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      addQCDscale_muR_ttH(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      addQCDscale_muR_VV(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      # EW Corrections #
      addEWcorr_qqZZ(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      # pdf Uncertainties #
      add_pdf_Higgs_gg(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      add_pdf_Higgs_qqbar(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      add_pdf_qqbar(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      add_pdf_As_Higgs_gg(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      add_pdf_As_Higgs_qqbar(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      add_pdf_As_qqbar(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      # Add BR Uncert #
      addhzzbr(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      # Add pythia tune uncertainty #
      add_pythiatune(scale_syst,processes,Pythia_Tune_Dictionary,year,final_state,Event_Tag)
      # Add pythia scale uncertainty #
      add_pythiascale(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      # Add Lumi uncertainty #
      addlumi_Uncorrelated(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      addlumi_Correlated(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)

      # Add the CMS EffE and Effmu #
      if final_state != "4mu":
        addCMS_EFF_e(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      if final_state != "4e":
        addCMS_EFF_mu(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)  
      addZjets(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      #addCMS_EFF_e(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      #addCMS_EFF_mu(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      #addEWcorr_qqZZ(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)

      # Need a more involved way to do the SF uncertainties #

      Return_Yield_Scale_Photon_Scale_Factors_Uncertainty(scale_syst,processes,Photon_SF_Scale_Dictionary,Yield_Change_Pull_Up,Yield_Change_Pull_Down,year,final_state,rate,Event_Tag)
    else:
      addlumi_Uncorrelated(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)
      addhzzbr(scale_syst,processes,Systematics_Dictionary,year,final_state,Event_Tag)

    ibkg = 0 
    for i,procc in enumerate(processes):
        line =line +" "+chanel
        line_p = line_p + " " +procc
        if "bkg_" in procc :
            
            line_indx = line_indx +" "+str(ibkg+1)
            #lineQCDsyst = lineQCDsyst + " 1.1"
            ibkg += 1
        else :
            line_indx = line_indx +" -"+ str(i+1)
            #lineQCDsyst = lineQCDsyst + " -"
        #if ("0PM" in procc[0] ) :
        #print chanell,procc[0]  , procc[1] 
        #if ("bkg" in procc[0] ) :
        #  print chanell,procc[0]  , procc[1] 
        
        line_rate = line_rate+ " "+str(rate[i])
    line = line+"\n"
    line_p = line_p + "\n"
    line_indx = line_indx + "\n"
    line_rate = line_rate+"\n"            
    #lineQCDsyst = lineQCDsyst +"\n"        
    f.write(line)
    f.write(line_p)
    f.write(line_indx)
    f.write(line_rate)
    f.write("------------\n")
    for scalesyst in scale_syst :
        payload = scalesyst+"\n"
        f.write(payload)
    for shapsyst in lineSHsyst :
        payload = shapsyst+"\n"
        f.write(payload)
    
    
    f.close()
    #print "written datacard"
    
