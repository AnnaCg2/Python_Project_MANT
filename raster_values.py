import numpy as np

from raster import *
from fuzzlogic import*

class ValuesRaster(Raster):
    def __init__(self, file_name, file_name2, fuzzy_parameters, fish_class, plot_fuzzy_example, band=1, raster_array=None, geo_info=False):
        """
        A GeoTiff Raster dataset (wrapped osgeo.gdal. Dataset)
        :param file_name: STR of a GeoTiff file name including directory (must end on ".tif")
        :param hsi_curve: nested list of [[par-values], [HSI-values]], where
                    [par-values] (e.g., velocity values) and
                    [HSI-values] must have the same length.
        :param band: INT of the band number to use
        """
        try:
            raster1=Raster(file_name=file_name, band=band, raster_array=raster_array, geo_info=geo_info)
            raster2 = Raster(file_name=file_name2, band=band, raster_array=raster_array, geo_info=geo_info)
        except:
            logging.error("ERROR:Velocity or Depth tiff missing, incorrect format,name, or used in other program")


        vel=raster1.array
        depth=raster2.array

        Raster.__init__(self, file_name=file_name, band=band, raster_array=raster_array, geo_info=geo_info)

        if depth.shape[0] != vel.shape[0]:
            logging.error("ERROR:Rows not equal dimension depth is {0} vel is {1}".format(depth.shape[0],vel.shape[0]))
        if depth.shape[1] != vel.shape[1]:
            logging.error("ERROR:Columns not equal dimension depth is {0} vel is {1}".format(depth.shape[1], vel.shape[1]))

        self.make_hsi(vel, depth, fuzzy_parameters, fish_class, plot_fuzzy_example)



    def make_hsi(self, vel,depth,fuzzy_parameters, fish_class, plot_fuzzy_example):
        self.array = np.zeros((depth.shape[0], depth.shape[1])) #creates a zeroes array for the required size array
        (membership, x_values) = create_membership_functions(fuzzy_parameters)
        percent_old = 0

        for x in range(depth.shape[0]): #loops over rows


            percent_new = int(x*100 / depth.shape[0])
            for y in range(depth.shape[1]): #loops over col

                if np.isnan(depth[x,y]) == True or depth[x,y] == 0:
                #if depth[x,y] != np.nan or depth[x,y]!= 0:
                    self.array[x, y] = 0


                else:

                    (self.array[x, y], aggregated, habitat_activation_values, habitat_activation) \
                        = fuzzylogic(vel[x, y], depth[x, y], fish_class, membership, x_values)



            if percent_new > percent_old:
                percent_old=percent_new
                print( percent_old,"% complete")

        if plot_fuzzy_example:
            logging.warning("Graphs must be closed before running \"calculate_habitat_area\"")
            membership, x_values = create_membership_functions(fuzzy_parameters)
            (habitat, aggregated, habitat_activation_values, habitat_activation) = fuzzylogic(vel[914, 1], depth[914, 1], fish_class, membership, x_values)
            fig = plot_fuzzy(x_values, membership)
            fig2 = plot_defuzzy(habitat, x_values, membership, aggregated, habitat_activation_values, habitat_activation)

        return self._make_raster("fuzz")  # flow velocity or water depths in self.array are replaced by HSI values


    # def depth_vel_values(self):
    #
    #     return(self.vel_array[914,1],self.depth_array[914,1])
