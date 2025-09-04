import requests

ngw_host = 'https://sandbox.nextgis.com'
auth = ('administrator','demodemo')
vector_layer_id = 9

if __name__ == '__main__':
    resource_url = ngw_host + '/api/resource/' + str(vector_layer_id)
    resource = requests.get(resource_url, auth = auth).json()

    if resource['resource']['cls'] == 'vector_layer' or resource['resource']['cls'] == 'postgis_layer':
        features = requests.get(resource_url + '/feature/', auth = auth).json()
        for feature in features:
            print(feature)