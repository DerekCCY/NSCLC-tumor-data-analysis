'''---Import Package---'''
import os
import pandas as pd
import numpy as np
import random
from plot import *
from sklearn.preprocessing import StandardScaler
from sorting import *
from _utils import *

# If you think that print all the metrics is useless, you can uncomment them!
# Hints: Each !!! means that you can print the data to check their shape and content!

# Hints: You have two choice to Calculate percentage: metric_percentage_calculation or sorting
# Hints: When you change your methods, remember to change the function and the saving directory!

'''------ data_directory: Input File Directory ------'''
def main(data_directory):
    
    ### === clustering_data_generation ===
    metric, cname1, cname2 = clustering_data_generation(data_directory)
    
    metric_df = pd.DataFrame(metric, index=cname1, columns=cname2)
    
    '''Add a test target'''
    genders = np.random.choice(['Male', 'Female'], size=metric_df.shape[1])
    gender_row = pd.DataFrame([genders], columns=metric_df.columns[0:], index=['Gender'])
    metric_df = pd.concat([gender_row, metric_df])
    
    row_dict = {'Male': 'green', 'Female': 'yellow'}

    col_colors = metric_df.loc['Gender'].map(row_dict)
    metric = metric_df.drop(index='Gender').to_numpy(dtype=float)
    '''====================================================================================='''

    ### === metric_normalize ===
    metric_normalize_percentage = np.zeros(metric.shape)
    metric_normalize_percentage_df = metric_percentage_calculation(metric_normalize_percentage, metric, cname1, cname2)

    ### === metric_log_percentage ===
    metric_log = np.log(metric+1)
    #metric_log_df = pd.DataFrame(metric_log,index=cname1, columns=cname2)
    #metric_log_percentage = np.zeros(metric.shape)
    #metric_log_percentage_df = metric_percentage_calculation(metric_log_percentage,metric_log, cname1, cname2)

    ### === metric_log_normalize_percentage ===
    metric_log_percentage_normalize = np.zeros(metric_log.shape)
    metric_log_percentage_normalize_df = metric_percentage_calculation(metric_log_percentage_normalize, metric_log, cname1, cname2)
    # metric_log_percentage_normalize_df.to_csv("cell density after log transform and normalization.csv")
    
    ### === Choose graph type ===
    metric_type = [metric_normalize_percentage_df,metric_log_percentage_normalize_df]
    
    save_parent_directory_normalizing = 'Results/Clustermap/Normalizing'
    save_parent_directory_sorting = 'Results/Clustermap/Sorting'
    save_the_image(metric_type, col_colors,save_parent_directory_sorting)

if __name__ == "__main__":
    data_directory = '/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Data/Endometrial cancer Panel 2 cell density data'
    main(data_directory)