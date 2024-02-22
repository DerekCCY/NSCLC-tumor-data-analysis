import numpy as np
import pandas as pd
import argparse
from sklearn.impute import SimpleImputer

import seaborn as sns
import matplotlib.pyplot as plt

'''Preprocess Data'''

def preprocess_data(df):
    
    '''Data preprocessing'''
    
    # Missing values
    
    missing_values = df.isnull().sum()
    print(f"missing values: {missing_values}")
    
    # Methods to tackle missing values
    '''
    # 方法1: 使用均值填補數值型特徵的缺失值
    mean_value = df['column_name'].mean()
    df['column_name'].fillna(mean_value, inplace=True)
    
    # 方法2: 使用中位數填補數值型特徵的缺失值
    median_value = df['column_name'].median()
    df['column_name'].fillna(median_value, inplace=True)
    
    # 方法3: 使用眾數填補類別型特徵的缺失值
    mode_value = df['column_name'].mode()[0]
    df['column_name'].fillna(mode_value, inplace=True)
    
    # 方法4: 使用前向填補或後向填補
    df['column_name'].fillna(method='ffill', inplace=True)  # 使用前向填補
    df['column_name'].fillna(method='bfill', inplace=True)  # 使用後向填補
    
    # 方法5: 使用插值法填補數值型特徵的缺失值
    df['column_name'].interpolate(method='linear', inplace=True)
    
    # 方法6: 使用機器學習模型填補缺失值
    imputer = SimpleImputer(strategy='mean')  # 可以使用不同的策略，如'median', 'most_frequent'等
    df['column_name'] = imputer.fit_transform(df[['column_name']])
    '''
    return df

'''Calculate statistics'''

def statistics(df):
    
    print(f'Number of non-zero values: {df.count()}')
    mean_original = df.mean()
    std_original = df.std()
    q1_original = df.quantile(0.25)
    q2_original = df.quantile(0.5)
    q3_original = df.quantile(0.75)
    print(f'Mean_original: {mean_original} | Std_original: {std_original} | q1_original: {q1_original} | q2_original: {q2_original} | q3_original: {q3_original}')
    
    # 將所有數值大於 0 的值提取出來計算統計量
    positive_values = df[df >= 0.01].dropna()
    print(f'Number of non-zero values: {positive_values.count()}')
    mean = positive_values.mean()
    std = positive_values.std()
    q1 = positive_values.quantile(0.25)
    q2 = positive_values.quantile(0.5)
    q3 = positive_values.quantile(0.75)
    print(f'Mean: {mean} | Std: {std} | q1: {q1} | q2: {q2} | q3: {q3}')
    
    return {'Mean_original': mean_original , 'Std_original': std_original, 'q1_original':q1_original, 
            'q2_original':q2_original, 'q3_original': q3_original, 'Mean': mean , 'Std': std, 'q1':q1, 'q2':q2, 'q3': q3}
    
    