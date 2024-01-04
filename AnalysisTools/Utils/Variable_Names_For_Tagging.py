def TagAC19():
    Names = ["pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal","pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal","pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal","pConst_JJVBF_BKG_MCFM_JECNominal",
            "pConst_HadZH_BKG_MCFM_JECNominal","pConst_HadWH_BKG_MCFM_JECNominal","pConst_JJQCD_BKG_MCFM_JECNominal","p_HadZH_mavjj_true_JECNominal","p_HadWH_mavjj_true_JECNominal",
            "p_JVBF_SIG_ghv1_1_JHUGen_JECNominal",
            "pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal",
            "p_HadWH_mavjj_JECNominal",
            "p_HadWH_SIG_ghw1_1_JHUGen_JECNominal",
            "p_HadZH_mavjj_JECNominal",
            "p_HadZH_SIG_ghz1_1_JHUGen_JECNominal",
            "nExtraLep",  
            "nExtraZ",
            "nCleanedJetsPt30",
            "nCleanedJetsPt30BTagged_bTagSF",  
            "JetQGLikelihood", 
            "p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal",  
            "p_JQCD_SIG_ghg2_1_JHUGen_JECNominal",
            "p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal", 
            "p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal",
            "p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal",
            "p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal",
            "p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal",
            "p_JVBF_SIG_ghv1_1_JHUGen_JECNominal",
            "pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal",  
            "p_HadWH_SIG_ghw1_1_JHUGen_JECNominal",  
            "p_HadWH_SIG_ghw2_1_JHUGen_JECNominal",  
            "p_HadWH_SIG_ghw4_1_JHUGen_JECNominal",  
            "p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal",  
            "p_HadZH_SIG_ghz1_1_JHUGen_JECNominal",
            "p_HadZH_SIG_ghz2_1_JHUGen_JECNominal",   
            "p_HadZH_SIG_ghz4_1_JHUGen_JECNominal",   
            "p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal",   
            "p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal",  
            "p_HadWH_mavjj_JECNominal",  
            "p_HadWH_mavjj_true_JECNominal",  
            "p_HadZH_mavjj_JECNominal",
            "p_HadZH_mavjj_true_JECNominal",  
            "JetPhi",  
            "ZZMass",  
            "ZZPt",  
            "PFMET",
            "PhotonIsCutBasedLooseID"]

    return Names

def TagUntagged_Plus_GammaH():
    Names = ["PhotonPt","PhotonIsCutBasedLooseID"]
    return Names

def TagUntagged_Plus_qqGammaH():
    Names = ["PhotonPt","PhotonIsCutBasedTightID"]
    return Names

