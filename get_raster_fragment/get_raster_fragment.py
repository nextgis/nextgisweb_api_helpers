from osgeo import gdal

def get_raster_fragment(input_raster_path, output_raster_path, bounds):
    if not bounds or len(bounds) != 4:
        raise ValueError("Bounds must be 4 float elements")
    if any(isinstance(item, str) for item in bounds):
        raise ValueError("Bounds must be 4 float elements")
    print("BBox is valid, driving through...")
    minx, miny, maxx, maxy = bounds[0], bounds[1], bounds[2], bounds[3]
    print("Reading raster...")
    src_ds = gdal.Open(input_raster_path)
    translate_options = gdal.TranslateOptions(
        projWin=[minx, maxy, maxx, miny],
        format='COG',
        outputType=gdal.GDT_Unknown
    )
    print("Writing to {}".format(output_raster_path))
    gdal.Translate(output_raster_path, src_ds, options=translate_options)
    src_ds = None
    print("Finished")
    return output_raster_path

get_raster_fragment("/vsicurl/https://demo.nextgis.ru/api/resource/5099/cog",
               "5099_output.tiff",
               [4183421.0468197627924383, 7498377.8124515060335398, 4183600.5441526495851576, 7498525.0406009564176202])