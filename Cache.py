'''

Author: Hung-hsuan
Functions:

'''


import numpy as np
import xlrd, xlwt
from xlutils.copy import copy
import math
import random
import copy as cy

class Cache:

    def __init__(self):
        self.vehicle_file_path1 = "document\cache_1.xls"
        self.vehicle_file_path2 = "document\cache_2.xls"
        self.file_path = "document\cache.xls"
        self.vehicle_cache_set = []      
        self.file_detail_set = []        

    
    def get_vehicle_cache_set(self, vehicle_id):
        rb = xlrd.open_workbook(self.vehicle_file_path1, encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        vehicle_id = int(vehicle_id)
        for i in range(rs.nrows):
            if vehicle_id == int(rs.cell_value(i, 0)):
                vehicle_id = i
        for item in range(rs.ncols):
            if rs.cell_value(vehicle_id, item) != '':
                self.vehicle_cache_set.append(rs.cell_value(vehicle_id, item))
        return self.vehicle_cache_set



    def get_detail_information(self, file_id):
        rb = xlrd.open_workbook(self.file_path, encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        data_item = {}
        for i in range(rs.nrows):
            if file_id == rs.cell_value(i, 0):
                data_item['data_id'] = rs.cell_value(i, 0)
                data_item['data_size'] = rs.cell_value(i, 1)
                data_item['data_request_times'] = rs.cell_value(i, 2)
                data_item['data_type'] = rs.cell_value(i, 3)
                break
        return data_item


   
    def update_vehicle_file_popularity(self, vehicle_id, file_id, vehicle_file_popularity):
        a = 0.01                  
        self.file_id = file_id
        data_item = Cache.get_detail_information(self, self.file_id)
        file_type = data_item['data_type']
        file_type = int(file_type)
        copy_vehicle_file_popularity = cy.deepcopy(vehicle_file_popularity[vehicle_id][file_type-1])
        vehicle_file_popularity[vehicle_id][file_type-1] = vehicle_file_popularity[vehicle_id][file_type - 1] + (2 / np.pi) * math.atan(a * data_item['data_request_times']) * (1 - vehicle_file_popularity[vehicle_id][file_type - 1])
        Subtraction = 1 - vehicle_file_popularity[vehicle_id][file_type-1]    
    
        for i in range(0, 10):           
            if i != file_type:
                k = 0
                for j in range(0, 9):
                    random_num = random.uniform(0, Subtraction)         
                    if k == 8:
                        vehicle_file_popularity[vehicle_id][i - 1] = random_num
                    else:
                        Subtraction = Subtraction - random_num
                        vehicle_file_popularity[vehicle_id][i - 1] = random_num
                        k = k + 1
        return vehicle_file_popularity


    
    def file_element_order(self):
        rb = xlrd.open_workbook(self.file_path, encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        these_element = ['data_id', 'data_size', 'data_request_times', 'data_type']
        this_element = -1

        data_cell = {}
        for i in range(rs.nrows):
            data = []
            data.append(rs.cell_value(i, 1))
            data.append(rs.cell_value(i, 2))
            data.append(rs.cell_value(i, 3))
            data_cell[rs.cell_value(i, 0)] = data
      
        dict = {}
        data_item_order = sorted(data_cell.items(), key=lambda x:x[1][1], reverse=True)   
        for item in data_item_order:
            dict[item[0]] = item[1]
        return dict


    def update_vehicle_cache_set(self, vehicle_id, vehicle_max_cache_size, vehicle_file_popularity, store):
        cache_file = []             
        total_file_size = 0         
        sbs_cache = store           
        sbs_cache_hit = []
        rb = xlrd.open_workbook(self.vehicle_file_path1, encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        wb = copy(rb)
        ws = wb.get_sheet('contents')

        type = [[] for i in range(10)]  
        data_item_order = Cache.file_element_order(self)
        for key in data_item_order:
            for j in range(1, 11):
                if int(data_item_order[key][2]) == j:
                    type[j-1].append(int(key))
                    break
        file_percent = []
        for em in vehicle_file_popularity[vehicle_id]:
            file_percent.append(em/sum(vehicle_file_popularity[vehicle_id]))
       


        for i in range(0, 100000):
            parameter = random.random()
            if parameter > 0 and parameter < file_percent[0]:
                cache_file_id = int(type[0][0])
                data_item = Cache.get_detail_information(self, cache_file_id)
                total_file_size = total_file_size + data_item['data_size']
                if total_file_size <= vehicle_max_cache_size:
                    cache_file.append(cache_file_id)
                    type[0].remove(cache_file_id)
                    fg = 0
                    for item in sbs_cache:
                        item = int(item)
                        fg = 0
                        if item == int(cache_file_id):
                            sbs_cache_hit.append(1)
                            fg = 1
                            break
                    if fg == 0:
                        sbs_cache_hit.append(0)
                else:
                    break
            else:
                for j in range(0, 9):
                    if parameter > file_percent[j] and parameter < file_percent[j+1]:
                        cache_file_id = int(type[j+1][0])
                        data_item = Cache.get_detail_information(self, cache_file_id)
                        total_file_size = total_file_size + data_item['data_size']
                        if total_file_size <= vehicle_max_cache_size:
                            cache_file.append(cache_file_id)
                            type[j+1].remove(cache_file_id)
                            fg = 0
                            for item in sbs_cache:
                                item = int(item)
                                fg = 0
                                if item == cache_file_id:
                                    sbs_cache_hit.append(1)
                                    fg = 1
                                    break
                            if fg == 0:
                                sbs_cache_hit.append(0)
                        else:
                            break
            if total_file_size >= vehicle_max_cache_size:
                break
 
        for i in range(1, rs.ncols):
            ws.write(vehicle_id - 1, i, None)

        for j in range(1, len(cache_file)):
            ws.write(vehicle_id - 1, j, cache_file[j-1])

        wb.save(self.vehicle_file_path1)
        return sbs_cache_hit
