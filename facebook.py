import requests

# Set your access token and other necessary parameters
access_token = 'EAAPcBfyB4yEBOzK8THMWZBUmqW4QjusVnMd8AsBdRRlwVqQyOBBxVbumbj6pBg9Ek1tYMi911KRm2tlSQLjSqrsnnravnXHTJVrybbkJiCALojRMdExbkPuyx1Sqjt29HwtchCisq1ofZBrIRRVz25ZAj9QvGQqHUUYVqHeDNKdP51XXXAXCw0pwsBCS5l4ZAhIEchG5qwJEFZBPxADrKljg2vjz9BT6D8ncZD'
ad_account_id = '3308140236145379'
app_id = '1086343199449889'

# Define the endpoint URL for the reports
# Define the endpoint URL for the reports
import requests
from datetime import datetime
from datetime import timedelta
import mysql.connector

end = (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y')

fields = 'campaign_name,adset_name,ad_name,reach,impressions,frequency,spend,clicks,cpc,cpm,inline_link_click_ctr,purchase_roas'

url = 'https://graph.facebook.com/v18.0/act_3308140236145379/insights?level=ad&time_range[since]=2023-12-01&time_range[until]=2023-12-30&fields=' + str(
    fields) + '&access_token=EAAPcBfyB4yEBOzK8THMWZBUmqW4QjusVnMd8AsBdRRlwVqQyOBBxVbumbj6pBg9Ek1tYMi911KRm2tlSQLjSqrsnnravnXHTJVrybbkJiCALojRMdExbkPuyx1Sqjt29HwtchCisq1ofZBrIRRVz25ZAj9QvGQqHUUYVqHeDNKdP51XXXAXCw0pwsBCS5l4ZAhIEchG5qwJEFZBPxADrKljg2vjz9BT6D8ncZD'

data = requests.get(url)
print(data.text)
