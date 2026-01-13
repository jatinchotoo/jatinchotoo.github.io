import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURATION ---
base_path = os.getcwd()
data_path = os.path.join(base_path, 'data')
image_path = os.path.join(base_path, 'images')

if not os.path.exists(image_path):
    os.makedirs(image_path)

def run_analytics():
    print("--- GENERATING EXECUTIVE ROIC REPORT ---")
    
    master_file = os.path.join(data_path, 'Master_Consolidated_Fact.csv')
    if not os.path.exists(master_file):
        print(f"❌ Error: {master_file} not found.")
        return

    df = pd.read_csv(master_file)
    df.columns = df.columns.str.strip().str.lower()

    # 1. Pivot Logic: Transform rows into Financial Metrics
    # We filter for Revenue and Assets specifically
    revenue_df = df[df['group_category'].str.contains('Revenue', case=False, na=False)]
    assets_df = df[df['group_category'].str.contains('Assets', case=False, na=False)]

    # 2. Group by Entity
    rev_grouped = revenue_df.groupby('entity')['amount_usd'].sum().rename('revenue')
    ast_grouped = assets_df.groupby('entity')['amount_usd'].sum().rename('assets')

    # Merge into a Final Report
    report = pd.concat([rev_grouped, ast_grouped], axis=1).fillna(0)

    # 3. Financial Engineering Logic
    # NOPAT = Revenue * 0.75 (Assumed 25% Tax)
    report['nopat'] = report['revenue'] * 0.75
    
    # ROIC Calculation
    report['roic_%'] = (report['nopat'] / report['assets'].replace(0, float('nan'))) * 100
    report['roic_%'] = report['roic_%'].round(2)

    # 4. Exports
    report.to_csv(os.path.join(data_path, 'Final_ROIC_Report.csv'))
    report.to_excel(os.path.join(data_path, 'Executive_Performance_Summary.xlsx'))

    print("\n" + "="*65)
    print("              GLOBAL ALPHA PORTFOLIO STRATEGY REPORT")
    print("="*65)
    print(report)
    print("="*65)

    # 5. Visual Intelligence
    print("--- GENERATING PERFORMANCE VISUALS ---")
    plot_df = report.reset_index().dropna(subset=['roic_%'])
    
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    # Color logic: Green if beats 10% hurdle, else Red
    colors = ['#2ecc71' if x >= 10 else '#e74c3c' for x in plot_df['roic_%']]
    
    sns.barplot(x='entity', y='roic_%', data=plot_df, palette=colors, hue='entity', legend=False)
    plt.axhline(10, color='black', linestyle='--', label='10% Hurdle Rate')
    
    plt.title('Global Subsidiary Performance: ROIC Benchmarking', fontsize=14, fontweight='bold')
    plt.ylabel('ROIC %')
    plt.xticks(rotation=15)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(image_path, 'roic.png'), dpi=300)
    plt.close()
    
    print(f"✅ Reports and visuals saved successfully.")

if __name__ == "__main__":
    run_analytics()