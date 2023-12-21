import ROOT 
import array
import itertools
import pandas as pd
import numpy as np
import re
import pickle
from ..Utils.ReWeightSample import Reweight_Branch, Reweight_Branch_NoHff, ParseHypothesis, CheckIsIso, Reweight_Branch_NoHff_From_Template_Name
from ..Utils.HexMath import weightedaverage, kspoissongaussian
from collections import Counter
import math
from ..Utils.root_numpy import tree2array
from .BinMapper.Test_Analytic import Get_Bin_Number

def IsInterf(Hypothesis):
  IsInterf = False
  temp_hypothesis = Hypothesis
  if "interf" in Hypothesis:
    IsInterf = True
    temp_hypothesis = Hypothesis.split("-")[0]
  return IsInterf, temp_hypothesis

def Parse_Tagged_Mode(Tag,Analysis_Config):
  # Get the Categorization from Analysis Config #
  Categorization = Analysis_Config.TaggingProcess
  print (Tag,Categorization)
  cat_num = -999
  # Parse the Categorization and return  the number for the tag #
  if Categorization in("Tag_AC_19_Scheme_2"):
    if Tag == "Untagged":
      cat_num =  0
    elif Tag == "VBF1jTagged":
      cat_num =  1
    elif Tag == "VBF2jTagged":
      cat_num =  2
    elif Tag == "VHLeptTagged": 
      cat_num =  3
    elif Tag == "VHHadrTagged":
      cat_num =  4
    elif Tag == "ttHLeptTagged": 
      cat_num =  5
    elif Tag == "ttHHadrTagged":
      cat_num =  6
    elif Tag == "VHMETTagged":
      cat_num =  7
    elif Tag == "Boosted":
      cat_num =  8  
  elif Categorization in("Tag_Untagged_and_gammaH"):
    if Tag == "Untagged":
      cat_num =  0
    elif Tag == "gammaH":
      cat_num = 9
  elif Categorization in("Tag_Untagged_and_qq_gammaH"):
    if Tag == "Untagged":
      cat_num =  0
    elif Tag == "gammaH":
      cat_num = 9
  elif Categorization in ("Tag_All_Untagged"):
    if Tag == "Untagged":
      cat_num = 0
  try:
    cat_num != -999 
  except ValueError:
    print("Please select valid Tagged Mode!")

  return cat_num 

def Parse_Final_States(fs): 
  # Return the absolute value of |Z1Flav * Z2Flav|
  if fs == '4l':
    return False, null 
  elif fs == '2e2mu':
    return True, 11*11*13*13
  elif fs == '4mu':
    return True, 13*13*13*13
  elif fs == '4e':
    return True, 11*11*11*11
  else:
    raise ValueError("Please select a valid final state")

def Sort_Coupling_Order(couplings):
  def user_sorter(x):
    if x == 'g1':
      return 1
    elif x == 'g2':
      return 2
    elif x == 'g4':
      return 3
    elif x == 'g2Zg':
      return 4
    elif x == 'g4Zg':
      return 5
    elif x == 'g2gg':
      return 6
    elif x == 'g4gg':
      return 7
    elif x == 'g1prime2':
      return 8
    elif x == 'ghzgs1prime2':
      return 9
    elif x == 'wCuu':
      return 10 
    elif x == 'wCdd':
      return 11 
    elif x == 'wCss':
      return 12 
    elif x == 'wCcc':
      return 13 
  return sorted(couplings, key=user_sorter)

def Get_Prod_Mode_From_Sample_Name(Sample_Name):
  if ('ggH' in Sample_Name):
    Sample_Name = 'ggH'
  elif ('VBF' in Sample_Name):
    Sample_Name = 'qqH'
  elif ('ZH' in Sample_Name):
    Sample_Name = 'ZH'
  elif any(prod in Sample_Name for prod in ['Wminus','Wplus','WH']):
    Sample_Name = 'WH'
  elif any(prod in Sample_Name for prod in ['tqH','tWH','ttH','tHW']):
    Sample_Name = 'ttH'
  elif ('bbH' in Sample_Name):
    Sample_Name = 'bbH'
  elif ('qqgammaH' in Sample_Name):
    Sample_Name = 'qqgammaH'
  elif ('gammaH' in Sample_Name):
    Sample_Name = 'gammaH'
  elif any(prod in Sample_Name for prod in ["ggTo4e","ggTo2e2mu","ggTo2e2tau","ggTo2mu2tau","ggTo4mu","ggTo4tau"]): 
    Sample_Name = 'bkg_ggzz'
  elif("ZZTo4l" in Sample_Name):
    Sample_Name = 'bkg_qqzz'
  elif all(prod in Sample_Name for prod in ["VBF","Contin"]) or prod in ["TTLToLL_M1to0_MLM","TTZToLLNuNu_M10","TTZJets_M10_MLM","TTZZ","TTWW","ZZZ","WWZ","WZZ"] or prod in ["OffshellAC"]: 
    Sample_Name = 'bkg_ew'
  elif("Data" in Sample_Name):
    Sample_Name = 'bkg_zjets'
  return Sample_Name

def Filter_SMAC_Only(Template_Names):
  filtered_names = []
  for name in Template_Names:
    data_obs_match = re.match("(data_obs)",name)
    Grouped = re.match("(?P<production>gg|tt|bb|qq|Z|Wplus|Wminus|V|gamma)H_(?:(?P<Hffpure>0(?:PM|M)ff)_)?(?:(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg|Mgg|PHgg|MZg|PHZg))|(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1234])*))$",name)
    if Grouped != None:
      #print("Matched",Grouped.groups())
      grouped_dict = Grouped.groupdict()
      if (grouped_dict["HVVint"] != None):
        Interf_String=grouped_dict["HVVint"]
        #print("Int",name)
        if re.match("(g11g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1])*$",Interf_String) or re.match("(g12g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[2])*$",Interf_String):
          filtered_names.append(name)
      if (grouped_dict["HVVpure"] != None):
        filtered_names.append(name)
    if data_obs_match != None:
      filtered_names.append(name)
  #print("filtered",filtered_names)
  return filtered_names

def Filter_HZZ_Only(Template_Names):
  filtered_names = []
  for name in Template_Names:
    data_obs_match = re.match("(data_obs)",name)
    Grouped = re.match("(?P<production>gg|tt|bb|qq|Z|Wplus|Wminus|V|gamma)H_(?:(?P<Hffpure>0(?:PM|M)ff)_)?(?:(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg|Mgg|PHgg|MZg|PHZg))|(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1234])*))$",name)
    if Grouped != None:
      grouped_dict = Grouped.groupdict()
      if (grouped_dict["HVVint"] != None):
        Interf_String=grouped_dict["HVVint"]
        if (re.match("(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2)[1234])*)$",Interf_String)) and not (re.match("(?P<HVVint>(?:g(?:2gg|4gg|2Zg|4Zg)[1234])*)$",Interf_String)):
          filtered_names.append(name)
      if (grouped_dict["HVVpure"] != None):
        if (re.search("(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg)*)$",name)):
          filtered_names.append(name)
    if data_obs_match != None:
      filtered_names.append(name)
  #print("HZZ Filtered",filtered_names)
  return filtered_names

