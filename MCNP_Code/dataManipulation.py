import re
import csv
import numpy as np
import matplotlib.pyplot as plt

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

def save_data(filename,headers,tally_lists):
    with open(filename,'w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(tally_lists)
    return

def make_graph_compare2(first_data_table,second_data_table,tally_number,
                        plot_title,first_legend,second_legend):
    # Variable requirements:
        # Both data tables need to be for the full range of data from a whole
        #  set of simulations. In other words, they should have 55 columns (one
        #  for each of tally cells) and 84 rows (one for each energy bin)
        # Tally number should be from 0 to 54 to signify which element will get
        #  compared.
        # This section is for Tally 4186, which is at x=-14 from the center
       
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
    first_data_list = np.zeros(84)
    second_data_list = np.zeros(84)
    for i in range(84):
        first_data_list[i] = first_data_table.loc[i][tally_number]
        second_data_list[i] = second_data_table.loc[i][tally_number]

    if len(str(tally_number)) == 1:
        tally_number = '0'+str(tally_number)
        
    fig,ax = plt.subplots()
    ax.semilogx(E_bins,first_data_list,E_bins,second_data_list)
    ax.legend([f'{first_legend} - Tally 4{tally_number}6',f'{second_legend} - Tally 4{tally_number}6'])
    ax.set_xlim(E_bins[0],E_bins[83])
    ax.set_title(f'{plot_title} - Tally 4{tally_number}6')
    fig.savefig(f'{plot_title} - Tally 4{tally_number}6',dpi=400)
    plt.close(fig)
    return

def make_surface_plots(data_table):
    # This function saves the data to be imported into Matlab for a surface
    #  plot. I couldn't find a nice way to have an interactive 3d figure like
    #  Matlab has, so I took this path.
    x = np.arange(-9,10,1)
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
    all_tallys = data_table.to_numpy()
    x_tallys = np.vstack((all_tallys[:,18],all_tallys[:,16],all_tallys[:,14],
                          all_tallys[:,12],all_tallys[:,10],all_tallys[:,8],
                          all_tallys[:,6],all_tallys[:,4],all_tallys[:,2],
                          all_tallys[:,0],all_tallys[:,1],all_tallys[:,3],
                          all_tallys[:,5],all_tallys[:,7],all_tallys[:,9],
                          all_tallys[:,11],all_tallys[:,13],all_tallys[:,15],
                          all_tallys[:,17]))
    x_tallys = np.transpose(x_tallys)
    for i in range(len(x_tallys)):
        x_tallys[i] = x_tallys[i]/max(x_tallys[i])
    X,Y = np.meshgrid(x,E_bins)
    
    np.savetxt('TLD_position.csv',X,delimiter=',')
    np.savetxt('E_bin.csv',Y,delimiter=',')
    np.savetxt('Response.csv',x_tallys,delimiter=',')
    return

def get_tld_totals(tally_table):
    # This function will take in the table containing all the tally information
    #  from the TLDs and will extract the sum of tallys for each TLD and put 
    #  each one in the correct axis and in the correct order. The first number
    #  in each array will be for the negative of that axis and the second will
    #  be for the positive.
    # The first axis of the variable "tld_totals" is for the X axis of the PNS,
    #  the second is for the Y axis, and the third is for the Z axis.
    tld_totals = np.zeros((3,19))
    X_tld_names = ['4186','4166','4146','4126','4106','4086','4066','4046',
                   '4026','4006','4016','4036','4056','4076','4096','4116',
                   '4136','4156','4176']
    Y_tld_names = ['4366','4346','4326','4306','4286','4266','4246','4226',
                   '4206','4006','4196','4216','4236','4256','4276','4296',
                   '4316','4336','4356']
    Z_tld_names = ['4546','4526','4506','4486','4466','4446','4426','4406',
                   '4386','4006','4376','4396','4416','4436','4456','4476',
                   '4496','4516','4536']
    for i in range(19):
        tld_totals[0,i] = sum(tally_table[X_tld_names[i]].values)
        tld_totals[1,i] = sum(tally_table[Y_tld_names[i]].values)
        tld_totals[2,i] = sum(tally_table[Z_tld_names[i]].values)
    return tld_totals