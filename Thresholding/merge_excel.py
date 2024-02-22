import pandas as pd
import os

folder_path = '/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Data/Opal immune cells/35 patients 的immune cell 資料/'

combined_df = pd.DataFrame()

for filename in os.listdir(folder_path):
    
    if filename.endswith('.xlsx'):
        
        excel_path = os.path.join(folder_path, filename)
        df = pd.read_excel(excel_path)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
        
combined_df.to_excel('/Users/ccy/Documents/NTU/大四上/NSCLC-tumor-data-analysis/Data/Opal immune cells/combined_excel.xlsx', index=False)
        