def Filter_Photons_Only(Template_Names):
  filtered_names = []
  for name in Template_Names:
    data_obs_match = re.match("(data_obs)",name)
    Grouped = re.match("(?P<production>gg|tt|bb|qq|Z|Wplus|Wminus|V|gamma)H_(?:(?P<Hffpure>0(?:PM|M)ff)_)?(?:(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg|Mgg|PHgg|MZg|PHZg))|(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1234])*))$",name)
    if Grouped != None:
      grouped_dict = Grouped.groupdict()
      if (grouped_dict["HVVint"] != None):
        Interf_String=grouped_dict["HVVint"]
        if not (re.match("(?P<HVVint>(?:g(?:2|4|1prime2|hzgs1prime2)[1234])*)$",Interf_String)) and (re.match("(?P<HVVint>(?:g(?:1|2gg|4gg|2Zg|4Zg)[1234])*)$",Interf_String)):
          filtered_names.append(name)
      if (grouped_dict["HVVpure"] != None):
        if not (re.search("(?P<HVVpure>0(?:M|PH|L1|L1Zg)*)$",name)):
          filtered_names.append(name)
    if data_obs_match != None:
      filtered_names.append(name)
  #print("Photon Filtered",filtered_names)
  return filtered_names

def Filter_Two_Hypothesis_Only_Prod_Or_Decay(Template_Names):
  filtered_names = []
  for name in Template_Names:
    data_obs_match = re.match("(data_obs)",name)
    Grouped = re.match("(?P<production>gg|tt|bb|qq|Z|Wplus|Wminus|V|gamma)H_(?:(?P<Hffpure>0(?:PM|M)ff)_)?(?:(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg|Mgg|PHgg|MZg|PHZg))|(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1234])*))$",name)
    if Grouped != None:
      grouped_dict = Grouped.groupdict()
      if (grouped_dict["HVVint"] != None):
        Interf_String=grouped_dict["HVVint"]
        Num_Match = 0
        for coupl in ["g11","g12","g21","g22","g41","g42","g2gg1","g2gg2","g4gg1","g4gg2","g2Zg1","g2Zg2","g4Zg1","g4Zg2","g1prime21","g1prime22","ghzgs1prime21","ghzgs1prime22"]:
            if coupl in Interf_String:
                Num_Match += 1
        if Num_Match == 2:
            filtered_names.append(name)
      if (grouped_dict["HVVpure"] != None):
          filtered_names.append(name)
    if data_obs_match != None:
      filtered_names.append(name)
  #print("Two Hypothesis Only Decay or Prod: ",filtered_names)
  return filtered_names
def StripRepeatedCouplings(Template_Names):
  return [*set(Template_Names)]
  
def GammaH_XS_Filter(Template_Names):
  filtered_names = []
  for name in Template_Names:
    data_obs_match = re.match("(data_obs)",name)
    if "gammaH" in name:
      if "0PM" not in name and "g1" not in name:
        filtered_names.append(name)
    else:
      if "0PM" in name:
        filtered_names.append(name)
    if data_obs_match != None:
      filtered_names.append(name)
  #if "gammaH_0PM" not in filtered_names:
  #  filtered_names.append("gammaH_0PM")
  print("Filtered for SM gammaH Rate: ",filtered_names)
  return filtered_names

def qq_GammaH_XS_Filter(Template_Names,prod):
  filtered_names = []
  for name in Template_Names:
    data_obs_match = re.match("(data_obs)",name)
    # Filter out the samples that are not SM Higgs or qq -> yH #
    if "qqgammaH" in name:
      if "0PM" not in name and "g1" not in name:
        if any(x in name for x in ["wCuu1","wCdd1","wCss1","wCcc1"]): continue
        if prod == "uuH" and any(x in name for x in ["wCdd","wCss","wCcc"]): continue
        if prod == "ddH" and any(x in name for x in ["wCuu","wCss","wCcc"]): continue
        if prod == "ssH" and any(x in name for x in ["wCdd","wCuu","wCcc"]): continue
        if prod == "ccH" and any(x in name for x in ["wCdd","wCss","wCuu"]): continue
        else: filtered_names.append(name)
    elif "0PM" in name: filtered_names.append(name)
    else: continue
    if data_obs_match != None:
      filtered_names.append(name)
  print("Filtered for qq + gammaH Rate: ",filtered_names)
  return filtered_names

def Add_Systematics(Template_Names,final_state):
  New_Names = []
  for name in Template_Names:
    if not any(string in name for string in ["bkg","data"]):
      New_Names.append(name)
      New_Names.append(name+"_CMS_res_"+final_state+"Up")
      New_Names.append(name+"_CMS_res_"+final_state+"Down")
      New_Names.append(name+"_CMS_scale_"+final_state+"Up")
      New_Names.append(name+"_CMS_scale_"+final_state+"Down")
    else:
      New_Names.append(name)
  return New_Names


def Convert_Hypothesis_And_Prodution_Mode_To_Template_Name(hypothesis_list,prod,**kwargs):
  Do_Systematics = False
  Final_State = None
  if kwargs['Do_Systematics'] == True:
    Do_Systematics = True
  if 'Final_State' in kwargs:
    Final_State = kwargs.get('Final_State')
  print("Final_State: ",Final_State)
  print("ProdMode : ",prod)
  print("Hypothesis: ",hypothesis_list["Hypothesis"])
  Name_List = []
  Options = hypothesis_list["Options"]
  couplings = hypothesis_list["Hypothesis"]
  production_mode = prod
  if ('ggH' in production_mode):
    production_mode = 'ggH'
  elif ('VBF' in production_mode):
    production_mode = 'qqH'
  elif any(prod in production_mode for prod in ['ZH']):
    production_mode = 'ZH'
  elif any(prod in production_mode for prod in ['WplusH']):
    production_mode = 'WplusH'
  elif any(prod in production_mode for prod in ['WminusH']):
    production_mode = 'WminusH'
  elif any(prod in production_mode for prod in ['tqH','tWH','ttH']):
    production_mode = 'ttH'
  elif any(x == prod for x in ["uuH","ddH","ssH","ccH"]):
    production_mode = 'qqgammaH'
  elif ('gammaH' in production_mode):
    production_mode = 'gammaH'
  elif ('bbH' in production_mode):
    production_mode = 'bbH'
  elif("ggZZ" in production_mode): 
    Name_List.append("bkg_ggzz")
    return Name_List
  elif("qqZZ" in production_mode):
    Name_List.append("bkg_qqzz")
    return Name_List
  elif("ew_bkg" in production_mode):
    Name_List.append("bkg_ew")
    return Name_List
  elif("ZX" in production_mode):
    Name_List.append("bkg_zjets")
    return Name_List
  elif("Data" in production_mode):
    Name_List.append("data_obs")
  else:
    raise ValueError("Please pass a valid production mode in Convert_Hypothesis_And_Prodution_Mode_To_Template_Name")
  if production_mode in ['ggH',"ttH","bbH","qqgammaH"]:
    All_Combinations = [p for p in itertools.product(couplings,repeat=2)]
    #print(All_Combinations)
    for combo in All_Combinations:
      counted = Counter(combo)
      #print(combo)
      coupling_names = []
      for key in counted.keys():
        coupling_names.append(key)
      sorted_names = Sort_Coupling_Order(coupling_names)
      temp_str = production_mode+"_"
      for name in sorted_names:
        #print(sorted_names)
        if counted[name] == 2: # Sort out the pure samples 
          if name == "g1":
            temp_str+="0PM"
          elif name == "g2":
            temp_str+="0PH"
          elif name == "g4":
            temp_str+="0M"
          elif name == "g1prime2":
            temp_str+="0L1"
          elif name == "ghzgs1prime2":
            temp_str+="0L1Zg"
          elif name == "g2gg":
            temp_str+="0PHgg"
          elif name == "g4gg":
            temp_str+="0Mgg"
          elif name == "g2Zg":
            temp_str+="0PHZg"
          elif name == "g4Zg":
            temp_str+="0MZg"
          elif name == "wCuu":
            temp_str+="0wCuu"
          elif name == "wCdd":
            temp_str+="0wCdd"
          elif name == "wCss":
            temp_str+="0wCss"
          elif name == "wCcc":
            temp_str+="0wCcc"  
        else:
          temp_str += name+str(counted[name])
      Name_List.append(temp_str)
  elif production_mode in ['gammaH',"WplusH","WminusH","VH","ZH","qqH"]:
    All_Combinations = [p for p in itertools.product(list(set(couplings) - set(['g2','g4','g1prime2','ghzgs1prime2'])), repeat=4)]
    for combo in All_Combinations:
      counted = Counter(combo)
      coupling_names = []
      for key in counted.keys():
        coupling_names.append(key)
      sorted_names = Sort_Coupling_Order(coupling_names)
      temp_str = production_mode+"_"
      for name in sorted_names:
        if counted[name] == 4: # Sort out the pure samples 
          if name == "g1":
            temp_str+="0PM"
          elif name == "g2":
            temp_str+="0PH"
          elif name == "g4":
            temp_str+="0M"
          elif name == "g1prime2":
            temp_str+="0L1"
          elif name == "ghzgs1prime2":
            temp_str+="0L1Zg"
          elif name == "g2gg":
            temp_str+="0PHgg"
          elif name == "g4gg":
            temp_str+="0Mgg"
          elif name == "g2Zg":
            temp_str+="0PHZg"
          elif name == "g4Zg":
            temp_str+="0MZg"
          elif name == "wCuu":
            temp_str+="0wCuu"
          elif name == "wCdd":
            temp_str+="0wCdd"
          elif name == "wCss":
            temp_str+="0wCss"
          elif name == "wCcc":
            temp_str+="0wCcc" 
        else:
          temp_str += name+str(counted[name])
      Name_List.append(temp_str)
  #print("Here SM",Name_List)
  # If production only or decay only is specified we only include 2 potential couplings in either the production or the decay #
  if "Decay_Only" in Options:
    Name_List = Filter_Two_Hypothesis_Only_Prod_Or_Decay(Name_List)
  if "Prod_Only" in Options:
    Name_List = Filter_Two_Hypothesis_Only_Prod_Or_Decay(Name_List)
  if "SM+AC_Only" in Options:
    Name_List = Filter_SMAC_Only(Name_List)
  if "HZZ_Only" in Options:
    Name_List = Filter_HZZ_Only(Name_List)
  if "Photons_Only" in Options:
    Name_List = Filter_Photons_Only(Name_List)
  if "gammaH_XS_Only" in Options:
    Name_List = GammaH_XS_Filter(Name_List)
  if "qq_gammaH_XS_Only" in Options:
    Name_List = qq_GammaH_XS_Filter(Name_List,prod) # include prod since we cannot reweight to any non pure hypothesis :(
  # Add Sytematics to the template Names # 
  if Do_Systematics:
    Name_List = Add_Systematics(Name_List,Final_State)
  #print("Stripping Repeated Couplings: ")
  Name_List = StripRepeatedCouplings(Name_List)
  #print("New Coupling List After Stripping: ", Name_List)
  return Name_List

