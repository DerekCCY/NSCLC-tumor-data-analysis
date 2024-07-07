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
    
    ''' Clustering_data_generation '''
    metric, cname1, cname2 = clustering_data_generation(data_directory)
    
    ''' Metadata '''
    col_metadata = pd.read_excel("Data/Endometrial cancer Panel 2 cell density data/meta_data/col_metadata.xlsx",index_col=0)
    row_metadata = pd.read_excel("Data/Endometrial cancer Panel 2 cell density data/meta_data/row_metadata.xlsx",index_col=0)
    row_colors, col_colors, row_palette, col_palette = metadata(row_metadata, col_metadata)

    ''' Choose graph type '''
    print("What type of information do you want in your plot? Choose 0 or 1 depending on the answer")
    print('0 for Normalized percentages with meta data and 1 for Logarithm plus Normalized with meta data')
    ch1 = int(input('Input selection: '))
    print("")
    
    print("What name do you want to give your plot?  Do NOT write the file type (e.g., png, jpeg, etc)")
    ch2 = input('Write name (do not leave spaces): ')
    print("")

    save_parent_directory_normalizing = 'Results/Clustermap/Normalizing'
    save_parent_directory_sorting = 'Results/Clustermap/Sorting'     

    save_clustermap_dir_selection = f'{save_parent_directory_normalizing}/{ch2}.png'        
    save_legend_dir = f'{save_parent_directory_normalizing}/legend.png'  
    
    if ch1 == 0:
        ### === metric_normalize ===
        metric_normalize_percentage = np.zeros(metric.shape)
        metric_normalize_percentage_df = metric_percentage_calculation(metric_normalize_percentage, metric, cname1, cname2)
        plot_clustermap(metric_normalize_percentage_df, row_colors, col_colors, save_clustermap_dir_selection)
    elif ch1 == 1:
        ### === metric_log_normalize_percentage ===
        metric_log = np.log(metric+1)
        metric_log_percentage_normalize = np.zeros(metric_log.shape)
        metric_log_percentage_normalize_df = metric_percentage_calculation(metric_log_percentage_normalize, metric_log, cname1, cname2)
        # metric_log_percentage_normalize_df.to_csv("cell density after log transform and normalization.csv")
        plot_clustermap(metric_log_percentage_normalize_df, row_colors, col_colors, save_clustermap_dir_selection)
    
    plot_legend(row_palette, col_palette, save_legend_dir)


if __name__ == "__main__":
    data_directory = '/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Data/Endometrial cancer Panel 2 cell density data'
    main(data_directory)