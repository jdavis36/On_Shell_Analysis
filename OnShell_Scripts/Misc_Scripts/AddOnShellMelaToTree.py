import os
import sys
from AnalysisTools.Utils import Config as Config

# Arguments should be a path to the directory with all templates #

outputdir = sys.argv[1]
# Input is the txt files that list the path to the processed trees #
Input_Trees = sys.argv[2]
MELA_Probabilities = sys.argv[3] # Separate the MELAProbabilities into Decay and Production Probabilities 
DecayOrProd = sys.argv[4]
# Load up the analysis configuration #

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Optimal_Binning")
#Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only")

def Get_Native_Prob(File_Name):
  Native_Prob_Dictionary_Decay= {"ggH":{"SM":"p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen",
                                 "0PH":"p_Gen_GG_SIG_ghg2_1_ghz2_1p65684_JHUGen",
                                 "0M":"p_Gen_GG_SIG_ghg2_1_ghz4_2p55052_JHUGen",
                                 "0L1":"p_Gen_GG_SIG_ghg2_1_ghz1prime2_n1p210042E4_JHUGen",
                                 "0L1Zg":"p_Gen_GG_SIG_ghg2_1_ghza1prime2_n7p613351E4_JHUGen",
                                 "0PHf05ph0":"p_Gen_GG_SIG_ghg2_1_ghz1_1_ghz2_1p65684_JHUGen",
                                 "0Mf05ph0":"p_Gen_GG_SIG_ghg2_1_ghz1_1_ghz4_2p55052_JHUGen",
                                 "0L1f05ph0":"p_Gen_GG_SIG_ghg2_1_ghz1_1_ghz1prime2_n1p210042E4_JHUGen",
                                 "0L1Zgf05ph0":"p_Gen_GG_SIG_ghg2_1_ghz1_1_ghza1prime2_n7p613351E4_JHUGen"},
                                 "gammaH":{"0PHZy":"p_Gen_Dec_SIG_ghza2_0p0477547_JHUGen",
                                           "0PHyy":"p_Gen_Dec_SIG_gha2_0p0530640_JHUGen",
                                           "0MZy":"p_Gen_Dec_SIG_ghza4_0p0529487_JHUGen",
                                           "0Myy":"p_Gen_Dec_SIG_gha2_0p0536022_JHUGen",
                                           "0PHZyf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghza2_0p0477547_JHUGen",
                                           "0PHyyf05ph0":"p_Gen_Dec_SIG_ghz1_1_gha2_0p0530640_JHUGen",
                                           "0MZyf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghza4_0p0529487_JHUGen",
                                           "0Myyf05ph0":"p_Gen_Dec_SIG_ghz1_1_gha4_0p0526022_JHUGen"},
                                  "VBFH":{"SM":"p_Gen_Dec_SIG_ghz1_1_JHUGen",
                                          "0PH":"p_Gen_Dec_SIG_ghz2_0p27196_JHUGen",
                                          "0M":"p_Gen_Dec_SIG_ghz4_0p297979_JHUGen",
                                          "0L1":"p_Gen_Dec_SIG_ghz1prime2_n0p21582E4_JHUGen",
                                          "0L1Zg":"p_Gen_Dec_SIG_ghza1prime2_n0p4091E4_JHUGen",
                                          "0PHf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz2_0p27196_JHUGen",
                                          "0Mf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz4_0p297979_JHUGen",
                                          "0L1f05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz1prime2_n0p21582E4_JHUGen",
                                          "0L1Zgf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghza1prime2_n0p4091E4_JHUGen"},
                                  "WplusH":{"SM":"p_Gen_Dec_SIG_ghz1_1_JHUGen",
                                          "0PH":"p_Gen_Dec_SIG_ghz2_0p112481_JHUGen",
                                          "0M":"p_Gen_Dec_SIG_ghz4_0p1236136_JHUGen",
                                          "0L1":"p_Gen_Dec_SIG_ghz1prime2_n0p0525274E4_JHUGen",
                                          "0PHf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz2_0p112481_JHUGen",
                                          "0Mf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz4_0p1236136_JHUGen",
                                          "0L1f05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz1prime2_n0p0525274E4_JHUGen"},
                                  "WminusH":{"SM":"p_Gen_Dec_SIG_ghz1_1_JHUGen",
                                          "0PH":"p_Gen_Dec_SIG_ghz2_0p112481_JHUGen",
                                          "0M":"p_Gen_Dec_SIG_ghz4_0p1236136_JHUGen",
                                          "0L1":"p_Gen_Dec_SIG_ghz1prime2_n0p0525274E4_JHUGen",
                                          "0PHf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz2_0p112481_JHUGen",
                                          "0Mf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz4_0p1236136_JHUGen",
                                          "0L1f05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz1prime2_n0p0525274E4_JHUGen"},
                                  "ZH":{"SM":"p_Gen_Dec_SIG_ghz1_1_JHUGen",
                                          "0PH":"p_Gen_Dec_SIG_ghz2_0p112481_JHUGen",
                                          "0M":"p_Gen_Dec_SIG_ghz4_0p144057_JHUGen",
                                          "0L1":"p_Gen_Dec_SIG_ghz1prime2_n0p0517788E4_JHUGen",
                                          "0L1Zg":"p_Gen_Dec_SIG_ghza1prime2_n0p06429534E4_JHUGen",
                                          "0PHf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz2_0p112481_JHUGen",
                                          "0Mf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz4_0p144057_JHUGen",
                                          "0L1f05ph0":"p_Gen_Dec_SIG_ghz1_1_ghz1prime2_n0p0517788E4_JHUGen",
                                          "0L1Zgf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghza1prime2_n0p06429534E4_JHUGen"},
                                  "bbH":{"SM":"p_Gen_Dec_SIG_ghz1_1_JHUGen"},
                                  "ttH":{"SM":"p_Gen_Dec_SIG_ghz1_1_JHUGen"},
                                 }
  Native_Prob_Dictionary_Production = {"ggH":{"SM":"",
                                              "0PH":"",
                                              "0M":"",
                                              "0L1":"",
                                              "0L1Zg":"",
                                              "0PHf05ph0":"",
                                              "0Mf05ph0":"",
                                              "0L1f05ph0":"",
                                              "0L1Zgf05ph0":""},
                                 "gammaH":{"0PHZy":"p_Gen_GammaH_SIG_ghza2_0p0477547_JHUGen",
                                           "0PHyy":"p_Gen_GammaH_SIG_gha2_0p0530640_JHUGen",
                                           "0MZy":"p_Gen_GammaH_SIG_ghza4_0p0529487_JHUGen",
                                           "0Myy":"p_Gen_GammaH_SIG_gha4_0p0536022_JHUGen",
                                           "0PHZyf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghza2_0p0477547_JHUGen",
                                           "0PHyyf05ph0":"p_Gen_Dec_SIG_ghz1_1_gha2_0p0530640_JHUGen",
                                           "0MZyf05ph0":"p_Gen_Dec_SIG_ghz1_1_ghza4_0p0529487_JHUGen",
                                           "0Myyf05ph0":"p_Gen_Dec_SIG_ghz1_1_gha4_0p0526022_JHUGen"},
                                  "VBFH":{"SM":"p_Gen_VBF_SIG_ghv1_1_JHUGen",
                                          "0PH":"p_Gen_VBF_SIG_ghv2_0p27196_JHUGen",
                                          "0M":"p_Gen_VBF_SIG_ghv4_0p297979_JHUGen",
                                          "0L1":"p_Gen_VBF_SIG_ghv1prime2_n0p21582E4_JHUGen",
                                          "0L1Zg":"p_Gen_VBF_SIG_ghza1prime2_n0p4091E4_JHUGen",
                                          "0PHf05ph0":"p_Gen_VBF_SIG_ghz1_1_ghz2_0p27196_JHUGen",
                                          "0Mf05ph0":"p_Gen_VBF_SIG_ghz1_1_ghz4_0p297979_JHUGen",
                                          "0L1f05ph0":"p_Gen_VBF_SIG_ghz1_1_ghz1prime2_n0p21582E4_JHUGen",
                                          "0L1Zgf05ph0":"p_Gen_VBF_SIG_ghz1_1_ghza1prime2_n0p4091E4_JHUGen"},
                                  "WplusH":{"SM":"p_Gen_WH_SIG_ghz1_1_JHUGen",
                                          "0PH":"p_Gen_WH_SIG_ghz2_0p112481_JHUGen",
                                          "0M":"p_Gen_WH_SIG_ghz4_0p1236136_JHUGen",
                                          "0L1":"p_Gen_WH_SIG_ghz1prime2_n0p0525274E4_JHUGen",
                                          "0PHf05ph0":"p_Gen_WH_SIG_ghz1_1_ghz2_0p112481_JHUGen",
                                          "0Mf05ph0":"p_Gen_WH_SIG_ghz1_1_ghz4_0p1236136_JHUGen",
                                          "0L1f05ph0":"p_Gen_WH_SIG_ghz1_1_ghz1prime2_n0p0525274E4_JHUGen"},
                                  "WminusH":{"SM":"p_WH_SIG_ghz1_1_JHUGen",
                                          "0PH":"p_Gen_WH_SIG_ghz2_0p112481_JHUGen",
                                          "0M":"p_Gen_WH_SIG_ghz4_0p1236136_JHUGen",
                                          "0L1":"p_Gen_WH_SIG_ghz1prime2_n0p0525274E4_JHUGen",
                                          "0PHf05ph0":"p_Gen_WH_SIG_ghz1_1_ghz2_0p112481_JHUGen",
                                          "0Mf05ph0":"p_Gen_WH_SIG_ghz1_1_ghz4_0p1236136_JHUGen",
                                          "0L1f05ph0":"p_Gen_WH_SIG_ghz1_1_ghz1prime2_n0p0525274E4_JHUGen"},
                                  "ZH":{"SM":"p_Gen_Dec_SIG_ghz1_1_JHUGen",
                                          "0PH":"p_Gen_ZH_SIG_ghz2_0p112481_JHUGen",
                                          "0M":"p_Gen_ZH_SIG_ghz4_0p144057_JHUGen",
                                          "0L1":"p_Gen_ZH_SIG_ghz1prime2_n0p0517788E4_JHUGen",
                                          "0L1Zg":"p_Gen_ZH_SIG_ghza1prime2_n0p06429534E4_JHUGen",
                                          "0PHf05ph0":"p_Gen_ZH_SIG_ghz1_1_ghz2_0p112481_JHUGen",
                                          "0Mf05ph0":"p_Gen_ZH_SIG_ghz1_1_ghz4_0p144057_JHUGen",
                                          "0L1f05ph0":"p_Gen_ZH_SIG_ghz1_1_ghz1prime2_n0p0517788E4_JHUGen",
                                          "0L1Zgf05ph0":"p_Gen_ZH_SIG_ghz1_1_ghza1prime2_n0p06429534E4_JHUGen"},
                                  "bbH":{"SM":""},
                                  "ttH":{"SM":""},
                                 }
                    
  prod_mode = None
  if "ggH" in File_Name:
    prod_mode = "ggH"
  elif "VBFH" in File_Name:
    prod_mode = "WminusH"
  elif "WminusH" in File_Name:
    prod_mode = "WminusH"
  elif "WplusH" in File_Name:
    prod_mode = "WplusH"
  elif "ZH" in File_Name:
    prod_mode = "ZH"
  elif "bbH" in File_Name:
    prod_mode = "bbH"
  elif "ttH" in File_Name:
    prod_mode = "ttH"
  elif "gammaH" in File_Name:
    prod_mode = "gammaH"
  else:
    prod_mode = "gammaH"
  # Dumb way of parsing the couplings #
  if "0PHZyf05ph0" in File_Name:
    hypo = "0PHZyf05ph0"
  elif "0PHyyf05ph0" in File_Name:
    hypo = "0PHyyf05ph0"
  elif "0MZyf05ph0" in File_Name:
    hypo = "0MZyf05ph0"
  elif "0Myyf05ph0" in File_Name:
    hypo = "0Myyf05ph0"
  elif "0PHf05ph0" in File_Name:
    hypo = "0PHf05ph0"
  elif "0Mf05ph0" in File_Name:
    hypo = "0Mf05ph0"
  elif "0L1f05ph0" in File_Name:
    hypo = "0L1f05ph0" 
  elif "0L1Zgf05ph0" in File_Name:
    hypo = "0L1Zgf05ph0"
  elif "0PHyy" in File_Name:
    hypo = "0PHyy"
  elif "0PHZy" in File_Name:
    hypo = "0PHZy"
  elif "0Myy" in File_Name:
    hypo = "0Myy"
  elif "0MZy" in File_Name:
    hypo = "0MZy"
  elif "0PH" in File_Name:
    hypo = "0PH"
  elif "0M" in File_Name:
    hypo = "0M"
  elif "0L1Zg" in File_Name:
    hypo = "0L1Zg"
  elif "0L1" in File_Name:
    hypo = "0L1"  
  else:
    hypo = "SM"
  if prod_mode == None or hypo == None:
    raise ValueError("Native Probability Failed to Match for {}".format(File_Name))
  print(prod_mode,hypo)
  Native_Prob_Decay = Native_Prob_Dictionary_Decay[prod_mode][hypo]
  Native_Prob_Production = Native_Prob_Dictionary_Production[prod_mode][hypo]
  return Native_Prob_Decay,Native_Prob_Production

