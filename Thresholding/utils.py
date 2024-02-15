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