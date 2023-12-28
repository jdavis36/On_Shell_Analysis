import os
import sys
cmnd = "combine --robustFit=0 --algo grid --floatOtherPOIs=0 --alignEdges=1 -P CMS_zz4l_fai1 --saveSpecifiedFunc=RF,RV --saveInactivePOI=0 --X-rtd OPTIMIZE_BOUNDS=0 --X-rtd TMCSO_AdaptivePseudoAsimov=0 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=999999999 -t -1 -V -v 3 --saveNLL -M MultiDimFit -m 125 -d scanworkspace.root --points 101  --setParameterRanges CMS_zz4l_fai1=-1,1"
os.system(cmnd)
os.system("mv higgsCombineTest.MultiDimFit.mH125.root  higgs_fullrange.root")
