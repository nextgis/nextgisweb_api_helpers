# Add a layer (style) to an existing Web map, keeping it's content intact
# Prerequisits (use sandbox.nextgis.com to try): 
# - known web map id
# - known layer style id

import requests

ngw_host = 'https://sandbox.nextgis.com'
auth = ('administrator','demodemo')
webmap_id = 5
api_url = ngw_host + '/api/resource/' + str(webmap_id)

# Get Web map contents
resp = requests.get(api_url, auth=auth, timeout=30)
webmap_json = resp.json()['webmap']

# Add a new Web map layer (i.e. style)
new_layer = {
    "item_type": "layer",
    "display_name": "madcity2",
    "layer_enabled": True,
    "layer_identifiable": True,
    "layer_adapter": "image",
    "layer_style_id": 12,
}
webmap_json["root_item"]["children"].append(new_layer)
payload = {"webmap": webmap_json}

# Send new payload
resp = requests.put(api_url, auth=auth, json=payload, timeout=30)

if resp.status_code != 200:
    print(resp.text)