def Convert_Hypothesis_And_Prodution_Mode(hypothesis,production_mode): #This function takes as input a given hypothesis and returns the correct naming convention for the combine physics model

  # establish naming convention for production mode#
  if ('ggH' in production_mode):
    production_mode = 'ggH'
  elif ('VBF' in production_mode):
    production_mode = 'qqH'
  elif any(prod in production_mode for prod in ['ZH','WH','Wplus','Wminus','VH']):
    production_mode = 'VH'
  elif any(prod in production_mode for prod in ['tqH','tWH','ttH']):
    production_mode = 'ttH'
  elif ('bbH' in production_mode):
    production_mode = 'bbH'
  elif("ggZZ" in production_mode):
    return "bkg_ggzz"
  elif("qqZZ" in production_mode):
    return "bkg_qqzz"
  elif("ew_bkg" in production_mode):
    return "bkg_ew"
  elif("ZX" in production_mode):
    return "bkg_zjets"
  Coupling_Dict = ParseHypothesis(hypothesis) # Needed to parse out the naming conventions
  if CheckIsIso(Coupling_Dict):
    if Coupling_Dict["ghz1"] != 0:
      return production_mode+"_"+"0PM"
    elif Coupling_Dict["ghz2"] != 0:
      return production_mode+"_"+"0PH"
    elif Coupling_Dict["ghz4"] != 0:
      return production_mode+"_"+"0M"
    elif Coupling_Dict["ghz1prime2"] != 0:
      return production_mode+"_"+"0L1"
    elif Coupling_Dict["ghza1prime2"] != 0:
      return production_mode+"_"+"0L1Zg"
    elif Coupling_Dict["ghza2"] != 0:
      return production_mode+"_"+"0PHZg"
    elif Coupling_Dict["ghza4"] != 0:
      return production_mode+"_"+"0MZg"
    elif Coupling_Dict["gha2"] != 0:
      return production_mode+"_"+"0PHgg"
    elif Coupling_Dict["gha4"] != 0:
      return production_mode+"_"+"0Mgg"
  else:
    if any(prod in production_mode for prod in ['ggH',"qqH","VH","bbH"]):
      coupling_string = ''
      for key in Coupling_Dict.keys():
        if Coupling_Dict[key] != 0:
          if key == "ghz1":
            coupling_string += 'g11'
          elif key == "ghz2":
            coupling_string += 'g21'
          elif key == "ghz4" != 0:
            coupling_string += 'g41'
          elif key == "ghz1prime2":
            coupling_string += 'g1prime21'
          elif key == "ghza1prime2" != 0:
            coupling_string += 'ghzgs1prime21'
          elif key == "ghza2":
            coupling_string += 'g2za1'
          elif key == "ghza4":
            coupling_string += 'g4za1'
          elif key == "gha2":
            coupling_string += 'g2gg1'
          elif key == "gha4":
            coupling_string += 'g4gg1'
    if any(prod in production_mode for prod in ['gammaH']):
      coupling_string = ''
      for key in Coupling_Dict.keys():
        if Coupling_Dict[key] != 0:
          if key == "ghz1":
            coupling_string += 'g11'
          elif key == "ghz2":
            coupling_string += 'g21'
          elif key == "ghz4" != 0:
            coupling_string += 'g41'
          elif key == "ghz1prime2":
            coupling_string += 'g1prime21'
          elif key == "ghza1prime2" != 0:
            coupling_string += 'ghzgs1prime21'
          elif key == "ghza2":
            coupling_string += 'g2za1'
          elif key == "ghza4":
            coupling_string += 'g4za1'
          elif key == "gha2":
            coupling_string += 'g2gg1'
          elif key == "gha4":
            coupling_string += 'g4gg1'
    elif production_mode == 'ttH': #Need to include Hff couplings???#
      coupling_string = ''
      for key in Coupling_Dict.keys():
        if Coupling_Dict[key] != 0:
          print(key)
          if key == "ghz1":
            coupling_string += 'g11'
          elif key == "ghz2":
            coupling_string += 'g21'
          elif key == "ghz4" != 0:
            coupling_string += 'g41'
          elif key == "ghz1prime2":
            coupling_string += 'g1prime21'
          elif key == "ghza1prime2" != 0:
            coupling_string += 'ghzgs1prime21'
          elif key == "ghza2":
            coupling_string += 'g2za1'
          elif key == "ghza4":
            coupling_string += 'g4za1'
          elif key == "gha2":
            coupling_string += 'g2gg1'
          elif key == "gha4":
            coupling_string += 'g4gg1'
  return production_mode + "_" + coupling_string

def Trim_Dict(d,keys):
  n = d.copy()
  for key in keys:
    del n[key]
  return n

def Get_Bin_Num(value,bin_edges):
  for i in range(1, len(bin_edges)):
    if bin_edges[i-1] <= value <= bin_edges[i]:
      #print(bin_edges)
      #print(bin_edges[i])
      return i 
  #print(value)
  return 0 

