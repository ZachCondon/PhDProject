# Generate MCNP deck for ANS

from datetime import datetime
import os
import shutil
import math
import random

def make_today_dir():
    # This function makes a new folder using today's date. This folder is the
    #  daily folder. It checks for the presence of the folder already and will
    #  not create anything if this function already ran today. My goal is to be
    #  able to have a time sequential list of folders for me to reference data 
    #  in the future.
    # The format of the new_directory text file is:
        # C:/Users/zacht/OneDrive/OSU/Research/MCNP/PNS Model/YYYY-MM-DD
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    new_directory = date_string
    parent_directory = "C:/Users/zacht/OneDrive/OSU/Research/MCNP/PNS Model/"
    path = os.path.join(parent_directory,new_directory)
    try:
        os.mkdir(path)
    except:
        print(f"Today's directory {date_string} already exists")
    return new_directory

def make_run_dir():
    # This function make the directory for the current run. It uses today's
    #  date to navigate to the current daily directory, then will create a
    #  directory associated with the current time (the "dt_string" variable)
    #  is a string with the current time. If there is a directory already
    #  associated with the curren time, it will make a second one with "_2"
    #  appended to the end. If that one already exists (for example, this script
    #  was run three times in one minute), it will do nothing and say to wait.
    # The format for the two variables that are returned:
        # path = "C:/Users/zacht/OneDrive/OSU/Research/MCNP/PNS Model/YYYY-MM-DD
        # new_directory = "YYYY-MM-DD_TTTT"
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    parent_directory = "C:/Users/zacht/OneDrive/OSU/Research/MCNP/PNS Model/" + date_string + "/"
    dt_string = now.strftime("%Y-%m-%d_%H%M")
    new_directory = dt_string
    path = os.path.join(parent_directory,new_directory)
    try:
        os.mkdir(path)
    except:
        path = path + "_2"
        try:
            os.mkdir(path)
            print(f"Directory {dt_string} already exists. Making a second directory: {dt_string}_2")
        except:
            print("There are already two directories for this minute. Please just wait a minute.")
    return path, new_directory

def write_run_notes(run_path,current_time_directory,num_runs,source_text):
    # This function writes a .txt file and allows me to input notes for each 
    #  run. Ideally, I will have set things that I will record each time, but
    #  I am sure as I move forward, I will learn more things that I need to 
    #  keep track of.
    # The format of the input variables is:
        # run_path = "C:/Users/zacht/OneDrive/OSU/Research/MCNP/PNS Model/2022-08-18/2022-08-18_1526"
        # current_time_directory = "2022-08-18_1526"
        # num_runs = "84"
        # source_text = ["xxx","xxx","xxx",...]
    run_notes = open(run_path + '\\notes_' + current_time_directory + '.txt',"x")
    now = datetime.now()
    run_notes.write(f'*****Notes for PNS model run generated at {now.strftime("%Y-%m-%d_%H%M")}*****. \n')
    run_notes.write('\n')
    run_notes.write(f'    Number of energy bins: {num_runs}. \n')
    run_notes.write('    Source information' + source_text + '\n')
    run_notes.write('\n')
    run_notes.write('    NOTE: In case the run times out, the file *_cont.bash will continue the run.\n')
    run_notes.write('\n')
    notes_input = 'start notes'
    print("Write notes here. After each sentence, hit 'enter'\n")
    print("To stop writing notes, type 'end'\n")
    while notes_input != 'end':
        notes_input = input('Write notes here, line by line: ')
        run_notes.write(notes_input + ' \n')
    run_notes.write('If this is a broad spectrum source, energy info will be below in order from lowest to highest energy:')
    run_notes.close()
    
def append_run_notes(run_path,current_time_directory,i,source_strength):
    # This function appends the notes file for this simulation with the energy
    # information that is generated randomly.
    # The format of the input variables is:
        # run_path = "C:/Users/zacht/OneDrive/OSU/Research/MCNP/PNS Model/2022-08-18/2022-08-18_1532"
        # current_time_directory = "2022-08-18_1532"
        # i = N
            # The variable "i" is the number of simulations that are generated
            # and each simulation has a random number of randomly generated
            # energy values.
        # source_strength = [N.NNN, N.NNN, N.NNN, ...]
            # This variable will be a random length that corresponds to the 
            # number of randomized energy values for each simulation.
    append_notes = open(run_path + '\\notes_' + current_time_directory + '.txt',"a")
    append_notes.write('\n')
    spectrum_text = str(i+1) + ": "
    for s in source_strength:
        spectrum_text += "   " + "{:.3}".format(s)
    append_notes.write(spectrum_text + "\n")
    append_notes.close()

def define_which_source(which_source,E_bins,sdef_list):
    # This function is important in that it defines what neutron source is used
    #  in each input deck. Within each if statement is a for loop that appends
    #  the sdef_list array with a line of text for each energy bin. Right now, 
    #  there are 84 energy bins and the sdef_list array will have 84 entries,
    #  which will get iteratively put into each of the input decks. There is
    #  also an sdef_mod variable that gets introduced. This will contain
    #  specifics/modifications for the source. It can be a range of things, but
    #  one example is that it is used to distribute the source and define the 
    #  emission probabilities.
    # Source 1 - The original source used by Paige Witter. I used it to 
    #  recreate her work and verify that I was getting the same results. It is
    #  a planar source that is as large as the PNS assembly (sphere and stand).
    #  The neutrons are always emitted perpendicular to the source plane,
    #  distributed linearly anywhere from the source plane.
    # Source 2 (Currently not working, I think I just need to change the
    #  material so that there isn't a void between the detector and source) - 
    #  This is my first attempt at changing the source. I am attempting to
    #  create a spherical source directed inward. I don't have any modifiations
    #  on the emission direction, so the particles are emitted in any inward 
    #  direction from the source sphere.
    # Source 3 - This is a single-energy, point source located at x=30 cm that 
    #  emits particles in a cone directed at the sphere. The cone ensures that
    #  9 in 10 particles (see SB1 line) is directed at the PNS.
    # Source 4 - This source will be a point source located at a random
    #  location at a distance of 30 to 100 cm and consists of a range of
    #  energies. It consists of the original 84 energy bins from the original 
    #  PNS design. Each energy will have a random strength. This randomization 
    #  is not realistic compared to a real neutron spectrum though.
    # Source 5 - This is six sources, along all of the Cartesian axes (positive
    #  x, negative x, positive y, etc.). This source is used to make the 
    #  simulation symmetric to make a detector response matrix.
    source_strength = 0
    if which_source == 1:
        for E in E_bins:
            sdef_list.append("sdef X=25 Y=D1 Z=D2 EXT=0 VEC=-1 0 0 DIR=1 PAR=N ERG="+str(E)+" EFF=0.000001\n")
        sdef_mod = ["si1 H -16 16\n",
                    "sp1 D 0 1\n",
                    "si2 H -31.16 16\n",
                    "sp2 D 0 1\n"]
        source_text = 'Source 1: Plane source emitted toward detector (original source).'
    elif which_source == 2:
        for E in E_bins:
            sdef_list.append("SDEF   SUR=9999   NRM=-1   PAR=N   ERG="+str(E)+"\n")
        sdef_mod = []
        source_text = 'Source 2: Spherical shell encompassing detector, emitting inward.'
    elif which_source == 3:
        source_pos = 30 # this is the position of the source from the origin
        for E in E_bins:
            sdef_list.append("SDEF   POS="+str(source_pos)+" 0 0 ERG="+str(E)+" PAR=N  VEC=-1 0 0  DIR=d1\n")
        cos_value = round(math.cos(math.atan(15/source_pos)),2)
        sdef_mod = ["SI1  -1   0.9   1\n",
                    "SP1  0    "+str(1+cos_value)+"  "+str(1-cos_value)+"\n",
                    "SB1  0    1     9\n"]
        source_text = 'Source 3: A point source emitting radiation in a cone that encompasses only the detector.'
    elif which_source == 4:
        # Set the first source line
        source_pos = [round(random.uniform(30,100),1), round(random.uniform(30,100),1), round(random.uniform(30,100),1)]
        sdef_list.append("SDEF   POS="+str(source_pos[0])+" "+str(source_pos[1])+" "+str(source_pos[2])+" ERG=d1 PAR=N  VEC=-"+str(source_pos[0])+" -"+str(source_pos[1])+" -"+str(source_pos[2])+"  DIR=d2\n")
        # Initialize sdef_mod array
        sdef_mod = []
        # Define the source information with all of the energy values
        SI1_text = "SI1 L"
        i = 0
        for E in E_bins:
            i += 1
            SI1_text += "    " + "{:.2e}".format(E)
            if i == 10:
                sdef_mod.append(SI1_text + "&\n")
                SI1_text = ""
                i = 0
        sdef_mod.append(SI1_text + "\n")
        
        # Define the source strength for each energy
        random_source_strength = [random.random() for _ in range(84)]
        source_strength = [round(strength/sum(random_source_strength),3) for strength in random_source_strength]
        SP1_text = "SP1 D"
        i = 0
        for S in source_strength:
            i += 1
            SP1_text += "    " + "{:.3}".format(S)
            if i == 10:
                sdef_mod.append(SP1_text + "&\n")
                SP1_text = ""
                i = 0
        sdef_mod.append(SP1_text + "\n")
        # Define the direction modification so that the neutrons are emitted in a cone at the PNS
        distance_sourceToDetector = math.sqrt(source_pos[0]**2+source_pos[1]**2+source_pos[2]**2)
        mu = round(math.cos(math.atan(15/distance_sourceToDetector)),4)
        sdef_mod.append("SI2  -1   "+str(mu)+"   1\n")
        sdef_mod.append("SP2  0    "+str(1+mu)+"  "+str(1-mu)+"\n")
        sdef_mod.append("SB2  0    1     99\n")
        source_text = ''
    elif which_source == 5:
        for E in E_bins:
            sdef_list.append("SDEF POS=d1 VEC=FPOS=d2 PAR=N ERG="+str(E)+" DIR=d9\n")
        sdef_mod = []
        sdef_mod.append("SI1 L  -50 0 0   50 0 0   0 50 0   0 -50 0   0 0 50   0 0 -50\n")
        sdef_mod.append("SP1    .166     .167     .166     .167      .167     .167\n")
        sdef_mod.append("DS2 L   50 0 0  -50 0 0   0 -50 0  0 50 0   0 0 -50   0 0 50\n")
        mu = round(math.cos(math.atan(15/50)),4)
        sdef_mod.append("SI9    -1   "+str(mu)+"   1\n")
        sdef_mod.append("SP9     0    "+str(1+mu)+"  "+str(1-mu)+"\n")
        sdef_mod.append("SB9     0    1     99\n")
        
        
        # for E in E_bins:
        #     sdef_list.append((
        #         "sdef POS=50 0 0 ERG="+str(E)+" PAR=N VEC=-50 0 0 DIR=d1\n",
        #         "sdef POS=-50 0 0 ERG="+str(E)+" PAR=N VEC=50 0 0 DIR=d2\n",
        #         "sdef POS=0 50 0 ERG="+str(E)+" PAR=N VEC=0 -50 0 DIR=d3\n",
        #         "sdef POS=0 -50 0 ERG="+str(E)+" PAR=N VEC=0 50 0 DIR=d4\n",
        #         "sdef POS=0 0 50 ERG="+str(E)+" PAR=N VEC=0 0 -50 DIR=d5\n",
        #         "sdef POS=0 0 -50 ERG="+str(E)+" PAR=N VEC=0 0 50 DIR=d6\n"))
        # sdef_mod = []
        # mu = round(math.cos(math.atan(15/50)),4)
        # for i in range(6):
        #     sdef_mod.append("SI"+str(i+1)+"  -1   "+str(mu)+"   1\n")
        #     sdef_mod.append("SP"+str(i+1)+"  0    "+str(1+mu)+"  "+str(1-mu)+"\n")
        #     sdef_mod.append("SB"+str(i+1)+"  0    1     99\n")
        source_text = 'Source 5: Point sources on each of six axes.'

    return source_text, sdef_mod, source_strength
            
