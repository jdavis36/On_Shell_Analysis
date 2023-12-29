import os, glob
import sys 
import ROOT as ROOT 
from AnalysisTools.Utils import Config
import getopt

# This script takes the output of the make all templates script as input
# The input should be a path to the directory which includes all Templates for each category and production mode
# Input will be parsed according to the event tag string in the filenames 

def main(argv):
  inputdir = ''
  outputdir = ''
  configname = ''
  try:
    opts, args = getopt.getopt(argv,"hi:o:cf",["ifile=","ofile=","config="])
  except getopt.GetoptError:
    print('Collect_Templates.py -i <treelistpath> -o <output_directory> --config <config_file>')
    sys.exit(2)
  for opt, arg, in opts:
    if opt == '-h':
      print('Collect_Templates.py -i <treelistpath> -o <output_directory> -config <config_file>')
      sys.exit()
    elif opt in ("-i", "--ifile"):
        inputdir = arg
    elif opt in ("-o", "--ofile"):
        outputdir = arg
    elif opt in ("-cf", "--config"):
        configname = arg
  if not all([inputdir, outputdir, configname]):
        print('Collect_Templates.py -i <treelistpath> -o <output_directory> -config <config_file>')
        sys.exit(2)
  if not outputdir.endswith("/"):
        outputdir = outputdir+"/"
    
  print(inputdir,outputdir,configname)
  Input_Dir = inputdir
  Output_Dir = outputdir


  if not os.path.exists(Output_Dir):
    os.mkdir(Output_Dir)

  # Make the output directory 
  Input_Dir=Input_Dir.strip("/")
  Output_Dir=Output_Dir.strip("/")
  Analysis_Config = Config.Analysis_Config(configname)
  Categories = Analysis_Config.Event_Categories
  Coupling_Name = Analysis_Config.Coupling_Name
  Final_States = Analysis_Config.Final_States
  TreeFile = Analysis_Config.TreeFile

  for Final_State in Final_States:
    for Year in ["2016","2017","2018"]: # Only to make sure we combine the 2016APV and 2016 datasets
      for cat in Categories:
        Temp_Hist_List = []
        used_names = []
        for filename in glob.iglob(Input_Dir+'/**', recursive=True):
          # Handle possible extenstions/ file paths with weird naming conventions
          root_name = filename.split("/")[-1]
          #Unforunately had to add something to stop double counting gammaH files since gammaH is a category and a production mode ... (Maybe Fix this?)
          if cat == 'gammaH' and any( category in filename for category in ['Untagged']): continue
          if os.path.isfile(filename) and (cat in root_name) and (Year in root_name) and (Final_State in root_name) and (TreeFile in root_name)  and ('unrolled' in filename): # filter dirs
            fin = ROOT.TFile(filename)
            print(filename)
            for key in fin.GetListOfKeys():
              if "TH1F" in key.GetClassName():
                h_name = key.GetName()
                h_temp = fin.Get(h_name)
                h_temp.SetDirectory(0)
                #print(h_name)
                if h_name not in used_names:
                  Temp_Hist_List.append(h_temp)
                  used_names.append(h_name)
                elif h_name == "ggH_0L1" and "0L1Zg" in used_names: 
                  #print("/n/n/n/n/n HERE")
                  Temp_Hist_List.append(h_temp)
                  used_names.append(h_name)
                else: 
                # Find the name in the histogram
                  Temp_Hist_List.append(h_temp)
            fin.Close()

        # After saving all relevant histograms #
        # Combine all histograms with the the same names #
        hist_combine = []
        for h_name in used_names:
          first = True
          h_temp = ROOT.TH1F()
          for h in Temp_Hist_List:
            if (h.GetName() == h_name) and (first):
              h_temp = h
              h_temp.SetDirectory(0)
              first = False
              #print(h_name,h_temp.Integral())
            elif (h.GetName() == h_name) and not first:
              h_temp.Add(h)
              #print(h_name,h_temp.Integral())
          hist_combine.append(h_temp)
        # Choose Naming Convntion for the combined templates
          
        # If the ouptut root file would be empty, do not save #
        if len(hist_combine) == 0: continue
        else:
          fout = ROOT.TFile(Output_Dir+"/templates_combined_"+cat+"_"+Coupling_Name+"_"+Final_State+"_"+TreeFile+"_"+Year+".root","recreate")
          fout.cd()
          print("Saving: ",Output_Dir+"/templates_combined_"+cat+"_"+Coupling_Name+"_"+Final_State+"_"+TreeFile+"_"+Year+".root")
          for h in hist_combine:
            h.Write()
          fout.Close()
if __name__ == "__main__":
    main(sys.argv[1:])
