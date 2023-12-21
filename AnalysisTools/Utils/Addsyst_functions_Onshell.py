lumi = {'2016':20,'2016APV':15.9,'2017':41.5,'2018':59.7} # Lumi Dict for placeholder

def weighted_avg(x,y,xw,yw):
    return (x*xw + y*yw)/(xw+yw)

def get_2016(syst_dict,year,final_state,category,prod_mode,syst_name):
    Has_2016 = False
    Has_2016APV = False
    try:
        Val2016APV = syst_dict["2016APV"][final_state][category][prod_mode][syst_name].split("/")
        Has_2016APV = True
    except:
        Has_2016APV = False
    try:
        Val2016 = syst_dict["2016"][final_state][category][prod_mode][syst_name].split("/")
        Has_2016 = True
    except:
        Has_2016 = False
    if (Has_2016APV and Has_2016):
        if len(Val2016) > 1:
          PullUp = weighted_avg(float(Val2016[0]),float(Val2016APV[0]),lumi["2016"],lumi["2016APV"])
          PullDown = weighted_avg(float(Val2016[1]),float(Val2016APV[1]),lumi["2016"],lumi["2016APV"])
          return str(PullUp)+"/"+str(PullDown)
        else:
          Pull = weighted_avg(float(Val2016[0]),float(Val2016APV[0]),lumi["2016"],lumi["2016APV"])
          return str(Pull)
    elif (Has_2016APV and not Has_2016):
        return str(Val2016APV[0])+"/"+str(Val2016APV[1])
    elif(not Has_2016APV and Has_2016):
        return str(Val2016[0])+"/"+str(Val2016[1])

def get_2016_Photon_SF(syst_dict,year,final_state,prod_mode,syst_name):
    Has_2016 = False
    Has_2016APV = False
    try:
        Val2016APV = syst_dict["2016APV"][final_state][prod_mode][syst_name]
        Has_2016APV = True
    except:
        Has_2016APV = False
    try:
        Val2016 = syst_dict["2016"][final_state][prod_mode][syst_name]
        Has_2016 = True
    except:
        Has_2016 = False
    if (Has_2016APV and Has_2016):
          Pull = weighted_avg(float(Val2016),float(Val2016APV),lumi["2016"],lumi["2016APV"])
          return Pull
    elif (Has_2016APV and not Has_2016):
        return Val2016APV
    elif(not Has_2016APV and Has_2016):
        return Val2016

def get_2016_Tunes(syst_dict,year,final_state,category,prod_mode):
    Has_2016 = False
    Has_2016APV = False
    try:
        Val2016APV = syst_dict["2016APV"][final_state][category][prod_mode].split("/")
        Has_2016APV = True
    except:
        Has_2016APV = False
    try:
        Val2016 = syst_dict["2016"][final_state][category][prod_mode].split("/")
        Has_2016 = True
    except:
        Has_2016 = False
    if (Has_2016APV and Has_2016):
      if len(Val2016) > 1:
        PullUp = weighted_avg(float(Val2016[0]),float(Val2016APV[0]),lumi["2016"],lumi["2016APV"])
        PullDown = weighted_avg(float(Val2016[1]),float(Val2016APV[1]),lumi["2016"],lumi["2016APV"])
        return str(PullUp)+"/"+str(PullDown)
      else:
        Pull = weighted_avg(float(Val2016[0]),float(Val2016APV[0]),lumi["2016"],lumi["2016APV"])
        return str(Pull)
    elif (Has_2016APV and not Has_2016):
        return str(Val2016APV[0])+"/"+str(Val2016APV[1])
    elif(not Has_2016APV and Has_2016):
        return str(Val2016[0])+"/"+str(Val2016[1])

def addhzzbr(lines,processes,syst_dict,year,final_state,category):
    line = "BR_hzz lnN"
    for pr in processes :
        if "bkg" not in pr : 
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " + str(round(float(get_2016(syst_dict,year,final_state,category,prod_mode,"hzz_br")),2))
                    else:   
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["hzz_br"]
        else :
             line = line + " -"
    
    lines.append(line)    

def addlumi_Uncorrelated(lines,processes,syst_dict,year,final_state,category):
    line = "lumi_13TeV_Uncorrelated_{y} lnN".format(y=year)
    for pr in processes :
        if "zjets" not in pr and "bkg_ew" not in pr:
          for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["lumi_13TeV_"+year]
        else:
          line = line + " -"
    lines.append(line)    