# For condor submission setup a few directories etc #
CMSSW_PATH = Analysis_Config.CMSSW_PATH
Work_Dir = Analysis_Config.Work_Dir
if not outputdir.endswith("/"):
  outputdir = outputdir+"/"

if not os.path.exists(outputdir):
  os.mkdir(outputdir)

condor_dir = outputdir+"condor/"
if not os.path.exists(outputdir+"condor"):
  os.mkdir(outputdir+"condor")

# Open the list of input Trees #
with open(Input_Trees,'r') as tree_list: 
  # Format should include the native probabilities separated by a space at the end of the file name in the input 
  job_num = 0
  for line in tree_list:
    fin = line
    ## Function To Determine the hypothesis from the file path #
    jhuprob_decay, jhuprob_prod = Get_Native_Prob(fin)
    input_string = ''
    ### For Condor submission ###
    Path_To_Condor_Template = "OnShell_Scripts/OnShell_MELA_Probs/condor_template.sub"
    Path_To_Bash_Template = "OnShell_Scripts/OnShell_MELA_Probs/MELA_submission_template.sh"
    #############################
    cmd = "python3 MELAcalc.py"
    input_string += " -i " + fin.strip('\n')
    #### Parse the subdirectory path ###
    path = fin
    head_tail = os.path.split(path)
    parsed_subdir = head_tail[0].split("/")
    parsed_subdir = parsed_subdir[1:]
    sub = ""
    for i in parsed_subdir[::-1][:4]:
      sub = "/"+ i + sub
    input_string += " -s " + sub
    # ========Output Directory======#
    sub_out_parsed = sub.split("/")
    sub_out = ''
    for i in sub_out_parsed[1:-1]:
      sub_out += "/" + i  
    input_string += " -o " + outputdir+sub_out
    # ====== branchfile ===========#
    input_string += " -b " + MELA_Probabilities
    # ====== Add the JHUGen Probability from the input ====== #
    if DecayOrProd.upper() == "DECAY":
      input_string += " -j " + jhuprob_decay
    if DecayOrProd.upper() == "PROD":
      input_string += " -j " + jhuprob_prod
    # ====== Setup Condor Submission ===== #
    condor_submission_string = "condor_submit"
    copy_bash_string = "cp "+Path_To_Bash_Template +" "+condor_dir+"submit_"+str(job_num)+".sh"
    copy_condor_string= "cp "+Path_To_Condor_Template +" "+condor_dir+"condor_"+str(job_num)+".sub"
    path_to_bash=condor_dir+"submit_"+str(job_num)+".sh"
    path_to_condor=condor_dir+"condor_"+str(job_num)+".sub"
    os.system(copy_bash_string)
    os.system(copy_condor_string)
    template_cmd = cmd + input_string 
    print(template_cmd)
    # Now we fill the template correctly #
    os.system("sed -i \"s+CMSSW+cd "+CMSSW_PATH+"+g\" "+path_to_bash)
    os.system("sed -i \"s+UTILS+cd "+Work_Dir+"+g\" "+path_to_bash)
    os.system("sed -i \"s+COMMAND+"+template_cmd+"+g\" "+path_to_bash)
    # Now we fill the condor script corretly #
    os.system("sed -i \"s+NAME+executable              = "+path_to_bash+"+g\" "+path_to_condor)
    os.system("sed -i \"s+OUTOUT+"+condor_dir+"Out"+str(job_num)+".out+g\" "+path_to_condor)
    os.system("sed -i \"s+OUTERR+"+condor_dir+"Out"+str(job_num)+".err+g\" "+path_to_condor)
    os.system("sed -i \"s+OUTLOG+"+condor_dir+"Out"+str(job_num)+".log+g\" "+path_to_condor)
    os.system("condor_submit "+path_to_condor)
    print("condor_submit "+path_to_condor)
    job_num = job_num + 1 
    
#MELAcalc.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-l <lhe2root>) (-m <mcfmprob>)
