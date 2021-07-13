import re
import numpy as np


name = None
prev_itr = int()
new_itr = int()


def main():
    text = name + '_' + str(prev_itr).zfill(2) + '_' + str(new_itr).zfill(2) + '_v2_redo'

    def search_string_in_file(string_to_search):
        line_number = 0
        global found
        found = 0
        with open((text + '.feb'), 'r') as read_obj:
            for line in read_obj:
                line_number += 1
                # For each line, check if line contains the string
                if string_to_search in line:
                    # If yes, then use line_number associated with the string
                    found = line_number
        # Return line_number that string was found
        return found


    def list_search_string_in_file(string_to_search):
        line_number = 0
        global get_number
        get_number = []
        with open(text + '.feb', 'r') as read_obj:
            for line in read_obj:
                # For each line, check if line contains the string
                if string_to_search in line:
                    # If yes, then use line_number associated with the string
                    get_number.append(line_number)
                line_number += 1
        # Return line_number that string was found
        return get_number


    def generate_full_xyz_file(coord_start,coord_end):
        arr = []
        count = 0
        with open((text + '.feb'), 'r') as f:
            line = f.readlines()
            #Clears whitespaces
            strip_line = [elem.strip() for elem in line]
            real_coord_end = coord_end - 2
            #Establish start and end of the xyz coordinates in the feb file
            raw_coordinates = strip_line[coord_start:real_coord_end]
            while count < len(raw_coordinates):
                #Removes unwanted characters
                clean = raw_coordinates[count].replace('</node>','').replace('<node id="%s">'%(count+1),'')
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

    def prescribed_node_id(prescribe_start,prescribe_end):
    #prescribe_start = search_string_in_file('<NodeSet name="PrescribedDisplacement01_x">')
    #prescribe_end = search_string_in_file('<SolidDomain name="Part1" mat="Material1"/>')
        prescribe_arr = []
        count = 0
        with open((text + '.feb'), 'r') as f:
            line = f.readlines()
            strip_line = [elem.strip() for elem in line]
            #deletes the prescribed displacement lines to avoid integers complications later down the line
            del_index_array_01 = list_search_string_in_file('<NodeSet name="PrescribedDisplacement')
            # del_index_array_02 = list_search_string_in_file('<NodeSet name="FixedDisplacement')
            # full_del_index_array = np.hstack((del_index_array_01, del_index_array_02))
            clean_strip_line = np.delete(strip_line, del_index_array_01)
            real_prescribe_start = prescribe_start
            real_prescribe_end = prescribe_end - (2 + len(del_index_array_01)) #2 lines above where it needs to end and the deleted lines beforehand accounted for
            raw_prescribe = clean_strip_line[real_prescribe_start:real_prescribe_end]
        #Remove non-numeric data from the list
        while count < len(raw_prescribe):
            numeric_string = re.sub("[^0-9]", "", raw_prescribe[count])
            prescribe_arr.append(numeric_string)
            count += 1
        #prescribe_numbers = np.stack(prescribe_arr,axis=0)
        filter_prescribe_arr = list(filter(None, prescribe_arr))
        n = [int(i) for i in filter_prescribe_arr]
        #removes duplicate
        dupe = set()
        non_dupe = []
        for item in n:
            if item not in dupe:
                dupe.add(item)
                non_dupe.append(item)
        return non_dupe

    #List of all the node xyz coordinates in the order specified by the feb file
    full_xyz_coordinates = generate_full_xyz_file(search_string_in_file('<Nodes name="Object01">'),search_string_in_file('<Elements type="hex8" name="Part1">'))
    #List of all the node ids in the order specified by the feb file
    node_ids = prescribed_node_id(search_string_in_file('</Elements>'),search_string_in_file('</Mesh>'))


    #Empty array to be appended with prescribed node id coordinates
    prescribed_node_xyz = []
    c = 0
    #Set each node_id as an index to grab their respective coordinates
    for i in node_ids:
        #List number is always one more than the node_id number as list starts at 0
        c = i - 1
        #Appends the prescribed node id coordinates into empty array iteratively
        prescribed_node_xyz.append(full_xyz_coordinates[c])

    # print(len(prescribed_node_xyz))
    #exit(-1)

    list_to_del = []
    count = 0
    while count < len(prescribed_node_xyz):
        a = count + 2
        list_to_del.append(a)
        b = count + 3
        list_to_del.append(b)
        count += 4

    altered_prescribed_node_xyz = np.delete(prescribed_node_xyz, np.array(list_to_del), 0)
    # print(altered_prescribed_node_xyz)
    #Save coordinates as xyz file to be meshed
    np.savetxt((text + '_full_node_xyz.txt'), full_xyz_coordinates, delimiter=' ', fmt='%3.6f')
    np.savetxt((text + '_prescribed_coordinates.xyz'), prescribed_node_xyz, delimiter=' ', fmt='%3.6f')
    np.savetxt((text + '_altered_prescribed_coordinates.xyz'), altered_prescribed_node_xyz, delimiter=' ', fmt='%3.6f')

    print('prescribed_nodes extracted!')
