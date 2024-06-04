'''---Import Package---'''
import os
import pandas as pd
import numpy as np
from plot import *
from sklearn.preprocessing import StandardScaler
from Sorting import *
from scipy.stats import zscore

# If you think that print all the metrics is useless, you can uncomment them!

'''------ Merge Sort ------'''
mergeSort = Sort()
def Sorting(new_metric ,data, index, column):
    for i in range(new_metric.shape[0]):    # i = number of cells
        if isinstance(data, pd.DataFrame):
            row = data.iloc[i, :].values
        else:
            row = data[i, :]
            
        sorted_array = mergeSort.merge_sort(list(row))
        print(f"Sorted array: {sorted_array}")
        sorted_array_length = len(sorted_array)
        for j in range(sorted_array_length):    # j= number of patients
            element_position = sorted_array.index(row[j])
            new_metric[i, j] = ((sorted_array_length - element_position )/ sorted_array_length) *100    # Calculate PR
            
    print(f"new metric: { new_metric }")                    
    metric_df = pd.DataFrame(new_metric, index, column)
    
    return metric_df

'''--- datadir: Input File Directory ---'''

def main(datadir):
    
    datalist = [f for f in os.listdir(datadir) if f.endswith('.xlsx')]   # parent directory -> subdirectory -> datalist

    ### === Read Excel ===
    density = []
    cell_type = []
    info = []
    patients_number = []

    for i in range(len(datalist) - 1):
        data = pd.read_excel(os.path.join(datadir, datalist[i]),engine='openpyxl')
        info.append(data.iloc[1:, :].values)            # extract all value except column name, [row, col]
        '''
        if data.shape[0] == 11:
            density.append(data.iloc[2:, 4].values)        # density column
            cell_type.append(data.iloc[2:, 0].values)      # cells name
            patients_number.append(data.iloc[1, 1])        # patients number
        '''

    ### === List to Numpy (np.concatenate) ===
    
    info = np.concatenate(info, axis=0)

    ### === Unique value and index (np.unique) ===
    
    cname1, u1a, u2a = np.unique(info[:, 0], return_index=True, return_inverse=True) # cname1 會是所有免疫細胞的名稱，u1a包含原始數組中每個唯一值第一次出現的索引的數組，u2a: 一個數組，表示應用於唯一值時可以重構原始數組的索引
    cname2, u1b, u2b = np.unique(info[:, 1], return_index=True, return_inverse=True) # cname2 會是所有病人的編號，u1b包含原始數組中每個唯一值第一次出現的索引的數組，u2b: 一個數組，表示應用於唯一值時可以重構原始數組的索引
    
    ### === Initialize Metric ===
    
    metric = np.zeros((len(cname1), len(cname2)))  #create an empty metric

    ### === Map the value [ np.ravel_multi_index((u2a, u2b), metric.shape) ]  [ tuple (u2a, u2b)轉換為一維數組 ] ===
    
    indtmp = np.ravel_multi_index((u2a, u2b), metric.shape)   
    tmpk = info[:, 4]
    
    metric.flat[indtmp] = tmpk
    metric_df = pd.DataFrame(metric,index=cname1, columns=cname2)    
    metric_df = metric_df.apply(zscore, axis=0)

    ### === metric_normalize ===
    metric_normalize = np.zeros(metric.shape)
    metric_normalize_df = Sorting(metric_normalize, metric_df, cname1, cname2)

    ### === metric_log_normalize ===
    metric_log = np.log(metric+1)
    metric_log_normalize = np.zeros(metric_log.shape)
    metric_log_normalize_df = Sorting(metric_log_normalize, metric_log, cname1, cname2)
    
    metric_log_df = pd.DataFrame(metric_log,index=cname1, columns=cname2)  # observe the data after log transformation
    metric_log_df.to_csv("cell density after log transform.csv")

    ### Choose graph type
    metric = [metric_normalize_df, metric_log_normalize_df]
    save_dir_selection = ['Results/Clustermap/Sorting/clustermap_normalize.png', 'Results/Clustermap/Sorting/clustermap_log_normalize.png']
    plot_clustermap(metric[1],save_dir_selection[1])

if __name__ == "__main__":
    datadir = '/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Data/Endometrial cancer Panel 2 cell density data'
    main(datadir)