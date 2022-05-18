
from Cache import Cache
from Zipf import Zipf
from Request import Request
from UCB1 import UCB1
from Request_hit import Request_hit
# from UCB1 import UCB1
from Update_Cache import Update_Cache
import copy
import test as ts
import xlwt

def excel_update():

    all_cache_hit_rate_list = []
    counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
    ucb_value = [0 for i in range(10)]  
    expect_reward_estimate = [0 for i in range(10)]
    vehicle_file_popularity = {}  
    user_request_result = {}
    vehicle_cluster = ts.Test1()
    zipf1 = Zipf()
    zipf = zipf1.get_zipf(11)  
    d_value_set = []

    vehicle_cluster_list = []
    for item_1 in vehicle_cluster:
        for item_2 in vehicle_cluster[item_1]:
            for item_3 in item_2:
                vehicle_cluster_list.append(item_3)
        vehicle_cluster_set = set(vehicle_cluster_list)
        vehicle_cluster_list = list(vehicle_cluster_set)
   
    for item in vehicle_cluster_list:
        vehicle_file_popularity[item] = copy.deepcopy(zipf)       
    sbs_cache_hit_rate = 0
    period = 0
    for i in range(0, 50):
        period = period + 1
        print('period='+str(period))
        ucb1 = UCB1(ucb_value, expect_reward_estimate, counts, vehicle_file_popularity, user_request_result, d_value_set, vehicle_cluster, sbs_cache_hit_rate)
        ucb_value, expect_reward_estimate, counts, vehicle_file_popularity, user_request_result, d_value_set, single_cache_hit_rate, sbs_cache_hit_rate = ucb1.ucb1(vehicle_cluster_list)
        all_cache_hit_rate_list.append(single_cache_hit_rate)

    
    rwb = xlwt.Workbook()
    rws = rwb.add_sheet('contents')
    for m in range(0, len(all_cache_hit_rate_list)):
        rws.write(m+1, 0, all_cache_hit_rate_list[m])
    rwb.save('F:\\result\\proposed\\all_cache_hit_rate_list.xls')

excel_update()
