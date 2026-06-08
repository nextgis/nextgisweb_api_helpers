import json

import requests

ngw_host = 'https://sandbox.nextgis.com'
auth = ('administrator','demodemo')
vector_layer_id = 11
feature_id = 1
attachment_filename = 'PA190477_ShiftN_crop.jpg'

if __name__ == '__main__':
    with open(attachment_filename, 'rb') as f:
        #upload attachment to NGW
        response = requests.put(ngw_host + '/api/component/file_upload/', data=f, auth=auth)
        response.raise_for_status()
        json_data = response.json()
        json_data['name'] = attachment_filename

    attach_data = {}
    attach_data['file_upload'] = json_data

    #add attachment to a feature
    post_url = ngw_host + '/api/resource/' + str(vector_layer_id) +'/feature/' + str(feature_id) + '/attachment/'
    response.raise_for_status()
    response = requests.post(post_url, data=json.dumps(attach_data), auth=auth)
    
    if response.status_code != 200:
        print(response.text)
    else:
        print("Success. See result here: https://sandbox.nextgis.com/resource/11/feature/1")
