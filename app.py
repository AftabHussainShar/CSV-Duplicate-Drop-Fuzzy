import pandas as pd
import os
from fuzzywuzzy import fuzz
import numpy as np  

directory = './'
desired_order = ['First Name', 'Last Name', 'Company', 'Address1', 'Address2', 'City', 'State', 'Zip Code', 'Phone']
merged_data = pd.DataFrame(columns=desired_order)

for file in os.listdir(directory):
    if file.endswith('.csv'):
        file_path = os.path.join(directory, file)
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

        df = df.fillna("Unknown")
        for col in desired_order:
            if col not in df.columns:
                df[col] = "Unknown"

        df = df[desired_order]
        merged_data = pd.concat([merged_data, df], ignore_index=True, sort=False)
for col in desired_order:
    if col not in merged_data.columns:
        merged_data[col] = "Unknown"

merged_data.to_csv('merged_file.csv', index=False)
print("Merged CSV file created successfully.")

merged_file_path = 'merged_file.csv'  
merged_data = pd.read_csv(merged_file_path)
merged_data.replace("Unknown", pd.NA, inplace=True)
merged_data = merged_data.dropna(subset=merged_data.columns, how='all')
output_file_path = 'merged_file.csv'
merged_data.to_csv(output_file_path, index=False)
print("Cleaned and saved the merged CSV file successfully.")
cleaned_merged_file_path = 'merged_file.csv'  
merged_data = pd.read_csv(cleaned_merged_file_path)
merged_data = merged_data.dropna(subset=['Address1', 'Address2'], how='all')
output_file_path = 'merged_file.csv'
merged_data.to_csv(output_file_path, index=False)
print("Filtered and saved the final merged CSV file successfully.")

final_merged_file_path = 'merged_file.csv'  
merged_data = pd.read_csv(final_merged_file_path)

def calculate_similarity(str1, str2):
    if pd.isna(str1) or pd.isna(str2):
        return 0
    return fuzz.ratio(str1, str2)


mask = merged_data.duplicated(subset=['First Name', 'Address1', 'Address2'], keep='first')
duplicate_data = merged_data[mask]
duplicate_file_path = 'duplicate_file.csv'
duplicate_data.to_csv(duplicate_file_path, index=False)
print("Duplicate rows saved to 'duplicate_file.csv'.")
merged_data = merged_data[~mask]
final_output_file_path = 'final_merged_file.csv'
merged_data.to_csv(final_output_file_path, index=False)
print("Final filtered and saved the merged CSV file successfully.")