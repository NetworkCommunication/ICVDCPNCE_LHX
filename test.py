'''

Author: Hung-hsuan

'''
import copy
import copy as cp
import Get_Move
from Cache import *
import numpy as np
import Global_Constant as gc

def Test1():
    path = "xy.tcl"
    movement_matrix, init_position = Get_Move.get_position(path)

 
    vehicle_cluster_set_large = {}
    cluster_header = {}    
    for current_t in range(266, 297, gc.update_period):
        vehicle_id = []
        vehicle_information_set = {}
        vehicle_cluster = {}

        vehicle_have_no_network_in_place = Get_Move.get_node_have_no_network_in_place(movement_matrix, current_t)
        for item in vehicle_have_no_network_in_place:
            vehicle_id.append(item[0, 1])
            vehicle_information_set.setdefault(item[0, 1], []).append(item[0, 2])
            vehicle_information_set.setdefault(item[0, 1], []).append(item[0, 3])
        judge_vehicle_matrix = [[0] * len(vehicle_id) for i in range(len(vehicle_id))]      
        value = -1
        for i in range(0, len(vehicle_id)):
            for j in range(0, len(vehicle_id)):
                value = Get_Move.judge_node_vehicle(movement_matrix, vehicle_id[i], vehicle_id[j], current_t)
                judge_vehicle_matrix[i][j] = value
 
        k = 0
        for i in range(0, len(vehicle_id)):
            vehicle_cluster.setdefault(k, []).append(vehicle_id[i])
            for j in range(0, len(vehicle_id)):
                if judge_vehicle_matrix[i][j] == 1 and j != i:
                    vehicle_cluster.setdefault(k, []).append(vehicle_id[j])
            k = k + 1
 

        vehicle_cluster_1 = {}
        for im in vehicle_cluster:
            a = cp.deepcopy(vehicle_cluster[im])
            a = set(a)
            if vehicle_cluster_1 == {}:
                vehicle_cluster_1.setdefault(im, []).append(a)
            else:
                b = []
                flag = 0
                for em in vehicle_cluster_1:
                    b = cp.deepcopy(vehicle_cluster[em])
                    b = set(b)
                    if (a.issubset(b) == True or b.issubset(a) == True) and im != em:
                        flag = 1
                if flag == 0:
                    vehicle_cluster_1.setdefault(im, []).append(a)
 

        vehicle_cluster_list_large = []
        for item_1 in vehicle_cluster_1:
            vehicle_cluster_list = []
            vehicle_cluster_set = vehicle_cluster_1[item_1][0]
            for item in vehicle_cluster_set:
                vehicle_cluster_list.append(item)
            vehicle_cluster_list_large.append(vehicle_cluster_list)
        vehicle_cluster_set_large[current_t] = vehicle_cluster_list_large


  
        for item_1 in vehicle_cluster_1:
            for item_2 in vehicle_cluster_1[item_1]:
                speed_set = {}
                for item_3 in item_2:
                    vehicle_speed = Get_Move.get_vehicle_speed_current(movement_matrix, item_3, current_t)
                    speed_set[item_3] = vehicle_speed
                speed_set_sort = sorted(speed_set.items(), key=lambda x: x[1])
                if len(speed_set_sort) % 2 == 0:
                    a = speed_set_sort[int(len(speed_set_sort)/2)][0]
                    b = speed_set_sort[int(len(speed_set_sort)/2 - 1)][0]
                    if a != b:
                        cluster_header.setdefault(current_t, []).append(100000)
                        cluster_header.setdefault(current_t, []).append(a)
                        cluster_header.setdefault(current_t, []).append(b)
                        cluster_header.setdefault(current_t, []).append(1000000)
                    else:
                        cluster_header.setdefault(current_t, []).append(a)
                else:
                    a = speed_set_sort[int(len(speed_set_sort) / 2)][0]
                    cluster_header.setdefault(current_t, []).append(a)
 
    return vehicle_cluster_set_large
    


