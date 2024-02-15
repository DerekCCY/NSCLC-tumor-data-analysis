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
    parser.add_argument('--input_file_path', default='/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Data/Opal immune cells/35 patients 的immune cell 資料/Opal 221_1_all immune cell subsets.xlsx')
    parser.add_argument('--input_image_path', default='/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Data/Opal immune cells/image/221_1')
    parser.add_argument('--column_name', default = 'Nucleus FoxP3 (Opal 620) Mean (Normalized Counts, Total Weighting)')
    parser.add_argument('--save_data_visualizing_path', default='/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Images/Threaholding/data_visualizing')
    parser.add_argument('--save_output_image_path', default='/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Images/Threaholding/output_image')
    args = parser.parse_args()
    
    '''=========================================================== Data Value ==============================================================='''
    data = pd.read_excel(args.input_file_path, usecols='C, E, F, K')  # Read the Excel file
    df = pd.DataFrame(data)  # Create a DataFrame from the data
    print(df)
    print(type(df))
    preprocess_data(df)    
    
    plt.figure(figsize=(20, 15))
    sns.set_theme()
    sns.set_style('whitegrid')
    sns.set_context(font_scale=1)
    sns.barplot(x= df['Sample Name'], y=df['Nucleus FoxP3 (Opal 620) Mean (Normalized Counts, Total Weighting)'])
    plt.xticks(rotation = 90)
    plt.title('FoxP3 Data Observation')
    plt.savefig(os.path.join(args.save_data_visualizing_path, "FoxP3_Data_Observation.png"), bbox_inches='tight')
    
    '''========================================================= Data Distribution =========================================================='''
    
    mean = df[args.column_name].mean()
    std = df[args.column_name].std()
    print(f'Mean: {mean}')
    print(f'Std: {std}')
    
    # 繪製直方圖和正態分佈曲線
    plt.figure(figsize=(20,15))
    sns.histplot(df[args.column_name], kde=True, color='skyblue', bins=30, stat='density', label='Data Distribution')
    plt.title('Data distribution and Normal distribution curve')
    plt.xlabel('value')
    plt.ylabel('density')

    # 繪製正態分佈曲線
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mean, std)
    plt.plot(x, p, 'k', linewidth=2, label='Normal Distribution Curve')
    
    # 添加圖例
    plt.legend()
    plt.savefig(os.path.join(args.save_data_visualizing_path,"Data_distribution_and_Normal_distribution_curve.png"), bbox_inches = 'tight')
    
    '''========================================================== Thresholding ================================================================'''
    
    threshold_value = mean + 3 * std
    
    # observe how many points are bigger than threshold
    threshold_points = df[ df[args.column_name] > threshold_value ]
    print(threshold_points)
    
    for sample_name in threshold_points['Sample Name'].unique():
        
        base_name = sample_name.split('.im3')[0]
        coordinate_name = '_FoxP3_path_view.tif'
        complete_name = base_name + coordinate_name
        
        input_image = os.path.join(args.input_image_path, complete_name)
        image = Image.open(input_image)
        draw = ImageDraw.Draw(image)
        
        #sample_points = threshold_points [ threshold_points['Sample Name'] == sample_name ]
        
        for _, points in threshold_points.iterrows():
            x = points['Cell X Position']
            y = points['Cell Y Position']
            
            draw.ellipse([x-5, y-5, x+5, y+5], outline='blue', fill='blue')
    
        image.save(os.path.join(args.save_output_image_path, str(base_name)+'.png'))
        
if __name__ == "__main__":
    main()
    