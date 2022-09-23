# Script to automate multiple PNS model runs
import generateModel as gm

# ---------------------------------------------------------------------------
# |                              Automate PNS                               |
# ---------------------------------------------------------------------------
# This script generates MCNP input decks and the required batch script file to 
#  run those input decks on LLNL's Quartz supercomputer.
# The input parameters needed are:                          | Variable Name  |
    # The number of particles in the run                    |     nps        |
    # The number of compute nodes that will be requested    |   numNodes     |
    # The number of cores each input deck will request      |   numCores     |
    # The neutron source                                    | which_source   |
        # This variable is used within a function in        |                |
        #  generateModel that has each source explicitly    |                |
        #  written. See below for more specifics.           |                |
    # A source list (initialized, but empty) that is filled |                |
    #  in with a function in generateModel                  |   sdef_list    |
    # The neutron energies in each input deck               |    E_bins      |
    # The names of each of those bins, used for             |                |
    #  standardizing the naming scheme                      | E_bins_names   |
# The outputs of this script are:
    # 84 MCNP input decks that are identical except for the neutron energy.*
        # *this will likely change because I would like to incorporate sources 
        #   that are a spectrum of energies, each with their own probability. 
        #   This will make developing training data much easier to automate.
    # A bash file that is used to send these input decks to the supercomputer.
    # A continuation bash file that will pick up the MCNP run just in case it
    #  times out on quartz. There is a 24 hour job time-limit on quartz. This 
    #  continuation file should only be used once. If I run into a situation in
    #  which more than 48 hours is needed, I will need to modify this file.
    # A notes file. Upon running this script, the user is asked for prompts. 
    #  These prompts will be recorded in this file and should contain relevant
    #  information regarding the creation of these input decks. 
# Instructions to run these input decks on Quartz:
    # Open up the unix terminal
    # Navigate to the quartzTransfer directory
    # Change permissions for the whole directory
        # chmod -R 'directory name'
    # SFTP into the Quartz computer while in the quartzTransfer directory
        # sftp condon3@quartz.llnl.gov
        # Navigate to the directory you want to put the info in
        # put -R 'directory name'
        # exit
    # SSH into the Quartz computer
        # ssh condon3@quartz.llnl.gov
    # Navigate to within the directory with all of the input decks
    # sbatch 'sbatch file name'

# ---------------------------------------------------------------------------
# |                            Input Parameters                             |
# ---------------------------------------------------------------------------
# The following input parameters can be changed, but probably not often. The 
#  one I expect to be adjusted most often is the neutron source. I would like
#  automate a randomized source for neutrons. I think a point source will be 
#  easiest to randomize, but I will also need to look into distributed sources,
#  such as a line source or a plane source.
nps = "1e10"
numNodes = 1
numCores = 36
# Below are the source options
# Option 1 is the original source, which is a plane source directing particles 
#  to the detector. This source seems to imitate a neutron beam.
# Option 2 is a spherical shell source directing particles inward
# Option 3 (not implemented yet) will be a point source that will direct
#  particles only at the detector with the appropriate weighting.
which_source = 2
sdef_list = []

# As of right now, the following parameters should NOT be changed. These are 
#  hard coded energy bins used to generate the input decks. For consistency in
#  this research, these bins should not be modified. Later efforts, when I'm 
#  incorporating a source that includes a range of energy, this parameter may
#  actually be moved to be within the generateModel function.
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

# All these E_bin_names should have a period after the first number, but that
#  period wasn't working with file naming systems, so I omitted it.
E_bin_names = ["1e-9MeV","158e-9MeV","251e-9MeV","398e-9MeV","631e-9MeV",
               "1e-8MeV","158e-8MeV","251e-8MeV","398e-8MeV","631e-8MeV",
               "1e-7MeV","158e-7MeV","251e-7MeV","398e-7MeV","631e-7MeV",
               "1e-6MeV","158e-6MeV","251e-6MeV","398e-6MeV","631e-6MeV",
               "1e-5MeV","158e-5MeV","251e-5MeV","398e-5MeV","631e-5MeV",
               "1e-4MeV","158e-4MeV","251e-4MeV","398e-4MeV","631e-4MeV",
               "1e-3MeV","158e-3MeV","251e-3MeV","398e-3MeV","631e-3MeV",
               "1e-2MeV","158e-2MeV","251e-2MeV","398e-2MeV","631e-2MeV",
               "1e-1MeV","126e-1MeV","158e-1MeV","2e-1MeV","251e-1MeV",
               "316e-1MeV","398e-1MeV","501e-1MeV","631e-1MeV","794e-1MeV",
               "1e0MeV","112e0MeV","126e0MeV","141e0MeV","158e0MeV",
               "178e0MeV","2e0MeV","224e0MeV","251e0MeV","282e0MeV",
               "316e0MeV","355e0MeV","398e0MeV","447e0MeV","501e0MeV",
               "562e0MeV","631e0MeV","708e0MeV","794e0MeV","891e0MeV",
               "1e1MeV","112e1MeV","126e1MeV","141e1MeV","158e1MeV",
               "178e1MeV","2e1MeV","251e1MeV","316e1MeV","398e1MeV",
               "501e1MeV","631e1MeV","794e1MeV","1e2MeV"]

# This last line of code initiates the execution that generates the input decks
#  and batch files.
gm.write_PNS_input(E_bins,E_bin_names,sdef_list,nps,which_source,numNodes,numCores)