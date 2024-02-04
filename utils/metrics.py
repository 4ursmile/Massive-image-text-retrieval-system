import numpy as np

class metrics:
    def __init__(self, ground_truth):
        self.self.ground_truth = ground_truth
    def calculate_Precision(self, list_result, query):
        total_true = 0
        for res in list_result:
            if self.ground_truth[res] == self.ground_truth[query]:
                total_true+=1
        return total_true/len(list_result)
    def calculate_APK(self, list_result, query, k):
        total_true = 0
        total_precision = 0
        for i in range(k):
            if self.ground_truth[list_result[i]] == self.ground_truth[query]:
                total_true+=1
            total_precision+=self.calculate_Precision(list_result[:i+1], query)
        if total_true == 0:
            return 0
        return total_precision/total_true
    def calculate_Recall(self, list_result, query):
        total_true = 0
        for res in list_result:
            if self.ground_truth[res] == self.ground_truth[query]:
                total_true+=1
        return total_true/50
    def calculate_mAPK(self, list_results, queries, k):
        total_AP = 0
        for i, query in enumerate(queries):
            total_AP+=self.calculate_APK(list_results[i], query, k)
        return total_AP/len(queries)
    def calculate_AR(self, list_results, queries):
        total_R = 0
        for list_result, query in zip(list_results, queries):
            total_R+=self.calculate_Recall(list_result, query)
        return total_R/len(queries)