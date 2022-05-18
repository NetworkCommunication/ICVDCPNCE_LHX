'''
Date: 2021.06.28
Author: Hung-hsuan
Functions:
1、获得车辆的行驶轨迹，根据车辆的id获得周边通信范围内的车辆；
2、根据基站的位置获取在基站通信范围内的车辆。
'''

import numpy as np
import re
import Global_Constant as gc



def read_files(path):
    node_num = 0
    sim_time = 0
    with open(path, 'r') as f:
        # 对文件f的每一行
        for line in f:
            if line.find('set opt(nn)') >= 0:
                line_list = re.split('[\s]', line)
                node_num = int(float(line_list[2]))
            if line.find('set opt(stop)') >= 0:
                line_list = re.split('[\s]', line)
                sim_time = int(float(line_list[2])) 
    return node_num, sim_time



def get_position(mobile_file_path):
    x_max = 0
    y_max = 0
    z_max = 0
    with open(mobile_file_path, 'r') as f:
        movement_list = []
        init_position_list = []
        item_list = []
        key = 0
        for line in f:
            line_list = re.split('[\s]', line) 
            if line_list[0] != '':
                #print(line_list)
                item_list.append(float(line_list[2])) 
                item_list.append(float(line_list[3][8:-1])) 
                if float(line_list[5]) > x_max:
                    x_max = float(line_list[5]) # x坐标
                if float(line_list[6]) > y_max:
                    y_max = float(line_list[6]) # y坐标
                if float(line_list[7][0:-1]) > z_max:
                    z_max = float(line_list[7][0:-1]) 
                item_list.append(float(line_list[5]))
                item_list.append(float(line_list[6]))
                item_list.append(float(line_list[7][0:-1]))
                movement_list.append(item_list)
                item_list = []
            else:
                key = key + 1
    
                if key % 3 == 1:
                    item_list.append(int(line_list[2][7:-1]))
                if key % 3 != 0:
                    item_list.append(float(line_list[7])) # x
                if key % 3 == 0:
                    item_list.append(float(line_list[7])) # y
                    init_position_list.append(item_list)
                    #print(item_list)
                    item_list = []


        movement_matrix = np.mat(movement_list) # 创建矩阵
        init_position_matrix = np.mat(init_position_list)
        return movement_matrix, init_position_matrix



def get_node_position_no_network(movement_matrix, current_t):
    vehicles_no_network_set = []
    sbs_position_left = gc.sbs_position_left
    sbs_position_right = gc.sbs_position_right
    sbs_position_up = gc.sbs_position_up
    sbs_position_down = gc.sbs_position_down
    current_move = movement_matrix[np.nonzero(movement_matrix[:, 0].A == current_t)[0], :]
    # print(current_move)
    for vehicle in current_move:
        distance_1 = pow(pow((vehicle[0, 2] - sbs_position_left[0]), 2) + pow((vehicle[0, 3] - sbs_position_left[1]), 2), 0.5)
        distance_2 = pow(pow((vehicle[0, 2] - sbs_position_right[0]), 2) + pow((vehicle[0, 3] - sbs_position_right[1]), 2), 0.5)
        distance_3 = pow(pow((vehicle[0, 2] - sbs_position_up[0]), 2) + pow((vehicle[0, 3] - sbs_position_up[1]), 2), 0.5)
        distance_4 = pow(pow((vehicle[0, 2] - sbs_position_down[0]), 2) + pow((vehicle[0, 3] - sbs_position_down[1]), 2), 0.5)
        if distance_1 > gc.sbs_max_tranmission_distance and distance_2 > gc.sbs_max_tranmission_distance and distance_3 > gc.sbs_max_tranmission_distance and distance_4 > gc.sbs_max_tranmission_distance:
            vehicles_no_network_set.append(vehicle)
    return vehicles_no_network_set