def initialize_PNS_deck(run_path,filename,Ebin):
    # This function makes a new file for each input deck. It also writes the
    #  first line of the input deck.
    # Input variables
        # run_path - This variable is a string that is defined in the function 
        #  make_run_dir(), which returns it as the variable 'path'. It is hard 
        #  coded for my directory path, so that the input decks are always 
        #  saved in the same area.
        #  Example: 'C:/Users/zacht/OneDrive/OSU/Research/MCNP/PNS Model/YYYY-MM-DD'
        # filename - This variable is a string that is defined in the function
        #  write_PNS_input(), which returns it as the variable 'filename'. It
        #  is iterated in a for loop so that each input deck has a unique name.
        #  Example: '/PNS_X.XXeXMeV'
        # Ebin - This variable is a list of doubles and is defined in the file
        #  automatePNS.py. It contains each of the 84 energy bins.
    PNS_model = open(run_path + filename,"x")
    PNS_model.write("MCNP6 model of the LLNL PNS sphere ("+ str(Ebin)+ " MeV)\n")
    PNS_model.close()
    
def TRCL(new_cell_num, like_cell_num, x_shift, y_shift, z_shift):
    # There are a lot of TRCLs in the input deck and this function just makes 
    #  it easy to call this instead of writing out each TRCL.
    return str(new_cell_num)+ " LIKE " + str(like_cell_num)+ " BUT TRCL= ("+ str(x_shift) + " "+ str(y_shift)+ " "+ str(z_shift)+ ")\n"

