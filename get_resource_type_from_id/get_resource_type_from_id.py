# Get resource type from a resource ID
# Try on sandbox.nextgis.com
# Prerequisites:
# - Resource with ID exists

import requests

ngw_host = "https://sandbox.nextgis.com"
auth = ("administrator", "demodemo")
resource_id = 5

if __name__ == "__main__":
    response = requests.get(
        f"{ngw_host}/api/resource/{resource_id}",
        auth=auth,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    resource_type = data["resource"]["cls"]
    print(resource_type)
