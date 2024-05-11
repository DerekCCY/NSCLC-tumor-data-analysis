import numpy as np
import pandas as pd
import os
import argparse
from sklearn.impute import SimpleImputer
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
from PIL import Image, ImageDraw

from utils import *

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file_path', default='/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Data/Opal immune cells/35 patients 的immune cell 資料')
    parser.add_argument('--input_image_path', default='/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Data/Opal immune cells/image/221_2')
    parser.add_argument('--column_name', default = 'Nucleus FoxP3 (Opal 620) Mean (Normalized Counts, Total Weighting)')
    parser.add_argument('--save_data_visualizing_root', default='/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Images/Threaholding/data_visualizing')
    parser.add_argument('--save_output_image_path', default='/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Images/Threaholding/output_image')
    args = parser.parse_args()
    
    # result_df 存計算結果
    columns = ['File Name', 'Mean_original', 'Std_original', 'q1_original', 'q2_original', 'q3_original','Mean', 'bigger_than_mean', 'Std', 'q1','bigger_than_q1', 'q2','bigger_than_q2', 'q3', 'bigger_than_q3']
    result_df = pd.DataFrame(columns=columns)
    
    '''=========================================================== Data Value ==============================================================='''
    
    for filename in sorted(os.listdir(args.input_file_path)):
        
        file = os.path.join(args.input_file_path, filename)
        if os.path.isfile(file):
            data = pd.read_excel(file, usecols='C, E, F, K')  # Read the Excel file
            df = pd.DataFrame(data)  # Create a DataFrame from the data
            print(df)
            print(type(df))
            
            # 檢查有無缺失值
            preprocess_data(df)    
    
            plt.figure(figsize=(20, 15))
            sns.set_theme()
            sns.set_style('whitegrid')
            sns.set_context(font_scale=1)
            sns.barplot(x= df['Sample Name'], y=df['Nucleus FoxP3 (Opal 620) Mean (Normalized Counts, Total Weighting)'])
            plt.xticks(rotation = 90)
            plt.title('FoxP3 Data Observation')
            
            saved_path = os.path.join(args.save_data_visualizing_root, filename)
            if not os.path.exists(saved_path):
                os.mkdir(saved_path)                

            plt.savefig(os.path.join(saved_path, "FoxP3_Data_Observation.png"), bbox_inches='tight')
    
            '''========================================================= Original Data Distribution =========================================================='''
            # save statistic 
            stats = statistics(df[args.column_name])
            stats['File Name'] = filename
            result_df = pd.concat([result_df, pd.DataFrame(stats, index=[0])], ignore_index=True)
            
            # Histogram and Distribution Curve
            plt.figure(figsize=(20,15))
            sns.histplot(df[args.column_name], kde=True, color='skyblue', bins=30, stat='density', label='Data Distribution')
            plt.title('Data distribution and Normal distribution curve')
            plt.xlabel('value')
            plt.ylabel('density')

            # Normal Distribution Curve
            mean = df[args.column_name].mean()
            std = df[args.column_name].std()
            xmin, xmax = plt.xlim()
            x = np.linspace(xmin, xmax, 100)
            p = norm.pdf(x, mean, std)
            plt.plot(x, p, 'k', linewidth=2, label='Normal Distribution Curve')

            # 添加圖例
            plt.legend()
            plt.savefig(os.path.join(saved_path,"Data_distribution_and_Normal_distribution_curve.png"), bbox_inches = 'tight')
            
    # 將結果寫入 Excel 檔案
    result_excel_path = '/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Images/Threaholding/statistics/statistics.xlsx'
    result_df.to_excel(result_excel_path, index=False)     
    
    '''========================================================== Thresholding ================================================================
    
    threshold_value = mean
    
    for sample_name in df['Sample Name'].unique():
        
        print(f'sample_name: {sample_name}')
        
        base_name = sample_name.split('.im3')[0]
        coordinate_name = '_FoxP3_path_view.tif'
        complete_name = base_name + coordinate_name
        
        input_image = os.path.join(args.input_image_path, complete_name)
        image = Image.open(input_image)
        draw = ImageDraw.Draw(image)
        
        # Coordinate problem
        image_height = image.size[1]
    
        # observe how many points are bigger than threshold
        threshold_points = df[ (df['Sample Name'] == sample_name) & (df[args.column_name] > threshold_value) ]

        print("threshold_points")
        print(threshold_points)
        #sample_points = threshold_points [ threshold_points['Sample Name'] == sample_name ]
        
        for _, points in threshold_points.iterrows():
            x = points['Cell X Position']
            y = image_height - points['Cell Y Position'] 
            
            draw.ellipse([x-5, y-5, x+5, y+5], outline='blue', fill='blue')
    
        image.save(os.path.join(args.save_output_image_path, str(base_name)+'.png'))'''
        
if __name__ == "__main__":
    main()