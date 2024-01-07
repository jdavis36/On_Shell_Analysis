from .Analytic import place_entry as bin_map_for_testing
import os
import sys
#Dynamically import the Analysis Config#

full_path = os.path.realpath(__file__)
parent_directory = os.path.dirname(full_path)
sys.path.append(parent_directory+"/../../Utils/")

from Config import Analysis_Config

def Get_Bin_Number(Optimal_Discriminant_Dictionary,Obserables_List):

    if Optimal_Discriminant_Dictionary["Name"] == "Analytic":
        return bin_map_for_testing(Optimal_Discriminant_Dictionary["nbins"],Obserables_List)[1]
    else:
        return 
