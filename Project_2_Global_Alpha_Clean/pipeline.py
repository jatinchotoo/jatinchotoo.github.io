import pandas as pd
import os

# Set path to the 'data' subfolder
base_path = os.path.join(os.getcwd(), 'data')

print("--- STARTING GLOBAL ALPHA ETL PIPELINE ---")

# 1. Load Excel Mapping from the data folder
try:
    mapping_path = os.path.join(base_path, 'dim_Mapping_Logic.xlsx.xlsx')
    mapping = pd.read_excel(mapping_path, sheet_name='Account_Mapping')
    currencies = pd.read_excel(mapping_path, sheet_name='Currency_Master')
    print("✅ Mapping Logic Loaded.")
except Exception as e:
    print(f"❌ Error: Could not find mapping file in {base_path}")
    exit()

# 2. Files to Load (matching your specific filenames)
files_to_load = {
    'BioGrowth': 'Raw_BioGrowth.csv.xlsx',
    'CryptoFlow': 'Raw_CryptoFlow.csv.xlsx',
    'FinShield Re': 'Raw_FinShield.csv.xlsx',
    'Nexus Strategic': 'Raw_Nexus.csv.xlsx',
    'Omni-Retail': 'Raw_OmniRetail.csv.xlsx',
    'Terra-Grid': 'Raw_TerraGrid.csv.xlsx'
}

all_data = []

for entity, file_name in files_to_load.items():
    file_path = os.path.join(base_path, file_name)
    if os.path.exists(file_path):
        temp_df = pd.read_excel(file_path)
        
        # Split logic for the comma-separated data inside the Excel
        if len(temp_df.columns) == 1:
            col_name = temp_df.columns[0]
            new_df = temp_df[col_name].str.split(',', expand=True)
            new_df.columns = col_name.split(',')
            temp_df = new_df
        
        # Standardize columns
        temp_df.columns = [str(c).upper().strip().replace(' ', '').replace('_', '') for c in temp_df.columns]
        temp_df.rename(columns={'ACCOUNTCODE': 'Account_Code', 'LOCALAMOUNT': 'Local_Amount'}, inplace=True)
        temp_df['Entity'] = entity
        all_data.append(temp_df)
        print(f"✅ Loaded & Cleaned: {entity}")

# 3. Process and Merge
if all_data:
    df_raw = pd.concat(all_data, ignore_index=True)
    df_raw['Account_Code'] = df_raw['Account_Code'].astype(str).str.strip().str.upper()
    mapping['Local_Account_Code'] = mapping['Local_Account_Code'].astype(str).str.strip().str.upper()
    
    # Join with Mapping Logic
    df_master = df_raw.merge(mapping, left_on=['Entity', 'Account_Code'], right_on=['Entity_Name', 'Local_Account_Code'], how='left')
    
    # Currency Mapping
    country_map = {'BioGrowth': 'Switzerland', 'CryptoFlow': 'Brazil', 'Terra-Grid': 'India', 'Omni-Retail': 'Germany (EU)', 'FinShield Re': 'United Kingdom', 'Nexus Strategic': 'South Africa'}
    df_master['Country'] = df_master['Entity'].map(country_map)
    df_master = df_master.merge(currencies, on='Country', how='left')
    
    # Calculate USD Amount
    df_master['Amount_USD'] = pd.to_numeric(df_master['Local_Amount'], errors='coerce') * df_master['FX_Rate_to_USD'].fillna(1.0)

    # Save output to the data folder
    output_path = os.path.join(base_path, 'Master_Consolidated_Fact.csv')
    df_master.to_csv(output_path, index=False)
    print(f"\n🎉 SUCCESS: Master File created in /data folder.")