def write_cell_card(run_path,filename):
    # This function writes all of the cell cards. It uses the two variables
    #  'run_path' and 'filename' to be able to open the input deck file and 
    #  append each line. 
    imp1 = "imp:n=1 imp:a=1 imp:p=1 imp:e=1"
    imp3 = "imp:n=3 imp:a=3 imp:p=3 imp:e=3"
    PNS_model = open(run_path + filename,"a")
    PNS_model.write("C    **************CELL CARD**************\n")
    PNS_model.write("C    -------MOIST AIR AROUND SPHERE-------\n")
    PNS_model.write("801    1 -1.29E-3 -800 20000 20100 20200 20300 #2000 #2001 #2002 #2003 #2004 &\n     " + imp1 + "\n")
    PNS_model.write("C    ---------SPHERE AND CYLINDER---------\n")
    PNS_model.write("C    Poly sphere (outside of cylinder and holes)\n")
    PNS_model.write("10000 20 -0.93  -20000 20100 20200 20300 #2000 "+ imp1+ "\n")
    PNS_model.write("C    X-axis cylinder\n")
    PNS_model.write("10100 20 -0.93  -20100 21000 21100 21200 21300 21400 21500 21600 21700 21800 &\n     21900 22000 22100 22200 22300 22400 22500 22600 22700 22800 &\n     "+ imp1+ "\n")
    PNS_model.write("C    Y-axis cylinder\n")
    PNS_model.write("10200 20 -0.93  -20200 20100 23000 23100 23200 23300 23400 23500 23600 23700 &\n     23800 23900 24000 24100 24200 24300 24400 24500 24600 24700 &\n     "+ imp1+ "\n")
    PNS_model.write("C    Z-axis cylinder\n")
    PNS_model.write("10300 20 -0.93  -20300 20100 20200 25000 25100 25200 25300 25400 25500 25600 &\n     25700 25800 25900 26000 26100 26200 26300 26400 26500 26600 26700 &\n     "+ imp1+ "\n")
    PNS_model.write("C    ---------HOLES IN CYLINDER---------\n")
    PNS_model.write("C             (Filled with air)         \n")
    PNS_model.write("C    X-axis holes\n")
    PNS_model.write("11000 1 -1.2E-3 (-21000:-21100:-21200:-21300:-21400:-21500:-21600:-21700:-21800:-21900:\n"
                    "        -22000:-22100:-22200:-22300:-22400:-22500:-22600:-22700:-22800)-20100 #200 #201\n"
                    "        #202 #203 #204 #205 #206 #207 #208 #209 #210 #211 #212 #213 #214 #215 #216 #217\n"
                    "        #218 #400 #401 #402 #403 #404 #405 #406 #407 #408 #409 #410 #411 #412 #413 #414\n"
                    "        #415 #416 #417 #418 #300 #301 #302 #303 #304 #305 #306 #307 #308 #309 #310 #311\n"
                    "        #312 #313 #314 #315 #316 #317 #318 #500 #501 #502 #503 #504 #505 #506 #507 #508\n"
                    "        #509 #510 #511 #512 #513 #514 #515 #516 #517 #518 #600 #601 #602 #603 #604 #605\n"
                    "        #606 #607 #608 #609 #610 #611 #612 #613 #614 #615 #616 #617 #618 #700 #701 #702\n"
                    "        #703 #704 #705 #706 #707 #708 #709 #710 #711 #712 #713 #714 #715 #716 #717 #718\n"
                    "        "+ imp1+ "\n")
    PNS_model.write("C    Y-axis holes\n")
    PNS_model.write("11100 1 -1.2E-3 (-23000:-23100:-23200:-23300:-23400:-23500:-23600:-23700:-23800:-23900:\n"
                    "        -24000:-24100:-24200:-24300:-24400:-24500:-24600:-24700) -20200 #219 #220 #221\n"
                    "        #222 #223 #224 #225 #226 #227 #228 #229 #230 #231 #232 #233 #234 #235 #236 #419\n"
                    "        #420 #421 #422 #423 #424 #425 #426 #427 #428 #429 #430 #431 #432 #433 #434 #435\n"
                    "        #436 #319 #320 #321 #322 #323 #324 #325 #326 #327 #328 #329 #330 #331 #332 #333\n"
                    "        #334 #335 #336 #519 #520 #521 #522 #523 #524 #525 #526 #527 #528 #529 #530 #531\n"
                    "        #532 #533 #534 #535 #536 #619 #620 #621 #622 #623 #624 #625 #626 #627 #628 #629\n"
                    "        #630 #631 #632 #633 #634 #635 #636 #719 #720 #721 #722 #723 #724 #725 #726 #727\n"
                    "        #728 #729 #730 #731 #732 #733 #734 #735 #736 "+ imp1+ "\n")
    PNS_model.write("C    Z-axis holes\n")
    PNS_model.write("11200 1 -1.2E-3 (-25000:-25100:-25200:-25300:-25400:-25500:-25600:-25700:-25800:-25900:\n"
                    "        -26000:-26100:-26200:-26300:-26400:-26500:-26600:-26700)-20300 #237 #238 #239 #240\n"
                    "        #241 #242 #243 #244 #245 #246 #247 #248 #249 #250 #251 #252 #253 #254 #437 #438 #439\n"
                    "        #440 #441 #442 #443 #444 #445 #446 #447 #448 #449 #450 #451 #452 #453 #454 #337\n"
                    "        #338 #339 #340 #341 #342 #343 #344 #345 #346 #347 #348 #349 #350 #351 #352 #353\n"
                    "        #354 #537 #538 #539 #540 #541 #542 #543 #544 #545 #546 #547 #548 #549 #550 #551\n"
                    "        #552 #553 #554 #637 #638 #639 #640 #641 #642 #643 #644 #645 #646 #647 #648 #649\n"
                    "        #650 #651 #652 #653 #654 #737 #738 #739 #740 #741 #742 #743 #744 #745 #746 #747\n"
                    "        #748 #749 #750 #751 #752 #753 #754 "+ imp1+ "\n")
    PNS_model.write("C    --------TLD MATERIAL (A-SIDE)------\n")
    PNS_model.write("C    X-axis front casing of Li-6\n")
    PNS_model.write("200 24 -1.42 -200 "+ imp1+ "\n")
    PNS_model.write(TRCL(201, 200, 3, 0, 0))
    PNS_model.write(TRCL(202, 200, -3, 0, 0))
    PNS_model.write(TRCL(203, 200, 6, 0, 0))
    PNS_model.write(TRCL(204, 200, -5.8, 0, 0))
    PNS_model.write(TRCL(205, 200, 8, 0, 0))
    PNS_model.write(TRCL(206, 200, -7.8, 0, 0))
    PNS_model.write(TRCL(207, 200, 9, 0, 0))
    PNS_model.write(TRCL(208, 200, -8.8, 0, 0))
    PNS_model.write(TRCL(209, 200, 10, 0, 0))
    PNS_model.write(TRCL(210, 200, -10, 0, 0))
    PNS_model.write(TRCL(211, 200, 11, 0, 0))
    PNS_model.write(TRCL(212, 200, -11, 0, 0))
    PNS_model.write(TRCL(213, 200, 12, 0, 0))
    PNS_model.write(TRCL(214, 200, -12, 0, 0))
    PNS_model.write(TRCL(215, 200, 13, 0, 0))
    PNS_model.write(TRCL(216, 200, -13, 0, 0))
    PNS_model.write(TRCL(217, 200, 14, 0, 0))
    PNS_model.write(TRCL(218, 200, -14, 0, 0))
    PNS_model.write("C    Y-axis front casing of Li-6\n")
    PNS_model.write("219 24 -1.42 -201 TRCL= (0 3 0) "+ imp1+ "\n")
    PNS_model.write("220 24 -1.42 -202 TRCL= (0 -3 0) "+ imp1+ "\n")
    PNS_model.write("221 24 -1.42 -201 TRCL= (0 6 0) "+ imp1+ "\n")
    PNS_model.write("222 24 -1.42 -202 TRCL= (0 -5.8 0) "+ imp1+ "\n")
    PNS_model.write("223 24 -1.42 -201 TRCL= (0 8 0) "+ imp1+ "\n")
    PNS_model.write("224 24 -1.42 -202 TRCL= (0 -7.8 0) "+ imp1+ "\n")
    PNS_model.write("225 24 -1.42 -201 TRCL= (0 9 0) "+ imp1+ "\n")
    PNS_model.write("226 24 -1.42 -202 TRCL= (0 -8.8 0) "+ imp1+ "\n")
    PNS_model.write("227 24 -1.42 -201 TRCL= (0 10 0) "+ imp1+ "\n")
    PNS_model.write("228 24 -1.42 -202 TRCL= (0 -10 0) "+ imp1+ "\n")
    PNS_model.write("229 24 -1.42 -201 TRCL= (0 11 0) "+ imp1+ "\n")
    PNS_model.write("230 24 -1.42 -202 TRCL= (0 -11 0) "+ imp1+ "\n")
    PNS_model.write("231 24 -1.42 -201 TRCL= (0 12 0) "+ imp1+ "\n")
    PNS_model.write("232 24 -1.42 -202 TRCL= (0 -12 0) "+ imp1+ "\n")
    PNS_model.write("233 24 -1.42 -201 TRCL= (0 13 0) "+ imp1+ "\n")
    PNS_model.write("234 24 -1.42 -202 TRCL= (0 -13 0) "+ imp1+ "\n")
    PNS_model.write("235 24 -1.42 -201 TRCL= (0 14 0) "+ imp1+ "\n")
    PNS_model.write("236 24 -1.42 -202 TRCL= (0 -14 0) "+ imp1+ "\n")
    PNS_model.write("C    Z-axis front casing of Li-6\n")
    PNS_model.write("237 24 -1.42 -203 TRCL= (-1 0 3) "+ imp1+ "\n")
    PNS_model.write("238 24 -1.42 -204 TRCL= (-1 0 -3) "+ imp1+ "\n")
    PNS_model.write("239 24 -1.42 -203 TRCL= (-1 0 6) "+ imp1+ "\n")
    PNS_model.write("240 24 -1.42 -204 TRCL= (-1 0 -5.8) "+ imp1+ "\n")
    PNS_model.write("241 24 -1.42 -203 TRCL= (-1 0 8) "+ imp1+ "\n")
    PNS_model.write("242 24 -1.42 -204 TRCL= (-1 0 -7.8) "+ imp1+ "\n")
    PNS_model.write("243 24 -1.42 -203 TRCL= (-1 0 9) "+ imp1+ "\n")
    PNS_model.write("244 24 -1.42 -204 TRCL= (-1 0 -8.8) "+ imp1+ "\n")
    PNS_model.write("245 24 -1.42 -203 TRCL= (-1 0 10) "+ imp1+ "\n")
    PNS_model.write("246 24 -1.42 -204 TRCL= (-1 0 -10) "+ imp1+ "\n")
    PNS_model.write("247 24 -1.42 -203 TRCL= (-1 0 11) "+ imp1+ "\n")
    PNS_model.write("248 24 -1.42 -204 TRCL= (-1 0 -11) "+ imp1+ "\n")
    PNS_model.write("249 24 -1.42 -203 TRCL= (-1 0 12) "+ imp1+ "\n")
    PNS_model.write("250 24 -1.42 -204 TRCL= (-1 0 -12) "+ imp1+ "\n")
    PNS_model.write("251 24 -1.42 -203 TRCL= (-1 0 13) "+ imp1+ "\n")
    PNS_model.write("252 24 -1.42 -204 TRCL= (-1 0 -13) "+ imp1+ "\n")
    PNS_model.write("253 24 -1.42 -203 TRCL= (-1 0 14) "+ imp1+ "\n")
    PNS_model.write("254 24 -1.42 -204 TRCL= (-1 0 -14) "+ imp1+ "\n")
    print('Detector material options: 22=>Li6, 2=>Au')
    detectorMaterial = input('Which material for detector? ')
    PNS_model.write("C    X-axis Li-6\n")
    PNS_model.write("400 "+ detectorMaterial + " -2.635 -400 "+ imp3+ "\n")
    PNS_model.write(TRCL(401, 400, 3, 0, 0))
    PNS_model.write(TRCL(402, 400, -3, 0, 0))
    PNS_model.write(TRCL(403, 400, 6, 0, 0))
    PNS_model.write(TRCL(404, 400, -5.8, 0, 0))
    PNS_model.write(TRCL(405, 400, 8, 0, 0))
    PNS_model.write(TRCL(406, 400, -7.8, 0, 0))
    PNS_model.write(TRCL(407, 400, 9, 0, 0))
    PNS_model.write(TRCL(408, 400, -8.8, 0, 0))
    PNS_model.write(TRCL(409, 400, 10, 0, 0))
    PNS_model.write(TRCL(410, 400, -10, 0, 0))
    PNS_model.write(TRCL(411, 400, 11, 0, 0))
    PNS_model.write(TRCL(412, 400, -11, 0, 0))
    PNS_model.write(TRCL(413, 400, 12, 0, 0))
    PNS_model.write(TRCL(414, 400, -12, 0, 0))
    PNS_model.write(TRCL(415, 400, 13, 0, 0))
    PNS_model.write(TRCL(416, 400, -13, 0, 0))
    PNS_model.write(TRCL(417, 400, 14, 0, 0))
    PNS_model.write(TRCL(418, 400, -14, 0, 0))
    PNS_model.write("C    Y-axis Li-6\n")
    PNS_model.write("419 "+ detectorMaterial + " -2.635 -401 TRCL= (0 3 0) "+ imp3+ "\n")
    PNS_model.write("420 "+ detectorMaterial + " -2.635 -402 TRCL= (0 -3 0) "+ imp3+ "\n")
    PNS_model.write("421 "+ detectorMaterial + " -2.635 -401 TRCL= (0 6 0) "+ imp3+ "\n")
    PNS_model.write("422 "+ detectorMaterial + " -2.635 -402 TRCL= (0 -5.8 0) "+ imp3+ "\n")
    PNS_model.write("423 "+ detectorMaterial + " -2.635 -401 TRCL= (0 8 0) "+ imp3+ "\n")
    PNS_model.write("424 "+ detectorMaterial + " -2.635 -402 TRCL= (0 -7.8 0) "+ imp3+ "\n")
    PNS_model.write("425 "+ detectorMaterial + " -2.635 -401 TRCL= (0 9 0) "+ imp3+ "\n")
    PNS_model.write("426 "+ detectorMaterial + " -2.635 -402 TRCL= (0 -8.8 0) "+ imp3+ "\n")
    PNS_model.write("427 "+ detectorMaterial + " -2.635 -401 TRCL= (0 10 0) "+ imp3+ "\n")
    PNS_model.write("428 "+ detectorMaterial + " -2.635 -402 TRCL= (0 -10 0) "+ imp3+ "\n")
    PNS_model.write("429 "+ detectorMaterial + " -2.635 -401 TRCL= (0 11 0) "+ imp3+ "\n")
    PNS_model.write("430 "+ detectorMaterial + " -2.635 -402 TRCL= (0 -11 0) "+ imp3+ "\n")
    PNS_model.write("431 "+ detectorMaterial + " -2.635 -401 TRCL= (0 12 0) "+ imp3+ "\n")
    PNS_model.write("432 "+ detectorMaterial + " -2.635 -402 TRCL= (0 -12 0) "+ imp3+ "\n")
    PNS_model.write("433 "+ detectorMaterial + " -2.635 -401 TRCL= (0 13 0) "+ imp3+ "\n")
    PNS_model.write("434 "+ detectorMaterial + " -2.635 -402 TRCL= (0 -13 0) "+ imp3+ "\n")
    PNS_model.write("435 "+ detectorMaterial + " -2.635 -401 TRCL= (0 14 0) "+ imp3+ "\n")
    PNS_model.write("436 "+ detectorMaterial + " -2.635 -402 TRCL= (0 -14 0) "+ imp3+ "\n")
    PNS_model.write("C    Z-axis Li-6\n")
    PNS_model.write("437 "+ detectorMaterial + " -2.635 -403 TRCL= (-1 0 3) "+ imp3+ "\n")
    PNS_model.write("438 "+ detectorMaterial + " -2.635 -404 TRCL= (-1 0 -3) "+ imp3+ "\n")
    PNS_model.write("439 "+ detectorMaterial + " -2.635 -403 TRCL= (-1 0 6) "+ imp3+ "\n")
    PNS_model.write("440 "+ detectorMaterial + " -2.635 -404 TRCL= (-1 0 -5.8) "+ imp3+ "\n")
    PNS_model.write("441 "+ detectorMaterial + " -2.635 -403 TRCL= (-1 0 8) "+ imp3+ "\n")
    PNS_model.write("442 "+ detectorMaterial + " -2.635 -404 TRCL= (-1 0 -7.8) "+ imp3+ "\n")
    PNS_model.write("443 "+ detectorMaterial + " -2.635 -403 TRCL= (-1 0 9) "+ imp3+ "\n")
    PNS_model.write("444 "+ detectorMaterial + " -2.635 -404 TRCL= (-1 0 -8.8) "+ imp3+ "\n")
    PNS_model.write("445 "+ detectorMaterial + " -2.635 -403 TRCL= (-1 0 10) "+ imp3+ "\n")
    PNS_model.write("446 "+ detectorMaterial + " -2.635 -404 TRCL= (-1 0 -10) "+ imp3+ "\n")
    PNS_model.write("447 "+ detectorMaterial + " -2.635 -403 TRCL= (-1 0 11) "+ imp3+ "\n")
    PNS_model.write("448 "+ detectorMaterial + " -2.635 -404 TRCL= (-1 0 -11) "+ imp3+ "\n")
    PNS_model.write("449 "+ detectorMaterial + " -2.635 -403 TRCL= (-1 0 12) "+ imp3+ "\n")
    PNS_model.write("450 "+ detectorMaterial + " -2.635 -404 TRCL= (-1 0 -12) "+ imp3+ "\n")
    PNS_model.write("451 "+ detectorMaterial + " -2.635 -403 TRCL= (-1 0 13) "+ imp3+ "\n")
    PNS_model.write("452 "+ detectorMaterial + " -2.635 -404 TRCL= (-1 0 -13) "+ imp3+ "\n")
    PNS_model.write("453 "+ detectorMaterial + " -2.635 -403 TRCL= (-1 0 14) "+ imp3+ "\n")
    PNS_model.write("454 "+ detectorMaterial + " -2.635 -404 TRCL= (-1 0 -14) "+ imp3+ "\n")
    PNS_model.write("C    X-axis back casing of Li-6\n")
    PNS_model.write("300 24 -1.42 -300 "+ imp1+ "\n")
    PNS_model.write(TRCL(301, 300, 3, 0, 0))
    PNS_model.write(TRCL(302, 300, -3, 0, 0))
    PNS_model.write(TRCL(303, 300, 6, 0, 0))
    PNS_model.write(TRCL(304, 300, -5.8, 0, 0))
    PNS_model.write(TRCL(305, 300, 8, 0, 0))
    PNS_model.write(TRCL(306, 300, -7.8, 0, 0))
    PNS_model.write(TRCL(307, 300, 9, 0, 0))
    PNS_model.write(TRCL(308, 300, -8.8, 0, 0))
    PNS_model.write(TRCL(309, 300, 10, 0, 0))
    PNS_model.write(TRCL(310, 300, -10, 0, 0))
    PNS_model.write(TRCL(311, 300, 11, 0, 0))
    PNS_model.write(TRCL(312, 300, -11, 0, 0))
    PNS_model.write(TRCL(313, 300, 12, 0, 0))
    PNS_model.write(TRCL(314, 300, -12, 0, 0))
    PNS_model.write(TRCL(315, 300, 13, 0, 0))
    PNS_model.write(TRCL(316, 300, -13, 0, 0))
    PNS_model.write(TRCL(317, 300, 14, 0, 0))
    PNS_model.write(TRCL(318, 300, -14, 0, 0))
    PNS_model.write("C    Y-axis back casing of Li-6\n")
    PNS_model.write("319 24 -1.42 -301 TRCL= (0 3 0) "+ imp1+ "\n")
    PNS_model.write("320 24 -1.42 -302 TRCL= (0 -3 0) "+ imp1+ "\n")
    PNS_model.write("321 24 -1.42 -301 TRCL= (0 6 0) "+ imp1+ "\n")
    PNS_model.write("322 24 -1.42 -302 TRCL= (0 -5.8 0) "+ imp1+ "\n")
    PNS_model.write("323 24 -1.42 -301 TRCL= (0 8 0) "+ imp1+ "\n")
    PNS_model.write("324 24 -1.42 -302 TRCL= (0 -7.8 0) "+ imp1+ "\n")
    PNS_model.write("325 24 -1.42 -301 TRCL= (0 9 0) "+ imp1+ "\n")
    PNS_model.write("326 24 -1.42 -302 TRCL= (0 -8.8 0) "+ imp1+ "\n")
    PNS_model.write("327 24 -1.42 -301 TRCL= (0 10 0) "+ imp1+ "\n")
    PNS_model.write("328 24 -1.42 -302 TRCL= (0 -10 0) "+ imp1+ "\n")
    PNS_model.write("329 24 -1.42 -301 TRCL= (0 11 0) "+ imp1+ "\n")
    PNS_model.write("330 24 -1.42 -302 TRCL= (0 -11 0) "+ imp1+ "\n")
    PNS_model.write("331 24 -1.42 -301 TRCL= (0 12 0) "+ imp1+ "\n")
    PNS_model.write("332 24 -1.42 -302 TRCL= (0 -12 0) "+ imp1+ "\n")
    PNS_model.write("333 24 -1.42 -301 TRCL= (0 13 0) "+ imp1+ "\n")
    PNS_model.write("334 24 -1.42 -302 TRCL= (0 -13 0) "+ imp1+ "\n")
    PNS_model.write("335 24 -1.42 -301 TRCL= (0 14 0) "+ imp1+ "\n")
    PNS_model.write("336 24 -1.42 -302 TRCL= (0 -14 0) "+ imp1+ "\n")
    PNS_model.write("C    Z-axis front casing of Li-6\n")
    PNS_model.write("337 24 -1.42 -303 TRCL= (-1 0 3) "+ imp1+ "\n")
    PNS_model.write("338 24 -1.42 -304 TRCL= (-1 0 -3) "+ imp1+ "\n")
    PNS_model.write("339 24 -1.42 -303 TRCL= (-1 0 6) "+ imp1+ "\n")
    PNS_model.write("340 24 -1.42 -304 TRCL= (-1 0 -5.8) "+ imp1+ "\n")
    PNS_model.write("341 24 -1.42 -303 TRCL= (-1 0 8) "+ imp1+ "\n")
    PNS_model.write("342 24 -1.42 -304 TRCL= (-1 0 -7.8) "+ imp1+ "\n")
    PNS_model.write("343 24 -1.42 -303 TRCL= (-1 0 9) "+ imp1+ "\n")
    PNS_model.write("344 24 -1.42 -304 TRCL= (-1 0 -8.8) "+ imp1+ "\n")
    PNS_model.write("345 24 -1.42 -303 TRCL= (-1 0 10) "+ imp1+ "\n")
    PNS_model.write("346 24 -1.42 -304 TRCL= (-1 0 -10) "+ imp1+ "\n")
    PNS_model.write("347 24 -1.42 -303 TRCL= (-1 0 11) "+ imp1+ "\n")
    PNS_model.write("348 24 -1.42 -304 TRCL= (-1 0 -11) "+ imp1+ "\n")
    PNS_model.write("349 24 -1.42 -303 TRCL= (-1 0 12) "+ imp1+ "\n")
    PNS_model.write("350 24 -1.42 -304 TRCL= (-1 0 -12) "+ imp1+ "\n")
    PNS_model.write("351 24 -1.42 -303 TRCL= (-1 0 13) "+ imp1+ "\n")
    PNS_model.write("352 24 -1.42 -304 TRCL= (-1 0 -13) "+ imp1+ "\n")
    PNS_model.write("353 24 -1.42 -303 TRCL= (-1 0 14) "+ imp1+ "\n")
    PNS_model.write("354 24 -1.42 -304 TRCL= (-1 0 -14) "+ imp1+ "\n")
    PNS_model.write("C    --------TLD MATERIAL (B-SIDE)------\n")
    PNS_model.write("C    X-axis front casing of Li-7\n")
    PNS_model.write("500 24 -1.42 -500 "+ imp1+ "\n")
    PNS_model.write(TRCL(501, 500, 3, 0, 0))
    PNS_model.write(TRCL(502, 500, -3, 0, 0))
    PNS_model.write(TRCL(503, 500, 6, 0, 0))
    PNS_model.write(TRCL(504, 500, -5.8, 0, 0))
    PNS_model.write(TRCL(505, 500, 8, 0, 0))
    PNS_model.write(TRCL(506, 500, -7.8, 0, 0))
    PNS_model.write(TRCL(507, 500, 9, 0, 0))
    PNS_model.write(TRCL(508, 500, -8.8, 0, 0))
    PNS_model.write(TRCL(509, 500, 10, 0, 0))
    PNS_model.write(TRCL(510, 500, -10, 0, 0))
    PNS_model.write(TRCL(511, 500, 11, 0, 0))
    PNS_model.write(TRCL(512, 500, -11, 0, 0))
    PNS_model.write(TRCL(513, 500, 12, 0, 0))
    PNS_model.write(TRCL(514, 500, -12, 0, 0))
    PNS_model.write(TRCL(515, 500, 13, 0, 0))
    PNS_model.write(TRCL(516, 500, -13, 0, 0))
    PNS_model.write(TRCL(517, 500, 14, 0, 0))
    PNS_model.write(TRCL(518, 500, -14, 0, 0))
    PNS_model.write("C    Y-axis front casing of Li-7\n")
    PNS_model.write("519 24 -1.42 -501 TRCL= (0 3 0) "+ imp1+ "\n")
    PNS_model.write("520 24 -1.42 -502 TRCL= (0 -3 0) "+ imp1+ "\n")
    PNS_model.write("521 24 -1.42 -501 TRCL= (0 6 0) "+ imp1+ "\n")
    PNS_model.write("522 24 -1.42 -502 TRCL= (0 -5.8 0) "+ imp1+ "\n")
    PNS_model.write("523 24 -1.42 -501 TRCL= (0 8 0) "+ imp1+ "\n")
    PNS_model.write("524 24 -1.42 -502 TRCL= (0 -7.8 0) "+ imp1+ "\n")
    PNS_model.write("525 24 -1.42 -501 TRCL= (0 9 0) "+ imp1+ "\n")
    PNS_model.write("526 24 -1.42 -502 TRCL= (0 -8.8 0) "+ imp1+ "\n")
    PNS_model.write("527 24 -1.42 -501 TRCL= (0 10 0) "+ imp1+ "\n")
    PNS_model.write("528 24 -1.42 -502 TRCL= (0 -10 0) "+ imp1+ "\n")
    PNS_model.write("529 24 -1.42 -501 TRCL= (0 11 0) "+ imp1+ "\n")
    PNS_model.write("530 24 -1.42 -502 TRCL= (0 -11 0) "+ imp1+ "\n")
    PNS_model.write("531 24 -1.42 -501 TRCL= (0 12 0) "+ imp1+ "\n")
    PNS_model.write("532 24 -1.42 -502 TRCL= (0 -12 0) "+ imp1+ "\n")
    PNS_model.write("533 24 -1.42 -501 TRCL= (0 13 0) "+ imp1+ "\n")
    PNS_model.write("534 24 -1.42 -502 TRCL= (0 -13 0) "+ imp1+ "\n")
    PNS_model.write("535 24 -1.42 -501 TRCL= (0 14 0) "+ imp1+ "\n")
    PNS_model.write("536 24 -1.42 -502 TRCL= (0 -14 0) "+ imp1+ "\n")
    PNS_model.write("C    Z-axis front casing of Li-7\n")
    PNS_model.write("537 24 -1.42 -503 TRCL= (-1 0 3) "+ imp1+ "\n")
    PNS_model.write("538 24 -1.42 -504 TRCL= (-1 0 -3) "+ imp1+ "\n")
    PNS_model.write("539 24 -1.42 -503 TRCL= (-1 0 6) "+ imp1+ "\n")
    PNS_model.write("540 24 -1.42 -504 TRCL= (-1 0 -5.8) "+ imp1+ "\n")
    PNS_model.write("541 24 -1.42 -503 TRCL= (-1 0 8) "+ imp1+ "\n")
    PNS_model.write("542 24 -1.42 -504 TRCL= (-1 0 -7.8) "+ imp1+ "\n")
    PNS_model.write("543 24 -1.42 -503 TRCL= (-1 0 9) "+ imp1+ "\n")
    PNS_model.write("544 24 -1.42 -504 TRCL= (-1 0 -8.8) "+ imp1+ "\n")
    PNS_model.write("545 24 -1.42 -503 TRCL= (-1 0 10) "+ imp1+ "\n")
    PNS_model.write("546 24 -1.42 -504 TRCL= (-1 0 -10) "+ imp1+ "\n")
    PNS_model.write("547 24 -1.42 -503 TRCL= (-1 0 11) "+ imp1+ "\n")
    PNS_model.write("548 24 -1.42 -504 TRCL= (-1 0 -11) "+ imp1+ "\n")
    PNS_model.write("549 24 -1.42 -503 TRCL= (-1 0 12) "+ imp1+ "\n")
    PNS_model.write("550 24 -1.42 -504 TRCL= (-1 0 -12) "+ imp1+ "\n")
    PNS_model.write("551 24 -1.42 -503 TRCL= (-1 0 13) "+ imp1+ "\n")
    PNS_model.write("552 24 -1.42 -504 TRCL= (-1 0 -13) "+ imp1+ "\n")
    PNS_model.write("553 24 -1.42 -503 TRCL= (-1 0 14) "+ imp1+ "\n")
    PNS_model.write("554 24 -1.42 -504 TRCL= (-1 0 -14) "+ imp1+ "\n")
    PNS_model.write("C    X-axis Li-7\n")
    PNS_model.write("600 23 -2.635 -600 "+ imp3+ "\n")
    PNS_model.write(TRCL(601, 600, 3, 0, 0))
    PNS_model.write(TRCL(602, 600, -3, 0, 0))
    PNS_model.write(TRCL(603, 600, 6, 0, 0))
    PNS_model.write(TRCL(604, 600, -5.8, 0, 0))
    PNS_model.write(TRCL(605, 600, 8, 0, 0))
    PNS_model.write(TRCL(606, 600, -7.8, 0, 0))
    PNS_model.write(TRCL(607, 600, 9, 0, 0))
    PNS_model.write(TRCL(608, 600, -8.8, 0, 0))
    PNS_model.write(TRCL(609, 600, 10, 0, 0))
    PNS_model.write(TRCL(610, 600, -10, 0, 0))
    PNS_model.write(TRCL(611, 600, 11, 0, 0))
    PNS_model.write(TRCL(612, 600, -11, 0, 0))
    PNS_model.write(TRCL(613, 600, 12, 0, 0))
    PNS_model.write(TRCL(614, 600, -12, 0, 0))
    PNS_model.write(TRCL(615, 600, 13, 0, 0))
    PNS_model.write(TRCL(616, 600, -13, 0, 0))
    PNS_model.write(TRCL(617, 600, 14, 0, 0))
    PNS_model.write(TRCL(618, 600, -14, 0, 0))
    PNS_model.write("C    Y-axis Li-7\n")
    PNS_model.write("619 23 -2.635 -601 TRCL= (0 3 0) "+ imp3+ "\n")
    PNS_model.write("620 23 -2.635 -602 TRCL= (0 -3 0) "+ imp3+ "\n")
    PNS_model.write("621 23 -2.635 -601 TRCL= (0 6 0) "+ imp3+ "\n")
    PNS_model.write("622 23 -2.635 -602 TRCL= (0 -5.8 0) "+ imp3+ "\n")
    PNS_model.write("623 23 -2.635 -601 TRCL= (0 8 0) "+ imp3+ "\n")
    PNS_model.write("624 23 -2.635 -602 TRCL= (0 -7.8 0) "+ imp3+ "\n")
    PNS_model.write("625 23 -2.635 -601 TRCL= (0 9 0) "+ imp3+ "\n")
    PNS_model.write("626 23 -2.635 -602 TRCL= (0 -8.8 0) "+ imp3+ "\n")
    PNS_model.write("627 23 -2.635 -601 TRCL= (0 10 0) "+ imp3+ "\n")
    PNS_model.write("628 23 -2.635 -602 TRCL= (0 -10 0) "+ imp3+ "\n")
    PNS_model.write("629 23 -2.635 -601 TRCL= (0 11 0) "+ imp3+ "\n")
    PNS_model.write("630 23 -2.635 -602 TRCL= (0 -11 0) "+ imp3+ "\n")
    PNS_model.write("631 23 -2.635 -601 TRCL= (0 12 0) "+ imp3+ "\n")
    PNS_model.write("632 23 -2.635 -602 TRCL= (0 -12 0) "+ imp3+ "\n")
    PNS_model.write("633 23 -2.635 -601 TRCL= (0 13 0) "+ imp3+ "\n")
    PNS_model.write("634 23 -2.635 -602 TRCL= (0 -13 0) "+ imp3+ "\n")
    PNS_model.write("635 23 -2.635 -601 TRCL= (0 14 0) "+ imp3+ "\n")
    PNS_model.write("636 23 -2.635 -602 TRCL= (0 -14 0) "+ imp3+ "\n")
    PNS_model.write("C    Z-axis Li-7\n")
    PNS_model.write("637 23 -2.635 -603 TRCL= (-1 0 3) "+ imp3+ "\n")
    PNS_model.write("638 23 -2.635 -604 TRCL= (-1 0 -3) "+ imp3+ "\n")
    PNS_model.write("639 23 -2.635 -603 TRCL= (-1 0 6) "+ imp3+ "\n")
    PNS_model.write("640 23 -2.635 -604 TRCL= (-1 0 -5.8) "+ imp3+ "\n")
    PNS_model.write("641 23 -2.635 -603 TRCL= (-1 0 8) "+ imp3+ "\n")
    PNS_model.write("642 23 -2.635 -604 TRCL= (-1 0 -7.8) "+ imp3+ "\n")
    PNS_model.write("643 23 -2.635 -603 TRCL= (-1 0 9) "+ imp3+ "\n")
    PNS_model.write("644 23 -2.635 -604 TRCL= (-1 0 -8.8) "+ imp3+ "\n")
    PNS_model.write("645 23 -2.635 -603 TRCL= (-1 0 10) "+ imp3+ "\n")
    PNS_model.write("646 23 -2.635 -604 TRCL= (-1 0 -10) "+ imp3+ "\n")
    PNS_model.write("647 23 -2.635 -603 TRCL= (-1 0 11) "+ imp3+ "\n")
    PNS_model.write("648 23 -2.635 -604 TRCL= (-1 0 -11) "+ imp3+ "\n")
    PNS_model.write("649 23 -2.635 -603 TRCL= (-1 0 12) "+ imp3+ "\n")
    PNS_model.write("650 23 -2.635 -604 TRCL= (-1 0 -12) "+ imp3+ "\n")
    PNS_model.write("651 23 -2.635 -603 TRCL= (-1 0 13) "+ imp3+ "\n")
    PNS_model.write("652 23 -2.635 -604 TRCL= (-1 0 -13) "+ imp3+ "\n")
    PNS_model.write("653 23 -2.635 -603 TRCL= (-1 0 14) "+ imp3+ "\n")
    PNS_model.write("654 23 -2.635 -604 TRCL= (-1 0 -14) "+ imp3+ "\n")
    PNS_model.write("C    X-axis back casing of Li-7\n")
    PNS_model.write("700 24 -1.42 -700 "+ imp1+ "\n")
    PNS_model.write(TRCL(701, 700, 3, 0, 0))
    PNS_model.write(TRCL(702, 700, -3, 0, 0))
    PNS_model.write(TRCL(703, 700, 6, 0, 0))
    PNS_model.write(TRCL(704, 700, -5.8, 0, 0))
    PNS_model.write(TRCL(705, 700, 8, 0, 0))
    PNS_model.write(TRCL(706, 700, -7.8, 0, 0))
    PNS_model.write(TRCL(707, 700, 9, 0, 0))
    PNS_model.write(TRCL(708, 700, -8.8, 0, 0))
    PNS_model.write(TRCL(709, 700, 10, 0, 0))
    PNS_model.write(TRCL(710, 700, -10, 0, 0))
    PNS_model.write(TRCL(711, 700, 11, 0, 0))
    PNS_model.write(TRCL(712, 700, -11, 0, 0))
    PNS_model.write(TRCL(713, 700, 12, 0, 0))
    PNS_model.write(TRCL(714, 700, -12, 0, 0))
    PNS_model.write(TRCL(715, 700, 13, 0, 0))
    PNS_model.write(TRCL(716, 700, -13, 0, 0))
    PNS_model.write(TRCL(717, 700, 14, 0, 0))
    PNS_model.write(TRCL(718, 700, -14, 0, 0))
    PNS_model.write("C    Y-axis back casing of Li-7\n")
    PNS_model.write("719 24 -1.42 -701 TRCL= (0 3 0) "+ imp1+ "\n")
    PNS_model.write("720 24 -1.42 -702 TRCL= (0 -3 0) "+ imp1+ "\n")
    PNS_model.write("721 24 -1.42 -701 TRCL= (0 6 0) "+ imp1+ "\n")
    PNS_model.write("722 24 -1.42 -702 TRCL= (0 -5.8 0) "+ imp1+ "\n")
    PNS_model.write("723 24 -1.42 -701 TRCL= (0 8 0) "+ imp1+ "\n")
    PNS_model.write("724 24 -1.42 -702 TRCL= (0 -7.8 0) "+ imp1+ "\n")
    PNS_model.write("725 24 -1.42 -701 TRCL= (0 9 0) "+ imp1+ "\n")
    PNS_model.write("726 24 -1.42 -702 TRCL= (0 -8.8 0) "+ imp1+ "\n")
    PNS_model.write("727 24 -1.42 -701 TRCL= (0 10 0) "+ imp1+ "\n")
    PNS_model.write("728 24 -1.42 -702 TRCL= (0 -10 0) "+ imp1+ "\n")
    PNS_model.write("729 24 -1.42 -701 TRCL= (0 11 0) "+ imp1+ "\n")
    PNS_model.write("730 24 -1.42 -702 TRCL= (0 -11 0) "+ imp1+ "\n")
    PNS_model.write("731 24 -1.42 -701 TRCL= (0 12 0) "+ imp1+ "\n")
    PNS_model.write("732 24 -1.42 -702 TRCL= (0 -12 0) "+ imp1+ "\n")
    PNS_model.write("733 24 -1.42 -701 TRCL= (0 13 0) "+ imp1+ "\n")
    PNS_model.write("734 24 -1.42 -702 TRCL= (0 -13 0) "+ imp1+ "\n")
    PNS_model.write("735 24 -1.42 -701 TRCL= (0 14 0) "+ imp1+ "\n")
    PNS_model.write("736 24 -1.42 -702 TRCL= (0 -14 0) "+ imp1+ "\n")
    PNS_model.write("C    Z-axis front casing of Li-7\n")
    PNS_model.write("737 24 -1.42 -703 TRCL= (-1 0 3) "+ imp1+ "\n")
    PNS_model.write("738 24 -1.42 -704 TRCL= (-1 0 -3) "+ imp1+ "\n")
    PNS_model.write("739 24 -1.42 -703 TRCL= (-1 0 6) "+ imp1+ "\n")
    PNS_model.write("740 24 -1.42 -704 TRCL= (-1 0 -5.8) "+ imp1+ "\n")
    PNS_model.write("741 24 -1.42 -703 TRCL= (-1 0 8) "+ imp1+ "\n")
    PNS_model.write("742 24 -1.42 -704 TRCL= (-1 0 -7.8) "+ imp1+ "\n")
    PNS_model.write("743 24 -1.42 -703 TRCL= (-1 0 9) "+ imp1+ "\n")
    PNS_model.write("744 24 -1.42 -704 TRCL= (-1 0 -8.8) "+ imp1+ "\n")
    PNS_model.write("745 24 -1.42 -703 TRCL= (-1 0 10) "+ imp1+ "\n")
    PNS_model.write("746 24 -1.42 -704 TRCL= (-1 0 -10) "+ imp1+ "\n")
    PNS_model.write("747 24 -1.42 -703 TRCL= (-1 0 11) "+ imp1+ "\n")
    PNS_model.write("748 24 -1.42 -704 TRCL= (-1 0 -11) "+ imp1+ "\n")
    PNS_model.write("749 24 -1.42 -703 TRCL= (-1 0 12) "+ imp1+ "\n")
    PNS_model.write("750 24 -1.42 -704 TRCL= (-1 0 -12) "+ imp1+ "\n")
    PNS_model.write("751 24 -1.42 -703 TRCL= (-1 0 13) "+ imp1+ "\n")
    PNS_model.write("752 24 -1.42 -704 TRCL= (-1 0 -13) "+ imp1+ "\n")
    PNS_model.write("753 24 -1.42 -703 TRCL= (-1 0 14) "+ imp1+ "\n")
    PNS_model.write("754 24 -1.42 -704 TRCL= (-1 0 -14) "+ imp1+ "\n")
    PNS_model.write("C    ---------------CRADLE--------------\n")
    PNS_model.write("C    Upper ring\n")
    PNS_model.write("2000 3 -2.7 (-2001 2000):(-2003 2002):(-2005 2004):(-2007 2006) &\n"
                    "           :(-2009 2008):(-2011 2010):(-2013 2012) "+ imp1+ "\n")
    PNS_model.write("C    Lower ring and base\n")
    PNS_model.write("2001 3 -2.7 -2014 2015 2016 2017 "+ imp1+ "\n")
    PNS_model.write("C    Legs\n")
    PNS_model.write("2002 3 -2.7 -2020 #2000 #2001 "+ imp1+ "\n")
    PNS_model.write("2003 3 -2.7 -2021 #2000 #2001 "+ imp1+ "\n")
    PNS_model.write("2004 3 -2.7 -2022 #2000 #2001 "+ imp1+ "\n")
    PNS_model.write("C    ----------EXTERNAL UNIVERSE--------\n")
    PNS_model.write("999  0 800 imp:n=0 imp:a=0 imp:p=0 imp:e=0\n")
    PNS_model.write("C    ************END OF CELLS************\n")
    
    PNS_model.write("\n")   # blank line at the end of the cell card
    PNS_model.close()

