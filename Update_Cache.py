'''
Author: Hung-hsuan

'''

import xlrd, xlwt
from Cache import Cache
import pandas as pd
import numpy as np
import random
from xlutils.copy import copy
import copy as copy1


class Update_Cache:

    def __init__(self, ucb_value, vehicle_file_popularity):
        self.vehicle_file_popularity = vehicle_file_popularity
        self.ucb_value = ucb_value
        print('self.ucb_value='+str(self.ucb_value))

    def upadate_cache_2(self, vehicle_set):
        store = []                                                          
        store1 = []
        cache_maxsize = 12500                                          
        each_vehicle_max_size = 2500                                
        each_vehicle_max_size_1 = 500                                     
        data_cache_size = 0                                                
        data_request_times = []                               
        data_type = []                                                    
        data_size = []                                                    
        data_id = []                                                       
        type = [[] for i in range(10)]                                    
        data_request_size = {}                                            
        rb = xlrd.open_workbook('document\cache.xls', encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        rb1 = xlrd.open_workbook('document\cache_1.xls', encoding_override="utf-8")    
        rs1 = rb1.sheet_by_name('contents')
        rb2 = xlrd.open_workbook('document\cache_2.xls', encoding_override="utf-8")  
        wb = copy(rb2)
        ws = wb.get_sheet('contents')
        cache = Cache()
        for i in range(rs.nrows):
            data_item = cache.get_detail_information(rs.cell_value(i, 0))
            data_id.append(data_item['data_id'])
            data_size.append(data_item['data_size'])
            data_request_times.append(data_item['data_request_times'])
            data_type.append(data_item['data_type'])
        df = pd.DataFrame({'data_id': data_id, 'data_size': data_size, 'data_request_times': data_request_times, 'data_type': data_type})
        ds = df.sort_values(by='data_request_times', ascending=False)
        data = np.array(ds).tolist()
        for item in range(0, len(data)):
            for i in range(1, 11):
                if i == int(data[item][3]):
                    type[i-1].append(data[item][0])
                    break
            data_request_size[int(data[item][0])] = data[item][1]
 
        sun = 0
        L = []
        for em in self.ucb_value:
            sun = sun + em
        for im in self.ucb_value:
            L.append(im/sun)
        # print("L="+str(L))
        for i in range(1000000):
            if data_cache_size <= cache_maxsize:
                control_parameter = random.random()                        
                if control_parameter >= 0 and control_parameter < L[0] and len(type[0]) != 0:
                    select_id = type[0][0]
                    select_id = int(select_id)
                    type[0].remove(select_id)
                    data_cache_size = data_cache_size + data_request_size[select_id]
                    store.append(select_id)
                else:
                    p = L[0]
                    for j in range(1, 10):
                        if control_parameter >= p and control_parameter < p + L[j] and len(type[j]) != 0:
                            select_id = type[j][0]
                            select_id = int(select_id)
                            type[j].remove(select_id)
                            data_cache_size = data_cache_size + data_request_size[select_id]
                            store.append(select_id)
                            break
                        else:
                            p = p + L[j]
            else:
                break


        for vehicel_item in vehicle_set:
            store1 = copy1.deepcopy(store)
            each_vehicle_max_size2 = 0
            vehicel_item = int(vehicel_item)
            for i in range(1, rs1.ncols):
                ws.write(vehicel_item - 1, i, None)

            for j in range(1, 10000000):
                if each_vehicle_max_size2 < each_vehicle_max_size_1 and len(store1) != 0:
                    id_again = int(random.choice(store1))
                    ws.write(vehicel_item - 1, j, id_again)
                    each_vehicle_max_size2 = each_vehicle_max_size2 + data_request_size[int(id_again)]
                    store1.remove(id_again)
                else:
                    break

        wb.save('document\cache_2.xls')


        all_sbs_cache_hit_rate = []
        for vehicle in vehicle_set:
            vehicle = int(vehicle)
            sbs_cache_hit_rate = cache.update_vehicle_cache_set(vehicle, each_vehicle_max_size, self.vehicle_file_popularity, store)
            for em in sbs_cache_hit_rate:
                all_sbs_cache_hit_rate.append(em)

        sun = 0
        for en in all_sbs_cache_hit_rate:
            sun = sun + en
        hit_rate = sun / len(all_sbs_cache_hit_rate)

        return hit_rate
