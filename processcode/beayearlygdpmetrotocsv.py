import requests
import pandas as pd
import time
import os


BEA_KEY = "YOUR BEA API"

metros = {
    'St. Louis': ['29099', '29183', '29189', '29219', '17113', '17117', '17163', '51099'],
    'Austin': ['48453'],
    'Dallas': ['48113', '48121', '48139', '48231', '48257', '48397', '48485'],
    'Memphis': ['47157', '47093', '47097', '47167', '28033', '28153'],
    'Tulsa': ['40143', '40037', '40131', '40145']
}

years = list(range(2013, 2024))

results = []

print("Fetching GDP data from BEA (2013-2023)...")
print("=" * 60)

for city, counties in metros.items():
    print(f"\n{city}:")
    
    for year in years:
        total_gdp = 0
        year_success = False
        
        for county in counties:
            url = f"https://apps.bea.gov/api/data/?UserID={BEA_KEY}&method=GetData&datasetname=Regional&TableName=CAGDP2&LineCode=1&GeoFips={county}&Year={year}&ResultFormat=JSON"
            
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
                        if 'Data' in data['BEAAPI']['Results'] and data['BEAAPI']['Results']['Data']:
                            gdp_thousands = float(data['BEAAPI']['Results']['Data'][0]['DataValue'])
                            total_gdp += gdp_thousands
                            year_success = True
            except Exception as e:
                pass
            
            time.sleep(0.1)
        
        if year_success:
            gdp_billions = total_gdp / 1_000_000
            results.append({
                'city': city,
                'year': year,
                'gdp_billions': gdp_billions
            })
            print(f"  {year}: ${gdp_billions:.1f}B")
        else:
            print(f"  {year}: No data")

df = pd.DataFrame(results)
pivot = df.pivot(index='year', columns='city', values='gdp_billions')

print("\n" + "=" * 60)
print("GDP Data (2013-2023)")
print("=" * 60)
print(pivot.round(1))

df.to_csv('data/processed/gdp_data_2013_2023.csv', index=False)


print("\nSaved to:")
print("  data/processed/gdp_data_2013_2023.csv")