def Get_Bin_Num_From_Edges(value,bin_edges):
  for i in range(1, len(bin_edges)):
    if bin_edges[i-1] <= value <= bin_edges[i]:
      #print(bin_edges)
      #print(bin_edges[i])
      return i 
  #print(value)
  return 0 

def Convert_Tuple_To_Bin(Tuples,Discriminants):
  # Input should be a tuple of the discriminant values
  # And the Discrminant Names with binning 
  # Make sure that the length of the tuple is the number of input discriminants 

  New_Tuples = []
  for t in Tuples:
    tup_list = list(t)
    index = 0
    for key in Discriminants.keys():
      bin_edges = Discriminants[key]
      tup_list[index] = Get_Bin_Num(t[index],bin_edges)
      #if tup_list[index] < 1:
      #  print(key)
      index += 1
    New_Tuples.append(tuple(tup_list))

  return New_Tuples

def Get_Z_Value(Discriminant_Values,Discriminants):
  # Input should be 2 dictionaries with keys of the names of the discriminants
  # The expected binning is with integer bins (0,1,2,3,4 etc) and the length must equal the 
  # number of bins for each discriminants multiplied together
  # Once the bin index is decided assign a value between the two bin edges and return that value for the Z_Value
   # each iteration is assigned an integer bin number. Then we return the bin number - .5 
  Binning_Num = []
  for key in Discriminants.keys():
    Binning_Num.append(list(range(1, len(Discriminants[key]))))
  Tuples_Of_Bin_Num = list(itertools.product(*Binning_Num))
  df = pd.DataFrame.from_dict(Discriminant_Values)
  # Convert the input Discriminats values to a Tuple of Values

  Tuple_Of_Discriminant_Values=list(df.itertuples(index=False, name=None))  
  Binned_Tuples = Convert_Tuple_To_Bin(Tuple_Of_Discriminant_Values,Discriminants)
  Index_Of_Match=[]
  # Sort through the new tuples to return a list of bins for each event 
  for tup in Binned_Tuples:
    try:
      Index_Of_Match.append(Tuples_Of_Bin_Num.index(tup))
    except ValueError:
      Index_Of_Match.append(-999)
  # Add .5 to ach index to push into the correct bin
  Index_Of_Match = [i + .5 for i in Index_Of_Match]
  return Index_Of_Match

def findoutliers(binval, binerr,debugprint=False):
    val = binval.copy()
    err = binerr.copy()
    absval = binval.copy()
    
    relativeerror = [err[i] / absval[i] if absval[i] else float("inf") for i in range(len(absval))] 
                     
    outliers = {}
    
    for name in range(len(val)):
      if debugprint: print(name, val[name], relativeerror[name], absval[name])
      if debugprint: print("still here!")
      errortoset = None
      for othername in range(len(val)):
        #look at the other names that have bigger errors but comparable relative errors
        if err[othername] <= err[name]: continue
        if err[othername] == 0: continue
        if debugprint: print("here with", othername)
        if val[name] == 0 or relativeerror[othername] <= relativeerror[name] * ((1 + 1.5 * np.log10(err[othername] / err[name]) * kspoissongaussian(1/relativeerror[name]**2))):
          if debugprint: print("here 2 with", othername)
          if errortoset is None: errortoset = 0
          errortoset = max(errortoset, err[othername])
      if errortoset is not None:
        outliers[name] = (val[name], errortoset)
    if outliers != {}:
      print("Found Outliers:", outliers)
    return outliers

def updatebinvalues(val,err,outliers):
    for outlier in outliers.keys():
        val[outlier] = outliers[outlier][0]
        err[outlier] = outliers[outlier][1]
    return val,err

def Calculate_Average_And_Unc_From_Template_Bins(val,err):
  # Expects a list of values and error from a set of n histograms
  # We need to take the weighted average while also protecting against weird bin values/low statistics
  # first step is to remove values with 0 and save them separatley
  #print("initial values: ", val, "initial errors: ", err)
  temp_val = []
  temp_err = []
  temp_zeros_val = []
  temp_zeros_err = []
  maxerr = 0 
  # If bin is not filled we assume it should be 0
  if len(val) == 0:
    return 0,0
  for error in err:
    if not math.isnan(error) and not math.isinf(error): 
      if maxerr < error:
        maxerr = error
  #print("error, value before removing non zero",err,val)
  for i in range(len(val)): # Only apply outlier procedure to non zero values
    if (math.isnan(val[i]) or math.isnan(err[i])): continue
    elif (math.isinf(val[i]) or math.isinf(err[i])): continue  
    elif (err[i] != 0) :
      temp_val.append(val[i])
      temp_err.append(err[i])
    else:
      temp_zeros_val.append(val[i])
      temp_zeros_err.append(maxerr)
  val = temp_val
  err = temp_err
  if len(val) == 0:
    return 0,0
  
  outliers = findoutliers(val,err)
  val,err = updatebinvalues(val,err,outliers)
  val = val + temp_zeros_val 
  err = err + temp_zeros_err
  #print("final values: ", val, "final errors: ", err)
  #Sprint("Average: ", weightedaverage(val,err))
  return weightedaverage(val,err)

def GetBinOptimalDiscriminant1D(Discriminant_Values,Optimal_Discriminants,dct):
  # Find the bin number and then shift by 0.5 to make sure the 
  #value returned is between the 
  Bin_Value = []
  for i in range(len(Discriminant_Values[list(Discriminant_Values.keys())[0]])):
    Bin_Per_Discriminant = []
    for name in Optimal_Discriminants.keys():
      if name in Discriminant_Values:
        Bin_Per_Discriminant.append(Get_Bin_Num(Discriminant_Values[name][i],Optimal_Discriminants[name])-1)
        #print("Name:",name," ", Discriminant_Values[name][i])
    ns = {"temp_bin_num":None,"dct":dct}
    str_exec = "temp_bin_num = dct["
    for j in range(len(Bin_Per_Discriminant)):
      if j != len(Bin_Per_Discriminant) - 1:
        str_exec += str(Bin_Per_Discriminant[j]) +","
      else:
        str_exec += str(Bin_Per_Discriminant[j]) +"]"
    try:
      exec(str_exec,ns)
    except:
      raise ValueError("Failed to get bin of optimal discriminant")
    Bin_Value.append(ns["temp_bin_num"] + 0.5)
  return Bin_Value

def GetBinOptimalDiscriminant1D_bin_map(Discriminant_Values,Optimal_Discriminants):
  Bin_Values = []
  #print(Discriminant_Values,Optimal_Discriminants)
  #print(len(Discriminant_Values[list(Discriminant_Values.keys())[0]]),len(Discriminant_Values[list(Discriminant_Values.keys())[1]]))
  for i in range(len(Discriminant_Values[list(Discriminant_Values.keys())[0]])):
    Name_Ordered_Discriminants=[]
    for name in Optimal_Discriminants["Observables_For_Optimal"]:
      Name_Ordered_Discriminants.append(Discriminant_Values[name][i])
    try: 
      Bin_Values.append(Get_Bin_Number(Optimal_Discriminants,Name_Ordered_Discriminants) +0.5) # May NEED TO CONVERT TO ROOT Binning
      #print(Get_Bin_Number(Optimal_Discriminants,Name_Ordered_Discriminants))
    except: 
      Bin_Values.append(0)
    
  return Bin_Values