def Return_Needed_From_Discriminants_To_Calculate(Analysis_Config):
    Names = []
    if "Pt4l" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["ZZPt"])
    #===== Calculating Useful Info for OnShell Discriminants ======
    DoDiJet = False
    for name in Analysis_Config.Discriminants_To_Calculate:
        if "VBF" in name or "VH" in name:
            DoDiJet = True
    if DoDiJet:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal"])
    #================ Calculating AC discriminants ================
    if "D_0minus_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghz4_1_JHUGen"])
    if "D_CP_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_ghz4_1_JHUGen","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghz4_1_JHUGen"])
    if "D_0hplus_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghz2_1_JHUGen"])
    if "D_int_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_ghz2_1_JHUGen","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghz2_1_JHUGen"])
    if "D_L1_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen"])
    if "D_L1int_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_ghz1prime2_1E4_JHUGen","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen"])
    if "D_L1Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen"])
    if "D_L1Zgint_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_ghza1prime2_1E4_JHUGen","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen"])
    if "D_L1L1Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen", "p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen"])
    if "D_L1L1Zgint_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1prime2_1E4_ghza1prime2_1E4_JHUGen","p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen","p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen"])
    if "D_0minus_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghza4_1_JHUGen"])
    if "D_CP_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_ghza4_1_JHUGen","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghza4_1_JHUGen"])
    if "D_0hplus_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghza2_1_JHUGen"])
    if "D_int_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_ghza2_1_JHUGen","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_ghza2_1_JHUGen"])
    if "D_0minus_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_gha4_1_JHUGen"])
    if "D_CP_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_gha4_1_JHUGen","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_gha4_1_JHUGen"])
    if "D_0hplus_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_gha2_1_JHUGen"])
    if "D_int_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_gha2_1_JHUGen","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_GG_SIG_ghg2_1_gha2_1_JHUGen"])
    #=============== Calculating VBF Discriminants ================
    if "D_0minus_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal"])
    if "D_CP_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_ghv4_1_JHUGen_JECNominal","p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal"])
    if "D_0hplus_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal"])
    if "D_int_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_ghv2_1_JHUGen_JECNominal","p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal"])
    if "D_L1_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal"])
    if "D_L1int_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_ghv1prime2_1E4_JHUGen_JECNominal","p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal"])
    if "D_L1Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal"])
    if "D_L1Zgint_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_ghza1prime2_1E4_JHUGen_JECNominal","p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal"])
    if "D_0minus_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal"])
    if "D_CP_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_ghza4_1_JHUGen_JECNominal","p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal"])
    if "D_0hplus_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal"])
    if "D_int_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_ghza2_1_JHUGen_JECNominal","p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal"])
    #=============== Calculating VBF with Decay Discriminants ================
    if "D_0minus_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz4_1_JHUGen"])
    if "D_0hplus_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz2_1_JHUGen"])
    if "D_L1_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen"])
    if "D_L1Zg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen"])
    if "D_0minus_Zg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghza4_1_JHUGen"])
    if "D_0hplus_Zg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghza2_1_JHUGen"])
    if "D_0minus_gg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_JJVBF_SIG_gha4_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_gha4_1_JHUGen"])
    if "D_0hplus_gg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_JJVBF_SIG_gha2_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_gha2_1_JHUGen"])
    #=========== Calculating VH Hadronic Discriminants ============
        Names.extend(["p_HadWH_mavjj_JECNominal","p_HadWH_mavjj_true_JECNominal","pConst_HadWH_SIG_ghw1_1_JHUGen_JECNominal"])
        Names.extend(["p_HadZH_mavjj_JECNominal","p_HadZH_mavjj_true_JECNominal","pConst_HadZH_SIG_ghz1_1_JHUGen_JECNominal"])
    if "D_0minus_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadWH_SIG_ghw4_1_JHUGen_JECNominal","p_HadZH_SIG_ghz4_1_JHUGen_JECNominal"])
    if "D_CP_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadZH_SIG_ghz1_1_ghz4_1_JHUGen_JECNominal","p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadWH_SIG_ghw4_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz4_1_JHUGen_JECNominal"])
    if "D_0hplus_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadWH_SIG_ghw2_1_JHUGen_JECNominal","p_HadZH_SIG_ghz2_1_JHUGen_JECNominal"])
    if "D_int_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadZH_SIG_ghz1_1_ghz2_1_JHUGen_JECNominal","p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadWH_SIG_ghw2_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadWH_SIG_ghw2_1_JHUGen_JECNominal"])
    if "D_L1_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal","p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal"])
    if "D_L1int_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_ghw1prime2_1E4_JHUGen_JECNominal","p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal"])
    if "D_L1Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal"])
    if "D_L1Zgint_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal"])
    if "D_0minus_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_ghza4_1_JHUGen_JECNominal"])
    if "D_CP_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadZH_SIG_ghz1_1_ghza4_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_ghza4_1_JHUGen_JECNominal"])
    if "D_0hplus_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_ghza2_1_JHUGen_JECNominal"])
    if "D_int_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadZH_SIG_ghz1_1_ghza2_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_ghza2_1_JHUGen_JECNominal"])
    if "D_0minus_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_gha4_1_JHUGen_JECNominal"])
    if "D_CP_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadZH_SIG_ghz1_1_gha4_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_gha4_1_JHUGen_JECNominal"])
    if "D_0hplus_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_gha2_1_JHUGen_JECNominal"])
    if "D_int_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadZH_SIG_ghz1_1_gha2_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_HadZH_SIG_gha2_1_JHUGen_JECNominal"])
    #============== Calculating VH Decay Discriminants ============
    if "D_0minus_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_HadWH_SIG_ghw4_1_JHUGen_JECNominal","p_HadZH_SIG_ghz4_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz4_1_JHUGen"])
    if "D_0hplus_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_HadWH_SIG_ghw2_1_JHUGen_JECNominal","p_HadZH_SIG_ghz2_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz2_1_JHUGen"])
    if "D_L1_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal","p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen"])
    if "D_L1Zg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen"])
    if "D_0minus_Zg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_HadZH_SIG_ghza4_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghza4_1_JHUGen"])
    if "D_0hplus_Zg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_HadZH_SIG_ghza2_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghza2_1_JHUGen"])
    if "D_0minus_gg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_HadZH_SIG_gha4_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_gha4_1_JHUGen"])
    if "D_0hplus_gg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_SIG_ghz1_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_HadZH_SIG_gha2_1_JHUGen_JECNominal","p_GG_SIG_ghg2_1_gha2_1_JHUGen"])
    #================ Calculating BKG discriminants ===============
    if "D_bkg" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_m4l_SIG","p_QQB_BKG_MCFM","p_m4l_BKG"])
    if "D_bkg_ResUp" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_m4l_SIG_ResUp","p_QQB_BKG_MCFM","p_m4l_BKG_ResUp"])
    if "D_bkg_ResDown" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_m4l_SIG_ResDown","p_QQB_BKG_MCFM","p_m4l_BKG_ResDown"])
    if "D_bkg_ScaleUp" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_m4l_SIG_ScaleUp","p_QQB_BKG_MCFM","p_m4l_BKG_ScaleUp"])
    if "D_bkg_ScaleDown" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_GG_SIG_ghg2_1_ghz1_1_JHUGen","p_m4l_SIG_ScaleDown","p_QQB_BKG_MCFM","p_m4l_BKG_ScaleUp"])
    if "D_bkg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal","p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal","p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal","p_JJVBF_BKG_MCFM_JECNominal","p_HadZH_BKG_MCFM_JECNominal","p_HadWH_BKG_MCFM_JECNominal","p_JJQCD_BKG_MCFM_JECNominal","p_HadZH_mavjj_JECNominal","p_HadZH_mavjj_true_JECNominal","p_HadWH_mavjj_JECNominal","p_HadWH_mavjj_true_JECNominal","pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal","pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal","pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal","pConst_JJVBF_BKG_MCFM_JECNominal","pConst_HadZH_BKG_MCFM_JECNominal","pConst_HadWH_BKG_MCFM_JECNominal","pConst_JJQCD_BKG_MCFM_JECNominal","p_m4l_BKG","p_m4l_SIG"])
    if "D_bkg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
        Names.extend(["p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal","p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal","p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal","p_JJVBF_BKG_MCFM_JECNominal","p_HadZH_BKG_MCFM_JECNominal","p_HadWH_BKG_MCFM_JECNominal","p_JJQCD_BKG_MCFM_JECNominal","p_HadZH_mavjj_JECNominal","p_HadZH_mavjj_true_JECNominal","p_HadWH_mavjj_JECNominal","p_HadWH_mavjj_true_JECNominal","pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal","pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal","pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal","pConst_JJVBF_BKG_MCFM_JECNominal","pConst_HadZH_BKG_MCFM_JECNominal","pConst_HadWH_BKG_MCFM_JECNominal","pConst_JJQCD_BKG_MCFM_JECNominal","p_m4l_BKG","p_m4l_SIG"])

    return Names

def Needed_For_All():
    Names = ["Z1Flav","Z2Flav","ZZMass"]
    return Names

def Get_Scale_Values():
    Names = ["p_HadWH_mavjj_JECNominal","p_HadWH_mavjj_true_JECNominal","pConst_HadWH_SIG_ghw1_1_JHUGen_JECNominal","p_HadZH_mavjj_JECNominal","p_HadZH_mavjj_true_JECNominal","pConst_HadZH_SIG_ghz1_1_JHUGen_JECNominal"]
    return Names