import ROOT 
import os

def init_PhotonSF():
    Path_To_This_File = os.path.abspath(__file__)
    Path_To_This_Directory = os.path.split(Path_To_This_File)[0]
    Relative_Path_To_Photons ="PhotonSF/"
    Path_To_Photon_SF = os.path.join(Path_To_This_Directory,Relative_Path_To_Photons)
    
    Photon_SF = Path_To_Photon_SF+"photIDSF_LooseCutBased.root"
    f  = ROOT.TFile.Open(Photon_SF)
    return f 

def return_Photon_SF(Photon_SF,year,Pt,Eta):
    if any(year == name for name in ["2016","2016APV","2017","2018"]):
	    h2 = Photon_SF.Get("UL{0}_sf".format(year))
    else:
        raise ValueError("Did not choose correct year format for Photon SF")
    return h2.GetBinContent(h2 .GetXaxis().FindBin(Eta),h2 .GetYaxis().FindBin(Pt))

def return_Photon_SF_Up(Photon_SF,year,Pt,Eta):
    if any(year == name for name in ["2016","2016APV","2017","2018"]):	    
        h2 = Photon_SF.Get("UL{0}_sf".format(year))
    else:
        raise ValueError("Did not choose correct year format for Photon SF")
    return h2.GetBinContent(h2 .GetXaxis().FindBin(Eta),h2 .GetYaxis().FindBin(Pt)) + h2.GetBinErrorUp(h2 .GetXaxis().FindBin(Eta),h2 .GetYaxis().FindBin(Pt))

def return_Photon_SF_Down(Photon_SF,year,Pt,Eta):
    if any(year == name for name in ["2016","2016APV","2017","2018"]):	    
        h2 = Photon_SF.Get("UL{0}_sf".format(year))
    else:
        raise ValueError("Did not choose correct year format for Photon SF")
    return h2.GetBinContent(h2 .GetXaxis().FindBin(Eta),h2 .GetYaxis().FindBin(Pt)) - h2.GetBinErrorLow(h2 .GetXaxis().FindBin(Eta),h2 .GetYaxis().FindBin(Pt))