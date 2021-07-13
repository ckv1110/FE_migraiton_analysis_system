import os
import get_prescribe_node_id_xyz_v2 as get_node
import host_mesh_fit_data_v2 as hmf
import calculate_and_generate_prescribed_displacements_abs as calc
import replace_base_nodes_for_next_iter_abs as rep_nodes


exp = 't115_ctrl_tram'
itr = [1,10,19,28,37,46,55,64,72]
number = 0


def set_variable(script, count):
    if script == 'get_node':
        get_node.name = exp
        get_node.prev_itr = itr[0]
        get_node.new_itr = itr[count + 1]
    elif script == 'hmf':
        hmf.name = exp
        # hmf.prev_itr = itr[0]
        hmf.prev_itr = itr[count]
        hmf.new_itr = itr[count + 1]
    elif script == 'calc':
        calc.name = exp
        calc.prev_itr = itr[0]
        calc.abs_itr = itr[count]
        calc.new_itr = itr[count + 1]
    elif script == 'rep_nodes':
        rep_nodes.name = exp
        rep_nodes.prev_itr = itr[0]
        rep_nodes.abs_itr = itr[count]
        rep_nodes.new_itr = itr[count + 1]

def automate(counter):
    while counter <= (len(itr) - 2):
        print('Doing {}_{}_{}_v2_redo'.format(exp, str(itr[0]).zfill(2), str(itr[counter + 1]).zfill(2)))
        set_variable('get_node',counter)
        get_node.main()
        # set_variable('hmf',counter)
        # hmf.main()
        set_variable('calc',counter)
        calc.main()
        os.system('febio3 -i {}_{}_{}_v2_redo_hmf.feb'.format(exp, str(itr[0]).zfill(2), str(itr[counter + 1]).zfill(2)))
        set_variable('rep_nodes',counter)
        rep_nodes.main()
        counter += 1

#select index of the previous_itr number to start this function
def single(target_number):
    print('Doing {}_{}_{}_v2'.format(exp, str(itr[target_number]).zfill(2), str(itr[target_number + 1]).zfill(2)))
    set_variable('get_node', target_number)
    get_node.main()
    # set_variable('hmf', target_number)
    # hmf.main()
    set_variable('calc', target_number)
    calc.main()
    os.system('febio3 -i {}_{}_{}_v2_redo_hmf.feb'.format(exp, str(itr[target_number]).zfill(2), str(itr[target_number + 1]).zfill(2)))
    set_variable('rep_nodes', number)
    rep_nodes.main()

automate(number)
# single(1)