def write_surf_card(run_path,filename,which_source):
    # This function writes all of the surfaces within the PNS. It uses the 
    #  variables 'run_path' and 'filename' to open each input deck as this 
    #  function is called and it appends each line to the input deck. The
    #  variable 'which_source' isn't used yet, but will probably be used if I 
    #  start using more distributed sources so that the source surface can be
    #  adjusted based on the 'which_source' input. The below variables are the 
    #  definitions of some of sizes and locations of various aspects of the 
    #  PNS. It looked cleaner to put them all in the front end rather than 
    #  spread sporadically. This also allowed for using for loops instead of 
    #  hardcoding each line for each position.
    r = 15.1225                 # Sphere radius
    r_cyl = 1.89103             # Cylinder radius
    TLD_slot_w_min = -0.5       # Min value for width of slot for TLD
    TLD_slot_w_max = 0.5        # Max value for width of slot for TLD
    TLD_slot_l_min = -1.10516   # Min value of length of slot for TLD
    TLD_slot_l_max = 1.89484    # Max value of length of slot for TLD
    TLD_slot_x_ax_x_min = [-14.1258,-13.1155,-12.0995,-11.0925,-10.0865,-9.0655,-8.0625,-6.0575,-3.0875,-0.1795,2.7525,5.7525,7.7545,8.7585,9.7625,10.7915,11.8305,12.8575,13.8665]
    TLD_slot_x_ax_x_max = [-13.7555,-12.7585,-11.7495,-10.7355,-9.7205,-8.6975,-7.6725,-5.6965,-2.7015,0.1795,3.1155,6.1135,8.1245,9.1295,10.1565,11.1705,12.1995,13.2255,14.2235]
    TLD_slot_y_ax_y_min = [-14.1258,-13.1155,-12.0995,-11.0925,-10.0865,-9.0655,-8.0625,-6.0575,-3.0875,2.7525,5.7525,7.7545,8.7585,9.7625,10.7915,11.8305,12.8575,13.8665]
    TLD_slot_y_ax_y_max = [-13.7555,-12.7585,-11.7495,-10.7355,-9.7205,-8.6975,-7.6725,-5.6965,-2.7015,3.1155,6.1135,8.1245,9.1295,10.1565,11.1705,12.1995,13.2255,14.2235]
    TLD_slot_z_ax_z_min = [-14.1255,-13.1155,-12.0995,-11.0925,-10.0865,-9.0655,-8.0625,-6.0575,-3.0875,2.7525,5.7525,7.7545,8.7585,9.7625,10.7915,11.8305,12.8575,13.8665]
    TLD_slot_z_ax_z_max = [-13.7555,-12.7585,-11.7495,-10.7355,-9.7205,-8.6975,-7.6725,-5.6965,-2.7015,3.1155,6.1135,8.1245,9.1295,10.1565,11.1705,12.1995,13.2255,14.2235]
    TLD_slot_x_surf_names = [21000, 21100, 21200, 21300, 21400, 21500, 21600, 21700, 21800, 21900, 22000, 22100, 22200, 22300, 22400, 22500, 22600, 22700, 22800]
    TLD_slot_y_surf_names = [23000, 23100, 23200, 23300, 23400, 23500, 23600, 23700, 23800, 23900, 24000, 24100, 24200, 24300, 24400, 24500, 24600, 24700]
    TLD_slot_z_surf_names = [25000, 25100, 25200, 25300, 25400, 25500, 25600, 25700, 25800, 25900, 26000, 26100, 26200, 26300, 26400, 26500, 26600, 26700]
    num_x_TLDs = len(TLD_slot_x_ax_x_min)
    num_y_TLDs = len(TLD_slot_y_ax_y_min)
    num_z_TLDs = len(TLD_slot_z_ax_z_min)
    
    PNS_model = open(run_path + filename, "a")
    PNS_model.write("C    *************SURFACE CARD************\n")
    PNS_model.write("C    -----Container for entire sphere-----\n")
    PNS_model.write("800  RPP -110 110 -110 110 -161.2 110\n")
    PNS_model.write("C    -----SPHERE AND CYLINDER INSERTS-----\n")
    PNS_model.write("20000 SPH   0 0 0   " + str(r) + "\n")
    PNS_model.write("20100 RCC   -" +str(r)+ " 0 0    " +str(2*r)+ " 0 0   " +str(r_cyl)+ " $ X-axis cyl\n")
    PNS_model.write("20200 RCC   0 -" +str(r)+ " 0    0 " +str(2*r)+ " 0   " +str(r_cyl)+ " $ Y-axis cyl\n")
    PNS_model.write("20300 RCC   0 0 -" +str(r)+ "    0 0 " +str(2*r)+ "   " +str(r_cyl)+ " $ Z-axis cyl\n")
    PNS_model.write("C    HOLES IN CYLINDER\n")
    PNS_model.write("C    ----------X-axis TLD slots-----------\n")
    for i in range(num_x_TLDs):
        PNS_model.write(str(TLD_slot_x_surf_names[i])+ " RPP "+ str(TLD_slot_x_ax_x_min[i])+ " "+ str(TLD_slot_x_ax_x_max[i])+ "  "+ str(TLD_slot_w_min)+ " "+ str(TLD_slot_w_max)+ "  "+ str(TLD_slot_l_min)+ " "+ str(TLD_slot_l_max)+ "\n")
    PNS_model.write("C    ----------Y-axis TLD slots-----------\n")
    for i in range(num_y_TLDs):
        PNS_model.write(str(TLD_slot_y_surf_names[i])+ " RPP "+ str(TLD_slot_w_min)+ " "+ str(TLD_slot_w_max)+ "  "+ str(TLD_slot_y_ax_y_min[i])+ " "+ str(TLD_slot_y_ax_y_max[i])+ "  "+ str(TLD_slot_l_min)+ " "+ str(TLD_slot_l_max)+ "\n")
    PNS_model.write("C    ----------Z-axis TLD slots-----------\n")
    for i in range(num_z_TLDs):
        PNS_model.write(str(TLD_slot_z_surf_names[i])+ " RPP "+ str(-1*TLD_slot_l_max)+ " "+ str(-1*TLD_slot_l_min)+ "  "+ str(TLD_slot_w_min)+ " "+ str(TLD_slot_w_max)+ "  "+ str(TLD_slot_z_ax_z_min[i])+ " "+ str(TLD_slot_z_ax_z_max[i])+ "\n")
    PNS_model.write("C    ---------X-axis TLD SURFACES---------\n")
    PNS_model.write("200 RPP  0.0581  0.0781 -0.4275  0.4725  -0.603   1.814   $ Casing\n")
    PNS_model.write("400 RPP  0.02    0.0581 -0.15875 0.15875 -0.15875 0.15875 $ Li-6\n")
    PNS_model.write("300 RPP  0       0.02   -0.4725  0.4725  -0.603   1.814   $ Casing\n")
    PNS_model.write("500 RPP -0.02    0      -0.4725  0.4725  -0.603   1.814   $ Casing\n")
    PNS_model.write("600 RPP -0.0581 -0.02   -0.15875 0.15875 -0.15875 0.15875 $ Li-7\n")
    PNS_model.write("700 RPP -0.0781 -0.0581 -0.4725  0.4725  -0.603   1.814   $ Casing\n")
    PNS_model.write("C    -------(+) Y-axis TLD SURFACES-------\n")
    PNS_model.write("201 RPP -0.4275  0.4725   0.0581  0.0781 -0.603   1.814   $ Casing\n")
    PNS_model.write("401 RPP -0.15875 0.15875  0.02    0.0581 -0.15875 0.15875 $ Li-6\n")
    PNS_model.write("301 RPP -0.4725  0.4725   0       0.02   -0.603   1.814   $ Casing\n")
    PNS_model.write("501 RPP -0.4725  0.4725  -0.02    0      -0.603   1.814   $ Casing\n")
    PNS_model.write("601 RPP -0.15875 0.15875 -0.0581 -0.02   -0.15875 0.15875 $ Li-7\n")
    PNS_model.write("701 RPP -0.4725  0.4725  -0.0781 -0.0581 -0.603   1.814   $ Casing\n")
    PNS_model.write("C    -------(-) Y-axis TLD SURFACES-------\n")
    PNS_model.write("202 RPP -0.4275  0.4725  -0.0781 -0.0581 -0.603   1.814   $ Casing\n")
    PNS_model.write("402 RPP -0.15875 0.15875 -0.0581 -0.02   -0.15875 0.15875 $ Li-6\n")
    PNS_model.write("302 RPP -0.4725  0.4725  -0.02    0      -0.603   1.814   $ Casing\n")
    PNS_model.write("502 RPP -0.4725  0.4725   0       0.02   -0.603   1.814   $ Casing\n")
    PNS_model.write("602 RPP -0.15875 0.15875  0.02    0.0581 -0.15875 0.15875 $ Li-7\n")
    PNS_model.write("702 RPP -0.4725  0.4725   0.0581  0.0781 -0.603   1.814   $ Casing\n")
    PNS_model.write("C    -------(+) Z-axis TLD SURFACES-------\n")
    PNS_model.write("203 RPP -0.603   1.814   -0.4275  0.4725   0.0581  0.0781 $ Casing\n")
    PNS_model.write("403 RPP -0.15875 0.15875 -0.15875 0.15875  0.02    0.0581 $ Li-6\n")
    PNS_model.write("303 RPP -0.603   1.814   -0.4725  0.4725   0       0.02   $ Casing\n")
    PNS_model.write("503 RPP -0.603   1.814   -0.4725  0.4725  -0.02    0      $ Casing\n")
    PNS_model.write("603 RPP -0.15875 0.15875 -0.15875 0.15875 -0.0581 -0.02   $ Li-7\n")
    PNS_model.write("703 RPP -0.603   1.814   -0.4725  0.4725  -0.0781 -0.0581 $ Casing\n")
    PNS_model.write("C    -------(-) Z-axis TLD SURFACES-------\n")
    PNS_model.write("204 RPP -0.603   1.814   -0.4275  0.4725  -0.0781 -0.0581 $ Casing\n")
    PNS_model.write("404 RPP -0.15875 0.15875 -0.15875 0.15875 -0.0581 -0.02   $ Li-6\n")
    PNS_model.write("304 RPP -0.603   1.814   -0.4725  0.4725  -0.02    0      $ Casing\n")
    PNS_model.write("504 RPP -0.603   1.814   -0.4725  0.4725   0       0.02   $ Casing\n")
    PNS_model.write("604 RPP -0.15875 0.15875 -0.15875 0.15875  0.02    0.0581 $ Li-7\n")
    PNS_model.write("704 RPP -0.603   1.814   -0.4725  0.4725   0.0581  0.0781 $ Casing\n")
    PNS_model.write("C    ----------CRADLE UPPER RING----------\n")
    PNS_model.write("2000  RCC 0 0 -14.03 0 0 0.43 6.4   $ Part 1\n")
    PNS_model.write("2001  RCC 0 0 -14.03 0 0 0.43 8.2   $ Part 1\n")
    PNS_model.write("2002  RCC 0 0 -13.60 0 0 0.10 6.6   $ Part 2\n")
    PNS_model.write("2003  RCC 0 0 -13.60 0 0 0.10 8.2   $ Part 2\n")
    PNS_model.write("2004  RCC 0 0 -13.50 0 0 0.10 6.8   $ Part 3\n")
    PNS_model.write("2005  RCC 0 0 -13.50 0 0 0.10 8.2   $ Part 3\n")
    PNS_model.write("2006  RCC 0 0 -13.40 0 0 0.10 7.0   $ Part 4\n")
    PNS_model.write("2007  RCC 0 0 -13.40 0 0 0.10 8.2   $ Part 4\n")
    PNS_model.write("2008  RCC 0 0 -13.30 0 0 0.10 7.2   $ Part 5\n")
    PNS_model.write("2009  RCC 0 0 -13.30 0 0 0.10 8.2   $ Part 5\n")
    PNS_model.write("2010  RCC 0 0 -13.20 0 0 0.10 7.4   $ Part 6\n")
    PNS_model.write("2011  RCC 0 0 -13.20 0 0 0.10 8.2   $ Part 6\n")
    PNS_model.write("2012  RCC 0 0 -13.10 0 0 0.07 7.6   $ Part 7\n")
    PNS_model.write("2013  RCC 0 0 -13.10 0 0 0.07 8.1   $ Part 7\n")
    PNS_model.write("C    -------------CRADLE BASE-------------\n")
    PNS_model.write("2014  RCC  0    0    -31.16 0 0    0.80 16.0  $ Ring\n")
    PNS_model.write("2015  RCC  0.0  8.0  -31.16 0 0    0.80 5.0   $ Holes\n")
    PNS_model.write("2016  RCC  6.9 -4.0  -31.16 0 0    0.80 5.0   $ Holes\n")
    PNS_model.write("2017  RCC -6.9 -4.0  -31.16 0 0    0.80 5.0   $ Holes\n")
    PNS_model.write("C    -------------CRADLE LEGS-------------\n")
    PNS_model.write("2020  RCC  0.0  -14.8 -31.00  0.00  7.50 17.2 0.4   $ Leg\n")
    PNS_model.write("2021  RCC  12.8  7.4  -31.00 -6.48 -3.75 17.2 0.4   $ Leg\n")
    PNS_model.write("2022  RCC -12.8  7.4  -31.00  6.48 -3.75 17.2 0.4   $ Leg\n")
    PNS_model.write("C    -----------SOURCE SURFACES-----------\n")
    PNS_model.write("9999   SPH   0 0 0 50\n")
    PNS_model.write("C    ***********END OF SURFACES***********\n")
    PNS_model.write("\n")   # blank line at the end of the surface card
    PNS_model.close()
    
