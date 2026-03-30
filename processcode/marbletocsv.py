import h5py
import numpy as np
import pandas as pd
import os
import re

data_folder = 'data/raw/blackmarble'

cities = {
    'St. Louis': (38.63, -90.19),
    'Austin': (30.29, -97.74),
    'Dallas': (32.78, -96.80),
    'Memphis': (35.15, -90.05),
    'Tulsa': (36.17, -95.77)
}

results = []

for filename in os.listdir(data_folder):
    if '|' not in filename:
        continue
    
    filepath = os.path.join(data_folder, filename)
    
    year_match = re.search(r'\|(\d{4})', filename)
    if year_match:
        year = int(year_match.group(1))
    else:
        continue
    
    if year < 2013 or year > 2023:
        continue
    
    print(f"Processing {year}")
    
    try:
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
                    'city': city,
                    'light_intensity': light_value
                })
                print(f"  {city}: {light_value:.1f}")
                
    except Exception as e:
        print(f"  Error: {e}")

df = pd.DataFrame(results)
pivot = df.pivot(index='year', columns='city', values='light_intensity')

print("\n" + "="*60)
print("Light Intensity Data (2013-2023)")
print("="*60)
print(pivot.round(1))

df.to_csv('data/processed/black_marble_lights_2013_2023.csv', index=False)


print("\nSaved to:")
print("  data/processed/black_marble_lights_2013_2023.csv")
