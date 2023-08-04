#pip install tusclient
from tusclient.client import TusClient
from urllib.parse import urljoin
import requests

ngw_host = 'https://sandbox.nextgis.com'
auth = ('administrator','demodemo')
output_name = 'raster.tif'
style_name = 'raster.qml'
ngw_raster_name = 'raster'
ngw_style_name = 'raster_style'
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

def create_raster_resource(upload_meta,ngw_raster_name,ngw_parent_resource):
    resource = {
        "resource": {
            "cls": "raster_layer",
            "display_name": ngw_raster_name,
            "parent": {"id": ngw_parent_resource}
        },
        "raster_layer": {
            "source": upload_meta,
            "srs": {"id": 3857}
        }
     }

    root = "%s/api/resource/" % (ngw_host)
    response = requests.post(root, json=resource, auth=auth)
    if response.status_code != 201:
        print('Crashed: impossible to create raster at NGW. Status: %s' % response.text)
    else:
        print(response.text)
    
    return response.json()['id']
    
def create_raster_style(upload_meta,style_name,ngw_parent_resource):
    resource = {
        "resource": {
            "cls": "qgis_raster_style",
            "display_name": style_name,
            "parent": {"id": ngw_parent_resource}
        },
        "qgis_raster_style": {
            "file_upload": upload_meta
        }
     }

    root = "%s/api/resource/" % (ngw_host)
    response = requests.post(root, json=resource, auth=auth)
    if response.status_code != 201:
        print('Crashed: impossible to create style at NGW. Status: %s' % response.text)
    else:
        print(response.text)
    
    return response.json()['id']

if __name__ == '__main__':

    upload_meta = upload_file(output_name,ngw_host,auth)
    raster_layer_id = create_raster_resource(upload_meta,ngw_raster_name,ngw_parent_resource)
    upload_meta = upload_file(style_name,ngw_host,auth)
    raster_style_id = create_raster_style(upload_meta,style_name,raster_layer_id)
    