def write_material_card(run_path,filename):
    # This card defines all of the materials in the input deck and writes the
    #  associated card for them. I don't anticipate this will change much, but
    #  maybe later in the project it will.
    PNS_model = open(run_path + filename, "a")
    PNS_model.write("C    ************MATERIAL CARD************\n")
    PNS_model.write("C    Moist air from LLNL PNS; Other materials from PNNL Materials Compendium\n")
    PNS_model.write("C       Moist Air @ den = 1.2e-3 g/cm3\n")
    PNS_model.write("m1      8016   -0.2403 7014  -0.7460   18000 -1.239e-2\n")
    PNS_model.write("        6000  -1.21e-4 1001  -1.3367e-3\n")
    PNS_model.write("mt1     lwtr.60t\n")
    PNS_model.write("C       Al  aluminum, den = 2.7 g/cm3\n")
    PNS_model.write("m3      13027 -1\n")
    PNS_model.write("C       Au  gold, den = 19.1 g/cm3\n")
    PNS_model.write("m2      79197 -1\n")
    PNS_model.write("C 	POLYETHLENE, NON-BORATED, C2H4\n")
    PNS_model.write("m20	 1001.80C 	0.333338	$ H\n")
    PNS_model.write("		 6000.80C 	0.666662 	$ C\n")
    PNS_model.write("mt20 poly.01t\n")
    PNS_model.write("C LITHIUM-6 Flouride @ den = 2.635 g/cm3\n")
    PNS_model.write("m22 3006 -0.267585 9000 -0.732415\n")
    PNS_model.write("C LITHIUM-7 Flouride  @ den = 2.635 g/cm3\n")
    PNS_model.write("m23 3007 -0.267585 9000 -0.732415\n")
    PNS_model.write("C KAPTON POLYIMIDE FILM CASING @ den = 1.42 g/cm3\n")
    PNS_model.write("m24 1000 -0.026362 6000 -0.691133 7000 -0.073270 8000 -0.209235\n")
    PNS_model.write("C    ***********END OF MATERIAL***********\n")
    PNS_model.write("C\n")
    PNS_model.close()

