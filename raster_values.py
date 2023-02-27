import numpy as np
from raster import *
from fuzzlogic import*

class ValuesRaster(Raster):
    def __init__(self, file_name, file_name2, fuzzy_parameters, fish_class, plot_fuzzy_example, band=1,
                 raster_array=None, geo_info=False):
        """
       A GeoTiff Raster dataset (wrapped osgeo.gdal. Dataset)
        :param file_name: STR of velocity GeoTiff file name including directory (must end on ".tif")
        :param file_name: STR of depth GeoTiff file name including directory (must end on ".tif")
        :param fuzzy_parameters np.array that dictates the fuzzy parameters
        :param fish_class object of fish class
        :plot_fuzzy_example Boolean true or false to initiate fuzz example plotting
        :param band: INT of the band number to use
        Modified template from raster_hsi to use fuzzy logic
        """
        try:
            raster1 = Raster(file_name=file_name, band=band, raster_array=raster_array, geo_info=geo_info)
            raster2 = Raster(file_name=file_name2, band=band, raster_array=raster_array, geo_info=geo_info)
        except AttributeError:
            logging.error("ERROR:Velocity or Depth tiff missing, incorrect format,name, or used in other program")

        # Velocity and Depth array creation from geo tiffs
        vel = raster1.array
        depth = raster2.array

        Raster.__init__(self, file_name=file_name, band=band, raster_array=raster_array, geo_info=geo_info)

        if depth.shape[0] != vel.shape[0]:
            logging.error("ERROR:Rows not equal dimension depth is {0} vel is {1}"
                          .format(depth.shape[0]  ,vel.shape[0]))
        if depth.shape[1] != vel.shape[1]:
            logging.error("ERROR:Columns not equal dimension depth is {0} vel is {1}"
                          .format(depth.shape[1], vel.shape[1]))



        self.make_hsi(vel, depth, fuzzy_parameters, fish_class, plot_fuzzy_example)




    def make_hsi(self, vel,depth,fuzzy_parameters, fish_class, plot_fuzzy_example):
        """
               A GeoTiff Raster dataset (wrapped osgeo.gdal. Dataset)
               :param vel: numpy array of velocity
               :param depth: numpy array of velocity
               :param fuzzy_parameters np.array that dictates the fuzzy parameters
               :param plot_fuzzy_example Boolean true or false to initiate fuzz example plotting
               :param fish_class: fish class import for fuzzy rules


               """
        # Init loop
        self.array = np.zeros((depth.shape[0], depth.shape[1]))  # creates a zeroes array for the required size array

        #creates membership functions
        (membership, x_values) = create_membership_functions(fuzzy_parameters)
        percent_old = 0
        includes_nan = False

        # Loop over both arrays
        for x in range(depth.shape[0]):  # loops over rows

            #Calculates percent completed
            percent_new = int(x*100 / depth.shape[0])

            for y in range(depth.shape[1]):  # loops over col

                # Measure to reduce running time by setting Habitat to zero, when data NAN or depth zero
                if np.isnan(depth[x,y]) == True \
                        or depth[x,y] == 0:
                    includes_nan= True

                    self.array[x, y] = 0


                else:
                    # Runs fuzzy logic function for in vel and depth
                    (self.array[x, y], aggregated, habitat_activation_values, habitat_activation) \
                        = fuzzylogic(vel[x, y], depth[x, y], fish_class, membership, x_values)


            #Prints Update
            if percent_new > percent_old:
                percent_old=percent_new
                print(percent_old,"% complete")
            # Nan value warning
        if includes_nan ==True:

            logging.warning("WARNING:Input data includes Nan values or no depth. Habitat set to zero in those locations")

        if plot_fuzzy_example:
            self. make_fuzzyplot(fuzzy_parameters,fish_class,vel,depth)


        return self._make_raster("fuzz")  # flow velocity or water depths in self.array are replaced by HSI values

    def make_fuzzyplot(self,fuzzy_parameters,fish_class,vel,depth):
        """
               A GeoTiff Raster dataset (wrapped osgeo.gdal. Dataset)
               :param fuzzy_parameters np.array that dictates the fuzzy parameters
               :param fish_class: fish class import for fuzzy rules
               :param vel: numpy array of velocity
               :param depth: numpy array of velocity
               """
        logging.warning("WARNING:Graphs must be closed before running \"calculate_habitat_area\"")

        membership, x_values = create_membership_functions(fuzzy_parameters)
        (habitat, aggregated, habitat_activation_values, habitat_activation) \
            = fuzzylogic(vel[914, 1], depth[914, 1], fish_class, membership, x_values)

        # Figures
        fig = plot_fuzzy(x_values, membership)
        fig2 = plot_defuzzy(habitat, x_values, membership,
                            aggregated, habitat_activation_values, habitat_activation)
        return