def get_node_position_have_network(movement_matrix, current_t):
    vehicles_have_network_set_1 = []
    vehicles_have_network_set_2 = []
    vehicles_have_network_set_3 = []
    vehicles_have_network_set_4 = []
    sbs_position_left = gc.sbs_position_left
    sbs_position_right = gc.sbs_position_right
    sbs_position_up = gc.sbs_position_up
    sbs_position_down = gc.sbs_position_down

    current_move = movement_matrix[np.nonzero(movement_matrix[:, 0].A == current_t)[0], :]
    #print(current_move)
    for vehicle in current_move:
        distance_1 = pow(pow((vehicle[0, 2] - sbs_position_left[0]), 2) + pow((vehicle[0, 3] - sbs_position_left[1]), 2), 0.5)
        distance_2 = pow(pow((vehicle[0, 2] - sbs_position_right[0]), 2) + pow((vehicle[0, 3] - sbs_position_right[1]), 2), 0.5)
        distance_3 = pow(pow((vehicle[0, 2] - sbs_position_up[0]), 2) + pow((vehicle[0, 3] - sbs_position_up[1]), 2), 0.5)
        distance_4 = pow(pow((vehicle[0, 2] - sbs_position_down[0]), 2) + pow((vehicle[0, 3] - sbs_position_down[1]), 2), 0.5)
        #print(distance_2)
        if distance_1 <= gc.sbs_max_tranmission_distance:
            vehicles_have_network_set_1.append(vehicle)
        if distance_2 <= gc.sbs_max_tranmission_distance:
            vehicles_have_network_set_2.append(vehicle)
        if distance_3 <= gc.sbs_max_tranmission_distance:
            vehicles_have_network_set_3.append(vehicle)
        if distance_4 <= gc.sbs_max_tranmission_distance:
            vehicles_have_network_set_4.append(vehicle)
    return vehicles_have_network_set_1, vehicles_have_network_set_2, vehicles_have_network_set_3, vehicles_have_network_set_4


def get_node_vehicle_set(vehicle_matrix, vehicle_id, current_t):
    cluster_vehicle_set = []
    vehicle_x = 0
    vehicle_y = 0
    
    current_move = vehicle_matrix[np.nonzero(vehicle_matrix[:, 0].A == current_t)[0], :]
    for vehicle in current_move:
        if (int(vehicle[0, 1]) == int(vehicle_id)):
            vehicle_x = vehicle[0, 2]
            vehicle_y = vehicle[0, 3]
            break
    for vehicle in current_move:
        vehicles_distance = pow(pow((vehicle[0, 2] - vehicle_x), 2) + pow((vehicle[0, 3] - vehicle_y), 2), 0.5)
        if vehicles_distance <= (gc.v2v_max_tranmission_distance):
            cluster_vehicle_set.append(vehicle)
    return cluster_vehicle_set



def judge_node_vehicle(vehicle_matrix, vehicle_id_1, vehicle_id_2, current_t):
    vehicle_x_1 = 0
    vehicle_y_1 = 0
    vehicle_x_2 = 0
    vehicle_y_2 = 0
    current_move = vehicle_matrix[np.nonzero(vehicle_matrix[:, 0].A == current_t)[0], :]
    for vehicle in current_move:
        if (int(vehicle[0, 1]) == int(vehicle_id_1)):
            vehicle_x_1 = vehicle[0, 2]
            vehicle_y_1 = vehicle[0, 3]
            break

    for vehicle in current_move:
        if (int(vehicle[0, 1]) == int(vehicle_id_2)):
            vehicle_x_2 = vehicle[0, 2]
            vehicle_y_2 = vehicle[0, 3]
            break

    vehicles_distance = pow(pow((vehicle_x_1 - vehicle_x_2), 2) + pow((vehicle_y_1 - vehicle_y_2), 2), 0.5)
    if vehicles_distance <= gc.v2v_max_tranmission_distance:
        return 1
    else:
        return 0


def get_vehicle_speed_current(movement_position, vehicle_id, current_t):
    speed = -1
    current_move = movement_position[np.nonzero(movement_position[:, 0].A == current_t)[0], :]
    current_move_1 = movement_position[np.nonzero(movement_position[:, 0].A == current_t + 1)[0], :]
    current_move = current_move.tolist()
    current_move_1 = current_move_1.tolist()

    for i in range(0, len(current_move)):
        if vehicle_id == current_move[i][1]:
            for j in range(0, len(current_move_1)):
                if vehicle_id == current_move_1[j][1]:
                    speed = pow((pow((current_move[i][2] - current_move_1[j][2]), 2) + pow((current_move[i][3] - current_move_1[j][3]), 2)), 0.5)
    return speed

def judge_vehicle_sbs_to_another(movement_position, current_t):
    left_id = []
    right_id = []
    left_to_right = []
    right_to_left = []
    current_move = movement_position[np.nonzero(movement_position[:, 0].A == current_t)[0], :]
    movement_position_1 = current_move.tolist()

    for i in range(0, len(movement_position_1)):
        vehicles_distance = pow(pow((movement_position_1[i][2] - gc.sbs_position_left[0]), 2) + pow((movement_position_1[i][3] - gc.sbs_position_left[1]), 2), 0.5)
        if vehicles_distance <= gc.sbs_max_tranmission_distance:
            left_id.append(movement_position_1[i][1])


    for t in range(280, 311):
        current_move = movement_position[np.nonzero(movement_position[:, 0].A == t)[0], :]
        movement_position_2 = current_move.tolist()
        for j in left_id:
            for i in range(0, len(movement_position_2)):
                if j == movement_position_2[i][1]:
                    vehicles_distance_left_to_right = pow(pow((movement_position_2[i][2] - gc.sbs_position_right[0]), 2) + pow((movement_position_2[i][3] - gc.sbs_position_right[1]), 2), 0.5)
                    if vehicles_distance_left_to_right <= gc.sbs_max_tranmission_distance:
                        left_to_right.append(j)
                        break
    print("left_to_right="+str(left_to_right))







