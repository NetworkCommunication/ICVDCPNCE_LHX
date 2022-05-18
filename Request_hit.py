'''
Author: Hung-hsuan


'''


import numpy as np
from Request import Request
import xlrd, xlwt
from xlutils.copy import copy


class Request_hit:
    def __init__(self):
        self.vehicle_file_path = "document\cache.xls"
        self.vehicle_file_path1 = "document\cache_1.xls"
        self.vehicle_file_path2 = "document\cache_2.xls"



    def request_hit(self, vehicle_file_popularity, vehicle_cluster, vehicle_cluster_list):
        vehicle_one_cache = {}                                                        
        user_hit_set = {}
        local_hit_rate = {}                                                            
        not_cache = []

        request = Request(vehicle_cluster)
        total_request_num, all_request_files, user_request_result, vehicle_file_popularity = request.send_request(vehicle_file_popularity)
        rb = xlrd.open_workbook(self.vehicle_file_path1, encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        rb1 = xlrd.open_workbook(self.vehicle_file_path2, encoding_override="utf-8")
        rs1 = rb1.sheet_by_name('contents')

    
        for vehicle_id in vehicle_cluster_list:
            vehicle_id = int(vehicle_id)
            for i in range(1, rs.ncols):
                if rs.cell_value(vehicle_id - 1, i) != '':
                    vehicle_one_cache.setdefault(vehicle_id, []).append(rs.cell_value(vehicle_id - 1, i))
                else:
                    break
   
        for t in vehicle_cluster:
            vehicle_two_cache = []
            for item_1 in vehicle_cluster[t]:
                for vehicle_id in item_1:
                    vehicle_id = int(vehicle_id)
                    for i in range(1, rs1.ncols):
                        flag = 0
                        if rs1.cell_value(vehicle_id - 1, i) != '':
                            if vehicle_two_cache != []:
                                for item in vehicle_two_cache:
                                    if item == rs1.cell_value(vehicle_id - 1, i):
                                        flag = 1
                                        break
                                if flag == 0:
                                    vehicle_two_cache.append(rs1.cell_value(vehicle_id - 1, i))
                            else:
                                vehicle_two_cache.append(rs1.cell_value(vehicle_id - 1, i))
                        else:
                            break


            i = 0
            j = 0
            n = 0
    
            for vehicle_id_1 in user_request_result[t]:
                vehicle_id_1 = int(vehicle_id_1)
                flag = 0
                for item in user_request_result[t][vehicle_id_1]:
                    j = j + 1
                    item = int(item)
                    for em in vehicle_one_cache[vehicle_id_1]:
                        em = int(em)
                        if em == item:
                            flag = 1
                            break
                    if flag == 0:                     
                        n = n + 1
                        flag1 = 0                    
                        for im in vehicle_two_cache:
                            im = int(im)
                            if im == item:
                                flag1 = 1
                                break
                        if flag1 == 0:               
                            user_hit_set.setdefault(vehicle_id_1, []).append(0)
                            not_cache.append(item)
                        else:
                            user_hit_set.setdefault(vehicle_id_1, []).append(-1)       
                    else:
                        user_hit_set.setdefault(vehicle_id_1, []).append(1)             
        print("user_hit_set="+str(user_hit_set))



        sun = 0                                    
        suu = 0
        cooperation_cache_hit_num = 0              
        for item in user_hit_set:
            sum = 0                                
            for em in user_hit_set[item]:
                if em == 1:
                    sum = sum + 1
                    sun = sun + 1
                    suu = suu + 1
                elif em == -1:
                    cooperation_cache_hit_num = cooperation_cache_hit_num + 1
                    sun = sun + 1
            hit_rate = sum / len(user_hit_set[item])
            local_hit_rate.setdefault(item, []).append(hit_rate)

        all_cache_hit_rate = sun / total_request_num                           
        single_cache_hit_rate = suu / total_request_num
        if total_request_num == sun:                                            
            cooperation_hit_rate = 0
        else:
            cooperation_hit_rate = cooperation_cache_hit_num / (total_request_num - suu)
       

       
        rb2 = xlrd.open_workbook(self.vehicle_file_path, encoding_override="utf-8")
        rs2 = rb2.sheet_by_name('contents')
        wb2 = copy(rb2)
        ws2 = wb2.get_sheet('contents')

        for file_id in all_request_files:
            file_id = int(file_id)
            file_request_num = rs2.cell_value(file_id - 1, 2) + 1
            ws2.write(file_id - 1, 2, file_request_num)
        wb2.save(self.vehicle_file_path)

        return cooperation_hit_rate, local_hit_rate, all_cache_hit_rate, user_request_result, vehicle_file_popularity, single_cache_hit_rate