def GetBinOptimalDiscriminantND_bin_map(Discriminant_Values,Discriminants,Optimal_Discriminants,nbins):
  #sprint(Discriminant_Values,Discriminants,Optimal_Discriminants,nbins)
  Bin_Value = []
  Optimal_Value = [bin_value + 0.5 for bin_value in GetBinOptimalDiscriminant1D_bin_map(Discriminant_Values,Optimal_Discriminants)]  # This will return the value to go in the correct bin number
  
  # We now have the bin of the optimal discriminant #
  # Now we need to uniquely place the rest of the observables #
  Bin_Num_For_Not_Optimal = {}
  #Initialize#
  for name in Discriminant_Values.keys():
    if name not in Optimal_Discriminants["Observables_For_Optimal"]:
      Bin_Num_For_Not_Optimal[name] = [] 
      bin_edges = Discriminants[name]
      for value in Discriminant_Values[name]:
        Bin_Num_For_Not_Optimal[name].append(Get_Bin_Num_From_Edges(value,bin_edges))
  
  Combined_Not_Optimal_Bin_Num = 1
  for name in Bin_Num_For_Not_Optimal.keys():
    Combined_Not_Optimal_Bin_Num = Combined_Not_Optimal_Bin_Num * Bin_Num_For_Not_Optimal[name]
  
  Bin_Value = np.array(Combined_Not_Optimal_Bin_Num).astype(float) * np.array(Optimal_Value)
  Bin_Value = [bin_num - 0.5 for bin_num in Bin_Value]
  #print(Bin_Value)
  return Bin_Value

def GetBinOptimalDiscriminantND(Discriminant_Values,Discriminants,Optimal_Discriminants,nbins,dct): #Only Needed for Pickling OUTDATED#
  # The expected input is a list of all discriminants not used on x or y axis
  Bin_Value = []
  # Make Binning for Optimal_Discriminants
  Optimal_Bin_Edges = []
  for i in range(nbins + 1):
    Optimal_Bin_Edges.append(i)
  Optimal_Value = GetBinOptimalDiscriminant1D(Discriminant_Values,Optimal_Discriminants,dct) # Value to put optimal bin in correct position
  Combined_Discriminant_Values = {}
  Combined_Discriminant_Bins = {}
  for name in Discriminant_Values.keys():
    if name not in Optimal_Discriminants:
      Combined_Discriminant_Values[name] = Discriminant_Values[name]
      Combined_Discriminant_Bins[name] = Discriminants[name]
  Combined_Discriminant_Values["optimal"] = Optimal_Value
  Combined_Discriminant_Bins["optimal"] = Optimal_Bin_Edges
  Bin_Value = Get_Z_Value(Combined_Discriminant_Values,Combined_Discriminant_Bins)
  return Bin_Value

