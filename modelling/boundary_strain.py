import numpy as np

name = 't115_ctrl_tram'
new_itr = [10,19,28,37,46,55,64,72]

counter = 0
while counter < len(new_itr):
    number = new_itr[counter]
    p1_text = name + '_' + str(new_itr[counter]).zfill(2) + '_p1_strain.txt'


    def search_string_in_coord_text(string_to_search):
        line_number = 0
        global get_number
        with open(p1_text, 'r') as read_obj:
            for line in read_obj:
                line_number += 1
                # For each line, check if line contains the string
                if string_to_search in line:
                    # If yes, then use line_number associated with the string
                    get_number = line_number
        # Return line_number that string was found
        return get_number


    def generate_full_xyz_file(coord_start):
        arr = []
        count = 0
        with open(p1_text, 'r') as f:
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
                a = [float(i) for i in clean.split(" ")]
                #add these values into the 'arr' array
                arr.append(a)
                count += 1
        #Stack the array with axis = 0, so it will list downwards when writing into a file
        #xyz_coord = np.stack(arr)
        xyz_coord = arr
        # np.savetxt(name + '_' + str(new_itr).zfill(2) + '_final_step_p1.txt', xyz_coord, delimiter=' ', fmt='%3.6f')
        return xyz_coord


    id_p1 = generate_full_xyz_file(search_string_in_coord_text('Step  = 10'))

    boundary_ids = np.loadtxt('boundary_element_ids_ordered.txt')

    # id_p1 = np.loadtxt(name + '_' + str(new_itr).zfill(2) + '_final_step_p1.txt', usecols=1)
    # print(id_p1)

    b_count = 0
    boundary_p1 = []

    while b_count < len(boundary_ids):
        number = int(boundary_ids[b_count] - 1)
        boundary_p1.append(id_p1[number])
        b_count += 1


    # print(boundary_p1)
    # print(boundary_ids)

    np.savetxt(name + '_' + str(new_itr[counter]).zfill(2) + '_boundary_p1_strain.csv',boundary_p1, delimiter=',', fmt='%3.6f')

    counter += 1