def write_source_card(run_path,filename,sdef,sdef_mod):
    # This card writes in the source information using the 'sdef' and 
    #  'sdef_mod' variables, which are chosen in the function 
    #  define_which_source(). The for loop below iterates through all of the 
    #  strings within the 'sdef_mod' variable.
    PNS_model = open(run_path + filename, "a")
    PNS_model.write("C    *************SOURCE CARD*************\n")
    PNS_model.write("mode  n a p e  $ Transport neutrons\n")
    if isinstance(sdef,str):
        PNS_model.write(sdef)
    elif isinstance(sdef,tuple):
        for line in sdef:
            PNS_model.write(sdef)
    for line in sdef_mod:
        PNS_model.write(line)
    PNS_model.write("C    ************END OF SOURCE************\n")
    PNS_model.write("C\n")
    PNS_model.close()
    
def write_tally_card(run_path, filename):
    # This card writes all of the tally commands. I'm working based off of
    #  Paige's example and for some reason, she only has tallies on the Li-6.
    PNS_model = open(run_path + filename, "a")
    PNS_model.write("C    *************TALLY CARD**************\n")
    PNS_model.write("C Tally cards: Need gamma/alpha/nuetron energy deposition in each detector.\n")
    PNS_model.write("C    --------------LITHIUM 6--------------\n")
    PNS_model.write("C X-axis\n")
    PNS_model.write("+F4006 (400)\n")
    PNS_model.write("+F4016 (401)\n")
    PNS_model.write("+F4026 (402)\n")
    PNS_model.write("+F4036 (403)\n")
    PNS_model.write("+F4046 (404)\n")
    PNS_model.write("+F4056 (405)\n")
    PNS_model.write("+F4066 (406)\n")
    PNS_model.write("+F4076 (407)\n")
    PNS_model.write("+F4086 (408)\n")
    PNS_model.write("+F4096 (409)\n")
    PNS_model.write("+F4106 (410)\n")
    PNS_model.write("+F4116 (411)\n")
    PNS_model.write("+F4126 (412)\n")
    PNS_model.write("+F4136 (413)\n")
    PNS_model.write("+F4146 (414)\n")
    PNS_model.write("+F4156 (415)\n")
    PNS_model.write("+F4166 (416)\n")
    PNS_model.write("+F4176 (417)\n")
    PNS_model.write("+F4186 (418)\n")
    PNS_model.write("C Y-axis\n")
    PNS_model.write("+F4196 (419)\n")
    PNS_model.write("+F4206 (420)\n")
    PNS_model.write("+F4216 (421)\n")
    PNS_model.write("+F4226 (422)\n")
    PNS_model.write("+F4236 (423)\n")
    PNS_model.write("+F4246 (424)\n")
    PNS_model.write("+F4256 (425)\n")
    PNS_model.write("+F4266 (426)\n")
    PNS_model.write("+F4276 (427)\n")
    PNS_model.write("+F4286 (428)\n")
    PNS_model.write("+F4296 (429)\n")
    PNS_model.write("+F4306 (430)\n")
    PNS_model.write("+F4316 (431)\n")
    PNS_model.write("+F4326 (432)\n")
    PNS_model.write("+F4336 (433)\n")
    PNS_model.write("+F4346 (434)\n")
    PNS_model.write("+F4356 (435)\n")
    PNS_model.write("+F4366 (436)\n")
    PNS_model.write("C Z-axis\n")
    PNS_model.write("+F4376 (437)\n")
    PNS_model.write("+F4386 (438)\n")
    PNS_model.write("+F4396 (439)\n")
    PNS_model.write("+F4406 (440)\n")
    PNS_model.write("+F4416 (441)\n")
    PNS_model.write("+F4426 (442)\n")
    PNS_model.write("+F4436 (443)\n")
    PNS_model.write("+F4446 (444)\n")
    PNS_model.write("+F4456 (445)\n")
    PNS_model.write("+F4466 (446)\n")
    PNS_model.write("+F4476 (447)\n")
    PNS_model.write("+F4486 (448)\n")
    PNS_model.write("+F4496 (449)\n")
    PNS_model.write("+F4506 (450)\n")
    PNS_model.write("+F4516 (451)\n")
    PNS_model.write("+F4526 (452)\n")
    PNS_model.write("+F4536 (453)\n")
    PNS_model.write("+F4546 (454)\n")
    PNS_model.write("C    ************END OF TALLIES***********\n")
    PNS_model.close()

