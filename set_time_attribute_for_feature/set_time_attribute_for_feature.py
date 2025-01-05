# Set datetime attribute value for a particular feature
# Prerequisits (use sandbox.nextgis.com to try): 
# - known layer id
# - existing attribute DT of type DATETIME
# - existing feature 1

import requests
import json
from datetime import datetime

ngw_host = 'https://sandbox.nextgis.com'
auth = ('administrator','demodemo')
vector_layer_id = 7
feature_id = 1

if __name__ == '__main__':
    update_payload = {
        "fields": {
            "DT": datetime.now().isoformat()
        }
    }

    post_url = ngw_host + '/api/resource/' + str(vector_layer_id) +'/feature/' + str(feature_id) + '?dt_format=iso'
    response = requests.put(post_url, data=json.dumps(update_payload), auth=auth)

    if response.status_code == 200:
        print("Attribute updated successfully:", response.json())
    else:
        print("Attribute update failed:", response.status_code, response.text)

