from datetime import datetime
import os


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

def make_sbatch_files(path,E_bin_names,YYYYMMDD,YYYYMMDDTTTT):
    for E_bin in E_bin_names:
        sbatch_file = open(path + '\\' + E_bin + "batch.bash","x",newline='\n')
        sbatch_file.write("#!/bin/csh\n")
        sbatch_file.write("#SBATCH -N 1\n")
        sbatch_file.write("#SBATCH -J PNS_" + str(E_bin) + "\n")
        sbatch_file.write("#SBATCH -t 23:30:00\n")
        sbatch_file.write("#SBATCH -p pbatch\n")
        sbatch_file.write("#SBATCH --mail-type=ALL\n")
        sbatch_file.write("#SBATCH -A cbronze\n")
        sbatch_file.write("#SBATCH -D /g/g20/condon3/PNS/" + YYYYMMDDTTTT + "\n")
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
        sbatch_file.write("set echo\n")
        sbatch_file.write("setenv DATAPATH /usr/gapps/MCNP_DATA/620\n")
        sbatch_file.write("srun -n36 -k /usr/apps/mcnp/bin/mcnp6.mpi nam=PNS_" + E_bin + " mct=mctal_PNS_" + E_bin + " o=out_PNS_" + E_bin + " runtpe=r_PNS_" + E_bin + "\n")
        sbatch_file.write("\n")
        sbatch_file.write("wait\n")
        sbatch_file.write("echo 'Done'")
        sbatch_file.close()
        
def make_sbatch_bash_script(path,E_bin_names):
    bash_file = open(path + "\\submit_all.bash", "x",newline='\n')
    bash_file.write("#!/bin/csh\n")
    for E_bin in E_bin_names:
        bash_file.write("sbatch " + E_bin + "batch.bash\n")

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


YYYYMMDD = make_today_dir()
path, YYYYMMDDTTTT = make_run_dir()
make_sbatch_files(path,E_bin_names,YYYYMMDD,YYYYMMDDTTTT)
make_sbatch_bash_script(path,E_bin_names)