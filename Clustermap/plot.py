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


def plot_clustermap(metric_df, save_dir):
    
    '''Plot Setting'''
    plt.style.use("classic")
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 16
    cmap = ListedColormap(sns.color_palette("RdBu_r",10))
    clustermap = sns.clustermap(metric_df, row_cluster=True, col_cluster=True, 
                                method='average', cmap=cmap, figsize=(20, 12),
                                metric='euclidean',linewidths=0.5, linecolor='black')
    clustermap.ax_heatmap.set_xticklabels(clustermap.ax_heatmap.get_xticklabels(), rotation=90)
    clustermap.ax_heatmap.set_yticklabels(clustermap.ax_heatmap.get_yticklabels(), rotation=0)
    plt.savefig(save_dir)

def plot_neighborhood_enrichment(adata, cluster_key, save_dir):
    sq.pl.nhood_enrichment(
    adata,
    cluster_key,
    cmap="coolwarm",
    title="",
    method="ward",
    dpi=300,
    figsize=(10, 10),
    save=save_dir,
    cbar_kwargs={"label": "Z-score"},
    vmin=-50,
    vmax=50,
)