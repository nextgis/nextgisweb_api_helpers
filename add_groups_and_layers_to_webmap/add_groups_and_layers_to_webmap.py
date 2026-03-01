# Add a layer (style) to an existing Web map
# Try on sandbox.nextgis.com
# Prerequisites: 
# - known web map id
# - known layer style id
# - known first level group name
# - known second level group name
# Read more: https://sandbox.nextgis.com/doc/api#/Resource/put_api_resource__id_

import requests
import os

dir = os.path.dirname(os.path.abspath(__file__))
ngw_host = 'https://sandbox.nextgis.com'
auth = ('administrator','demodemo')

def add_groups_and_layer_to_web_map():
    webmap_id = 3155
    layer_style_id = 12
    first_group_name = 'group_1'
    second_group_name = 'group_2'
    lay_name = 'madcity'
    api_url = ngw_host + '/api/resource/' + str(webmap_id)
    resp = requests.get(api_url, auth=auth, timeout=30)
    
    new_first_group = {
        "item_type": "group",
        "display_name": first_group_name,
        "layer_enabled": True,
        'children': []
    }

    new_second_group = {
        "item_type": "group",
        "display_name": second_group_name,
        "layer_enabled": True,
        'children': []
    }

    new_layer = {
        "item_type": "layer",
        "display_name": lay_name,
        "layer_enabled": True,
        "layer_identifiable": True,
        "layer_adapter": "image",
        "layer_style_id": layer_style_id,
    }
    
    webmap_json = resp.json()['webmap']
    webmap_children = webmap_json["root_item"]["children"]
    
    k = 0
    ln = 0
    #Search first level group by name
    for child in webmap_children:
        if child['item_type'] == 'group' and child['display_name'] == first_group_name:
            z = 0
            yearn = 0
            children = child['children']
            gr_count = len(children)
            #Search second level group by name
            for child_v1 in children:
                if child_v1['item_type'] == 'group' and child_v1['display_name'] == second_group_name:
                    webmap_json["root_item"]["children"][k]["children"][z]["children"].append(new_layer)
                    payload = {"webmap": webmap_json}
                    resp = requests.put(api_url, auth=auth, json=payload, timeout=30)
                    print('For group: '+second_group_name+' added layer '+lay_name)
                    yearn = 1
                z = z + 1
            ln = 1
            #First level group is in, but no second level
            if yearn == 0:
                webmap_json["root_item"]["children"][k]["children"].append(new_second_group)
                webmap_json["root_item"]["children"][k]["children"][gr_count]["children"].append(new_layer)
                payload = {"webmap": webmap_json}
                resp = requests.put(api_url, auth=auth, json=payload, timeout=30)
                print('Inside group: '+first_group_name+' added group '+second_group_name+' and layer '+lay_name)
        k = k + 1
    #No first level group
    if ln == 0:
        webmap_json["root_item"]["children"].append(new_first_group)
        webmap_json["root_item"]["children"][k]["children"].append(new_second_group)
        webmap_json["root_item"]["children"][k]["children"][0]["children"].append(new_layer)
        payload = {"webmap": webmap_json}
        resp = requests.put(api_url, auth=auth, json=payload, timeout=30)
        print('Added group: '+first_group_name+'. Added group '+second_group_name+' and layer '+lay_name)

if __name__ == '__main__':
    add_groups_and_layer_to_web_map()