def addlumi_Correlated(lines,processes,syst_dict,year,final_state,category):
    line = "lumi_13TeV lnN"
    for pr in processes :
        if "zjets" not in pr and "bkg_ew" not in pr:
          for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["lumi_13TeV_"+year+"_Correlated"]
        else:
          line = line + " -"
    lines.append(line)    

def addQCDscale_muF_ggH(lines,processes,syst_dict,year,final_state,category):
    line = "QCDscale_muF_ggH lnN"
    for pr in processes :
        if "ggH" in pr :
            if "2016" in year: 
              line = line + " " + get_2016(syst_dict,year,final_state,category,"ggH","QCDscale_muF_ggH")
            else:
              line = line + " " + syst_dict[year][final_state][category]["ggH"]["QCDscale_muF_ggH"]
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addQCDscale_muF_qqH(lines,processes,syst_dict,year,final_state,category):
    line = "QCDscale_muF_qqH lnN"
    for pr in processes :
        if "qqH" in pr : 
            if "2016" in year: 
              line = line + " " + get_2016(syst_dict,year,final_state,category,"qqH","QCDscale_muF_qqH")
            else:
              line = line + " " + syst_dict[year][final_state][category]["qqH"]["QCDscale_muF_qqH"]
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addQCDscale_muF_VH(lines,processes,syst_dict,year,final_state,category):
    line = "QCDscale_muF_VH lnN"
    for pr in processes :
        if "VH" in pr : 
            if "2016" in year: 
              line = line + " " + get_2016(syst_dict,year,final_state,category,"VH","QCDscale_muF_VH")
            else:
              line = line + " " + syst_dict[year][final_state][category]["VH"]["QCDscale_muF_VH"]
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addQCDscale_muF_ttH(lines,processes,syst_dict,year,final_state,category):
    line = "QCDscale_muF_ttH lnN"
    for pr in processes :
        if "ttH" in pr : 
            if "2016" in year: 
              line = line + " " + get_2016(syst_dict,year,final_state,category,"ttH","QCDscale_muF_ttH")
            else:
              line = line + " " + syst_dict[year][final_state][category]["ttH"]["QCDscale_muF_ttH"]
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addQCDscale_muF_VV(lines,processes,syst_dict,year,final_state,category):
    line = "QCDscale_muF_VV lnN"
    for pr in processes :
        if "bkg_qqzz" in pr :
            if "2016" in year:
              line = line + " " + get_2016(syst_dict,year,final_state,category,"bkg_qqzz","QCDscale_muF_VV")
            else:
              line = line + " " + syst_dict[year][final_state][category]["bkg_qqzz"]["QCDscale_muF_VV"]
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addQCDscale_muR_ggH(lines,processes,syst_dict,year,final_state,category):
    line = "QCDscale_muR_ggH lnN"
    for pr in processes :
        if "ggH" in pr : 
            if "2016" in year: 
              line = line + " " + get_2016(syst_dict,year,final_state,category,"ggH","QCDscale_muR_ggH")
            else:
              line = line + " " + syst_dict[year][final_state][category]["ggH"]["QCDscale_muR_ggH"]
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addQCDscale_muR_qqH(lines,processes,syst_dict,year,final_state,category):
    line = "QCDscale_muR_qqH lnN"
    for pr in processes :
        if "qqH" in pr : 
            if "2016" in year: 
              line = line + " " + get_2016(syst_dict,year,final_state,category,"qqH","QCDscale_muR_qqH")
            else:
              line = line + " " + syst_dict[year][final_state][category]["qqH"]["QCDscale_muR_qqH"]
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addQCDscale_muR_VH(lines,processes,syst_dict,year,final_state,category):
    line = "QCDscale_muR_VH lnN"
    for pr in processes :
        if "VH" in pr : 
            if "2016" in year: 
              line = line + " " + get_2016(syst_dict,year,final_state,category,"VH","QCDscale_muR_VH")
            else:
              line = line + " " + syst_dict[year][final_state][category]["VH"]["QCDscale_muR_VH"]
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addQCDscale_muR_ttH(lines,processes,syst_dict,year,final_state,category):
    line = "QCDscale_muR_ttH lnN"
    for pr in processes :
        if "ttH" in pr : 
            if "2016" in year: 
              line = line + " " + get_2016(syst_dict,year,final_state,category,"ttH","QCDscale_muR_ttH")
            else:
              line = line + " " + syst_dict[year][final_state][category]["ttH"]["QCDscale_muR_ttH"]
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addQCDscale_muR_VV(lines,processes,syst_dict,year,final_state,category):
    line = "QCDscale_muR_VV lnN"
    for pr in processes :
        if "bkg_qqzz" in pr : 
            if "2016" in year:
              line = line + " " + get_2016(syst_dict,year,final_state,category,"bkg_qqzz","QCDscale_muR_VV")
            else:
              line = line + " " + syst_dict[year][final_state][category]["bkg_qqzz"]["QCDscale_muR_VV"]
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addCMS_EFF_e(lines,processes,syst_dict,year,final_state,category):
    line = "CMS_eff_e lnN"
    for pr in processes :
        if "zjets" not in pr and "bkg_ew" not in pr: 
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " + get_2016(syst_dict,year,final_state,category,prod_mode,"CMS_eff_e")
                    else:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["CMS_eff_e"]
        else :
            line = line + " -"    
    lines.append(line)

