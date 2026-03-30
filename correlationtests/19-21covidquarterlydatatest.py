import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load quarterly lights data
lights_df = pd.read_csv('data/processed/quarterly_lights_2019_2021.csv')

# Load quarterly GDP data (state-level)
gdp_df = pd.read_csv('data/processed/quarterly_state_gdp_all.csv')

# Map cities to states
city_to_state = {
    'Austin': 'Texas',
    'Dallas': 'Texas',
    'Memphis': 'Tennessee',
    'St. Louis': 'Missouri',
    'Tulsa': 'Oklahoma'
}

# Create quarter labels for merging
lights_df['quarter_label'] = lights_df['year'].astype(str) + ' Q' + lights_df['quarter'].astype(str)
gdp_df['quarter_label'] = gdp_df['year'].astype(str) + ' Q' + gdp_df['quarter_num'].astype(str)

# Merge lights and GDP
merged = []
for city, state in city_to_state.items():
    city_lights = lights_df[lights_df['city'] == city][['quarter_label', 'light_intensity']]
    city_lights.columns = ['quarter_label', city]
    
    state_gdp = gdp_df[gdp_df['state'] == state][['quarter_label', 'gdp_billions']]
    state_gdp.columns = ['quarter_label', state]
    
    merged_df = pd.merge(city_lights, state_gdp, on='quarter_label')
    merged_df['city'] = city
    merged.append(merged_df)

# Combine all cities
combined = pd.concat(merged, ignore_index=True)

# Create figure with 3 rows, 2 columns
fig, axes = plt.subplots(3, 2, figsize=(16, 18))

cities = ['Austin', 'Dallas', 'Memphis', 'St. Louis', 'Tulsa']

for idx, city in enumerate(cities):
    row = idx // 2
    col = idx % 2
    ax = axes[row, col]
    
    city_data = combined[combined['city'] == city].sort_values('quarter_label')
    
    quarters = city_data['quarter_label'].values
    lights = city_data[city].values
    
    state = city_to_state[city]
    gdp_vals = city_data[state].values
    
    ax.plot(quarters, lights, 'o-', color='orange', linewidth=2.5, markersize=8, label='Light Intensity')
    ax_twin = ax.twinx()
    ax_twin.plot(quarters, gdp_vals, 's-', color='blue', linewidth=2.5, markersize=8, label='GDP')
    
    ax.set_xlabel('Quarter', fontsize=10)
    ax.set_ylabel('Light (nW/cm²/sr)', color='orange', fontsize=10)
    ax_twin.set_ylabel('GDP ($B)', color='blue', fontsize=10)
    
    corr = np.corrcoef(lights, gdp_vals)[0,1]
    ax.set_title(f'{city} - Correlation: {corr:.3f}', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    ax.set_xticks(range(len(quarters)))
    ax.set_xticklabels(quarters, rotation=45, ha='right', fontsize=8)

# Remove the empty subplot (bottom right)
fig.delaxes(axes[2, 1])

plt.suptitle('Quarterly Nighttime Lights vs GDP by City (2019-2021)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('data/images/quarterly_lights_vs_gdp.png', dpi=150, bbox_inches='tight')
plt.show()

print("Saved to data/images/quarterly_lights_vs_gdp.png")