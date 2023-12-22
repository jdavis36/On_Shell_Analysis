import os, glob
import sys
import ROOT
import copy

# What this script does is trim and rename the template files and prepare them for the datacards.
# The expected input is a list of templates that would belong to the sample datacard.

#========================== How to run this ===========================
# 1. First argument is the name of the template you want to create

# 2. The next arguments are all of the input root files with the histrograms needed
def Make_Template_With_Fake_Data(OutName,names):
  # OutName = Output Root File Name
  # names = Input Root Files 

  hists = [] # Holds the histograms to add to the final TFile
  used_names = [] # Stores the names of the histrograms 

  for nm in names:
    fin = ROOT.TFile.Open(nm)
    for key in fin.GetListOfKeys():
      if "TH1F" in key.GetClassName():
        h_name = key.GetName()
        h_temp = fin.Get(h_name)
        h_temp.SetDirectory(0)
        if h_name not in used_names:
          #print(h_name)
          hists.append(h_temp)
          used_names.append(h_name)
    fin.Close()

  fout =  ROOT.TFile.Open(OutName,"recreate")
  fout.cd()

  # Now we will combine all of the Wplus Wminus and ZH templates into a single VH template
  WplusH_Hists = []
  WminusH_Hists = []
  ZH_Hists = []
  VH_Hists = []
  VH_Names = []
  hists_temp_copy = []
  for hist in hists:
    h_name = hist.GetName()
    #print(h_name)
    if "WplusH" in h_name:
      WplusH_Hists.append(hist)
      if h_name.split("WplusH_")[1] not in VH_Names:
        VH_Names.append(h_name.split("WplusH_")[1])
    elif "WminusH" in h_name:
      WminusH_Hists.append(hist)
      if h_name.split("WminusH_")[1] not in VH_Names:
        VH_Names.append(h_name.split("WminusH_")[1])
    elif "ZH" in h_name:
      ZH_Hists.append(hist)
      if h_name.split("ZH_")[1] not in VH_Names:
        VH_Names.append(h_name.split("ZH_")[1])
    else:
      hists_temp_copy.append(hist)
  
  hists = hists_temp_copy
  #print("VH: ",VH_Names) 
  for name in VH_Names:
    VH_comb = []
    for hist in ZH_Hists:
      if "ZH_" + name == hist.GetName():
        VH_comb.append(hist) 
    for hist in WplusH_Hists:
      if "WplusH_"+name == hist.GetName():
        VH_comb.append(hist) 
    for hist in WminusH_Hists:
      if "WminusH_"+name == hist.GetName():
        VH_comb.append(hist) 
    VH_Hist = VH_comb[0].Clone("VH_"+name)
    for i in range(1,len(VH_comb)):
      VH_Hist.Add(VH_comb[i])
    hists.append(VH_Hist)
  
  # Make a fake data histogram if need be#
  Make_Fake_Data = True
  if Make_Fake_Data:
    Fake_Data = []
    for hist in hists:
      h_name = hist.GetName()
      print(h_name)
      if ("0PM" in h_name) and ("gammaH" not in h_name):
        Fake_Data.append(hist)
        print(hist.Integral())
      if"gammaH_0PM" in hist.GetName():
        print("gammaH: ",hist.Integral())
        hist.Scale(4000)
        Fake_Data.append(hist)
      if "bkg" in h_name:
        Fake_Data.append(hist)
        print(hist.Integral())

    Fake_Data_Hist = Fake_Data[0].Clone("data_obs")
    for i in range(1,len(Fake_Data)):
      Fake_Data_Hist.Add(Fake_Data[i])
    
    Fake_Data_Hist.Write("data_obs")

  for hist in hists:
    # Unscale the gammaH_0PM histogram to keep the shape #
    if ("bkg_ew_negative" not in hist.GetName()):
      if ("bkg_ew_positive" in hist.GetName()):
        hist.Write("bkg_ew")
      elif ("gammaH_0PM" in hist.GetName()):
        hist.Scale(1/4000)
        hist.Write()
      else:
        if hist.Integral() != 0 or ("data_obs" in hist.GetName()):
          print(hist.GetName()) 
          hist.Write()
      
  print(OutName)

def main():
  output_dir = sys.argv[2]
  if not os.path.exists(output_dir):
      os.mkdir(output_dir)
  output_dir = output_dir.strip("/")
  Input_Dir = sys.argv[1]
  for filename in glob.iglob(Input_Dir+'/**', recursive=True):
    if os.path.isfile(filename) and (".root" in filename):
      out_ext=filename
      if "/" in filename:
        out_ext = filename.split("/")[-1]
        out_ext = out_ext.split(".")[0]+".input."+out_ext.split(".")[1]
      print("Parsing Root File: ",filename)
      Make_Template_With_Fake_Data(output_dir+"/"+out_ext,[filename]) 

if __name__ == "__main__":
    main()

