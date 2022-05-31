# Script to automate multiple PNS model runs
import generateModel as gm

# E_bins = [1e-2,1e-1,1]
# E_bin_names = ["10keV", "100keV", "1000keV"]
nps = "6e8"
numNodes = 1
numCores = 1
E_bins = [1e-9,1.58e-9,2.51e-9,3.98e-9,6.31e-9,
          1e-8,1.58e-8,2.51e-8,3.98e-8,6.31e-8,
          1e-7,1.58e-7,2.51e-7,3.98e-7,6.31e-7,
          1e-6,1.58e-6,2.51e-6,3.98e-6,6.31e-6,
          1e-5,1.58e-5,2.51e-5,3.98e-5,6.31e-5,
          1e-4,1.58e-4,2.51e-4,3.98e-4,6.31e-4,
          1e-3,1.58e-3,2.51e-3,3.98e-3,6.31e-3,
          1e-2,1.58e-2,2.51e-2,3.98e-2,6.31e-2,
          1e-1,1.26e-1,1.58e-1,2e-1,2.51e-1,3.16e-1,3.98e-1,5.01e-1,6.31e-1,7.94e-1,
          1e0,1.12e0,1.26e0,1.41e0,1.58e0,1.78e0,2e0,2.24e0,2.51e0,2.82e0,
          3.16e0,3.55e0,3.98e0,4.47e0,5.01e0,5.62e0,6.31e0,7.08e0,7.94e0,8.91e0,
          1e1,1.12e1,1.26e1,1.41e1,1.58e1,1.78e1,2e1,2.51e1,3.16e1,3.98e1,
          5.01e1,6.31e1,7.94e1,1e2]

E_bin_names = ["1e-9keV","1.58e-9keV","2.51e-9keV","3.98e-9keV","6.31e-9keV",
               "1e-8keV","1.58e-8keV","2.51e-8keV","3.98e-8keV","6.31e-8keV",
               "1e-7keV","1.58e-7keV","2.51e-7keV","3.98e-7keV","6.31e-7keV",
               "1e-6keV","1.58e-6keV","2.51e-6keV","3.98e-6keV","6.31e-6keV",
               "1e-5keV","1.58e-5keV","2.51e-5keV","3.98e-5keV","6.31e-5keV",
               "1e-4keV","1.58e-4keV","2.51e-4keV","3.98e-4keV","6.31e-4keV",
               "1e-3keV","1.58e-3keV","2.51e-3keV","3.98e-3keV","6.31e-3keV",
               "1e-2keV","1.58e-2keV","2.51e-2keV","3.98e-2keV","6.31e-2keV",
               "1e-1keV","1.26e-1keV","1.58e-1keV","2e-1keV","2.51e-1keV",
               "3.16e-1keV","3.98e-1keV","5.01e-1keV","6.31e-1keV","7.94e-1keV",
               "1e0keV","1.12e0keV","1.26e0keV","1.41e0keV","1.58e0keV",
               "1.78e0keV","2e0keV","2.24e0keV","2.51e0keV","2.82e0keV",
               "3.16e0keV","3.55e0keV","3.98e0keV","4.47e0keV","5.01e0keV",
               "5.62e0keV","6.31e0keV","7.08e0keV","7.94e0keV","8.91e0keV",
               "1e1keV","1.12e1keV","1.26e1keV","1.41e1keV","1.58e1keV",
               "1.78e1keV","2e1keV","2.51e1keV","3.16e1keV","3.98e1keV",
               "5.01e1keV","6.31e1keV","7.94e1keV","1e2keV"]
# for Ebin in E_bins:
#     E_bin_names.append(str(Ebin)+"MeV")
sdef_list = []
# Below are the source options
# Option 1 is the original source, which is a plane source directing particles to the detector
# Option 2 is a spherical shell source directing particles inward
which_source = 1
if which_source == 1:
    for E in E_bins:
        sdef_list.append("sdef X=25 Y=D1 Z=D2 EXT=0 VEC=-1 0 0 DIR=1 PAR=N ERG="+str(E)+" EFF=0.000001\n")
    sdef_mod = ["si1 H -16 16\n",
                "sp1 D 0 1\n",
                "si2 H -31.16 16\n",
                "sp2 D 0 1\n"]
elif which_source == 2:
    for E in E_bins:
        sdef_list.append("SDEF   SUR=999   NRM=-1   PAR=N   WGT=7.854e3\n")
    sdef_mod = []
gm.write_PNS_input(E_bins,E_bin_names,sdef_list,sdef_mod,nps,which_source,numNodes,numCores)