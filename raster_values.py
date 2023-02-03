import numpy as np

from raster import *
from fuzzlogic import*

class ValuesRaster(Raster):
    def __init__(self, file_name,file_name2,parameters, band=1, raster_array=None, geo_info=False):
        """
        A GeoTiff Raster dataset (wrapped osgeo.gdal. Dataset)
        :param file_name: STR of a GeoTiff file name including directory (must end on ".tif")
        :param hsi_curve: nested list of [[par-values], [HSI-values]], where
                    [par-values] (e.g., velocity values) and
                    [HSI-values] must have the same length.
        :param band: INT of the band number to use
        """

        raster1=Raster(file_name=file_name, band=band, raster_array=raster_array, geo_info=geo_info)
        vel=raster1.array
        raster2=Raster(file_name=file_name2, band=band, raster_array=raster_array, geo_info=geo_info)

        depth=raster2.array
        #print(depth.shape[0],depth.shape[1])
        fuzz_array=np.zeros((depth.shape[0],depth.shape[1]))


        for x in range(depth.shape[0]) :
            Percent=x/depth.shape[0]
            for y in range(depth.shape[1]):

                fuzz_array[x,y] = fuzzylogic(parameters,vel[x,y],depth[x,y])
                print(vel[x,y],depth[x,y])
                print(fuzz_array[x,y],"habitat",Percent)
        return raster1._make_raster("fuzz")  # flow velocity or water depths in self.array are replaced by HSI values


