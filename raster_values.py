import numpy as np

from raster import *
from fuzzlogic import*

class ValuesRaster(Raster):
    def __init__(self, file_name, file_name2, fuzzy_parameters, fish_class, band=1, raster_array=None, geo_info=False):
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
        Raster.__init__(self, file_name=file_name, band=band, raster_array=raster_array, geo_info=geo_info)


        self.make_hsi(vel,depth, fuzzy_parameters, fish_class)



    def make_hsi(self, vel,depth,fuzzy_parameters, fish_class):
        self.array = np.zeros((depth.shape[0], depth.shape[1])) #creates a zeroes array for the required size array

        for x in range(depth.shape[0]): #loops over rows
        # for x in range(2): #for testing
            Percent = (x / depth.shape[0])
            for y in range(depth.shape[1]): #loops over col
                self.array[x, y] = fuzzylogic(fuzzy_parameters, vel[x, y], depth[x, y], fish_class)
                print(vel[x, y], depth[x, y])
                print(self.array[x, y], "habitat", Percent)

        return self._make_raster("fuzz")  # flow velocity or water depths in self.array are replaced by HSI values
