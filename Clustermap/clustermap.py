'''---Import Package---'''
import os
import pandas as pd
import numpy as np
import random
from plot import *
from sklearn.preprocessing import StandardScaler
from sorting import *
from _utils import *
import config

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
    
    ''' Split data by factor '''
    (metric_factor1, cname2_factor1, col_metadata_factor1), (metric_factor2, cname2_factor2, col_metadata_factor2) = split_by_factor(metric, cname1, cname2, col_metadata)
    drawing_list = [metric_factor1, metric_factor2]
    cname2_factor_list = [cname2_factor1,cname2_factor2]
    
    ''' Graph type '''
    print(" What type of information do you want in your plot? Choose 0 or 1 depending on the answer ")
    print(" 0 for Normalized percentages with meta data and 1 for Logarithm plus Normalized with meta data ")
    ch1 = int(input(" Input selection: "))
    print("")      
    save_legend_dir = f'{config.SAVE_PARENT_DIRECTORY_NORMALIZING}/legend.png'  
    
    if ch1 == 0:
        # === metric_normalize ===
        for i in range(len(drawing_list)):
            metric_normalize_percentage = np.zeros(drawing_list[i].shape)
            metric_normalize_percentage_df = metric_percentage_calculation(metric_normalize_percentage, metric, cname1, cname2_factor_list[i])
            # Save each clustermap to a temporary file and then read it back for displaying in subplot
            temp_save_dir = f'{config.SAVE_PARENT_DIRECTORY_NORMALIZING}/temp_{i}.png'
            if i ==0:
                Plot_Clustermap.plot_clustermap_left(metric_log_percentage_normalize_df, row_colors, col_colors, temp_save_dir)
            else:
                Plot_Clustermap.plot_clustermap_right(metric_log_percentage_normalize_df, row_colors, col_colors, temp_save_dir)

    elif ch1 == 1:
        # === metric_log_normalize ===
        for i in range(len(drawing_list)):
            metric_log = np.log(drawing_list[i] + 1)
            metric_log_percentage_normalize = np.zeros(metric_log.shape)
            metric_log_percentage_normalize_df = metric_percentage_calculation(metric_log_percentage_normalize, metric_log, cname1, cname2_factor_list[i])
            # Save each clustermap to a temporary file and then read it back for displaying in subplot
            temp_save_dir = f'{config.SAVE_PARENT_DIRECTORY_NORMALIZING}/temp_{i}.png'
            if i ==0:
                Plot_Clustermap.plot_clustermap_left(metric_log_percentage_normalize_df, row_colors, col_colors, temp_save_dir)
            else:
                Plot_Clustermap.plot_clustermap_right(metric_log_percentage_normalize_df, row_colors, col_colors, temp_save_dir)

    plot_legend(row_palette, col_palette, save_legend_dir)



if __name__ == "__main__":
    main(config.INPUT)
    
    print(" What name do you want to give your plot?  Do NOT write the file type (e.g., png, jpeg, etc) ")
    ch2 = input(" Write name (do not leave spaces): ")
    print("")
    save_clustermap_dir = f'{config.SAVE_PARENT_DIRECTORY_NORMALIZING}/{ch2}.png'  
    
    Plot_Clustermap.plot_combined(os.path.join(config.SAVE_PARENT_DIRECTORY_NORMALIZING,'temp_0.png'), os.path.join(config.SAVE_PARENT_DIRECTORY_NORMALIZING,'temp_1.png'), save_clustermap_dir)
    