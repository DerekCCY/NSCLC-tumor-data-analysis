import sys
sys.path.append('/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis')
import pandas as pd
import numpy as np
import os
from plot import *
from sorting import Sort
import config

'''------ Clustering data generation ------'''
def clustering_data_generation(data_directory):
    
    datalist = [f for f in os.listdir(data_directory) if f.endswith('.xlsx')]   #取出母目錄中各子檔案存到datalist
    print(len(datalist))
    ### === Read Excel ===
    info = []    
    for i in range(len(datalist)):
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
    print(metric.shape)

    ### === Map the value [ np.ravel_multi_index((u2a, u2b), metric.shape) ]  [ tuple (u2a, u2b)轉換為一維數組 ] ===
    indtmp = np.ravel_multi_index((u2a, u2b), metric.shape)   
    # !!! print(indtmp)
    tmpk = info[:, 4]
    # !!! print(tmpk)
    metric.flat[indtmp] = tmpk
    return metric, cname1, cname2

'''------ Metadata function ------ '''
def metadata(row_metadata, col_metadata):
    # Define color palettes for the metadata

    row_palette = {
        'Panel': {'Panel1': 'CadetBlue', 'Panel2': 'PowDerBlue'},
        'Test': {'a': 'Gold', 'b': 'Khaki', 'c':'LemonChiffon'},
        #'':{'':'white'},
    }
    col_palette = {
        'Gender': {'M': 'LightBlue', 'F': 'LightPink'},
        'Areca nut': {'Y': 'Orange', 'N': 'Moccasin'},
        #'':{'':'white'}
    }
    # Create row and column color maps
    col_colors = pd.DataFrame(index=col_metadata.index)
    for meta_col in col_palette:
        col_colors[meta_col] = col_metadata[meta_col].map(col_palette[meta_col])
    
    row_colors = pd.DataFrame(index=row_metadata.index)
    for meta_col in row_palette:
        row_colors[meta_col] = row_metadata[meta_col].map(row_palette[meta_col])
    
    return row_colors, col_colors, row_palette, col_palette

'''------ Splitting function ------'''
def split_by_factor(metric, cname1, cname2, col_metadata, split_column=config.COL_SPLIT_FACTOR):
    # Separate columns based on gender
    male_indices = col_metadata[col_metadata[split_column] == 'M'].index
    female_indices = col_metadata[col_metadata[split_column] == 'F'].index
    
    # Convert these indices to positions in the original metric (assuming cname2 is aligned with col_metadata)
    male_indices = np.where(col_metadata.index.isin(male_indices))[0]
    female_indices = np.where(col_metadata.index.isin(female_indices))[0]
    
    # Subset metric for males and females
    metric_factor1 = metric[:, male_indices]
    metric_factor2 = metric[:, female_indices]
    
    # Subset column names for males and females
    cname2_factor1 = cname2[male_indices]
    cname2_factor2 = cname2[female_indices]
    
    # Subset metadata for males and females
    col_metadata_factor1 = col_metadata.iloc[male_indices]
    col_metadata_factor2 = col_metadata.iloc[female_indices]
    
    return (metric_factor1, cname2_factor1, col_metadata_factor1), (metric_factor2, cname2_factor2, col_metadata_factor2)

'''------ Normalization function ------'''
def zscore_normalization(row):
    mean_value = row.mean()
    std_dev = row.std()
    normalized_row = (row - mean_value) / std_dev
    return normalized_row

'''------ Calculate percentage function ------'''
mergeSort = Sort() # claim the mergeSort

def metric_percentage_calculation(new_metric ,data, index, column):
    selection = int(input("Select the percentage calculating method: Max-Min or Sorting? Enter 0 for Max-Min, enter 1 for Sorting: "))
    print("")
    print(new_metric.shape)
    for i in range(new_metric.shape[0]):  
        normalized_row = zscore_normalization(data[i, :].copy())  # 創建副本，避免修改原始數據   
        # !!! print(f"normalized_row {normalized_row}")
        row_min = normalized_row.min()   #取每橫列中最小值
        row_max = normalized_row.max()   #取每橫列中最大值
        # !!! print(row_min)
        # !!! print(row_max)
        if selection == 0:
            new_metric[i, :] = (normalized_row - row_min) / (row_max - row_min) * 100
            
        elif selection == 1:
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
