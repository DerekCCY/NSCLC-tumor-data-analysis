## non-small cell lung cancer(NSCLC)

## Patients and immune cell data
   * `Endometrial cancer Panel 2 cell density data`

## Environment 
   * `requirement.txt`

## Run
   * `python clustermap.py`
   * Log normalization
   
## Results in 'images' file
   * show the expression level of immune cell and cluster them into groups

## Description
   * In our study, we extracted the cell density of various cells from the experimental data of each participant and organized it into a data frame. This data frame is structured with thirty patients on the columns and ten different cell types on the rows, resulting in a dimension of [10 rows × 30 columns]. Following this, we performed a Logarithmic Transformation on all data. This step involved applying the natural logarithm (log) to each element in the metric matrix, following the formula log(x+1), where 'x' is the original value. This transformation is highly beneficial for data covering a wide range of magnitudes, as it effectively reduces skewness and unveils more apparent patterns.

   * Subsequently, as our focus is to observe the expression of each cell type across different patients, we performed Z-score normalization for each row and converted the expression levels of each patient into a percentage format. Finally, we employed the Euclidean distance metric to calculate similarity and utilized the average linkage method for hierarchical clustering. We then generated a heatmap and a relationship connection plot. The outcomes of this analysis were visualized to provide a clearer understanding of the relationships and patterns within our data. This approach offers a comprehensive and detailed insight into the cell density dynamics in our study population.