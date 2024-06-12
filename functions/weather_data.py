#%%
import requests
import pandas as pd


#%%
def astronomy_get(api_key, location, date):
    base_url = f"http://api.weatherapi.com/v1/astronomy.json"

    params = {
        "key": api_key,
        "q": location,
        "dt": date,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            df = pd.DataFrame(data['astronomy'])  
            df.reset_index(drop=False, inplace=True)
            return df
        except Exception as e:
            print(f"Error processing JSON")
            return pd.DataFrame()
    else:
        print(f"Error fetching data: {response.status_code}")


#%%
def current_weather_get(api_key, location):
    base_url = f"http://api.weatherapi.com/v1/current.json"

    params = {
        "key": api_key,
        "q": location,
        "aqi": "yes",
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            data = data['current']

            keys_to_remove = ['condition', 'air_quality']
            filtered_data = {key: value for key, value in data.items() if key not in keys_to_remove}

            df = pd.DataFrame(filtered_data, index=[0])  
            return df
        
        except Exception as e:
            print(f"Error processing JSON")
            return pd.DataFrame()
    else:
        print(f"Error fetching data: {response.status_code}")