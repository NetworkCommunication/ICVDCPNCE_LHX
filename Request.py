'''

@author: Hung-hsuan

'''

import random
from Zipf import Zipf
import xlrd
from Cache import Cache
import copy
import numpy as np
import math

class Request:

    def __init__(self, vehicle_cluster):
        self.vehicle_cluster = vehicle_cluster                


    # 获取
    def get_file(self):
        rb = xlrd.open_workbook('document\cache.xls', encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        data_type = [[] for i in range(10)]        
        for i in range(0, rs.nrows):
            for j in range(1, 11):
                if j == rs.cell_value(i, 3):
                    data_type[j-1].append(rs.cell_value(i, 0))
                    break
        return data_type


    def send_request(self, vehicle_file_popularity):
        a = 0.1                                        
        x = 1
        user_request_result_time = {}               
        data_type = Request.get_file(self)           
        all_request_files = []                      
        file_zipf = [[] for i in range(10)]         
        vehicle_has_been_request = []                


        zipf1 = Zipf()
        for i in range(0, len(data_type)):
            file_zipf[i].append(zipf1.get_zipf(len(data_type[i])))


      

        vehicle_request_popularity = copy.deepcopy(vehicle_file_popularity)         

        total_request_num = 0  
        user_request_list = {}
        for t in self.vehicle_cluster:
            user_request_result = {}  
            vehicle_request_number = {}  
            vehicle_id = []  
    
            vehicle_cluster_list = []
            for item_2 in self.vehicle_cluster[t]:
                for item_3 in item_2:
                    vehicle_cluster_list.append(item_3)
            vehicle_cluster_set = set(vehicle_cluster_list)
            vehicle_cluster_list = list(vehicle_cluster_set)

          
            for item in vehicle_cluster_list:
                vehicle_request_number[item] = zipf1.get_possion()[0]
    
            for k in vehicle_request_number:
                total_request_num = total_request_num + vehicle_request_number[k]
                
                for item in vehicle_cluster_list:
                    item = int(item)
                    vehicle_id.append(item)

            for m in range(0, 1000000):                
                sum = 0
                flag = 0                                  
                type_id = -1
                if vehicle_id:                            
                    user_id = int(random.choice(vehicle_id))
                    if vehicle_request_number[user_id] != 0:   
                        for item in vehicle_has_been_request:          
                            if item == user_id:                        
                                flag = 1
                                parameter = random.random()
                                if parameter > 1:                    
                                    type_id = random.randint(1, 10)    
                                    for it in range(1, 11):
                                        if it == type_id:
                                            vehicle_request_popularity[user_id][type_id-1] = vehicle_request_popularity[user_id][type_id-1] + (2/(np.pi)) * (math.atan(a * x)) * (1 - vehicle_request_popularity[user_id][type_id-1])
                                        else:
                                            vehicle_request_popularity[user_id][it-1] = vehicle_request_popularity[user_id][it-1] - (2 / (9 * np.pi)) * (math.atan(a * x)) * (1 - vehicle_request_popularity[user_id][it-1])
                                            if vehicle_request_popularity[user_id][it-1] <= 0:
                                                vehicle_request_popularity[user_id][it-1] = 0.01
                                else:
                                    control_parameter_1 = random.random()
                                    for i in range(0, 10):
                                        if sum < control_parameter_1 and control_parameter_1 <= (sum + vehicle_request_popularity[user_id][i]):
                                            type_id = i + 1
                                            for it in range(1, 11):
                                                if it == type_id:
                                                    vehicle_request_popularity[user_id][type_id-1] = vehicle_request_popularity[user_id][type_id-1] + (2/(np.pi)) * (math.atan(a * x)) * (1 - vehicle_request_popularity[user_id][type_id-1])
                                                else:
                                                    vehicle_request_popularity[user_id][it-1] = vehicle_request_popularity[user_id][it-1] - (2 / (9 * np.pi)) * (math.atan(a * x)) * (1 - vehicle_request_popularity[user_id][it-1])
                                                    if vehicle_request_popularity[user_id][it-1] <= 0:
                                                        vehicle_request_popularity[user_id][it-1] = 0.01
                                            break
                                        else:
                                            sum = sum + vehicle_request_popularity[user_id][i-1]
                                break

                        if flag == 0:                     
                            sun = 0
                            control_parameter_1 = random.random()
                            for i in range(0, 10):
                                if sun < control_parameter_1 and control_parameter_1 <= (sun + vehicle_file_popularity[user_id][i]):
                                    type_id = i + 1
                                    for it in range(1, 11):
                                        if it == type_id:
                                            vehicle_request_popularity[user_id][type_id-1] = vehicle_request_popularity[user_id][type_id-1] + (2/(np.pi)) * (math.atan(a * x)) * (1 - vehicle_request_popularity[user_id][type_id-1])
                                        else:
                                            vehicle_request_popularity[user_id][it-1] = vehicle_request_popularity[user_id][it-1] - (2 / (9 * np.pi)) * (math.atan(a * x)) * (1 - vehicle_request_popularity[user_id][it-1])
                                            if vehicle_request_popularity[user_id][it-1] <= 0:
                                                vehicle_request_popularity[user_id][it-1] = 0.01
                                    break
                                else:
                                    sun = sun + vehicle_file_popularity[user_id][i-1]
                            vehicle_has_been_request.append(user_id)                      

                        if type_id == -1:
                            type_id = 10
                      
                        control_parameter3 = random.random()
                        if control_parameter3 > 0.3:
                            flag = 0  
                            for item_n in range(0, 100000):
                                request_id = random.choice(data_type[type_id-1])
                                if user_id in user_request_list.keys():           
                                    for item in user_request_list[user_id]:
                                        if int(item) == int(request_id):                    
                                            flag = 1
                                            break
                                    if flag == 0:
                                        user_request_result.setdefault(user_id, []).append(request_id)
                                        user_request_list.setdefault(user_id, []).append(request_id)
                                        all_request_files.append(request_id)
                                        vehicle_request_number[user_id] = vehicle_request_number[user_id] - 1
                                        break
                                else:
                                    user_request_result.setdefault(user_id, []).append(request_id)
                                    user_request_list.setdefault(user_id, []).append(request_id)
                                    all_request_files.append(request_id)
                                    vehicle_request_number[user_id] = vehicle_request_number[user_id] - 1
                                    break                                   
                        else:
                            flag_1 = 0
                            sun = 0
                            control_parameter2 = random.random()
                            for j in range(0, len(file_zipf[type_id - 1][0])):
                                if sun < control_parameter2 and control_parameter2 <= (sun + file_zipf[type_id-1][0][j]):
                                    request_id = data_type[type_id-1][j + 1]
                                    if user_id in user_request_list.keys():           
                                        for item in user_request_list[user_id]:
                                            if int(item) == int(request_id):                    
                                                flag_1 = 1
                                                break
                                        if flag_1 == 0:
                                            user_request_result.setdefault(user_id, []).append(request_id)
                                            user_request_list.setdefault(user_id, []).append(request_id)
                                            all_request_files.append(request_id)
                                            vehicle_request_number[user_id] = vehicle_request_number[user_id] - 1
                                            break
                                    else:
                                        user_request_result.setdefault(user_id, []).append(request_id)
                                        user_request_list.setdefault(user_id, []).append(request_id)
                                        all_request_files.append(request_id)
                                        vehicle_request_number[user_id] = vehicle_request_number[user_id] - 1
                                        break                                     
                                else:
                                    sun = sun + file_zipf[type_id-1][0][j]
                    else:
                        vehicle_id.remove(user_id)                         
                else:
                    break  
            user_request_result_time.setdefault(t, user_request_result)
        print("user_request_result_time="+str(user_request_result_time))
        print("user_request_list=" + str(user_request_list))
        return total_request_num, all_request_files, user_request_result_time, vehicle_request_popularity
