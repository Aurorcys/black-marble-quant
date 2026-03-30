import h5py
import numpy as np
import pandas as pd
import os
import re
from glob import glob

os.makedirs('data/processed', exist_ok=True)

monthly_folder = 'data/raw/monthlyblackmarble'

cities = {
    'St. Louis': (38.63, -90.19),
    'Austin': (30.29, -97.74),
    'Dallas': (32.78, -96.80),
    'Memphis': (35.15, -90.05),
    'Tulsa': (36.17, -95.77)
}

month_map = {
    'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
    'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
}

years = [2019, 2020, 2021]
results = []

for year in years:
    files = glob(f'{monthly_folder}/h08v05|{year}*.h5')
    print(f"Found {len(files)} files for {year}")
    
    for filepath in sorted(files):
        filename = os.path.basename(filepath)
        
        month_match = re.search(r'\|' + str(year) + r'([A-Z]{3})\.h5', filename)
        if month_match:
            month_abbr = month_match.group(1)
            month = month_map[month_abbr]
        else:
            continue
        
        print(f"  Processing {year} {month_abbr}")
        
        with h5py.File(filepath, 'r') as f:
            data_fields = f['HDFEOS']['GRIDS']['VIIRS_Grid_DNB_2d']['Data Fields']
            lights = data_fields['NearNadir_Composite_Snow_Free'][:]
            lat = data_fields['lat'][:]
            lon = data_fields['lon'][:]
            
            for city, (city_lat, city_lon) in cities.items():
                lat_idx = np.argmin(np.abs(lat - city_lat))
                lon_idx = np.argmin(np.abs(lon - city_lon))
                
                y_start = max(0, lat_idx - 2)
                y_end = min(lights.shape[0], lat_idx + 3)
                x_start = max(0, lon_idx - 2)
                x_end = min(lights.shape[1], lon_idx + 3)
                
                city_area = lights[y_start:y_end, x_start:x_end]
                lit_pixels = city_area[city_area > 0]
                
                if len(lit_pixels) > 0:
                    light_value = np.mean(lit_pixels)
                else:
                    light_value = 0
                
                results.append({
                    'year': year,
                    'month': month,
                    'city': city,
                    'light_intensity': light_value
                })

df = pd.DataFrame(results)

# Save monthly data
df.to_csv('data/processed/monthly_lights_2019_2021.csv', index=False)

# Create quarterly averages
df['quarter'] = (df['month'] - 1) // 3 + 1
quarterly = df.groupby(['year', 'quarter', 'city'])['light_intensity'].mean().reset_index()

# Create quarter label
quarterly['quarter_label'] = quarterly['year'].astype(str) + ' Q' + quarterly['quarter'].astype(str)

# Save quarterly data
quarterly.to_csv('data/processed/quarterly_lights_2019_2021.csv', index=False)

# Create pivot table
quarterly_pivot = quarterly.pivot(index='quarter_label', columns='city', values='light_intensity')


print("\n" + "="*70)
print("QUARTERLY LIGHTS (2019-2021)")
print("="*70)
print(quarterly_pivot.round(1))

print("\n" + "="*70)
print("PANDEMIC DROP: Q2 2020 vs Q1 2020")
print("="*70)

for city in cities.keys():
    q1_2020 = quarterly[(quarterly['year'] == 2020) & (quarterly['quarter'] == 1) & (quarterly['city'] == city)]
    q2_2020 = quarterly[(quarterly['year'] == 2020) & (quarterly['quarter'] == 2) & (quarterly['city'] == city)]
    
    if len(q1_2020) > 0 and len(q2_2020) > 0:
        light_q1 = q1_2020['light_intensity'].values[0]
        light_q2 = q2_2020['light_intensity'].values[0]
        change = ((light_q2 - light_q1) / light_q1) * 100
        print(f"{city}: Q1 2020 {light_q1:.1f} → Q2 2020 {light_q2:.1f} ({change:+.1f}%)")

print("\nSaved to data/processed/")
print("  monthly_lights_2019_2021.csv")
print("  quarterly_lights_2019_2021.csv")
