import numpy as np
import xlwt, xlrd
import datetime
import copy
from Request import Request
from Cache import Cache
from Request_hit import Request_hit
from Update_Cache import Update_Cache

class UCB1:
    def __init__(self, ucb_value, expect_reward_estimate, counts, vehicle_file_popularity, user_request_result, d_value_set, vehicle_cluster, sbs_cache_hit_rate):
        self.ucb_value = ucb_value
        self.expect_reward_estimate = expect_reward_estimate
        self.counts = counts
        self.vehicle_cluster = vehicle_cluster
        self.arms = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  
        self.vehicle_file_popularity = vehicle_file_popularity
        self.user_request_result = user_request_result
        self.d_value_set = d_value_set
        self.sbs_cache_hit_rate = sbs_cache_hit_rate



    def get_file_detial(self, user_request_result):                                
        vehicle_final_request = []                                                   
        file_type = []                                                               
        file_type_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]                              
        for t in user_request_result:
            for item in user_request_result[t]:
                vehicle_final_request.append(user_request_result[t][item][-1])
        cache = Cache()
        for i in range(0, len(vehicle_final_request)):
            file_detail = cache.get_detail_information(vehicle_final_request[i])
            file_type.append(file_detail['data_type'])
        sum = 0
        for j in range(0, len(file_type)):
            for k in range(1, 11):
                if file_type[j] == k:
                    file_type_number[k-1] = file_type_number[k-1] + 1
                    sum = sum + 1
                    break
        return file_type_number, sum




    def pull(self, user_request_result):
        ucb_value1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        file_type_number, sum = UCB1.get_file_detial(self, user_request_result)
        print("file_type_number="+str(file_type_number))
        print("sum=" + str(sum))
        total_counts = np.sum(self.counts)
        for arm in self.arms:
            bonus = np.sqrt((2 * np.log(total_counts))/(self.counts[arm-1]))
            ucb_value1[arm-1] = self.ucb_value[arm-1] + (file_type_number[arm-1] / sum) * bonus
        best_arm = ucb_value1.index(max(ucb_value1)) + 1
        print("best_arm="+str(best_arm))
        print("ucb_value1=" + str(ucb_value1))
        return best_arm




    def ucb1(self, vehicle_cluster_list):
        best_arm = -1
        flag = 1
        for arm in self.arms: 
            if self.counts[arm-1] == 0:
                flag = 0
                best_arm = arm
                break
        if flag == 0:
            self.counts[best_arm - 1] = self.counts[best_arm - 1] + 1
            self.ucb_value = [0 for i in range(10)]
            self.ucb_value[best_arm-1] = 1
            vehicle_file_popularity = self.vehicle_file_popularity
            update = Update_Cache(self.ucb_value, vehicle_file_popularity)
            sbs_cache_hit_rate = update.upadate_cache_2(vehicle_cluster_list)
            self.d_value_set.append(sbs_cache_hit_rate)
            self.expect_reward_estimate[best_arm-1] = sbs_cache_hit_rate
            request_hit = Request_hit()
            self.cooperation_hit_rate, self.local_hit_rate, self.all_cache_hit_rate, self.user_request_result, self.vehicle_file_popularity, single_cache_hit_rate = request_hit.request_hit(vehicle_file_popularity, self.vehicle_cluster, vehicle_cluster_list)
            return self.ucb_value, self.expect_reward_estimate, self.counts, self.vehicle_file_popularity, self.user_request_result, self.d_value_set, single_cache_hit_rate, sbs_cache_hit_rate
        if flag == 1:
            best_arm = UCB1.pull(self, self.user_request_result)
            self.counts[best_arm - 1] = self.counts[best_arm - 1] + 1
            self.ucb_value = copy.deepcopy(self.expect_reward_estimate)
            update = Update_Cache(self.ucb_value, self.vehicle_file_popularity)
            sbs_cache_hit_rate = update.upadate_cache_2(vehicle_cluster_list)
            d_value = sbs_cache_hit_rate - self.sbs_cache_hit_rate
            print("d_value="+str(d_value))
            self.d_value_set.append(d_value)
            self.ucb_value[best_arm-1] = self.ucb_value[best_arm-1] + d_value/(self.counts[best_arm-1] + 1)
            self.expect_reward_estimate = copy.deepcopy(self.ucb_value)
            # 归一化
            suuu = 0
            for k in range(0, len(self.expect_reward_estimate)):
                suuu = suuu + self.expect_reward_estimate[k]
            for k in range(0, len(self.expect_reward_estimate)):
                self.expect_reward_estimate[k] = self.expect_reward_estimate[k] / suuu
            self.ucb_value = copy.deepcopy(self.expect_reward_estimate)
            request_hit = Request_hit()
            self.cooperation_hit_rate, self.local_hit_rate, self.all_cache_hit_rate, self.user_request_result, self.vehicle_file_popularity, single_cache_hit_rate = request_hit.request_hit(self.vehicle_file_popularity, self.vehicle_cluster, vehicle_cluster_list)
            return self.ucb_value, self.expect_reward_estimate, self.counts, self.vehicle_file_popularity, self.user_request_result, self.d_value_set, single_cache_hit_rate, sbs_cache_hit_rate
