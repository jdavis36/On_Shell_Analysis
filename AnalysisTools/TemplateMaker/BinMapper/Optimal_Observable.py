from .Analytic import*
import os
import sys
#Dynamically import the Analysis Config#

full_path = os.path.realpath(__file__)
parent_directory = os.path.dirname(full_path)
sys.path.append(parent_directory+"/../../Utils/")

def Get_Bin_Number(Optimal_Discriminant_Dictionary,Obserables_List):

    if Optimal_Discriminant_Dictionary["Name"] == "Analytic_SM_vs_g4":
        return place_entry_SM_vs_g4(Optimal_Discriminant_Dictionary["nbins"],Obserables_List)[1]
    elif Optimal_Discriminant_Dictionary["Name"] == "Analytic_SM_vs_g4int":
        return place_entry_SM_vs_g4_int(Optimal_Discriminant_Dictionary["nbins"],Obserables_List)[1]
    else:
        return 
