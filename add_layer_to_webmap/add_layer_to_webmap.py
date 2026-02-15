# Add a layer (style) to an existing Web map
# Try on sandbox.nextgis.com
# Prerequisites: 
# - known web map id
# - known layer style id
# Read more: https://sandbox.nextgis.com/doc/api#/Resource/put_api_resource__id_

import requests

ngw_host = 'https://sandbox.nextgis.com'
auth = ('administrator','demodemo')
webmap_id = 5
layer_style_id = 12
api_url = ngw_host + '/api/resource/' + str(webmap_id)

# Get Web map contents
resp = requests.get(api_url, auth=auth, timeout=30)
webmap_json = resp.json()['webmap']

# Add a new Web map layer (i.e. style)
new_layer = {
    "item_type": "layer",
    "display_name": "madcity",
    "layer_enabled": True,
    "layer_identifiable": True,
    "layer_adapter": "image",
    "layer_style_id": layer_style_id,
}
webmap_json["root_item"]["children"].append(new_layer)
payload = {"webmap": webmap_json}

# Send new payload
resp = requests.put(api_url, auth=auth, json=payload, timeout=30)

if resp.status_code != 200:
    print(resp.text)
