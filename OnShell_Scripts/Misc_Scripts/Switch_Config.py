import os
import sys 

New_Config = sys.argv[1]
Names_To_Modify=["MakeAllTemplates.py","OnShellTreeTagger.py","Collect_Templates.py","OnShell_Template.py","AddOnShellMelaToTree.py","Clean_Trees.py","Plot_Discriminants.py"]
File_Paths_To_Change=[]
rootdir = os.getcwd()
for subdir, dirs, files, in os.walk(rootdir):
  for file in files:
    if os.path.basename(os.path.join(subdir, file)) in Names_To_Modify:
      print(os.path.join(subdir,file))
      File_Paths_To_Change.append(File_Paths_To_Change)

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only")

for file_path in File_Paths_To_Change:
  with open(file_path,'r') as file:
    content = file.read()
  content = content.replace('')
