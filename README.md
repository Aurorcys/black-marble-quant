#Black Marble Economic Indicator

Quantitative analysis of NASA nighttime lights as a proxy for economic activity**


#Overview

This project investigates whether NASA's Black Marble nighttime lights data can serve as a leading indicator for economic activity. Using 5 US metropolitan areas (Austin, Dallas, Memphis, St. Louis, Tulsa) from 2013-2021, I compare satellite-derived light intensity with BEA GDP data to test the correlation.

Key Finding: Lights and GDP both dropped 8-20% during the COVID-19 pandemic (Q2 2020), proving the signal works during major economic shocks. Yearly correlations are weaker (0.1-0.3) due to noise, infrastructure changes (LED conversions), and suburban growth missed by city-center pixels.

#The Data

| Source | Product | Resolution | Years |
|--------|---------|------------|-------|
| NASA Black Marble | VNP46A3 (monthly) | 15 arc-sec (~463m) | 2013-2021 |
| BEA Regional GDP | Quarterly & Annual | Metro/State level | 2013-2021 |

#Results

#Pandemic Shock (Q2 2020)

| City | Lights Drop | State GDP Drop |
|------|-------------|----------------|
| Austin | -8.7% | -8.6% |
| Dallas | -19.8% | -8.6% |
| Memphis | -14.6% | -10.8% |
| St. Louis | -8.9% | -7.6% |
| Tulsa | -19.1% | -9.9% |

All cities showed a sharp drop in lights during Q2 2020, closely matching GDP declines. Dallas and Tulsa showed larger drops due to airport closures (DFW) and oil price collapse.

#Predictive Power (Lights → Next Year GDP)

| City | Predictive Correlation | Signal |
|------|------------------------|--------|
| St. Louis | 0.788 | Strong |
| Dallas | 0.501 | Moderate |
| Austin | -0.712 | Inverse (suburban growth) |
| Memphis | -0.272 | Weak inverse |
| Tulsa | 0.058 | No signal |

St. Louis shows the strongest predictive signal: when lights increase, GDP follows the next year.

#Limitations

- LED Conversions: Dallas lights dropped 10.5% in 2015 due to LED streetlight replacement, not economic decline
- Suburban Growth: Austin's GDP grew 38% while lights only grew 4% (growth occurred outside downtown pixel)
- Pixel Selection: Memphis shows negative correlation because economic growth (FedEx hub, medical district) missed the downtown pixel

#Project Structure

## Files

**correlationtests/**
- `19-21covidquarterlydatatest.py` - Quarterly analysis (2019-2021)
- `13-19yearlydattest.py` - Yearly analysis (2013-2019)

**data/raw/quarterdata/**
- `missouriquarterlygdp19-21SQGDP2.csv`
- `tennesseequarterlygdp19-21SQGDP2.csv`
- `oklahomaquarterlygdp19-21SQGDP2.csv`
- `texasquarterlygdp19-21SQGDP2.csv`

**images/**
- `quarterly_lights_vs_gdp.png`
- `yearly_lights_vs_gdp.png`

#data sources
BEA
NASA BLACK MARBLE

#data
To download the black marble data that I used, go to the EARTHDATA website, or paste this link: https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VNP46A4
VNP46A4 means the yearly black marble data, I personally used the h08v05 version which includes the metros I've stated above. The monthly data that I used to find
the quarterly was the VJ146A3 one, or the link https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3.


CONCLUSION:
While the light intensity of cities is a strong economic indicator in times of crisis, such as COVID. It occasionally gets disrupted by external factors, such as the
LED conversion which lowers the light intensity, NASA changing their sensor which makes the light intensity lower as well, or GDP growth being outside of the city like
factories or airports. Overall, the light intensity is a great indicator if only used well in combination of other confirmatiions to reduce the chance of false signals
from external factors.

Author
Cyrus, 16yr old

Acknowledgments
NASA Black Marble Team for open data
BEA for regional GDP statistics
LAADS DAAC for data distribution
