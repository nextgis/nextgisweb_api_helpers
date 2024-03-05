def get_raster_fragment(input_raster_path, output_raster_path, bounds):
    if not bounds or len(bounds) != 4:
        raise ValueError("Bounds must be 4 float elements")
    if any(isinstance(item, str) for item in bounds):
        raise ValueError("Bounds must be 4 float elements")
    print("BBox is valid, driving through...")
    bbox = box(*bounds)
    geometry = mapping(bbox)
    with rasterio.open(input_raster_path) as src:
        print("Reading raster...")
        out_image, out_transform = mask(src, [geometry], crop=True)
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "COG",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })
        print("Writing to {}".format(output_raster_path))
        with rasterio.open(output_raster_path, "w", **out_meta) as dest:
            dest.write(out_image)
    return output_raster_path
