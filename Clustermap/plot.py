import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import pandas as pd
import numpy as np
import scanpy as sc
import squidpy as sq

def plot_histogram(data, save_dir):
    data.hist(bins=15, figsize=(20,15))
    plt.suptitle("Histogram of cell type")
    plt.savefig(save_dir)
    
def plot_boxplot(data, save_dir):
    plt.figure(figsize=(20,15))
    sns.boxplot(data, orient='h')
    plt.suptitle("Boxplot of cell type")
    plt.savefig(save_dir)


def plot_clustermap(metric_df, row_colors, col_colors, save_dir):
    
    '''Plot Setting'''
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 20
    cmap = ListedColormap(sns.color_palette("RdBu_r",10))
    
    clustermap = sns.clustermap(metric_df, row_cluster=True, col_cluster=True, 
                                method='average', cmap=cmap, figsize=(25,20), 
                                row_colors= row_colors, col_colors=col_colors, 
                                metric='euclidean',linewidths=0.5, linecolor='black',
                                dendrogram_ratio=0.1, colors_ratio=0.04)
    
    ''' Customize dendrogram lines '''
    for ax in [clustermap.ax_row_dendrogram, clustermap.ax_col_dendrogram]:
        for line in ax.collections:
            line.set_color('black')  # Change dendrogram line color
            line.set_linewidth(1)  # Change dendrogram line width 
    
    ''' Adjust cbar'''
    x0, _y0, _w, _h = clustermap.cbar_pos
    clustermap.ax_cbar.set_position([x0, _y0, 0.03, 0.1])
    
    ''' X, Y parameters'''
    clustermap.ax_heatmap.set_xticklabels(clustermap.ax_heatmap.get_xticklabels(), rotation=90, fontsize=19.5) #改heatmap的x軸文字大小
    clustermap.ax_heatmap.set_yticklabels(clustermap.ax_heatmap.get_yticklabels(), rotation=0, fontsize=19.5) #改heatmap的y軸文字大小

    ''' Adjust col_colors and row_colors  '''#調整megadata的參數格子大小的話直接調整width和height后的數字 會變寬或是變窄
    current_ax_row_colors = clustermap.ax_row_colors.get_position()
    clustermap.ax_row_colors.set_position([current_ax_row_colors.x0, current_ax_row_colors.y0, current_ax_row_colors.width-0.02, current_ax_row_colors.height])
    
    current_ax_col_colors = clustermap.ax_col_colors.get_position()
    clustermap.ax_col_colors.set_position([current_ax_col_colors.x0, current_ax_col_colors.y0+0.02, current_ax_col_colors.width, current_ax_col_colors.height-0.02])

    ''' Adjust the position of the dendrograms according to the adjusted row and column colors '''
    #current_ax_row_dendrogram = clustermap.ax_row_dendrogram.get_position()
    #clustermap.ax_row_dendrogram.set_position([current_ax_row_dendrogram.x0, current_ax_row_dendrogram.y0, current_ax_row_dendrogram.width, current_ax_row_colors.height])
    #current_ax_col_dendrogram = clustermap.ax_col_dendrogram.get_position()
    #clustermap.ax_col_dendrogram.set_position([current_ax_col_dendrogram.x0, current_ax_col_colors.y0+0.02, current_ax_col_colors.width, current_ax_col_dendrogram.height]) 
    
    ''' Adjust col_colors and row_colors label font size '''
    for label in clustermap.ax_row_colors.get_xticklabels():
        label.set_fontsize(20)
    for label in clustermap.ax_col_colors.get_yticklabels():
        label.set_fontsize(20)
        
    plt.savefig(save_dir)

def plot_legend(row_palette, col_palette, save_dir):
    
    '''Create legends for the color annotations'''
    row_labels = row_palette.keys()
    col_labels = col_palette.keys()
    
    # Mapping the colors back to the keys for legend #動legend的點的大小
    row_legend_handles = [plt.Line2D([0], [0], color=row_palette[label][key], marker='.', linestyle='', markersize=20, 
                                    label=f"{label}: {key}") for label in row_labels for key in row_palette[label]]
    
    col_legend_handles = [plt.Line2D([0], [0], color=col_palette[label][key], marker='.', linestyle='', markersize=20, 
                                    label=f"{label}: {key}") for label in col_labels for key in col_palette[label]]
    
    plt.figure(figsize=(15,10))

    # Add legends to the plot
    #bbox_to_anchor=(0.21, -0.01) 括號中數字代表clinical legend出現位置的上下左右
    ax1 = plt.subplot(121)
    col_legend = ax1.legend(handles=col_legend_handles, loc='center',bbox_to_anchor=(0.5, 0.6), ncol=2, frameon=True, edgecolor='black')
    ax1.add_artist(col_legend)
    ax1.axis('off')

    ax2 = plt.subplot(122)
    row_legend = ax2.legend(handles=row_legend_handles, loc='center',bbox_to_anchor=(0.35, 0.6), ncol=2, frameon=True, edgecolor='black')
    ax2.add_artist(row_legend,)
    ax2.axis('off')

    plt.savefig(save_dir)
