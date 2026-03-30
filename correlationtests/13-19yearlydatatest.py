import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load yearly lights data (from your earlier extraction)
# If you don't have this CSV, use the data directly
light_yearly = {
    'year': [2013, 2014, 2015, 2016, 2017, 2018, 2019],
    'Austin': [130.39, 120.87, 127.67, 135.53, 128.31, 139.75, 135.21],
    'Dallas': [191.73, 183.55, 164.32, 182.33, 198.68, 213.47, 223.04],
    'Memphis': [175.39, 170.65, 173.72, 173.99, 174.58, 167.90, 167.56],
    'St. Louis': [310.28, 333.72, 364.73, 334.59, 290.12, 288.70, 284.66],
    'Tulsa': [112.00, 116.45, 122.80, 124.09, 134.92, 141.67, 115.90]
}

gdp_yearly = {
    'year': [2013, 2014, 2015, 2016, 2017, 2018, 2019],
    'Austin': [82.0, 88.8, 98.2, 104.2, 112.0, 120.0, 128.0],
    'Dallas': [248.0, 260.6, 276.4, 288.0, 305.0, 325.0, 340.0],
    'Memphis': [86.1, 88.1, 92.2, 95.4, 98.0, 101.0, 104.0],
    'St. Louis': [115.8, 119.8, 125.1, 129.3, 132.0, 135.0, 138.0],
    'Tulsa': [45.1, 47.9, 48.8, 46.3, 47.0, 48.5, 49.0]
}

light_df = pd.DataFrame(light_yearly)
gdp_df = pd.DataFrame(gdp_yearly)

cities = ['Austin', 'Dallas', 'Memphis', 'St. Louis', 'Tulsa']

fig, axes = plt.subplots(3, 2, figsize=(16, 18))

for idx, city in enumerate(cities):
    row = idx // 2
    col = idx % 2
    ax = axes[row, col]
    
    light_vals = light_df[city].values
    gdp_vals = gdp_df[city].values
    years = light_df['year'].values
    
    ax.plot(years, light_vals, 'o-', color='orange', linewidth=2.5, markersize=8, label='Light Intensity')
    ax_twin = ax.twinx()
    ax_twin.plot(years, gdp_vals, 's-', color='blue', linewidth=2.5, markersize=8, label='GDP')
    
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel('Light (nW/cm²/sr)', color='orange', fontsize=10)
    ax_twin.set_ylabel('GDP ($B)', color='blue', fontsize=10)
    
    corr = np.corrcoef(light_vals, gdp_vals)[0,1]
    ax.set_title(f'{city} - Correlation: {corr:.3f}', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Highlight the LED conversion period (2014-2016)
    if city in ['Dallas', 'St. Louis']:
        ax.axvspan(2014, 2016, alpha=0.2, color='gray', label='LED Conversion Period')
    elif city == 'Tulsa':
        ax.axvspan(2015, 2016, alpha=0.2, color='gray', label='Oil Price Crash')

# Remove empty subplot
fig.delaxes(axes[2, 1])

plt.suptitle('Yearly Nighttime Lights vs GDP by City (2013-2019)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('data/images/yearly_lights_vs_gdp.png', dpi=150, bbox_inches='tight')
plt.show()

print("Saved to data/images/yearly_lights_vs_gdp.png")

# Also show correlation summary
print("\n" + "="*70)
print("YEARLY CORRELATION SUMMARY (2013-2019)")
print("="*70)

for city in cities:
    light_vals = light_df[city].values
    gdp_vals = gdp_df[city].values
    corr = np.corrcoef(light_vals, gdp_vals)[0,1]
    print(f"{city:12s}: {corr:.3f}")