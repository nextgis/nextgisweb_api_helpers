import requests
import math

webgis_addr = 'https://demo.nextgis.com'
raster_id = 5918

def render_raster_style(webgis_addr, raster_id):
    extent_url = f'{webgis_addr}/api/resource/{raster_id}/extent'
    response = requests.get(extent_url)
    if response.status_code == 200:
        json_extent = response.json()
        extent_dict = {
            'minLon': json_extent['extent']['minLon'],
            'maxLon': json_extent['extent']['maxLon'],
            'minLat': json_extent['extent']['minLat'],
            'maxLat': json_extent['extent']['maxLat']
        }

        reproj_coords = {}
        for key, value in extent_dict.items():
            if 'Lon' in key:
                x = wgs84To3857X(value)
                reproj_coords[key] = x
            elif 'Lat' in key:
                y = wgs84To3857Y(value)
                reproj_coords[key] = y

    else:
        print(f'Error in coverage request, code  {response.status_code}')

    render_url = (f"{webgis_addr}/api/component/render/image?"
                  f"resource={raster_id}"
                  f"&extent={int(reproj_coords['minLon'])},{int(reproj_coords['minLat'])},{int(reproj_coords['maxLon'])},{int(reproj_coords['maxLat'])}"
                  f"&size=500,500")

    download_response = requests.get(render_url)
    if download_response.status_code == 200:
        with open(f'get_raster_style_preview\\{raster_id}.png', 'wb') as file:
            file.write(download_response.content)

def wgs84To3857X(x):
    earthRadius = 6378137.0
    return earthRadius * math.radians(float(x))

def wgs84To3857Y(y):
    earthRadius = 6378137.0
    return earthRadius * math.log(
        math.tan(math.pi / 4 + math.radians(float(y)) / 2)
    )

if __name__ == '__main__':
    render_raster_style(webgis_addr, raster_id)
