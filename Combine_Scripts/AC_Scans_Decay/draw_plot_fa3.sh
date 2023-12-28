python plotlimits_standalone.py --scan fa3_optimal.root "Expected fa3 optimal" kRed kDashed --scan fa3_D_CP.root "Expected fa3 D_CP" kBlue kDashed --scan fa3_D_CP_D0_minus.root "Expected fa3 D_CP D_0_Minus" kBlack kSolid --scan fa3_optimal_D_bkg.root "Expected fa3 Optimal +D_CP" kGreen kDashed --legendposition 0.5 0.6 0.9 0.9 --luminosity 42.5  --scanrange -1 1 --POI CMS_zz4l_fai1  --ytitle "-2#Delta ln L" --xtitle "f_{a3^{ZZ}}" --lettersize 0.02 output_fa3 --killpoints -2 -2 --noCMS
