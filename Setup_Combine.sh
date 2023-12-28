#!/bin/bash

echo "Will install higgs combine in $PWD"

#mkdir -p Higgs_Combine

#cd Higgs_Combine

CMSSW_VERSION="CMSSW_13_3_1"
#SCRAM_ARCH_VERSION_REPLACE="slc7_amd64_gcc900"

scram_arch_version=$SCRAM_ARCH_VERSION_REPLACE

echo "%MSG-MG5 SCRAM_ARCH version = $scram_arch_version"

echo "Installing CMSSW version $CMSSW_VERSION" 

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
#export SCRAM_ARCH=${scram_arch_version}
scramv1 project CMSSW ${CMSSW_VERSION}
cd ${CMSSW_VERSION}/src
eval `scramv1 runtime -sh`

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit

git checkout v9.1.0

mkdir -p Default_Setup_HVV
mkdir -p Default_Setup_gammaH

cp ../../../../Combine_Scripts/AC_Scans_Decay/* Default_Setup_HVV/
cp ../../../../Combine_Scripts/AC_Scans_GammaH/* Default_Setup_gammaH/

cp ../../../../Combine_Scripts/Shared/Plotting/* Default_Setup_HVV/
cp ../../../../Combine_Scripts/Shared/Plotting/* Default_Setup_gammaH/

cp ../../../../Combine_Scripts/Shared/Models/*py python/
cp ../../../../Combine_Scripts/Shared/Models/*cc src/
cp ../../../../Combine_Scripts/Shared/Models/*h interface/

eval `scramv1 runtime -sh`
scramv1 b clean; 
scramv1 b
