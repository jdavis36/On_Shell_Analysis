import math

def checkNegative(var):
    return any( val<0 for val in var )

def checkZero(var):
    return any( val==0 for val in var )

def checkNanInf(var):
    return any( ( math.isnan(val) or math.isinf(val) ) for val in var )

def HadWH_Scale_Nominal(p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,pConst_HadWH_SIG_ghw1_1_JHUGen_JECNominal):
  return p_HadWH_mavjj_JECNominal / p_HadWH_mavjj_true_JECNominal / pConst_HadWH_SIG_ghw1_1_JHUGen_JECNominal

def HadZH_Scale_Nominal(p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,pConst_HadZH_SIG_ghz1_1_JHUGen_JECNominal):
  return p_HadZH_mavjj_JECNominal / p_HadZH_mavjj_true_JECNominal / pConst_HadZH_SIG_ghz1_1_JHUGen_JECNominal

def R_ZZ_Zy_yy(ghz1 = 0, ghz2 = 0, ghz4 = 0, g1prime2 = 0, ghzgs1prime2 = 0, ghzgs2=0, ghzgs4=0, ghgsgs2 = 0 ,ghgsgs4 = 0, **kwargs):
  Rate = ((ghz1/2)**2 + 0.17*(g1prime2)**2 + 0.09*(ghz2)**2 + 0.04*(ghz4)**2 + 0.10*(ghzgs1prime2)**2 + 79.95*(ghzgs2)**2 +75.23*(ghzgs4)**2 
  + 29.00*(ghgsgs2)**2 + 29.47*(ghgsgs4)**2 + 0.81*(ghz1/2)*g1prime2 + 0.50*(ghz1/2)*ghz2 - 0.19*(ghz1/2)*ghzgs2 - 1.56*(ghz1/2)*ghzgs2
  + 0.06*(ghz1/2)*ghgsgs2 + 0.21*g1prime2*ghz2 - 0.07*g1prime2*ghzgs1prime2 - 0.64*g1prime2*ghzgs2 -0.05*ghz2*ghzgs1prime2 - 0.51*ghz2*ghzgs2
  - 0.02*ghz2*ghgsgs2 + 0.36*ghz4*ghzgs4 - 0.57*ghz4*ghgsgs4 + 1.80*ghzgs1prime2*ghzgs2 - 0.05*ghzgs1prime2*ghgsgs2 -1.84*ghzgs2*ghgsgs2 
  - 2.09*ghzgs4*ghgsgs4)

  return Rate

def gammaH_XS(ghzgs2=0,ghzgs4=0,ghgsgs2=0,ghgsgs4=0,**kwargs):
  Rate = ghzgs2**2 + ghzgs4**2 + 0.553*ghgsgs2**2+0.553*ghgsgs4**2 - 0.578*ghzgs2*ghgsgs2 - 0.578*ghzgs4*ghgsgs4
  Ref_XS = 1.33*10**1#pb
  return Ref_XS * Rate

def Get_SM_Xsec_Scale(production,year):
  xsec = None
  genxsec = None
  genBR = None 
  if "ggH" in production:
    if year == 2016:
      xsec = 0.0133352
      genxsec = 29.989999
      genBR = 0.0002744
    elif year == 2017:
      xsec = 0.0133352
      genxsec = 30.018800
      genBR = 0.0002744
    elif year == 2018:
      xsec = 0.0133352
      genxsec = 30.018800
      genBR = 0.0002744
    else:
      raise ValueError("Invalid Year for the Sample")
  elif "VBF" in production:
    if year == 2016:
      xsec = 0.0010381
      genxsec = 3.7690000
      genBR = 0.0002744
    elif year == 2017:
      xsec = 0.0010381
      genxsec = 3.7690000
      genBR = 0.0002744
    elif year == 2018:
      xsec = 0.0010381
      genxsec = 3.7690000
      genBR = 0.0002744
    else:
      raise ValueError("Invalid Year for the Sample")
  elif "ZH" in production:
    if year == 2016:
      xsec = 0.0006228
      genxsec = 0.75182
      genBR = 0.00074903
    elif year == 2017:
      xsec = 0.0006228
      genxsec = 0.75182
      genBR = 0.00074903
    elif year == 2018:
      xsec = 0.0006228
      genxsec = 0.75182
      genBR = 0.00074903
    else:
      raise ValueError("Invalid Year for the Sample")
  elif "WplusH" in production:
    if year == 2016:
      xsec = 0.0002305
      genxsec = 0.75182
      genBR = 0.0002745
    elif year == 2017:
      xsec = 0.0002305
      genxsec = 0.85
      genBR = 0.0002745
    elif year == 2018:
      xsec = 0.0002305
      genxsec = 0.85
      genBR = 0.0002745
    else:
      raise ValueError("Invalid Year for the Sample")
  elif "WplusH" in production:
    if year == 2016:
      xsec = 0.0001462
      genxsec = 0.5343000
      genBR = 0.0002744
    elif year == 2017:
      xsec = 0.0001462
      genxsec = 0.5343000
      genBR = 0.0002744
    elif year == 2018:
      xsec = 0.0001462
      genxsec = 0.5343000
      genBR = 0.0002744
    else:
      raise ValueError("Invalid Year for the Sample")
  elif "bbH" in production:
    if year == 2016:
      xsec = 0.0001346
      genxsec = 0.4880000
      genBR = 0.0002760
    elif year == 2017:
      xsec = 0.0001346
      genxsec = 0.4880000
      genBR = 0.0002760
    elif year == 2018:
      xsec = 0.0001346
      genxsec = 0.4880000
      genBR = 0.0002760
    else:
      raise ValueError("Invalid Year for the Sample")
  elif "ttH" in production:
    if year == 2016:
      xsec = 0.0003901
      genxsec = 0.5070999
      genBR = 0.0007694 
    elif year == 2017:
      xsec = 0.0003901
      genxsec = 0.5070999
      genBR = 0.0007694 
    elif year == 2018:
      xsec = 0.0003901
      genxsec = 0.5070999
      genBR = 0.0007694 
    else:
      raise ValueError("Invalid Year for the Sample")
  elif "gammaH" in production:
      return 1
  elif "bkg" in production:
      return 1
  else:
     return 1

  return xsec/(genxsec*genBR)

def Convert_Final_State_String_To_ZZ_Flav(Final_State):
  Final_State_Check = ""
  if Final_State == "4e":
    Final_State_Check = 11**2 * 11**2
  elif Final_State == "4mu":
    Final_State_Check = 13**2 * 13**2
  elif Final_State == "2e2mu":
    Final_State_Check = 11**2 * 13**2
  else:
    raise ValueError ("Invalid Final State in Calc_Systematics")
  return Final_State_Check