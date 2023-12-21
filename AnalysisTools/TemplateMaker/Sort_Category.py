def sort_category_templates(Analysis_Config,prod):
   if Analysis_Config.name in("OnShell_HVV_Photons_2021","gammaH_Photons_Decay_Only","gammaH_Photons_Decay_Only_Optimal_Binning","gammaH_Photons_Decay_Only_Kinematics","Test_Optimal_Binning_All_Untagged"):
     p_sorted = False
     print(prod)
     if "ZZTo4l" in prod and ("Contin" not in prod): 
       prod = "qqZZ"
       p_sorted = True
     elif any(x in prod for x in ["ggTo4e","ggTo2e2mu","ggTo2e2tau","ggTo2mu2tau","ggTo4mu","ggTo4tau"]): 
       prod = "ggZZ"
       p_sorted = True
     elif all(x in prod for x in ["VBF","Contin"]) or prod in ["TTLToLL_M1to0_MLM","TTZToLLNuNu_M10","TTZJets_M10_MLM","TTZZ","TTWW","ZZZ","WWZ","WZZ"] or prod in ["OffshellAC"]: 
       prod = "ew_bkg"
       p_sorted = True
     elif 'Data' in prod:
       prod = "ZX"
       p_sorted = True
     elif 'ggH' in prod:
       prod = "ggH"
       p_sorted = True
     elif 'VBF' in prod:
       prod = "VBF"
       p_sorted = True
     elif 'Wplus' in prod:
       prod = "WplusH"
       p_sorted = True
     elif 'Wminus' in prod:
       prod = "WminusH"
       p_sorted = True
     elif 'ZH' in prod and not 'ggZH' in prod:
       prod = "ZH"
       p_sorted = True
     elif 'ggZH' in prod:
       prod = "ggZH"
       p_sorted = True
     elif 'bbH' in prod:
       prod = 'bbH'
       p_sorted = True
     elif 'ttH' in prod:
       prod = 'ttH'
       p_sorted = True
     elif ('tHW' in prod) or ('tqH' in prod):
       prod = 'tH'
       p_sorted = True
     elif 'gammaH' in prod:
       prod = "gammaH" 
       p_sorted = True
     return prod,p_sorted 
   elif Analysis_Config.name in("gammaH_Photons_Decay_Only_Kinematics_Photon_Rate","Tree_Level_qqH_Photons_XS"):
     p_sorted = False
     if "ZZTo4l" in prod and ("OffshellAC" not in prod): 
       prod = "qqZZ"
       p_sorted = True
     elif any(x in prod for x in ["ggTo4e","ggTo2e2mu","ggTo2e2tau","ggTo2mu2tau","ggTo4mu","ggTo4tau"]): 
       prod = "ggZZ"
       p_sorted = True
     elif all(x in prod for x in ["VBF","Contin"]) or prod in ["TTLToLL_M1to0_MLM","TTZToLLNuNu_M10","TTZJets_M10_MLM","TTZZ","TTWW","ZZZ","WWZ","WZZ"] or prod in ["OffshellAC"]: 
       prod = "ew_bkg"
       p_sorted = True
     elif 'Data' in prod:
       prod = "ZX"
       p_sorted = True
     elif any(x in prod for x in ["ggH"]):
       prod = "ggH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x in prod for x in ["VBF"]):
       prod = "VBFH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x in prod for x in ["Wplus"]):
       prod = "WplusH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x in prod for x in ["Wminus"]):
       prod = "WminusH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x in prod for x in ["ZH","ggZH"]):
       prod = "ZH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x in prod for x in ["bbH"]):
       prod = "bbH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x in prod for x in ["ttH","tHW","tqH"]):
       prod = "ttH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x == prod for x in ["uuH","ddH","ssH","ccH"]) : #Since we cannot rewieght these samples yet have to treat them all separately 
       prod = prod 
       p_sorted = True   
     elif 'gammaH' in prod:
       prod = "gammaH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     print(prod)
     return prod,p_sorted 
   return prod,p_sorted 

def sort_category_systematics(Analysis_Config,prod):
  if Analysis_Config.name in("gammaH_Photons_Decay_Only_Kinematics_Photon_Rate"):
     p_sorted = False
     if "ZZTo4l" in prod and ("OffshellAC" not in prod): 
       prod = "qqZZ"
       p_sorted = True
     elif any(x in prod for x in ["ggTo4e","ggTo2e2mu","ggTo2e2tau","ggTo2mu2tau","ggTo4mu","ggTo4tau"]): 
       prod = "ggZZ"
       p_sorted = True
     elif all(x in prod for x in ["VBF","Contin"]) or prod in ["TTLToLL_M1to0_MLM","TTZToLLNuNu_M10","TTZJets_M10_MLM","TTZZ","TTWW","ZZZ","WWZ","WZZ"] or prod in ["OffshellAC"]: 
       prod = "ew_bkg"
       p_sorted = True
     elif 'Data' in prod:
       prod = "ZX"
       p_sorted = True
     elif any(x in prod for x in ["ggH"]):
       prod = "ggH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x in prod for x in ["VBF"]):
       prod = "qqH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x in prod for x in ["Wplus","Wminus","ZH","ggZH"]):
       prod = "VH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x in prod for x in ["bbH"]):
       prod = "bbH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x in prod for x in ["ttH","tHW","tqH"]):
       prod = "ttH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     elif any(x == prod for x in ["uuH","ddH","ssH","ccH"]): #Since we cannot rewieght these samples yet have to treat them all separately 
       prod = prod 
       p_sorted = True 
     elif 'gammaH' in prod:
       prod = "gammaH" # In this analysis we only consider decay information so we will call this production ggH in the meantime
       p_sorted = True
     print(prod)
     return prod,p_sorted 

