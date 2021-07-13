import numpy as np


name = None
prev_itr = int()
new_itr = int()
abs_itr = int()

def main():
    base_coord_file = name + '_' + str(prev_itr).zfill(2) + '_' + str(new_itr).zfill(2) + '_v2_redo_altered_prescribed_coordinates.xyz'
    # If you want absolute displacement use base file below for base node coordinates
    base_coord_file = name + '_' + str(prev_itr).zfill(3) + '_hmf.xyz'

    coord_file = name + '_' + str(new_itr).zfill(3) + '_hmf.xyz'
    base_feb_file = name + '_' + str(prev_itr).zfill(2) + '_' + str(new_itr).zfill(2) + '_v2_redo.feb'
    new_feb_file = name + '_' + str(prev_itr).zfill(2) + '_' + str(new_itr).zfill(2) + '_v2_redo_hmf.feb'


    def calculate_coord_differences(coord_axis):
        if coord_axis == 'x':
            col_type = 0
            base_x_coord = np.loadtxt(base_coord_file, usecols=(col_type))
            base_x_coord_32 = np.delete(base_x_coord, np.s_[0::2], 0)
            # print(base_x_coord_32)
            x_coord = np.loadtxt(coord_file, usecols=(col_type))
            grouped_x_coord = x_coord.reshape(-1, 2)
            mean_x_coord = np.mean(grouped_x_coord, axis=1)
            final_x_coord = mean_x_coord - base_x_coord_32
            # print(base_x_coord_32, mean_x_coord, final_x_coord)
            # exit(-1)
            return (final_x_coord)
        elif coord_axis == 'y':
            col_type = 1
            base_y_coord = np.loadtxt(base_coord_file, usecols=(col_type))
            base_y_coord_32 = np.delete(base_y_coord, np.s_[0::2], 0)
            # print(base_y_coord_32)
            y_coord = np.loadtxt(coord_file, usecols=(col_type))
            grouped_y_coord = y_coord.reshape(-1, 2)
            mean_y_coord = np.mean(grouped_y_coord, axis=1)
            # print(mean_y_coord)
            final_y_coord = mean_y_coord - base_y_coord_32
            return (final_y_coord)


    def find_string_in_file(string_search):
        line_number = 0
        with open(base_feb_file, 'r') as read_obj:
            for line in read_obj:
                if string_search in line:
                    ln = line_number
                line_number += 1
        return(ln)


    #Copies original text over to a copy file for editing and modifying
    with open(base_feb_file, 'r') as f:
        with open(new_feb_file, 'w+') as f1:
            for base_line in f:
                f1.write(base_line)


    #Overwrite displacement with deformed displacement
    def overwrite_line(axis, edit_line_number,number_string):
        unmod_file = open(new_feb_file, 'r+')
        line = unmod_file.readlines()
        old_line = line[edit_line_number]
        new_line = old_line.replace(
            '>1',
            '>{}'.format(calculate_coord_differences(axis)[number_string - 1]),
            -1
        )
        line[edit_line_number] = new_line
        mod_file = open(new_feb_file, 'w+')
        mod_file.writelines(line)
        mod_file.close()
        return

    #change the prev_itr's into abs_itr's to fo absolute calculations
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


    def write_coord_changes():
        number_string = 1
        while number_string <= 32:
            set_axis = 'x'
            editing_line = find_string_in_file(
                '<bc name="PrescribedDisplacement%s_%s" type="prescribe" node_set="PrescribedDisplacement%s_%s">'
                %(str(number_string).zfill(2), set_axis, str(number_string).zfill(2), set_axis)) + 2
            overwrite_line(set_axis, editing_line, number_string)

            set_axis = 'y'
            editing_line = find_string_in_file(
                '<bc name="PrescribedDisplacement%s_%s" type="prescribe" node_set="PrescribedDisplacement%s_%s">'
                %(str(number_string).zfill(2), set_axis, str(number_string).zfill(2), set_axis)) + 2
            overwrite_line(set_axis, editing_line, number_string)

            number_string += 1

        log_line = find_string_in_file('<logfile>')
        # log_node_displacement_line = find_string_in_file('<logfile>') + 2
        overwrite_log_line(log_line + 1, 'xyz')
        overwrite_log_line(log_line + 2, 'displacement')
        overwrite_log_line(log_line + 3, 'p1')


    write_coord_changes()

    print('prescribed_nodes calculated and replaced!')