def get_vehicle_speed(movement_position, vehicle_id):
    speed_set = []
    id = []
    movement_position = movement_position.tolist()
    for i in range(0, len(movement_position)):
        if vehicle_id == int(movement_position[i][1]):
            id.append(i)

    for j in range(0, len(id)):
        speed = pow((pow((movement_position[id[j]][2] - movement_position[id[j-1]][2]), 2) + pow((movement_position[id[j]][3] - movement_position[id[j-1]][3]), 2)), 0.5)
        if speed == 0:
            print(movement_position[id[j]][0])
        speed_set.append(speed)
    return speed_set




def get_vehicle_adspeed(movement_position, vehicle_id):
    id = []
    movement_position = movement_position.tolist()
    for i in range(0, len(movement_position)):
        if vehicle_id == int(movement_position[i][1]):
            id.append(i)

    for j in range(0, len(id)-2):
        speed1 = movement_position[id[j+1]][2] - movement_position[id[j]][2]
        speed2 = movement_position[id[j+2]][2] - movement_position[id[j+1]][2]
        s = speed2 - speed1
        print("movement_position[id[j+2]][2]=" + str(movement_position[id[j+2]][2]))
        print("movement_position[id[j+1]][2]=" + str(movement_position[id[j+1]][2]))
        print(speed2)



def get_node_have_no_network_in_place(movement_matrix, current_t):
    vehicle_have_no_network_in_place = []
    sbs_position_left = gc.sbs_position_left
    sbs_position_right = gc.sbs_position_right
    sbs_position_up = gc.sbs_position_up
    sbs_position_down = gc.sbs_position_down
    current_move = movement_matrix[np.nonzero(movement_matrix[:, 0].A == current_t)[0], :]
    for vehicle in current_move:
        if vehicle[0, 3] <= (sbs_position_left[1] + 100) and vehicle[0, 3] >= (sbs_position_left[1] - 100) and vehicle[0, 2] >= (sbs_position_left[0] + 250) and vehicle[0, 2] <= (sbs_position_right[0] - 250):
            vehicle_have_no_network_in_place.append(vehicle)
    return vehicle_have_no_network_in_place



def get_node_in_place(movement_matrix, current_t):
    vehicle_in_place = []
    sbs_position_left = gc.sbs_position_left
    sbs_position_right = gc.sbs_position_right
    sbs_position_up = gc.sbs_position_up
    sbs_position_down = gc.sbs_position_down
    current_move = movement_matrix[np.nonzero(movement_matrix[:, 0].A == current_t)[0], :]
    for vehicle in current_move:
        if vehicle[0, 3] <= (sbs_position_left[1] + 100) and vehicle[0, 3] >= (sbs_position_left[1] - 100) and vehicle[0, 2] >= (sbs_position_left[0] - 250) and vehicle[0, 2] <= (sbs_position_right[0] + 250):
            vehicle_in_place.append(vehicle)
    return vehicle_in_place




def judge_in_SBS(movement_position, vehicle_id, current_t):
    id = []
    sbs_position_left = gc.sbs_position_left
    sbs_position_right = gc.sbs_position_right
    sbs_position_up = gc.sbs_position_up
    sbs_position_down = gc.sbs_position_down
    movement_position = movement_position.tolist()

    for i in range(0, len(movement_position)):
        if vehicle_id == int(movement_position[i][1]):
            distance_1 = pow(pow((movement_position[i][2] - sbs_position_left[0]), 2) + pow((movement_position[i][3] - sbs_position_left[1]), 2), 0.5)
            distance_2 = pow(pow((movement_position[i][2] - sbs_position_right[0]), 2) + pow((movement_position[i][3] - sbs_position_right[1]), 2), 0.5)
            distance_3 = pow(pow((movement_position[i][2] - sbs_position_up[0]), 2) + pow((movement_position[i][3] - sbs_position_up[1]), 2), 0.5)
            distance_4 = pow(pow((movement_position[i][2] - sbs_position_down[0]), 2) + pow((movement_position[i][3] - sbs_position_down[1]), 2), 0.5)
            if distance_1 <= gc.sbs_max_tranmission_distance:
                print("1")
            elif distance_2 <= gc.sbs_max_tranmission_distance:
                print("2")
            elif distance_3 <= gc.sbs_max_tranmission_distance:
                print("3")
            elif distance_4 <= gc.sbs_max_tranmission_distance:
                print("4")
            else:
                print("0")
  

