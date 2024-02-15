'''---Import Package---'''
import os
import pandas as pd
import numpy as np
from plot import *
from sklearn.preprocessing import StandardScaler

def custom_normalize(row):
    mean_value = row.mean()
    std_dev = row.std()
    normalized_row = (row - mean_value) / std_dev
    return normalized_row

def metric_type(new_metric ,data, index, column, normalize):
    for i in range(new_metric.shape[0]):  
        if (normalize == True):
            normalized_row = custom_normalize(data[i, :].copy())  # 創建副本，避免修改原始數據   
            row_min = normalized_row.min()   #取每橫列中最小值
            row_max = normalized_row.max()   #取每橫列中最大值
            print(row_min)
            print(row_max)
            new_metric[i, :] = (normalized_row - row_min) / (row_max - row_min) * 100   #一列一列做標準化
        else :
            row_min = data[i, :].min()
            row_max = data[i, :].max()
            print(row_min)
            print(row_max)
            new_metric[i, :] = (data[i, :] - row_min) / (row_max - row_min) * 100
    metric_df = pd.DataFrame(new_metric, index, column)
    print('===============================')
    print(f"metric")
    print(metric_df.head(5))
    print('===============================')
    return metric_df

''' datadir: Input File Directory'''

def main(datadir):
    
    datalist = [f for f in os.listdir(datadir) if f.endswith('.xlsx')]   #取出母目錄中各子檔案存到datalist

    '''Read Excel'''
    density = []
    cell_type = []
    info = []
    patients_number = []

    for i in range(len(datalist) - 1):
        # 讀取 Excel 文件的內容
        data = pd.read_excel(os.path.join(datadir, datalist[i]),engine='openpyxl')
        info.append(data.iloc[1:, :].values)            # 取出所有值，除了col名稱
        '''
        if data.shape[0] == 11:
            density.append(data.iloc[2:, 4].values)        # 取 density column 的值
            cell_type.append(data.iloc[2:, 0].values)      # 免疫細胞的名稱
            patients_number.append(data.iloc[1, 1])        # 病人編號
        '''

    '''List to Numpy'''
    info = np.concatenate(info, axis=0)
    print('===============================')
    print("Info")
    print(info)
    print(info.shape)
    print('===============================')

    '''---Unique value and index---'''
    cname1, u1a, u2a = np.unique(info[:, 0], return_index=True, return_inverse=True) # cname1 會是所有免疫細胞的名稱，u1a包含原始數組中每個唯一值第一次出現的索引的數組，u2a: 一個數組，表示應用於唯一值時可以重構原始數組的索引
    cname2, u1b, u2b = np.unique(info[:, 1], return_index=True, return_inverse=True) # cname2 會是所有病人的編號，u1b包含原始數組中每個唯一值第一次出現的索引的數組，u2b: 一個數組，表示應用於唯一值時可以重構原始數組的索引
    print('===============================')
    print("cname1 & canme2")
    print(cname1)
    print(cname2)
    print('===============================')
    print('===============================')
    print("u1a & u1b")
    print(u1a)
    print(u1b)
    print('===============================')

    '''---Initialize Metric---'''
    metric = np.zeros((len(cname1), len(cname2)))
    print('===============================')
    print("metric")
    print(metric)
    print(metric.shape)
    print('===============================')

    '''---Map the value---'''
    indtmp = np.ravel_multi_index((u2a, u2b), metric.shape)   #轉換為一維數組
    print('===============================')
    print("indtmp")
    print(indtmp)
    print(indtmp.shape)
    print("===============================")

    tmpk = info[:, 4]
    print('===============================')
    print("tmpk")
    print(tmpk)
    print(tmpk.shape)
    print('===============================')
    metric.flat[indtmp] = tmpk
    metric_df = pd.DataFrame(metric,index=cname1, columns=cname2)
    print('===============================')
    print("metric")
    print(metric_df)
    metric_df.to_csv("cell_density.csv")
    print(f"metric_df.columns[7]: {metric_df.columns[7]}")
    print(f"metric_df.shape[1]: {metric_df.shape[1]}")
    print('===============================')

    '''---metric_origin---'''
    metric_percentage = np.zeros(metric.shape)
    metric_percentage_df = metric_type(metric_percentage, metric, cname1, cname2, 0)
    
    '''---metric_normalize---'''
    metric_normalize_percentage = np.zeros(metric.shape)
    metric_normalize_percentage_df = metric_type(metric_normalize_percentage, metric, cname1, cname2, 1)

    '''---metric_log_percentage---'''
    metric_log = np.log(metric+1)
    metric_log_df = pd.DataFrame(metric_log,index=cname1, columns=cname2)
    metric_log_df.to_csv("cell density after log transform.csv")
    metric_log_percentage = np.zeros(metric.shape)
    metric_log_percentage_df = metric_type(metric_log_percentage,metric_log, cname1, cname2, 0)

    '''---metric_log_normalize_percentage---'''
    metric_log_percentage_normalize = np.zeros(metric_log.shape)
    metric_log_percentage_normalize_df = metric_type(metric_log_percentage_normalize, metric_log, cname1, cname2, 1)

    '''Choose graph type'''
    metric = [metric_percentage_df ,metric_normalize_percentage_df,metric_log_percentage_df,metric_log_percentage_normalize_df]
    save_dir_selection = ['images/clustermap_origin_percentage.png','images/clustermap_normalize_percentage.png', 'images/clustermap_log_percentage.png','images/clustermap_log_normalize_percentage.png']
    
    plot_clustermap(metric[3],save_dir_selection[3])

if __name__ == "__main__":
    datadir = '/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Data/Endometrial cancer Panel 2 cell density data'
    main(datadir)