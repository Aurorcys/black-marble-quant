import pandas as pd
import os
import glob


gdp_folder = 'data/raw/quarterdata'
files = glob.glob(f'{gdp_folder}/*.csv')

print("Found files:")
for f in files:
    print(f"  {os.path.basename(f)}")

all_data = []

for file in files:
    print(f"\nProcessing {os.path.basename(file)}")
    
    # Skip the first 3 rows which are metadata
    df = pd.read_csv(file, skiprows=3)
    
    print(f"Columns: {df.columns.tolist()}")
    
    # Identify state from GeoName column
    state = df['GeoName'].iloc[0]
    
    # Filter for total GDP (LineCode = 1)
    df_total = df[df['LineCode'] == 1].copy()
    
    # Melt the quarter columns
    quarter_cols = [col for col in df_total.columns if 'Q' in str(col)]
    
    df_melted = df_total.melt(
        id_vars=['GeoName'],
        value_vars=quarter_cols,
        var_name='quarter',
        value_name='gdp_millions'
    )
    
    # Clean up
    df_melted['state'] = state
    df_melted['gdp_billions'] = df_melted['gdp_millions'] / 1000
    
    # Extract year and quarter number
    df_melted['year'] = df_melted['quarter'].str[:4].astype(int)
    df_melted['quarter_num'] = df_melted['quarter'].str[6]
    
    all_data.append(df_melted[['state', 'year', 'quarter_num', 'quarter', 'gdp_billions']])
    
    print(f"  Added {len(df_melted)} rows for {state}")

if all_data:
    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values(['state', 'year', 'quarter_num'])
    
    combined.to_csv('data/processed/quarterly_state_gdp_all.csv', index=False)
    
    pivot = combined.pivot(index='quarter', columns='state', values='gdp_billions')
    
    print("\n" + "="*70)
    print("QUARTERLY STATE GDP (2019-2022)")
    print("="*70)
    print(pivot.round(1))
    
    print("\n" + "="*70)
    print("PANDEMIC DROP: Q2 2020 vs Q1 2020")
    print("="*70)
    
    for state in combined['state'].unique():
        q1 = combined[(combined['state'] == state) & (combined['year'] == 2020) & (combined['quarter_num'] == '1')]
        q2 = combined[(combined['state'] == state) & (combined['year'] == 2020) & (combined['quarter_num'] == '2')]
        
        if len(q1) > 0 and len(q2) > 0:
            gdp_q1 = q1['gdp_billions'].values[0]
            gdp_q2 = q2['gdp_billions'].values[0]
            change = ((gdp_q2 - gdp_q1) / gdp_q1) * 100
            print(f"{state}: Q1 2020 ${gdp_q1:.1f}B → Q2 2020 ${gdp_q2:.1f}B ({change:+.1f}%)")
    
    print("\nSaved to data/processed/quarterly_state_gdp_all.csv")
else:
    print("No data processed.")