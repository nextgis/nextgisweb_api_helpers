# Add a vector layer with style 
# Try on sandbox.nextgis.com
# Prerequisites: 
# - install tusclient 'pip install tusclient'
# Read more: 
# - https://sandbox.nextgis.com/doc/api#/FileUpload/post_api_component_file_upload_
# - https://sandbox.nextgis.com/doc/api#/Resource/post_api_resource_

from tusclient.client import TusClient
from urllib.parse import urljoin
import requests
import os

dir = os.path.dirname(os.path.abspath(__file__))
ngw_host = 'https://sandbox.nextgis.com'
auth = ('administrator','demodemo')
input_data = dir + '/vector.geojson' # or shp in .zip
style_name = dir + '/vector.qml'
ngw_layer_name = 'vector'
ngw_style_name = 'vector_style'
ngw_parent_resource = 0

def upload_file(filename, ngw_host, auth):
        tus_upload_path = '/api/component/file_upload/'
        chunk_size = 4*2**20

        tus_client = TusClient(urljoin(ngw_host, tus_upload_path))
        uploader = tus_client.uploader(filename, metadata=dict(meta='data'), chunk_size=chunk_size)
        uploader.upload()
        furl = uploader.url

        response = requests.get(furl, auth=auth, json=True)
        upload_meta = response.json()

        return upload_meta

def create_layer(upload_meta,ngw_layer_name,ngw_parent_resource):
    resource = {
        "resource": {
            "cls": "vector_layer",
            "display_name": ngw_layer_name,
            "parent": {"id": ngw_parent_resource}
        },
        "vector_layer": {
            "source": upload_meta,
            "srs": {"id": 3857}
        }
     }

    root = "%s/api/resource/" % (ngw_host)
    response = requests.post(root, json=resource, auth=auth)
    if response.status_code != 201:
        print('Unable to create a vector' \
        ' layer in NGW. Status: %s' % response.text)
    else:
        print(response.text)
    
    return response.json()['id']
    
def create_style(upload_meta,style_name,ngw_parent_resource):
    resource = {
        "resource": {
            "cls": "qgis_vector_style",
            "display_name": style_name,
            "parent": {"id": ngw_parent_resource}
        },
        "qgis_vector_style": {
            "file_upload": upload_meta
        }
     }

    root = "%s/api/resource/" % (ngw_host)
    response = requests.post(root, json=resource, auth=auth)
    if response.status_code != 201:
        print('Unable to create style at NGW. Status: %s' % response.text)
    else:
        print(response.text)
    
    return response.json()['id']

if __name__ == '__main__':

    upload_meta = upload_file(input_data,ngw_host,auth)
    vector_layer_id = create_layer(upload_meta,ngw_layer_name,ngw_parent_resource)
    upload_meta = upload_file(style_name,ngw_host,auth)
    vector_style_id = create_style(upload_meta,style_name,vector_layer_id)
    