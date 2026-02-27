# aqipy
A python client for aqms.doe.ir (Iran's AQI measuring system)

## installation
install using:
```
pip install aqms-iran
```

## examples
**fetch city data:**
```
import aqipy

client = aqipy.AQIClient()
data = client.fetch_city_aqi_data('مشهد')
# or data = client.fetch_city_aqi_data('mashhad', names_are_farsi=False)

print(data)
```

**fetch station data**
```
import aqipy

client = aqipy.AQIClient()
data = client.fetch_all_stations()

station = 'دورود'
data = list(
    filter(
        lambda x: station in x['S'].strip(),
        data
    )
)[0]

print(data)
```