def write_print_card(run_path,filename,nps):
    # This card writes the print commands to record tallies at various nps's 
    #  throughout the run.
    PNS_model = open(run_path + filename, "a")
    PNS_model.write("C    *************PRINT CARD**************\n")
    PNS_model.write("dbcn  7j  1 0 0 0 0 154917 j\n") # This appears to be a debugging code?
    PNS_model.write("C        ndp     ndm     mct ndmp dmmp  Values below ckecked by LCh\n")
    PNS_model.write("prdmp   1.0e+09  0         1   2    0\n")
    PNS_model.write("ctme    57600      $ 1200\n")
    PNS_model.write("nps  "+nps+"\n")
    
def write_sbatch(run_path,dir1,dir2,Ebins,Ebin_names,numNodes,numCores):
    # This function writes the SBATCH file which is what is needed to run these
    #  input decks on Quartz.
    sbatch_file = open(run_path + '\\' + dir1 + "batch.bash","x",newline='\n')
    sbatch_file.write("#!/bin/csh\n")
    sbatch_file.write("#SBATCH -N " + str(len(Ebins)) + "\n")
    sbatch_file.write("#SBATCH -J Condon_PNS" + str(dir2) + "\n")
    sbatch_file.write("#SBATCH -t 23:30:00\n")
    sbatch_file.write("#SBATCH -p pbatch\n")
    sbatch_file.write("#SBATCH --mail-type=ALL\n")
    sbatch_file.write("#SBATCH -A cbronze\n")
    sbatch_file.write("#SBATCH -D /g/g20/condon3/PNS/" + dir2 + "\n")
    sbatch_file.write("\n")
    sbatch_file.write("echo '=================Job diagnostics================='\n")
    sbatch_file.write("date\n")
    sbatch_file.write("echo -n 'This machine is ';hostname\n")
    sbatch_file.write("echo -n 'My jobid is '; echo $SLURM_JOBID\n")
    sbatch_file.write("echo 'My path is:'\n")
    sbatch_file.write("echo $PATH\n")
    sbatch_file.write("echo 'My job info:'\n")
    sbatch_file.write("squeue -j $SLURM_JOBID\n")
    sbatch_file.write("echo 'Machine info'\n")
    sbatch_file.write("sinfo -s\n")
    sbatch_file.write("\n")
    sbatch_file.write("echo '=================Job Starting================='\n")
    sbatch_file.write("echo 'Job_id = $SLURM_JOBID'\n")
    for ebin_name in Ebin_names:
        sbatch_file.write("srun -N"+str(numNodes)+" -n"+str(numCores)+" mcnp6 i=PNS_"+str(ebin_name)+" o=out_PNS_"+str(ebin_name)+" runtpe=r_PNS_"+str(ebin_name)+" &\n")
    sbatch_file.write("\n")
    sbatch_file.write("wait\n")
    sbatch_file.write("echo 'Done'")
    sbatch_file.close()

