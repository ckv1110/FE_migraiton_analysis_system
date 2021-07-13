import numpy as np

name = 't115_rad_tram'
prev_itr = 1
new_itr = 72

base_coord_file = name + '_' + str(prev_itr).zfill(3) + '_hmf.xyz'
coord_file = name + '_' + str(new_itr).zfill(3) + '_hmf.xyz'

def calculate_coord_differences(coord_axis):
    if coord_axis == 'x':
        col_type = 0
        base_x_coord = np.loadtxt(base_coord_file, usecols=(col_type))
        grouped_base_x_coord = base_x_coord.reshape(-1, 2)
        base_x_coord_mean = np.mean(grouped_base_x_coord, axis=1)
        # print(base_x_coord_mean)
        x_coord = np.loadtxt(coord_file, usecols=(col_type))
        grouped_x_coord = x_coord.reshape(-1, 2)
        mean_x_coord = np.mean(grouped_x_coord, axis=1)
        final_x_coord = mean_x_coord - base_x_coord_mean
        # print(base_x_coord_mean, mean_x_coord)
        return (final_x_coord)
    elif coord_axis == 'y':
        col_type = 1
        base_y_coord = np.loadtxt(base_coord_file, usecols=(col_type))
        grouped_base_y_coord = base_y_coord.reshape(-1, 2)
        base_y_coord_mean = np.mean(grouped_base_y_coord, axis=1)
        # print(base_y_coord_32)
        y_coord = np.loadtxt(coord_file, usecols=(col_type))
        grouped_y_coord = y_coord.reshape(-1, 2)
        mean_y_coord = np.mean(grouped_y_coord, axis=1)
        # print(mean_y_coord)
        final_y_coord = mean_y_coord - base_y_coord_mean
        return (final_y_coord)

displacement = []
count = 0
x_disp = calculate_coord_differences('x')
y_disp = calculate_coord_differences('y')
while count < len(x_disp):
    a = np.sqrt((x_disp[count]**2) + (y_disp[count]**2))
    displacement.append(a)
    count += 1

a = np.vstack(x_disp)
b = np.vstack(y_disp)
c = np.vstack(displacement)

check_arr = np.hstack((a,b,c))
print(check_arr)

np.savetxt((name + '_' + str(prev_itr).zfill(2) + '_' + str(new_itr).zfill(2) + '_overall_displacement.csv'), c, delimiter=',', fmt='%3.6f')