'''
access_token = 'EAAPcBfyB4yEBOzK8THMWZBUmqW4QjusVnMd8AsBdRRlwVqQyOBBxVbumbj6pBg9Ek1tYMi911KRm2tlSQLjSqrsnnravnXHTJVrybbkJiCALojRMdExbkPuyx1Sqjt29HwtchCisq1ofZBrIRRVz25ZAj9QvGQqHUUYVqHeDNKdP51XXXAXCw0pwsBCS5l4ZAhIEchG5qwJEFZBPxADrKljg2vjz9BT6D8ncZD'
ad_account_id = '3308140236145379'
app_id = '1086343199449889'
'''

import requests

ad_account_id = '3308140236145379'
access_token = 'EAAPcBfyB4yEBOzK8THMWZBUmqW4QjusVnMd8AsBdRRlwVqQyOBBxVbumbj6pBg9Ek1tYMi911KRm2tlSQLjSqrsnnravnXHTJVrybbkJiCALojRMdExbkPuyx1Sqjt29HwtchCisq1ofZBrIRRVz25ZAj9QvGQqHUUYVqHeDNKdP51XXXAXCw0pwsBCS5l4ZAhIEchG5qwJEFZBPxADrKljg2vjz9BT6D8ncZD'
app_id = '1086343199449889'

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
