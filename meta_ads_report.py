import requests

ad_account_id = '00000000000'
access_token = 'your_account_token_id'
app_id = '0000000000000'

fields = 'campaign_name,adset_name,ad_name,reach,impressions,frequency,spend,clicks,cpc,cpm,inline_link_click_ctr,purchase_roas'

url = f"https://graph.facebook.com/v18.0/act_{ad_account_id}/insights?fields={fields}&access_token={access_token}"

try:
    response = requests.get(url)
    response.raise_for_status()  # Check for errors

    data = response.json()

    if 'data' in data and data['data']:
        print('Printing DATA')
        print(data)
    else:
        print("No data found.")
except requests.exceptions.HTTPError as err:
    print(f"HTTP Error: {err}")
    print(f"Response content: {response.text}")
except Exception as e:
    print(f"An error occurred: {e}")
