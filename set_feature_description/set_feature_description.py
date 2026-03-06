import requests
import json

ngw_host = 'https://sandbox.nextgis.com'
auth = ('administrator','demodemo')
vector_layer_id = 9
feature_id = 1

if __name__ == '__main__':
    update_payload = {
        "extensions" : {"description": "This is new description"}
    }

    post_url = ngw_host + '/api/resource/' + str(vector_layer_id) +'/feature/' + str(feature_id)
    response = requests.put(post_url, data=json.dumps(update_payload), auth=auth)

    if response.status_code == 200:
        print("Attribute updated successfully:", response.json())
    else:
        print("Attribute update failed:", response.status_code, response.text)