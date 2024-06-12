#%%
import requests

def get_ip():
    '''
    Gets the ip address of the user
    '''
    try:
        # Fetch IP from an external service
        ip = requests.get('https://api64.ipify.org?format=json').json()['ip']
    except requests.RequestException:
        ip = 'Could not fetch IP'
    return ip

def get_location(ip_address):
    '''
    Uses the user's ip to get basic location data.
    
    Parameters:
        - ip_address: An ip addresses, in this case the user's

    Returns:
        - city, region, zipcode, country strings
    '''
    try:
        # Make a GET request to the ipapi API
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        data = response.json()
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        country = data.get('country_name', 'Unknown')
        zipcode = data.get('postal', 'country')
        return city, region, zipcode, country
    except requests.RequestException:
        return "Unknown", "Unknown", "Unknown", "Unknown"

