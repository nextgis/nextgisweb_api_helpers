# Get resource ID from a resource link
# Try on sandbox.nextgis.com

from urllib.parse import urlparse
import re

ngw_host = "https://sandbox.nextgis.com"
resource_link = "https://sandbox.nextgis.com/resource/5/display?panel=layers"

if __name__ == "__main__":
    path = urlparse(resource_link).path
    match = re.search(r"/resource/(\d+)", path)
    if not match:
        raise ValueError(f"Cannot extract resource id from URL: {resource_link}")

    resource_id = int(match.group(1))
    print(resource_id)