def addCMS_EFF_mu(lines,processes,syst_dict,year,final_state,category):
    line = "CMS_eff_mu lnN"
    
    for pr in processes :
        if "zjets" not in pr and "bkg_ew" not in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " + get_2016(syst_dict,year,final_state,category,prod_mode,"CMS_eff_mu")
                    else:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["CMS_eff_mu"]
        else :
            line = line + " -"
    lines.append(line)


def addZjets(lines,processes,syst_dict,year,final_state,category):
    line = "zjet_"+final_state+"_"+year+" lnN"
    
    for pr in processes :
        if "zjets" in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " + get_2016(syst_dict,year,final_state,category,prod_mode,"zjet_"+final_state+"_"+year)
                    else:    
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["zjet_"+final_state+"_"+year]
        else :
            line = line + " -"
    lines.append(line)

def addEWcorr_qqZZ(lines,processes,syst_dict,year,final_state,category):
    line = "EWcorr_qqZZ lnN"
    for pr in processes :
        if "bkg_qqzz" in pr : 
            if "2016" in year:
              line = line + " " + get_2016(syst_dict,year,final_state,category,"bkg_qqzz","EWcorr_qqZZ")  
            else:
              line = line + " " + syst_dict[year][final_state][category]["bkg_qqzz"]["EWcorr_qqZZ"]
        else :
            line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def add_pythiatune(lines,processes,syst_dict,year,final_state,category):
    line = "CMS_pythia_tune lnN"
    for pr in processes :
        if "ggH" in pr or "qqH" in pr or "ttH" in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      print(get_2016_Tunes(syst_dict,year,final_state,category,prod_mode))
                      line = line + " " + get_2016_Tunes(syst_dict,year,final_state,category,prod_mode)  
                    else:    
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]
        else :
            line = line + " -"    
    lines.append(line)

def add_pythiascale(lines,processes,syst_dict,year,final_state,category):
    line = "CMS_pythia_scale lnN"
    for pr in processes :
        if "ggH" in pr or "qqH" in pr or "ttH" in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " +get_2016(syst_dict,year,final_state,category,prod_mode,"CMS_pythia_scale")    
                    else:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["CMS_pythia_scale"]
        else :
            line = line + " -"    
    lines.append(line)

def add_pdf_Higgs_gg(lines,processes,syst_dict,year,final_state,category):
    line = "pdf_Higgs_gg lnN"
    for pr in processes :
        if "ggH" in pr or "ttH" in pr or "bkg_ggzz" in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016"in year:
                      line = line + " " + get_2016(syst_dict,year,final_state,category,prod_mode,"pdf_Higgs_gg")  
                    else:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["pdf_Higgs_gg"]
        else :
            line = line + " -"    
    lines.append(line)

def add_pdf_As_Higgs_gg(lines,processes,syst_dict,year,final_state,category):
    line = "pdf_Higgs_As_gg lnN"
    for pr in processes :
        if "ggH" in pr or "ttH" in pr or "bkg_ggzz" in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " + get_2016(syst_dict,year,final_state,category,prod_mode,"pdf_As_Higgs_gg")    
                    else:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["pdf_As_Higgs_gg"]
        else :
            line = line + " -"    
    lines.append(line)