def write_sbatch_spectrum(run_path,dir1,dir2,num_runs):
    # This function writes the SBATCH file which is what is needed to run these
    #  input decks on Quartz. This function focuses on writing the sbtach file 
    #  for the input decks that contain an energy spectrum.
    sbatch_file = open(run_path + '\\' + dir1 + "batch.bash","x",newline='\n')
    sbatch_file.write("#!/bin/csh\n")
    sbatch_file.write("#SBATCH -N " + str(num_runs) + "\n")
    sbatch_file.write("#SBATCH -J Condon_PNS" + str(dir2) + "\n")
    sbatch_file.write("#SBATCH -t 23:30:00\n")
    sbatch_file.write("#SBATCH -p pbatch\n")
    sbatch_file.write("#SBATCH --mail-type=ALL\n")
    sbatch_file.write("#SBATCH -A cbronze\n")
    sbatch_file.write("#SBATCH -D /g/g20/condon3/PNS/" + dir2 + "\n")
    sbatch_file.write("\n")
    sbatch_file.write("echo '=================Job diagnostics================='\n")
    sbatch_file.write("date\n")
    sbatch_file.write("echo -n 'This machine is ';hostname\n")
    sbatch_file.write("echo -n 'My jobid is '; echo $SLURM_JOBID\n")
    sbatch_file.write("echo 'My path is:'\n")
    sbatch_file.write("echo $PATH\n")
    sbatch_file.write("echo 'My job info:'\n")
    sbatch_file.write("squeue -j $SLURM_JOBID\n")
    sbatch_file.write("echo 'Machine info'\n")
    sbatch_file.write("sinfo -s\n")
    sbatch_file.write("\n")
    sbatch_file.write("echo '=================Job Starting================='\n")
    sbatch_file.write("echo 'Job_id = $SLURM_JOBID'\n")
    for i in range(num_runs):
        sbatch_file.write("srun -N1 -n1 mcnp6 i=Run"+str(i+1)+"_rand_energy o=out_Run"+str(i+1)+"_rand_energy runtpe=r_Run"+str(i+1)+"_rand_energy &\n")
    sbatch_file.write("\n")
    sbatch_file.write("wait\n")
    sbatch_file.write("echo 'Done'")
    sbatch_file.close()
    
def write_sbatch_continuation(run_path,dir1,dir2,Ebins,Ebin_names,numNodes,numCores):
    # Quartz has a 24 hour time limit. In case that limit gets hit by the first
    #  batch file, this one will take the runtp files and continue the run.
    sbatch_file = open(run_path + '\\' + dir1 + "batch_cont.bash","x",newline='\n')
    sbatch_file.write("#!/bin/csh\n")
    sbatch_file.write("#SBATCH -N " + str(len(Ebins)) + "\n")
    sbatch_file.write("#SBATCH -J Condon_PNS" + str(dir2) + "\n")
    sbatch_file.write("#SBATCH -t 23:30:00\n")
    sbatch_file.write("#SBATCH -p pbatch\n")
    sbatch_file.write("#SBATCH --mail-type=ALL\n")
    sbatch_file.write("#SBATCH -A cbronze\n")
    sbatch_file.write("#SBATCH -D /g/g20/condon3/PNS/" + dir2 + "\n")
    sbatch_file.write("\n")
    sbatch_file.write("echo '=================Job diagnostics================='\n")
    sbatch_file.write("date\n")
    sbatch_file.write("echo -n 'This machine is ';hostname\n")
    sbatch_file.write("echo -n 'My jobid is '; echo $SLURM_JOBID\n")
    sbatch_file.write("echo 'My path is:'\n")
    sbatch_file.write("echo $PATH\n")
    sbatch_file.write("echo 'My job info:'\n")
    sbatch_file.write("squeue -j $SLURM_JOBID\n")
    sbatch_file.write("echo 'Machine info'\n")
    sbatch_file.write("sinfo -s\n")
    sbatch_file.write("\n")
    sbatch_file.write("echo '=================Job Starting================='\n")
    sbatch_file.write("echo 'Job_id = $SLURM_JOBID'\n")
    for ebin_name in Ebin_names:
        sbatch_file.write("srun -N"+str(numNodes)+" -n"+str(numCores)+" mcnp6 c r=r_PNS_"+str(ebin_name)+" o=out_PNS_"+str(ebin_name)+"_cont &\n")
    sbatch_file.write("\n")
    sbatch_file.write("wait\n")
    sbatch_file.write("echo 'Done'")
    sbatch_file.close()

def write_sbatch_continuation_spectrum(run_path,dir1,dir2,num_runs):
    # Quartz has a 24 hour time limit. In case that limit gets hit by the first
    #  batch file, this one will take the runtp files and continue the run.
    sbatch_file = open(run_path + '\\' + dir1 + "batch_cont.bash","x",newline='\n')
    sbatch_file.write("#!/bin/csh\n")
    sbatch_file.write("#SBATCH -N " + str(num_runs) + "\n")
    sbatch_file.write("#SBATCH -J Condon_PNS" + str(dir2) + "\n")
    sbatch_file.write("#SBATCH -t 23:30:00\n")
    sbatch_file.write("#SBATCH -p pbatch\n")
    sbatch_file.write("#SBATCH --mail-type=ALL\n")
    sbatch_file.write("#SBATCH -A cbronze\n")
    sbatch_file.write("#SBATCH -D /g/g20/condon3/PNS/" + dir2 + "\n")
    sbatch_file.write("\n")
    sbatch_file.write("echo '=================Job diagnostics================='\n")
    sbatch_file.write("date\n")
    sbatch_file.write("echo -n 'This machine is ';hostname\n")
    sbatch_file.write("echo -n 'My jobid is '; echo $SLURM_JOBID\n")
    sbatch_file.write("echo 'My path is:'\n")
    sbatch_file.write("echo $PATH\n")
    sbatch_file.write("echo 'My job info:'\n")
    sbatch_file.write("squeue -j $SLURM_JOBID\n")
    sbatch_file.write("echo 'Machine info'\n")
    sbatch_file.write("sinfo -s\n")
    sbatch_file.write("\n")
    sbatch_file.write("echo '=================Job Starting================='\n")
    sbatch_file.write("echo 'Job_id = $SLURM_JOBID'\n")
    for i in range(num_runs):
        sbatch_file.write("srun -N1 -n1 mcnp6 c r=r_Run"+str(i+1)+"_rand_energy o=out_Run"+str(i+1)+"_rand_energy_cont&\n")
    sbatch_file.write("\n")
    sbatch_file.write("wait\n")
    sbatch_file.write("echo 'Done'")
    sbatch_file.close()
    
def write_PNS_input(Ebins,Ebin_names,sdef_list,nps,which_source,numNodes,numCores):
    # This is the main function that calls all of the other functions to write
    #  the PNS input decks and batch files.
    sbatch_dir1 = make_today_dir()
    path,sbatch_dir2 = make_run_dir()
    if (which_source == 1) or (which_source == 2) or (which_source == 3) or (which_source == 5):
        num_runs = len(Ebins)
        source_text, sdef_mod, source_strength = define_which_source(which_source, Ebins, sdef_list)
        write_run_notes(path,sbatch_dir2,num_runs,source_text)
        write_sbatch(path,sbatch_dir1,sbatch_dir2,Ebins,Ebin_names,numNodes,numCores)
        write_sbatch_continuation(path,sbatch_dir1,sbatch_dir2,Ebins,Ebin_names,numNodes,numCores)
        for E in range(num_runs):
            filename = "\PNS_" + Ebin_names[E]
            initialize_PNS_deck(path,filename,Ebins[E])
            write_cell_card(path,filename)
            write_surf_card(path,filename,which_source)
            write_material_card(path,filename)
            write_source_card(path,filename,sdef_list[E],sdef_mod)
            write_tally_card(path,filename)
            write_print_card(path,filename,nps)
    elif which_source == 4:
        num_runs = 1
        source_text = "The source for this is a random spectrum, more info below\n"
        write_run_notes(path,sbatch_dir2,num_runs,source_text)
        write_sbatch_spectrum(path,sbatch_dir1,sbatch_dir2,num_runs)
        write_sbatch_continuation_spectrum(path,sbatch_dir1,sbatch_dir2,num_runs)
        for i in range(num_runs):
            filename = "\Run" + str(i+1) + "_rand_energy"
            initialize_PNS_deck(path,filename,0)
            write_cell_card(path,filename)
            write_surf_card(path,filename,which_source)
            write_material_card(path,filename)
            source_text, sdef_mod, source_strength = define_which_source(which_source,Ebins,sdef_list)
            append_run_notes(path,sbatch_dir2,i,source_strength)
            write_source_card(path,filename,sdef_list[i],sdef_mod)
            write_tally_card(path,filename)
            write_print_card(path,filename,nps)
    
    # Copy files from cloud-saved directory to a directory for transferring to 
    #  LLNL's quartz computer.
    source_directory = path
    destination_directory = 'C:\\Users\\zacht\\AppData\\Local\\Packages\\CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc\\LocalState\\rootfs\\home\\zach\\Research\\quartzTransfer\\' + sbatch_dir2
    shutil.copytree(source_directory,destination_directory)