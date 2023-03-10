from raster_hsi import HSIRaster
from time import perf_counter
from raster_values import*


def combine_hsi_rasters(raster_list, method="product"):
    """
    Combine HSI rasters into combined Habitat Suitability Index (cHSI) Rasters
    :param raster_list: list of HSIRasters (HSI)
    :param method: string (default="geometric_mean", alt="product)
    :return HSIRaster: contains float pixel values
    """
    if method == "geometric_mean":
        power = 1.0 / float(raster_list.__len__())
    else:
        power = 1.0

    chsi_raster = Raster(cache_folder + "chsi_start.tif",
                         raster_array=np.ones(raster_list[0].array.shape),
                         epsg=raster_list[0].epsg,
                         geo_info=raster_list[0].geo_transformation)
    for ras in raster_list:
        chsi_raster = chsi_raster * ras

    return chsi_raster ** power


def get_hsi_curve(json_file, life_stage, parameters):
    # read the JSON file with fun.read_json
    file_info = read_json(json_file)
    # instantiate output dictionary
    curve_data = {}
    # iterate through parameter list (e.g., ["velocity", "depth"])
    for par in parameters:
        # create a void list to store pairs of parameter-HSI values as nested lists
        par_pairs = []  # each pair gets its own little list and is nested within bigger list
        # iterate through the length of parameter-HSI curves in the JSON file
        for i in range(0, file_info[par][life_stage].__len__()):
            # if the parameter is not empty (i.e., __len__ > 0),
            # append the parameter-HSI (e.g., [u_value, HSI_value]) pair as nested list
            if str(file_info[par][life_stage][i]["HSI"]).__len__() > 0:
                try:
                    # only append data pairs if both parameter and HSI are numeric (floats)

                    par_pairs.append([float(file_info[par][life_stage][i][par_dict[par]]),
                                      float(file_info[par][life_stage][i]["HSI"])])
                except ValueError:
                    logging.warning("Invalid HSI curve entry for {0} in parameter {1}.".format(life_stage, par))
        # add the nested parameter pair list as pandas DataFrame to the curve_data dictionary
        # contains pandas dataframes for velocity and depth
        curve_data.update({par: pd.DataFrame(par_pairs, columns=[par_dict[par], "HSI"])})
        print(curve_data)
    return curve_data


def get_hsi_raster(tif_dir, hsi_curve):
    """
    Calculate and return Habitat Suitability Index Rasters
    :param tif_dir: string of directory and name of  a tif file with parameter values (e.g., depth in m)
    :param hsi_curve: nested list of [[par-values], [HSI-values]], where
                            [par-values] (e.g., velocity values) and
                            [HSI-values] must have the same length.
    :return hsi_raster: Raster with HSI values
    """
    return HSIRaster(tif_dir, hsi_curve)


def get_fuzzhsi_raster(tif_dir1, tif_dir2, fuzzy_parameters, fish_class, plot_fuzzy_example):
    """
        Calculate and return fuzzy logic Habitat Suitability Index Rasters
        :param tif_dir1: string of directory and name of  a tif file with parameter values velocity
        :param tif_dir2: string of directory and name of  a tif file with parameter values depth
        :param fuzzy_parameters np.array that dictates the fuzzy parameters
        :param fish_class object of fish class
        :param plot_fuzzy_example Boolean true or false to initiate fuzz example plotting
        :return hsi_raster: Raster with HSI values



        """

    return ValuesRaster(tif_dir1, tif_dir2, fuzzy_parameters, fish_class, plot_fuzzy_example)


@log_actions
@cache
def main(method, fish_file, tifs, hsi_output_dir, fuzzy_params, trout, parameters, life_stage, plot_fuzzy_example):
    # get HSI curves as pandas DataFrames nested in a dictionary
    logging.info("Using method of {}".format(method))
    try:
        if method == "hsi":

            hsi_curve = get_hsi_curve(fish_file, life_stage=life_stage, parameters=parameters)

            # create HSI rasters for all parameters considered and store the Raster objects in a dictionary
            eco_rasters = {}
            for par in parameters:
                hsi_par_curve = [list(hsi_curve[par][par_dict[par]]),
                                 list(hsi_curve[par]["HSI"])]
                eco_rasters.update({par: get_hsi_raster(tif_dir=tifs[par], hsi_curve=hsi_par_curve)})
                eco_rasters[par].save(hsi_output_dir + "hsi_%s.tif" % par)
        elif method == "fuzzy_logic":
            # creates fuzzy hsi raster using dictionary
            eco_rasters = {}
            eco_rasters.update({"fuzz_hsi": ValuesRaster(file_name=tifs["velocity"], file_name2=tifs["depth"],
                                                         fuzzy_parameters=fuzzy_params, fish_class=trout,
                                                         plot_fuzzy_example=plot_fuzzy_example)})
            eco_rasters["fuzz_hsi"].save(hsi_output_dir + "hsi_fuzzy.tif")

        # creates Tif with Habitat values
        chsi_raster = combine_hsi_rasters(raster_list=list(eco_rasters.values()),
                                          method="geometric_mean")
        chsi_raster.save(hsi_output_dir + "chsi.tif")
    except ValueError:
        logging.error("{} is not valid method or problem creating raster".format(method))


if __name__ == '__main__':
    # define global variables for the main() function
    parameters = ["velocity", "depth"]
    life_stage = "fry"  # either "fry", "juvenile", "adult", or "spawning"
    method = "fuzzy_logic"  # either fuzzy_logic or hsi
    trout = Fish("Rainbow Trout", life_stage)
    fuzzy_params = get_fuzzy_params(os.path.abspath("") + "\\habitat\\fuzzy_params.txt")
    plot_fuzzy_example = True

    # paths
    fish_file = os.path.abspath("") + "\\habitat\\trout.json"
    tifs = {"velocity": os.path.abspath("") + "\\basement\\flow_velocity.tif",
            "depth": os.path.abspath("") + "\\basement\\water_depth.tif"}
    hsi_output_dir = os.path.abspath("") + "\\habitat\\"

    # run code and evaluate performance
    t0 = perf_counter()
    main(method, fish_file, tifs, hsi_output_dir, fuzzy_params, trout, parameters, life_stage, plot_fuzzy_example)
    t1 = perf_counter()
    logging.info("Time elapsed " + str(t1 - t0) +" seconds")

