import sys
import os, glob
import ROOT as ROOT
from AnalysisTools.Utils import Config

# This script takes the output of the make all templates script as input
# The input should be a path to the directory which includes all Templates for each category and production mode
# Input will be parsed according to the event tag string in the filenames 

Input_Dir = sys.argv[1]

# Make the output directory 
Input_Dir=Input_Dir.strip("/")

# Recursively look for all names with a given event tag by looping over each tag 
#Analysis_Config = Config.Analysis_Config("OnShell_HVV_Photons_2021")
Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only")
Categories = Analysis_Config.Event_Categories

#names = ["data_obs"]
#Integral_Original = [69.564133]
#Integral_New_Scale = [53.0]
names =             ["ggH_0PM",     "ggH_0PH",    "ggH_0M",     "ggH_0L1",   "ggH_0L1Zg",  "ggH_g11g21_negative","ggH_g11g21_positive","ggH_g11g41_negative","ggH_g11g41_positive","ggH_g11g1prime21_negative","ggH_g11g1prime21_positive","ggH_g11ghzgs1prime21_negative","ggH_g11ghzgs1prime21_positive","ggH_g41g21_positive","ggH_g41g21_negative", "ggH_g41g1prime21_positive", "ggH_g41g1prime21_negative", "ggH_g41ghzgs1prime21_positive" ,"ggH_g41ghzgs1prime21_negative", "ggH_g21g1prime21_positive", "ggH_g21ghzgs1prime21_positive", "ggH_g21ghzgs1prime21_negative","bkg_zjets"  ,"bkg_ew"      ,"bkg_ggzz"   ,"bkg_qqzz"]
Integral_Original = [24.72699754181,9.96584854489,3.73711843119,16.8718792650,41.7620697835,0                    ,27.4174253455        ,1.38581349826       ,1.38152976809        ,0                          ,40.2327150575              ,0.41542207                     ,5.6260693                      ,13.666246    ,0.81226886    ,1.0268837    ,25.731580    ]
Integral_New_Scale = [20.7753759913,8.41171466474,3.11752165042,14.1603049704,35.0320542425,0                    ,23.1291367528        ,1.15082743223       ,1.15082743223        ,0                          ,33.7806934644              ,0.365910884178                 ,4.75400013804                  ,0.79322967           ,0.79322967           ,0.91936218,                 ,0.91936218                  , 0.38196288                      ,0.38196288                     ,19.153566                   ,2.7907363                       ,0.39789110                      ,9.52875918036,0.380308997829,1.91799129308,24.7374685035]

for filename in glob.iglob(Input_Dir+'/**', recursive=True):
  if os.path.isfile(filename):
    fin = ROOT.TFile(filename,"update")
    for key in fin.GetListOfKeys():
      #print(key.GetName())
      if "TH1F" in key.GetClassName():
        h_name = key.GetName()
        h_temp = fin.Get(h_name)
        h_temp.SetDirectory(0)
        print(h_name)
        if h_name in names:
          index = names.index(h_name)
          if Integral_Original[index] != 0 :
            h_temp.Scale(Integral_New_Scale[index]/h_temp.Integral())
            h_temp.Write()
    fin.Close()

  # After saving all relevant histograms #
  # Combine all histograms with the the same names #
