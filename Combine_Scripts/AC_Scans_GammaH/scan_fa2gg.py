import os
import sys
cmnd = "combine --robustFit=0 --algo grid --floatOtherPOIs=1 --alignEdges=1 -P g2gg --saveSpecifiedFunc=R,g2Zg,g1,kappa,ghg2 --saveInactivePOI=0 --X-rtd OPTIMIZE_BOUNDS=0 --X-rtd TMCSO_AdaptivePseudoAsimov=0 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=999999999 -t -1 -V -v 3 --saveNLL -M MultiDimFit -m 125 -d scanworkspace.root --points 100  --setParameterRanges R=1,1:g2gg=-0.7,0.7:ghg2=1,1:ghg4=0,0:g1=1,1"
os.system(cmnd)
os.system("mv higgsCombineTest.MultiDimFit.mH125.root  higgs_fullrange.root")