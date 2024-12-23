import requests
import json

ngw_host = 'https://sandbox.nextgis.com'
auth = ('administrator','demodemo')
vector_layer_id = 7
attachment_filename = 'PA190477_ShiftN_crop.jpg'

if __name__ == '__main__':
    feature = dict()
    feature['extensions'] = dict()
    feature['extensions']['attachment'] = None
    feature['extensions']['description'] = None
    feature['fields'] = dict()
    feature['fields']['NAME'] = 'Sample name'
    feature['fields']['AMENITY'] = 'cafe'
    feature['geom'] = 'POINT (%s %s)' % (50,50)

    #create feature
    post_url = ngw_host + '/api/resource/' + str(vector_layer_id) +'/feature/?srs=4326'
    response = requests.post(post_url, data=json.dumps(feature), auth=auth)
    feature_id = response.json()['id']

    if response.status_code == 200:
        print("Feature created successfully:", response.json())
    else:
        print("Error creating feature:", response.status_code, response.text)

    with open(attachment_filename, 'rb') as f:
        #upload attachment to NGW
        response = requests.put(ngw_host + '/api/component/file_upload/upload', data=f, auth=auth)
        json_data = response.json()
        json_data['name'] = attachment_filename

    attach_data = {}
    attach_data['file_upload'] = json_data

    #add attachment to a feature
    post_url = ngw_host + '/api/resource/' + str(vector_layer_id) +'/feature/' + str(feature_id) + '/attachment/'
    response = requests.post(post_url, data=json.dumps(attach_data), auth=auth)
    
    if response.status_code != 200:
        print(response.text)
