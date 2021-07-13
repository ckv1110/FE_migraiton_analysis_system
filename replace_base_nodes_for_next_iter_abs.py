import numpy as np

name = None
prev_itr = int()
new_itr = int()
abs_itr = int()

def main():
    coord_text = name + '_' + str(new_itr).zfill(2) + '_feb_xyz.txt'
    coord_to_replace = name + '_' + str(prev_itr).zfill(2) + '_' + str(new_itr).zfill(2) + '_v2_full_node_xyz.txt'
    base_feb_file = name + '_' + str(prev_itr).zfill(2) + '_' + str(new_itr).zfill(2) + '_v2_redo.feb'

    # Change to new_itr in 1st var for relative, prev_itr for abs
    # new_feb_file = name + '_' + str(new_itr).zfill(2) + '_' + str(new_itr + 1).zfill(2) + '_v2_redo.feb'

    if prev_itr == 0:
        new_feb_file = name + '_' + str(new_itr).zfill(2) + '_' + str(prev_itr + 10).zfill(2) + '_v2_redo.feb'  #to make 1_10 file
    elif new_itr == 64:
        # Change to new_itr in 1st var for relative, prev_itr for abs
        new_feb_file = name + '_' + str(prev_itr).zfill(2) + '_' + str(new_itr + 8).zfill(2) + '_v2_redo.feb'  # to make 64_72 file
    else:
        #Change to new_itr in 1st var for relative, prev_itr for abs
        new_feb_file = name + '_' + str(prev_itr).zfill(2) + '_' + str(new_itr + 9).zfill(2) + '_v2_redo.feb'



    def search_string_in_coord_text(string_to_search):
        line_number = 0
        global get_number
        with open(coord_text, 'r') as read_obj:
            for line in read_obj:
                line_number += 1
                # For each line, check if line contains the string
                if string_to_search in line:
                    # If yes, then use line_number associated with the string
                    get_number = line_number
        # Return line_number that string was found
        return get_number


    def find_string_in_file(string_search):
        line_number = 0
        with open(base_feb_file, 'r') as read_obj:
            for line in read_obj:
                if string_search in line:
                    ln = line_number
                line_number += 1
        return(ln)


    def generate_full_xyz_file(coord_start):
        arr = []
        count = 0
        with open(coord_text, 'r') as f:
            line = f.readlines()
            #Clears whitespaces
            strip_line = [elem.strip() for elem in line]
            real_coord_start = coord_start + 2
            real_coord_end = len(line)
            #Establish start and end of the xyz coordinates in the feb file
            raw_coordinates = strip_line[real_coord_start:real_coord_end]
            while count < len(raw_coordinates):
                #Removes unwanted characters
                clean = raw_coordinates[count].replace('<node id="%s">'%(count+1),'').replace('%s','')
                #Converts remaining number strings into float point values
                a = [float(i) for i in clean.split(",")]
                #add these values into the 'arr' array
                arr.append(a)
                count += 1
        #Stack the array with axis = 0, so it will list downwards when writing into a file
        #xyz_coord = np.stack(arr)
        xyz_coord = arr
        # np.savetxt('mesh_template_proper_full_nodes.xyz', xyz_coord, delimiter=' ', fmt='%3.6f')
        return(xyz_coord)


    node_xyz = generate_full_xyz_file(search_string_in_coord_text('Step  = 10'))


    # new_nodes = np.savetxt('mesh_01_feb_final_step_xyz.txt', node_xyz, delimiter=' ',fmt='%3.6f')


    node_z = np.loadtxt(coord_to_replace)
    #only collect xy coordinates
    node_x = []
    node_y = []
    new_node_z = []
    for i in node_xyz:
        node_x.append(i[0])
    for i in node_xyz:
        node_y.append(i[1])
    for i in node_z:
        new_node_z.append(i[2])
    #stack into x,y,z array
    final_node_xyz = np.hstack((np.vstack(node_x),np.vstack(node_y),np.vstack(new_node_z)))


    with open(base_feb_file, 'r') as f:
        with open(new_feb_file, 'w+') as f1:
            for base_line in f:
                f1.write(base_line)


    def list_search_string_in_file(string_to_search):
        line_number = 0
        # global get_number
        get_number = []
        with open(base_feb_file, 'r') as read_obj:
            for line in read_obj:
                # For each line, check if line contains the string
                if string_to_search in line:
                    # If yes, then use line_number associated with the string
                    get_number.append(line_number)
                line_number += 1
        # Return line_number that string was found
        return get_number


    def write_changes():
        count = 0
        editing_line_numbers = list_search_string_in_file('<node id="')
        with open(base_feb_file, 'r') as unmod:
            l = unmod.readlines()
            while count < (len(editing_line_numbers) - 2):
                edit_index = editing_line_numbers[count]
                new_line = ("\t\t\t" + '<node id="%s">' % (count + 1) + str(list(final_node_xyz[count])) + '</node>' + '\n').replace('[', '').replace(']', '').replace(', ', ',')
                l[edit_index] = new_line
                count += 1
            with open(new_feb_file, 'w') as mod:
                mod.writelines(l)
        return

    #Change the prev_itr in abs_itr to do absolute calculations in feb
    def overwrite_log_line(edit, type):
        unmod_file = open(new_feb_file, 'r+')
        line = unmod_file.readlines()
        old_line = line[edit]
        if type == 'xyz':
            new_line = old_line.replace(
                name + '_{}'.format(str(abs_itr).zfill(2)) + '_feb_xyz.txt',
                name + '_{}'.format(str(new_itr).zfill(2)) + '_feb_xyz.txt',
                -1
            )
        elif type == 'displacement':
            new_line = old_line.replace(
                name + '_{}'.format(str(abs_itr).zfill(2)) + '_xy_displacement.txt',
                name + '_{}'.format(str(new_itr).zfill(2)) + '_xy_displacement.txt',
                -1
            )
        elif type == 'p1':
            new_line = old_line.replace(
                name + '_{}'.format(str(abs_itr).zfill(2)) + '_p1_strain.txt',
                name + '_{}'.format(str(new_itr).zfill(2)) + '_p1_strain.txt',
                -1
            )
        line[edit] = new_line
        mod_file = open(new_feb_file, 'w+')
        mod_file.writelines(line)
        mod_file.close()
        return

    #comment write_changes out for abs
    # write_changes()

    log_line = find_string_in_file('<logfile>')
    # log_node_displacement_line = find_string_in_file('<logfile>') + 2
    overwrite_log_line(log_line + 1, 'xyz')
    overwrite_log_line(log_line + 2, 'displacement')
    overwrite_log_line(log_line + 3, 'p1')

    print('replacing nodes to new feb file success!')

