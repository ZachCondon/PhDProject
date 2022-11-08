# PhDProject

My project consists of two main parts:
  Developing and running MCNP simulations to get neutron spectra from a passive neutron spectrometer
  Developing a neural network to take those spectra and output the original neutron spectrum

Current scripts used:
  automatePNS.py
  generateModel.py
  scrapeThisRun.py
  objectivizeData.py

1. automatePNS.py

    OVERVIEW: This is the master script that generates the folder containing the files for running MCNP simulations of the PNS.
    
    OUTPUTS: The output of this is a folder that contains all of the files necessary to perform a simulation of the PNS on quartz (see improvements needed).
    USER INPUTS: 
      nps - a string for the desired number of particles to be simulated. For simulations that I've done, 1e10 can be completed in 18 hours on quartz.
      numNodes - the number of nodes for each simulation. I have only put one, because I think to parallelize on more than one node would require additional changes to the input decks.
      numCores - the number of cores that each simulation will use on a core. MCNP handles this parallelization easily and I leave this at the max that's on one node, 36.
      whichSource - see this code for the source options
    IMPORTS: generateModel.py
    FUNCTIONS: None
    IMPROVEMENTS NEEDED: Currently, the bash file to submit all of the mcnp input decks does not generate properly and I've been doing this by hand, which is terrible.

2. generateModel.py
    OVERVIEW: This script contains all of the PNS information and functions for generating the files required for running the MCNP simulations.
    OUTPUTS: This file doesn't have any direct outputs. It is run through the automatePNS.py file to generate all of the simulation files.
    USER INPUTS: No inputs should be changed in this file.
    IMPORTS: datetime, os, shutil, math, random
    FUNCTIONS: See code for more information about each particular function.
      make_today_dir():
      make_run_dir():
      write_run_notes(run_path,current_time_directory,num_runs,source_text):
      append_run_notes():
      define_which_source():
      initialize_PNS_deck():
      TRCL():
      write_cell_card():
      write_surf_card():
      write_material_card():
      write_source_card():
      write_tally_card():
      write_print_card():
      write_sbatch():
      write_sbatch_spectrum():
      write_sbatch_continuation():
      write_sbatch_continuation_spectrum():
      write_PNS_input():
    IMPROVEMENTS NEEDED: Need to add a function to make a bash file so that all of the simulations can be submitted with one bash file. Examples of the file are in the CompletedRuns folder.
    
3. scrapeThisRun.py
    OVERVIEW: This script goes through all of the MCNP output files in the folder that it's currently in and gathers all of the tally data from each. Currently, that means the Mean, Error, VoV, Slope, and FoM will be saved. It's saved as a dictionary in a pickle file.
    OUTPUTS: A pickle file containing all of the output data from MCNP output files in the folder that this script is currently in.
    USER INPUTS: There is a variable called nps that tells the regex command where to look for the information. It should be set at the nps that the input deck was set to run to for the last results (since MCNP saves information at regular intervals, only the last one should be saved).
    IMPORTS: re, csv, pickle, os, glob
    FUNCTIONS:
      get_tally_lines():
      get_nps_save_lines():
      get_mean_tallies():
      get_error_tallies():
      get_vov_tallies():
      get_slope_tallies():
      get_fom_tallies():
    IMPROVEMENTS NEEDED: Update so that notes is an included portion of the pickle file that is saved.

objectivizeData.py
    OVERVIEW: This function makes an object containing all of the data that I've gathered. This script is in a folder with all of my completed MCNP simulations.
    OUTPUTS: An object containg all data.
    USER INPUTS: None
    IMPORTS: glob, pickle, matplotlib.pyplot, numpy, csv
    FUNCTIONS:
    IMPROVEMENTS NEEDED:
