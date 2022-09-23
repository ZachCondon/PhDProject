# This script contains all the functions that I use to scrape the out files
#  from MCNP.

import re
import csv
import pickle

def get_tally_lines(filename,nps):
    # This function will pull the whole line of text from the MCNP output file
    #  that starts with the exact number of the nps. For most of the results, 
    #  the line of text will contain tally results for three cells. For the
    #  last line, there could be 1, 2, or 3 cells account for, depending on if
    #  the number of tallied cells is divisible by three.
    # Example: A input deck with 7 tallys will result in two lines of text with
    #  tally information from three cells and one line of text with tally info
    #  for just one cell.
    # Requirements for input variables:
        # filename: Either needs to be the absolute filename (including all 
        #  parent directors for the output file or just the file name if this
        #  function is used when in the output file's directory.
        # nps: This needs to be a whole number and written as an integer
        #  variable. It can be written in long notation (eg: 5000) or
        # scientific notation (eg: 5e3).
    linenum = 0
    tally_lines = list()
    tally_pattern = re.compile(r"\s{2}" + str(int(nps)) + r"\s{3}\d")
    with open (filename, 'rt') as myfile:
        for line in myfile:
            linenum += 1
            if tally_pattern.search(line) != None:
                tally_lines.append((line.rstrip('\n')))
    return tally_lines

def get_all_tally_info(filename,nps):
    # This function will use the function "get_tally_lines" to extract all the 
    #  lines of text that contain tally information. It will use those lines
    #  and call the other functions to ultimately save csv files for each of
    #  the following pieces of information that are given in the MCNP output:
        # mean
        # error
        # vov (variance of the variance)
        # slope
    # NOTE: This function will only get tally information for the one filename
    #  that is the input variable. To get all tallys for a full run, this
    #  function will need to be iterated over all the output files.
    # Requirements for input variables:
        # filename: Either needs to be the absolute filename (including all 
        #  parent directors for the output file or just the file name if this
        #  function is used when in the output file's directory.
        # nps: This needs to be a whole number and written as an integer
        #  variable. It can be written in long notation (eg: 5000) or
        # scientific notation (eg: 5e3).
    tally_lines = get_tally_lines(filename, nps)
    mean_list = get_mean_tallys(tally_lines)
    error_list = get_error_tallys(tally_lines)
    vov_list = get_vov_tallys(tally_lines)
    slope_list = get_slope_tallys(tally_lines)
    return mean_list, error_list, vov_list, slope_list

def get_mean_tallys(tally_lines):
    # This function will use the tally line text to pull the mean tally info.
    #  The output of this function is a 1D list containing the mean 
    #  tally values from tally F4006 to F4546. See my research journal for what
    #  each of the tally numbers refer to (search for the heading: Tally
    #  Information and Locations)
    #  https://docs.google.com/document/d/1CIg4ETJVoVQchuie8n_l7KHJ207i1lsxXQs1UgCE3TE/edit?usp=sharing
    mean_list = list()
    for tally_line in tally_lines:
        # print(tally_line)
        tally_line_float = [float(digit) for digit in tally_line.split() if digit.isdigit]
        mean_list.append(tally_line_float[1])
        try:
            mean_list.append(tally_line_float[6])
            mean_list.append(tally_line_float[11])
        except:
            pass
    return mean_list

def get_error_tallys(tally_lines):
    # This function will use the tally line text to pull the error tally info.
    #  The output of this function is a 1D list containing the error 
    #  tally values from tally F4006 to F4546. See my research journal for what
    #  each of the tally numbers refer to (search for the heading: Tally
    #  Information and Locations)
    #  https://docs.google.com/document/d/1CIg4ETJVoVQchuie8n_l7KHJ207i1lsxXQs1UgCE3TE/edit?usp=sharing
    error_list = list()
    for tally_line in tally_lines:
        # print(tally_line)
        tally_line_float = [float(digit) for digit in tally_line.split() if digit.isdigit]
        error_list.append(tally_line_float[2])
        try:
            error_list.append(tally_line_float[7])
            error_list.append(tally_line_float[12])
        except:
            pass
    return error_list

