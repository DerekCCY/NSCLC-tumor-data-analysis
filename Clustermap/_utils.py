import pandas as pd
import numpy as np
import os
from plot import *
from sorting import Sort

'''------ Clustering data generation ------'''
def clustering_data_generation(data_directory):
    
    datalist = [f for f in os.listdir(data_directory) if f.endswith('.xlsx')]   #取出母目錄中各子檔案存到datalist
    
    ### === Read Excel ===
    info = []    
    for i in range(len(datalist) - 1):
        data = pd.read_excel(os.path.join(data_directory, datalist[i]),engine='openpyxl')
        info.append(data.iloc[1:, :].values)            # 取出所有值，除了col名稱  [row, col]

    ### === List to Numpy (np.concatenate) ===
    info = np.concatenate(info, axis=0)
    # !!! print(info)

    ### === Unique value and index  (np.unique) ===
    cname1, u1a, u2a = np.unique(info[:, 0], return_index=True, return_inverse=True) # cname1 會是所有免疫細胞的名稱，u1a包含原始數組中每個唯一值第一次出現的索引的數組，u2a: 一個數組，表示應用於唯一值時可以重構原始數組的索引
    cname2, u1b, u2b = np.unique(info[:, 1], return_index=True, return_inverse=True) # cname2 會是所有病人的編號，u1b包含原始數組中每個唯一值第一次出現的索引的數組，u2b: 一個數組，表示應用於唯一值時可以重構原始數組的索引
    # !!! print("cname1 & canme2")
    # !!! print("u1a & u1b")
    # !!! print("u2a & u2b")

    ### === Initialize Metric ===
    metric = np.zeros((len(cname1), len(cname2)))  #create an empty metric
    # !!! print(metric)

    ### === Map the value [ np.ravel_multi_index((u2a, u2b), metric.shape) ]  [ tuple (u2a, u2b)轉換為一維數組 ] ===
    indtmp = np.ravel_multi_index((u2a, u2b), metric.shape)   
    # !!! print(indtmp)
    tmpk = info[:, 4]
    # !!! print(tmpk)
    metric.flat[indtmp] = tmpk
    return metric, cname1, cname2

'''------ Normalization function ------'''
def zscore_normalization(row):
    mean_value = row.mean()
    std_dev = row.std()
    normalized_row = (row - mean_value) / std_dev
    return normalized_row

'''------ Calculate percentage function ------'''
mergeSort = Sort() # claim the mergeSort

def metric_percentage_calculation(new_metric ,data, index, column):
    selection = int(input("Select the percentage calculating method: Max-Min or Sorting? Enter 1 for Max-Min, enter 2 for Sorting: "))
    print("")
    for i in range(new_metric.shape[0]):  
        normalized_row = zscore_normalization(data[i, :-1].copy())  # 創建副本，避免修改原始數據   
        # !!! print(f"normalized_row {normalized_row}")
        row_min = normalized_row.min()   #取每橫列中最小值
        row_max = normalized_row.max()   #取每橫列中最大值
        # !!! print(row_min)
        # !!! print(row_max)
        if selection == 1:
            new_metric[i, :-1] = (normalized_row - row_min) / (row_max - row_min) * 100
            
        elif selection == 2:
            sorted_array = mergeSort.merge_sort(list(normalized_row))
            sorted_array_length = len(sorted_array)
            for j in range(sorted_array_length):    # j= number of patients
                element_position = sorted_array.index(normalized_row[j])
                new_metric[i, j] = ((sorted_array_length - element_position )/ sorted_array_length) *100    # Calculate PR 
        
        else:
            print("Error! You answer the invalid number!")
            break

    metric_df = pd.DataFrame(new_metric, index, column)
    return metric_df

def save_the_image(metric_type, col_colors, save_parent_directory):
    print("What type of information do you want in your plot? Choose 0 or 1 depending on the answer")
    print('0 for Normalized percentages with meta data and 1 for Logarithm plus Normalized with meta data')
    ch1 = int(input('Input selection: '))
    print("")

    print("What name do you want to give your plot?  Do NOT write the file type (e.g., png, jpeg, etc)")
    ch2 = input('Write name (do not leave spaces): ')
    print("")

    save_dir_selection = f'{save_parent_directory}/{ch2}.png'        
    plot_clustermap(metric_type[ch1], col_colors, save_dir_selection)