def add_pdf_qqbar(lines,processes,syst_dict,year,final_state,category):
    line = "pdf_qqbar lnN"
    for pr in processes :
        if "bkg_qqzz" in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " + get_2016(syst_dict,year,final_state,category,prod_mode,"pdf_qqbar")  
                    else:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["pdf_qqbar"]
        else :
            line = line + " -"    
    lines.append(line)

def add_pdf_As_qqbar(lines,processes,syst_dict,year,final_state,category):
    line = "pdf_As_qqbar lnN"
    for pr in processes :
        if "bkg_qqzz" in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " + get_2016(syst_dict,year,final_state,category,prod_mode,"pdf_As_qqbar")   
                    else:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["pdf_As_qqbar"]
        else :
            line = line + " -"    
    lines.append(line)

def add_pdf_Higgs_qqbar(lines,processes,syst_dict,year,final_state,category):
    line = "pdf_Higgs_qqbar lnN"
    for pr in processes :
        if "qqH" in pr or "VH" in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " + get_2016(syst_dict,year,final_state,category,prod_mode,"pdf_Higgs_qqbar")
                    else:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["pdf_Higgs_qqbar"]
        else :
            line = line + " -"    
    lines.append(line)

def add_pdf_As_Higgs_qqbar(lines,processes,syst_dict,year,final_state,category):
    line = "pdf_As_Higgs_qqbar lnN"
    for pr in processes :
        if "qqH" in pr or "VH" in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " + get_2016(syst_dict,year,final_state,category,prod_mode,"pdf_As_Higgs_qqbar")
                    else:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["pdf_As_Higgs_qqbar"]
        else :
            line = line + " -"    
    lines.append(line)

def add_ecal_scale(lines,processes,syst_dict,year,final_state,category):
    line = "ecal lnN"
    for pr in processes :
        if "gammaH" in pr:  
            for prod_mode in syst_dict[year][final_state][category].keys():
                if prod_mode in pr:
                    if "2016" in year:
                      line = line + " " + get_2016(syst_dict,year,final_state,category,prod_mode,"CMS_pythia_scale")
                    else:
                      line = line + " " + syst_dict[year][final_state][category][prod_mode]["CMS_pythia_scale"]
        else :
            line = line + " -"    
    lines.append(line)

def Return_Yield_Scale_Photon_Scale_Factors_gammaH(year,final_state,process,yield_syst):
    #print(year,final_state,process)
    if year == "2016":
      yield_scale = get_2016_Photon_SF(yield_syst,year,final_state,process,"NewYield")
    else:
      yield_scale = yield_syst[year][final_state][process]["NewYield"]
    return yield_scale

def Return_Yield_ScaleUp_Photon_Scale_Factors_gammaH(year,final_state,process,yield_syst):
    #print(year,final_state,process)
    if year == "2016":
      yield_scale = get_2016_Photon_SF(yield_syst,year,final_state,process,"Yield_Uncertainty_Up")
    else:
      yield_scale = yield_syst[year][final_state][process]["Yield_Uncertainty_Up"]
    return yield_scale

def Return_Yield_ScaleDown_Photon_Scale_Factors_gammaH(year,final_state,process,yield_syst):
    #print(year,final_state,process)
    if year == "2016":
      yield_scale = get_2016_Photon_SF(yield_syst,year,final_state,process,"Yield_Uncertainty_Down")
    else:
      yield_scale = yield_syst[year][final_state][process]["Yield_Uncertainty_Down"]
    return yield_scale

def Return_Yield_Scale_Photon_Scale_Factors_Uncertainty(lines,processes,Photon_SF_Scale_Dictionary,yield_change_up,yield_change_down,year,final_state,rate,Event_Tag):
    line = "ID_SF lnN"
    for i in range(len(processes)) : 
        if not "bkg" in processes[i]: 
          for prod_mode in Photon_SF_Scale_Dictionary[year][final_state].keys():
            if prod_mode in processes[i]:
              try:
                if Event_Tag == "gammaH":
                    line = line + " " + str(Photon_SF_Scale_Dictionary[year][final_state][prod_mode]["Yield_Uncertainty_Up"])+"/"+str(Photon_SF_Scale_Dictionary[year][final_state][prod_mode]["Yield_Uncertainty_Down"])
                if Event_Tag == "Untagged":
                    line = line + " " + str((rate[i] - yield_change_up[year][final_state][processes[i]])/rate[i]) +"/"+ str((rate[i] - yield_change_down[year][final_state][processes[i]])/rate[i])
              except: line = line + " -"

        else:
          line = line + " -"

    lines.append(line)