def FillHistOnShell(targetprod,targetcateg,hlist,yeardict,Analysis_Config,year,final_state,**kwargs):
  # This should take an empty h_list and then fill with the templates 
  # target production will return which ever production that will be used to make the template ex (ggH,VBF etc) 
  # targetcateg is which tagged category is used to make the template 
  # h_list is an input dictionary 
  # year dict has paths and years attatched to each samples
  # year is an array of years to use#

  #The logic below will tell use to either sum or average the bins after we reweight the samples
  # We may need to support Sum and Average combined if we do a true decay only analysis
  # I.E creating a template where we reweight combinations of all production modes to one template 
  Combine_Production_Mode = "Average"
  Do_Systematics = False
  if kwargs['Combine_Production_Mode'] == "Sum":
    Combine_Production_Mode = "Sum"
  if kwargs['Do_Systematics'] == True:
    Do_Systematics = True
  # First We nee to parse the input category which tells us exactly which discriminants are needed #
  category = Parse_Tagged_Mode(targetcateg,Analysis_Config)
  print("Category ",category)
  UseOptimal = False
  if category == 0: #Untagged 
    if Analysis_Config.UseOptimal["Untagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_Untagged
      UseOptimal = True
    Discriminants = Analysis_Config.Untagged_Discriminants
  elif category == 1: #VBF1jTagged
    if Analysis_Config.UseOptimal["VBF1jTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_VBF1jTagged
      UseOptimal = True
    Discriminants = Analysis_Config.VBF1jTagged_Discriminants
  elif category == 2: #VBF2jTagged
    if Analysis_Config.UseOptimal["VBF2jTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_VBF2jTagged
      UseOptimal = True
    Discriminants = Analysis_Config.VBF2jTagged_Discriminants
  elif category == 3: #VHLeptTagged
    if Analysis_Config.UseOptimal["VHLeptTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_VHLeptTagged
      UseOptimal = True
    Discriminants = Analysis_Config.VHLeptTagged_Discriminants
  elif category == 4: #VHHadrTagged
    if Analysis_Config.UseOptimal["VHHadrTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_VHHadrTagged
      UseOptimal = True
    Discriminants = Analysis_Config.VHHadrTagged_Discriminants
  elif category == 5: #ttHLeptTagged
    if Analysis_Config.UseOptimal["ttHLeptTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_ttHLeptTagged
      UseOptimal = True
    Discriminants = Analysis_Config.ttHLeptTagged_Discriminants
  elif category == 6: #ttHHadrTagged
    if Analysis_Config.UseOptimal["ttHHadrTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_ttHHadrTagged
      UseOptimal = True
    Discriminants = Analysis_Config.ttHHadrTagged_Discriminants
  elif category == 7: #VHMETTagged
    if Analysis_Config.UseOptimal["VHMETTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_VHMETTagged
      UseOptimal = True
    Discriminants = Analysis_Config.VHMETTagged_Discriminants
  elif category == 8: #Boosted
    if Analysis_Config.UseOptimal["Boosted"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_Boosted
      UseOptimal = True
    Discriminants = Analysis_Config.Boosted_Discriminants
  elif category == 9: #gammaH
    if Analysis_Config.UseOptimal["gammaH"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_gammaH
      UseOptimal = True
    Discriminants = Analysis_Config.gammaH_Discriminants
  else:
    print("No category found")
  print(Discriminants)

  if "Data" not in targetprod: # Need for input to get the new weights
    isData = False
  else:
    isData = True

  Trees_Dict = yeardict[year] # Returns dictionary of all the samples for a given year
  Samples_To_Reweight = Trees_Dict[targetprod] #Returns the list of all samples of a given production mode 
  if len(Samples_To_Reweight) == 1:
    Samples_To_Reweight = Samples_To_Reweight[0] 
  lumi = Analysis_Config.lumi[year]
  Coupling_Name = Analysis_Config.Coupling_Name # Returns name of couplings used for analysis (what do we need to reweight to?)  
  Output_Name = "templates_"+str(targetprod)+"_"+str(targetcateg)+"_"+Coupling_Name+"_"+final_state+"_"+Analysis_Config.TreeFile+"_"+year+".root" #NEED to fix decay mode#
  Hypothesis_List = Analysis_Config.Hypothesis_List # Returns a list of all the hyptothesis to reweight to 
  print("Final_State_Before_Template_Names:", final_state)
  Template_Names = Convert_Hypothesis_And_Prodution_Mode_To_Template_Name(Hypothesis_List,targetprod,Final_State = final_state,Do_Systematics = Analysis_Config.Do_Shape_Systematics)
  DoMassFilter = Analysis_Config.DoMassFilter
  #Parse the final state to filter at the end#
  filter_final_state, final_state = Parse_Final_States(final_state)

  print("Samples To Reweight",Samples_To_Reweight)
  # Added a catch to check if the production mode is background #
  # Then this sets the Hypothesis List to only include SM #
  if any(x in targetprod for x in ["ggZZ","qqZZ","ew_bkg","ZX"]):
    Hypothesis_List = ["bkg"]  

  #Get name of discriminants and save them to a list of strings#
  D_Name=[]
  for key in Discriminants.keys():
    D_Name.append(key)

  Discriminant_Values = {}
  for name in D_Name:
    Discriminant_Values[name] = []
  
  # This part here will check if we need to use optimal discriminants for a given 
  # Category, we need to if each optimal observable is 
  if UseOptimal == True:  
    # This sorts which discriminant is optimal or not
    D_Name_NotOptimal = []
    D_Name_Optimal = []
    for name in D_Name: 
      if(name in Discriminants) and (name in Discriminants_Optimal["Observables_For_Optimal"]):
        D_Name_Optimal.append(name)
      else:
        D_Name_NotOptimal.append(name)
    print("Optimal",Discriminants_Optimal,"Not Optimal",D_Name_NotOptimal)
    """optpkl = Discriminants_Optimal["Path_To_Pickle"] 
    nbins = Discriminants_Optimal["nbins"] 
    #print(optpkl)
    with open(optpkl, "rb") as f:
     binning = sorted(pickle.load(f)[-nbins], key=lambda x: min(x))
     dct = {bin: i for i, bins in enumerate(binning) for bin in bins}
    """
    # Sort if we make a 1D,2D,or 3D histogram 
    if len(D_Name_NotOptimal) == 0:
      nx = Discriminants_Optimal["nbins"]
      xbins = array.array('d')  
      for i in range(nx+1):
        xbins.append(i)

      Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
      for name in Template_Names:
        Histogram_Dict[name] = ROOT.TH1F(name,name,nx,xbins) # Initialize the Histogram Dictionary with with each AC hypothesis you need
        
      for tn in Template_Names: # Choose which hypothesis to reweight to
        Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
        for sample in Samples_To_Reweight: # Loop over all samples with input production mode
          print("File:",sample)
          New_Weights = Reweight_Branch_NoHff_From_Template_Name(sample,tn,isData,Analysis_Config,lumi,year,DoMassFilter,"eventTree") # Returns New Weights for each event
          for Discriminant in D_Name:
            Discriminant_Values[Discriminant] = tree2array(tree=sample,branches=[Discriminant],top_branch_name="eventTree").astype(float);
          # Fill the histogram with the Discriminants for each template #
          Tag = tree2array(tree=sample,branches=["EventTag"],top_branch_name="eventTree").astype(int); # Need to know what category each event falls into
          Z1Flav = tree2array(tree=sample,branches=["Z1Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z1
          Z2Flav = tree2array(tree=sample,branches=["Z2Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z2
          # Make the temporary histogram for this specific sample input
          Temp_Hist = ROOT.TH1F(sample,sample,nx,xbins)
          Temp_Hist.Sumw2(True)
          xbin = GetBinOptimalDiscriminant1D_bin_map(Discriminant_Values,Discriminants_Optimal)
          #print("Category:",category)
          for i in range(len(New_Weights)):
            if Tag[i] == category:
              if filter_final_state:
                if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                  Temp_Hist.Fill(xbin[i],New_Weights[i])
              else:
                Temp_Hist.Fill(xbin[i],New_Weights[i])
          Temporary_Histogram_List.append(Temp_Hist)
          print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral())
        # Apply the logic for filling the combined histogram #
        # Loop over each bin and calculate the weighted average of each bin #
        for x in range(1,nx+1):
            binval=[] # list of bin values
            binerr=[] # list of error on each bin
            for hist in Temporary_Histogram_List:
              binval.append(hist.GetBinContent(x))
              binerr.append(hist.GetBinError(x))
            if "bkg" in Hypothesis_List:
              val = sum(binval)
              err = sum(i*i for i in binerr)
            else:
              val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
            Histogram_Dict[tn].SetBinContent(x,val)
            Histogram_Dict[tn].SetBinError(x,err)
        print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())
      # Make the Output File and return the output #
      for hist in Histogram_Dict.keys():
        hlist.append(Histogram_Dict[hist])
      return Output_Name

    elif len(D_Name_NotOptimal) == 1:
      nx = len(Discriminants[D_Name_NotOptimal[0]]) - 1 
      xbins = array.array('d',Discriminants[D_Name_NotOptimal[0]])
      ny = Discriminants_Optimal["nbins"] 
      ybins = array.array('d')
      for i in range(ny+1):
        ybins.append(i)
      print(nx,xbins,ny,ybins)
      Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
      for name in Template_Names:
        Histogram_Dict[name] = ROOT.TH2F(name,name,nx,xbins,ny,ybins) # Initialize the Histogram Dictionary with with each AC hypothesis you need

      for tn in Template_Names: # Choose which hypothesis to reweight to
        Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
        for sample in Samples_To_Reweight: # Loop over all samples with input production mode
          print("File:",sample)
           # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
          if Combine_Production_Mode == "Sum" and ("bkg" not in tn): # If we need to sum over samples make sure we send the correct production mode to the weight calculator
            # Get the production mode from the sample
            temp_prod = Get_Prod_Mode_From_Sample_Name(sample)
            new_tn = temp_prod + "_" + tn.split("_")[1]
            print("new_tn: ",new_tn)
            New_Weights = Reweight_Branch_NoHff_From_Template_Name(sample,new_tn,isData,Analysis_Config,lumi,year,DoMassFilter,"eventTree")
          else:
            New_Weights = Reweight_Branch_NoHff_From_Template_Name(sample,tn,isData,Analysis_Config,lumi,year,DoMassFilter,"eventTree") # Returns New Weights for each event
          for Discriminant in D_Name:
            Discriminant_Values[Discriminant] = tree2array(tree=sample,branches=[Discriminant],top_branch_name="eventTree").astype(float)
          # Fill the histogram with the Discriminants for each template #
          Tag = tree2array(tree=sample,branches=["EventTag"],top_branch_name="eventTree").astype(int); # Need to know what category each event falls into
          Z1Flav = tree2array(tree=sample,branches=["Z1Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z1
          Z2Flav = tree2array(tree=sample,branches=["Z2Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z2
          # Make the temporary histogram for this specific sample input
          Temp_Hist = ROOT.TH2F(sample,sample,nx,xbins,ny,ybins)
          Temp_Hist.Sumw2(True)
          ybin = GetBinOptimalDiscriminant1D_bin_map(Discriminant_Values,Discriminants_Optimal)
          #print("Category:",category)
          for i in range(len(New_Weights)):
            if Tag[i] == category:
              if filter_final_state:
                if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                  Temp_Hist.Fill(Discriminant_Values[D_Name_NotOptimal[0]][i],ybin[i],New_Weights[i])
              else:
                Temp_Hist.Fill(Discriminant_Values[D_Name_NotOptimal[0]][i],ybin[i],New_Weights[i])
          Temporary_Histogram_List.append(Temp_Hist)
          print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral())
        # Apply the logic for filling the combined histogram #
        # Loop over each bin and calculate the weighted average of each bin #
        for x in range(1,nx+1):
          for y in range(1,ny+1):
            binval=[] # list of bin values
            binerr=[] # list of error on each bin
            for hist in Temporary_Histogram_List:
              binval.append(hist.GetBinContent(x,y))
              binerr.append(hist.GetBinError(x,y))
            if "bkg" in Hypothesis_List:
              val = sum(binval)
              err = sum(i*i for i in binerr)
            else:
              val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
            Histogram_Dict[tn].SetBinContent(x,y,val)
            Histogram_Dict[tn].SetBinError(x,y,err)
        print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())
      # Make the Output File and return the output #
      for hist in Histogram_Dict.keys():
        hlist.append(Histogram_Dict[hist])
      return Output_Name


    elif len(D_Name_NotOptimal) >= 2:
      nx = len(Discriminants[D_Name_NotOptimal[0]])-1
      ny = len(Discriminants[D_Name_NotOptimal[1]])-1
      nz = None
      xbins = array.array('d',Discriminants[D_Name_NotOptimal[0]])
      ybins = array.array('d',Discriminants[D_Name_NotOptimal[1]])
      zbins = array.array('d')
      # Choose the z-axis to hold the rest of the discriminants
      num_bins=1
      for i in range(2,len(D_Name_NotOptimal)):
        num_bins *= len(Discriminants[D_Name_NotOptimal[i]]) - 1
      num_bins *= Discriminants_Optimal["nbins"]
      for i in range(0,num_bins + 1):
        zbins.append(i)
      nz = len(zbins) - 1
      Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
      
      for name in Template_Names:
        Histogram_Dict[name] = ROOT.TH3F(name,name,nx,xbins,ny,ybins,nz,zbins) # Initialize the Histogram Dictionary with with each AC hypothesis you need

      for tn in Template_Names: # Choose which hypothesis to reweight to
        Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
        for sample in Samples_To_Reweight: # Loop over all samples with input production mode
          # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
          print(sample)
          New_Weights = Reweight_Branch_NoHff_From_Template_Name(sample,tn,isData,Analysis_Config,lumi,year,DoMassFilter,"eventTree") # Returns New Weights for each event
          for Discriminant in D_Name:
            Discriminant_Values[Discriminant] = tree2array(tree=sample,branches=[Discriminant],top_branch_name="eventTree").astype(float)
          # Fill the histogram with the Discriminants for each template #
          Tag = tree2array(tree=sample,branches=["EventTag"],top_branch_name="eventTree").astype(int) # Need to know what category each event falls into
          Z1Flav = tree2array(tree=sample,branches=["Z1Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z1
          Z2Flav = tree2array(tree=sample,branches=["Z2Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z2
          # Make the temporary histogram for this specific sample input
          Temp_Hist = ROOT.TH3F(sample,sample,nx,xbins,ny,ybins,nz,zbins)
          Temp_Hist.Sumw2(True)
          # Trim the x and y axis Discriminants from the dictionary
          Discriminant_Values_Trimmed = Trim_Dict(Discriminant_Values,[D_Name_NotOptimal[0],D_Name_NotOptimal[1]])
          Discriminant_Trimmed = Trim_Dict(Discriminants,[D_Name_NotOptimal[0],D_Name_NotOptimal[1]])
          Z_bin = GetBinOptimalDiscriminantND_bin_map(Discriminant_Values_Trimmed,Discriminant_Trimmed,Discriminants_Optimal,num_bins)
          sum_weight = 0
          for i in range(len(New_Weights)):
            if Tag[i] == category:
              if filter_final_state:
                if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                  Temp_Hist.Fill(Discriminant_Values[D_Name_NotOptimal[0]][i],Discriminant_Values[D_Name_NotOptimal[1]][i],Z_bin[i],New_Weights[i])
                  sum_weight += New_Weights[i]
              else:
                Temp_Hist.Fill(Discriminant_Values[D_Name_NotOptimal[0]][i],Discriminant_Values[D_Name_NotOptimal[1]][i],Z_bin[i],New_Weights[i])
                sum_weight += New_Weights[i]
          print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral(),sum_weight)
          Temporary_Histogram_List.append(Temp_Hist)
        # Apply the logic for filling the combined histogram #
        # Loop over each bin and calculate the weighted average of each bin #
        for x in range (1,nx+1):
          for y in range(1,ny+1):
            for z in range(1,nz+1):
              binval=[] # list of bin values
              binerr=[] # list of error on each bin
              for hist in Temporary_Histogram_List:
                binval.append(hist.GetBinContent(x,y,z))
                binerr.append(hist.GetBinError(x,y,z))
              if "bkg" in Hypothesis_List:
                val = sum(binval)
                err = sum(i*i for i in binerr)
              else:
                val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
              Histogram_Dict[tn].SetBinContent(x,y,z,val)
              Histogram_Dict[tn].SetBinError(x,y,z,err)
        print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())
      # Make the Output File and return the output #
      for hist in Histogram_Dict.keys():
        hlist.append(Histogram_Dict[hist])
      return Output_Name

  elif len(Discriminants) == 1: # This will make a 1D histogram#
    # This is where we process categories with two discriminants #
    nx = len(Discriminants[D_Name[0]])-1
    xbins = array.array('d',Discriminants[D_Name[0]])
    print("Target Prod:", targetprod)
    # Now need to reweight each sample and add Fill the histograms #
    # Loop over the input trees and return the new weights #
       
    Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
    for name in Template_Names:
      Histogram_Dict[name] = ROOT.TH1F(name,name,nx,xbins) # Initialize the Histogram Dictionary with with each AC hypothesis you need
    for tn in Template_Names: # Choose which hypothesis to reweight to
      Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
      for sample in Samples_To_Reweight: # Loop over all samples with input production mode
        if Combine_Production_Mode == "Sum" and ("bkg" not in tn): # If we need to sum over samples make sure we send the correct production mode to the weight calculator
          # Get the production mode from the sample
          temp_prod = Get_Prod_Mode_From_Sample_Name(sample)
          new_tn = temp_prod + "_" + tn.split("_")[1]
          print("new_tn: ",new_tn)
          New_Weights = Reweight_Branch_NoHff_From_Template_Name(sample,new_tn,isData,Analysis_Config,lumi,year,DoMassFilter,"eventTree")
        else:
          New_Weights = Reweight_Branch_NoHff_From_Template_Name(sample,tn.split("_CMS")[0],isData,Analysis_Config,lumi,year,DoMassFilter,"eventTree") # Returns New Weights for each event
        D_Name_Temp = Discriminants.keys()
        New_D_bkg = "" # Depending on the systematic replace D_bkg with the correct syst version#
        if "res" in tn and "Up" in tn:
          New_D_bkg = "D_bkg_ResUp"
        elif "res" in tn and "Dn" in tn:
          New_D_bkg = "D_bkg_ResDown"
        elif "scale" in tn and "Up" in tn:
          New_D_bkg = "D_bkg_ScaleUp"
        elif "scale" in tn and "Up" in tn:
          New_D_bkg = "D_bkg_ScaleDown"
        else:
          New_D_bkg = "D_bkg"
        D_Name = list(map(lambda x: x.replace("D_bkg", New_D_bkg), D_Name_Temp))
        for Discriminant in D_Name:
          Discriminant_Values[Discriminant] = tree2array(tree=sample,branches=[Discriminant],top_branch_name="eventTree").astype(float);
        # Fill the histogram with the Discriminants for each template #
        Tag = tree2array(tree=sample,branches=["EventTag"],top_branch_name="eventTree").astype(int); # Need to know what category each event falls into
        Z1Flav = tree2array(tree=sample,branches=["Z1Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z1
        Z2Flav = tree2array(tree=sample,branches=["Z2Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z2
        # Make the temporary histogram for this specific sample input
        Temp_Hist = ROOT.TH1F(sample,sample,nx,xbins)
        Temp_Hist.Sumw2(True)
        for i in range(len(New_Weights)):
          if Tag[i] == category:
            if filter_final_state:
              if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                Temp_Hist.Fill(Discriminant_Values[D_Name[0]][i],New_Weights[i])
            else:
              Temp_Hist.Fill(Discriminant_Values[D_Name[0]][i],New_Weights[i])
        Temporary_Histogram_List.append(Temp_Hist)
        print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral())
      # Apply the logic for filling the combined histogram #
      # Loop over each bin and calculate the weighted average of each bin #
      for x in range(1,nx+1):
          binval=[] # list of bin values
          binerr=[] # list of error on each bin
          for hist in Temporary_Histogram_List:
            binval.append(hist.GetBinContent(x))
            binerr.append(hist.GetBinError(x))
          if "bkg" in Hypothesis_List or Combine_Production_Mode == "Sum":
            val = sum(binval)
            err = sum(i*i for i in binerr)
          else:
            val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
          Histogram_Dict[tn].SetBinContent(x,val)
          Histogram_Dict[tn].SetBinError(x,err)
      print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())         
    # Make the Output File and return the output #
    for hist in Histogram_Dict.keys():
      hlist.append(Histogram_Dict[hist])
    return Output_Name    

  elif len(Discriminants) == 2: # This will make a 2D histogram to unroll #
    # This is where we process categories with two discriminants #
    nx = len(Discriminants[D_Name[0]])-1
    ny = len(Discriminants[D_Name[1]])-1
    xbins = array.array('d',Discriminants[D_Name[0]])
    ybins = array.array('d',Discriminants[D_Name[1]])

    # Now need to reweight each sample and add Fill the histograms #
    # Loop over the input trees and return the new weights #
       
    Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
    for name in Template_Names:
      Histogram_Dict[name] = ROOT.TH2F(name,name,nx,xbins,ny,ybins) # Initialize the Histogram Dictionary with with each AC hypothesis you need
 
    for tn in Template_Names: # Choose which hypothesis to reweight to
      Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
      for sample in Samples_To_Reweight: # Loop over all samples with input production mode
        New_Weights = Reweight_Branch_NoHff_From_Template_Name(sample,tn,isData,Analysis_Config,lumi,year,DoMassFilter,"eventTree") # Returns New Weights for each event
        for Discriminant in D_Name:
          Discriminant_Values[Discriminant] = tree2array(tree=sample,branches=[Discriminant],top_branch_name="eventTree").astype(float);
        # Fill the histogram with the Discriminants for each template #
        Tag = tree2array(tree=sample,branches=["EventTag"],top_branch_name="eventTree").astype(int); # Need to know what category each event falls into
        Z1Flav = tree2array(tree=sample,branches=["Z1Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z1
        Z2Flav = tree2array(tree=sample,branches=["Z2Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z2
        # Make the temporary histogram for this specific sample input
        Temp_Hist = ROOT.TH2F(sample,sample,nx,xbins,ny,ybins)
        Temp_Hist.Sumw2(True)
        #print("Category:",category)
        for i in range(len(New_Weights)):
          if Tag[i] == category:
            if filter_final_state:
              if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                Temp_Hist.Fill(Discriminant_Values[D_Name[0]][i],Discriminant_Values[D_Name[1]][i],New_Weights[i])
            else:
              Temp_Hist.Fill(Discriminant_Values[D_Name[0]][i],Discriminant_Values[D_Name[1]][i],New_Weights[i])
        Temporary_Histogram_List.append(Temp_Hist)
        print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral())
      # Apply the logic for filling the combined histogram #
      # Loop over each bin and calculate the weighted average of each bin #
      for x in range(1,nx+1):
        for y in range(1,ny+1):
          binval=[] # list of bin values
          binerr=[] # list of error on each bin
          for hist in Temporary_Histogram_List:
            binval.append(hist.GetBinContent(x,y))
            binerr.append(hist.GetBinError(x,y))
          if "bkg" in Hypothesis_List:
            val = sum(binval)
            err = sum(i*i for i in binerr)
          else:
            val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
          Histogram_Dict[tn].SetBinContent(x,y,val)
          Histogram_Dict[tn].SetBinError(x,y,err)
      print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())         
    # Make the Output File and return the output #
    for hist in Histogram_Dict.keys():
      hlist.append(Histogram_Dict[hist])
    return Output_Name

  elif len(Discriminants) != 2:
    # Choose the first discriminant in the list to be the x axis
    nx = len(Discriminants[D_Name[0]]) - 1
    xbins = array.array('d',Discriminants[D_Name[0]])
    # Choose the second discriminant in the list to be the y axis 
    ny = len(Discriminants[D_Name[1]]) - 1 
    ybins = array.array('d',Discriminants[D_Name[1]])
    # Choose the z-axis to hold the rest of the discriminants  
    num_bins=1
    zbins = []

    for i in range(2,len(Discriminants)):
      num_bins *= len(Discriminants[D_Name[i]]) - 1
    for i in range(0,num_bins + 1):
      zbins.append(i)

    nz = len(zbins) - 1
    zbins = array.array('d',zbins)
    Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)

    for name in Template_Names:
      Histogram_Dict[name] = ROOT.TH3F(name,name,nx,xbins,ny,ybins,nz,zbins) # Initialize the Histogram Dictionary with with each AC hypothesis you need

    for tn in Template_Names: # Choose which hypothesis to reweight to
      Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
      for sample in Samples_To_Reweight: # Loop over all samples with input production mode
        if Combine_Production_Mode == "Sum" and ("bkg" not in tn): # If we need to sum over samples make sure we send the correct production mode to the weight calculator
          # Get the production mode from the sample
          temp_prod = Get_Prod_Mode_From_Sample_Name(sample)
          new_tn = temp_prod + "_" + tn.split("_")[1]
          print("new_tn: ",new_tn)
          New_Weights = Reweight_Branch_NoHff_From_Template_Name(sample,new_tn,isData,Analysis_Config,lumi,year,DoMassFilter,"eventTree")
        else:
          New_Weights = Reweight_Branch_NoHff_From_Template_Name(sample,tn,isData,Analysis_Config,lumi,year,DoMassFilter,"eventTree") # Returns New Weights for each event
        for Discriminant in D_Name:
          Discriminant_Values[Discriminant] = tree2array(tree=sample,branches=[Discriminant],top_branch_name="eventTree").astype(float)
        # Fill the histogram with the Discriminants for each template #
        Tag = tree2array(tree=sample,branches=["EventTag"],top_branch_name="eventTree").astype(int) # Need to know what category each event falls into
        Z1Flav = tree2array(tree=sample,branches=["Z1Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z1
        Z2Flav = tree2array(tree=sample,branches=["Z2Flav"],top_branch_name="eventTree").astype(int); # Need to know flavor of Z2
        # Make the temporary histogram for this specific sample input
        Temp_Hist = ROOT.TH3F(sample,sample,nx,xbins,ny,ybins,nz,zbins)
        Temp_Hist.Sumw2(True)
        # Trim the x and y axis Discriminants from the dictionary
        Discriminant_Values_Trimmed = Trim_Dict(Discriminant_Values,[D_Name[0],D_Name[1]])
        Discriminant_Trimmed = Trim_Dict(Discriminants,[D_Name[0],D_Name[1]])
        Z_bin = Get_Z_Value(Discriminant_Values_Trimmed,Discriminant_Trimmed)
        sum_weight = 0
        for i in range(len(New_Weights)):
          if Tag[i] == category:
            if filter_final_state:
              if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                Temp_Hist.Fill(Discriminant_Values[D_Name[0]][i],Discriminant_Values[D_Name[1]][i],Z_bin[i],New_Weights[i])
                sum_weight += New_Weights[i]
            else:
              Temp_Hist.Fill(Discriminant_Values[D_Name[0]][i],Discriminant_Values[D_Name[1]][i],Z_bin[i],New_Weights[i])
              sum_weight += New_Weights[i]
        print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral(),sum_weight)
        Temporary_Histogram_List.append(Temp_Hist)
      # Apply the logic for filling the combined histogram #
      # Loop over each bin and calculate the weighted average of each bin #
      for x in range (1,nx+1):
        for y in range(1,ny+1):
          for z in range(1,nz+1):
            binval=[] # list of bin values
            binerr=[] # list of error on each bin
            for hist in Temporary_Histogram_List:
              binval.append(hist.GetBinContent(x,y,z))
              binerr.append(hist.GetBinError(x,y,z))
            if "bkg" in Hypothesis_List:
              val = sum(binval)
              err = sum(i*i for i in binerr)
            else:
              val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
            Histogram_Dict[tn].SetBinContent(x,y,z,val)
            Histogram_Dict[tn].SetBinError(x,y,z,err)
      print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())
    # Make the Output File and return the output #
    for hist in Histogram_Dict.keys():
      hlist.append(Histogram_Dict[hist])
    return Output_Name