def get_vov_tallys(tally_lines):
    # This function will use the tally line text to pull the vov tally info.
    #  The output of this function is a 1D list containing the vov 
    #  tally values from tally F4006 to F4546. See my research journal for what
    #  each of the tally numbers refer to (search for the heading: Tally
    #  Information and Locations)
    #  https://docs.google.com/document/d/1CIg4ETJVoVQchuie8n_l7KHJ207i1lsxXQs1UgCE3TE/edit?usp=sharing
    vov_list = list()
    for tally_line in tally_lines:
        # print(tally_line)
        tally_line_float = [float(digit) for digit in tally_line.split() if digit.isdigit]
        vov_list.append(tally_line_float[3])
        try:
            vov_list.append(tally_line_float[8])
            vov_list.append(tally_line_float[13])
        except:
            pass
    return vov_list

def get_slope_tallys(tally_lines):
    # This function will use the tally line text to pull the slope tally info.
    #  The output of this function is a 1D list containing the slope 
    #  tally values from tally F4006 to F4546. See my research journal for what
    #  each of the tally numbers refer to (search for the heading: Tally
    #  Information and Locations)
    #  https://docs.google.com/document/d/1CIg4ETJVoVQchuie8n_l7KHJ207i1lsxXQs1UgCE3TE/edit?usp=sharing
    slope_list = list()
    for tally_line in tally_lines:
        # print(tally_line)
        tally_line_float = [float(digit) for digit in tally_line.split() if digit.isdigit]
        slope_list.append(tally_line_float[4])
        try:
            slope_list.append(tally_line_float[9])
            slope_list.append(tally_line_float[14])
        except:
            pass
    return slope_list

def get_statistics_check_lines(filename):
    # This function pulls all of the lines from the output file that say how
    #  many statistical checks each tally cell passed or missed.
    # The form the regex pattern is looking for is:
        # "     4NNN   XXssed"
    statistics_lines = list()
    statistics_pattern = re.compile(r"\s{5}4\d\d\d\s{3}\w\wssed")
    with open(filename, 'rt') as myfile:
        for line in myfile:
            if statistics_pattern.search(line) != None:
                statistics_lines.append((line.rstrip('\n')))
    return statistics_lines

def make_stats_dict(E_bin_names):
    # This function will take all of the statistic_lines from the function
    #  get_statistics_check_lines and make a dictionary storing all of the 
    #  information. The keys of the dictionary will be the tally names (eg. 
    #  "4006", "4016", ...) and the values will be the number of statistical
    #  checks that each tally passed in the MCNP run.
    # The way the output file (which the statistics lines came from) works is 
    #  that the line will either read:
        # "4006" passed all checks
    #  or
        # "4006" missed X out of 10 checks
    #  In the function below, I will get the number from the line of text and 
    #  subtract it from 10.
    tally_names = ['4006', '4016', '4026', '4036', '4046', '4056', '4066', 
               '4076', '4086', '4096', '4106', '4116', '4126', '4136', 
               '4146', '4156', '4166', '4176', '4186', '4196', '4206', 
               '4216', '4226', '4236', '4246', '4256', '4266', '4276', 
               '4286', '4296', '4306', '4316', '4326', '4336', '4346', 
               '4356', '4366', '4376', '4386', '4396', '4406', '4416', 
               '4426', '4436', '4446', '4456', '4466', '4476', '4486', 
               '4496', '4506', '4516', '4526', '4536', '4546']
    stats_dict = {}
    for E_bin in E_bin_names:
        stats_dict[E_bin] = {}
        
    for E_bin in E_bin_names:
        filename = 'out_PNS_'+E_bin
        statistics_lines = get_statistics_check_lines(filename)
        for name in tally_names:
            stats_dict[E_bin][name] = []

        for line in statistics_lines:
            for name in tally_names:
                if line.split()[0] == name:
                    if line.split()[1] == 'passed':
                        stats_dict[E_bin][name].append(10)
                    else:
                        stats_dict[E_bin][name].append(10-int(line.split()[2]))
    pickle_file_name = 'stats_checks.pickle'
    with open(pickle_file_name,'wb') as f:
          pickle.dump(stats_dict,f)
    return stats_dict

def save_data(filename,headers,tally_lists):
    with open(filename,'w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(tally_lists)
    return