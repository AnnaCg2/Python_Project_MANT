from fun import *
from raster_hsi import HSIRaster, Raster
from time import perf_counter
from raster_values import*
def combine_hsi_rasters(raster_list, method="geometric_mean"):
    """
    Combine HSI rasters into combined Habitat Suitability Index (cHSI) Rasters
    :param raster_list: list of HSIRasters (HSI)
    :param method: string (default="geometric_mean", alt="product)
    :return HSIRaster: contains float pixel values
    """
    if method == "geometric_mean":
        power = 1.0 / float(raster_list.__len__())
    else:
        # supposedly method is "product"
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
        par_pairs = [] #each pair gets its own little list and is nested within bigger list
        # iterate through the length of parameter-HSI curves in the JSON file
        for i in range(0, file_info[par][life_stage].__len__()):
            # if the parameter is not empty (i.e., __len__ > 0), append the parameter-HSI (e.g., [u_value, HSI_value]) pair as nested list
            if str(file_info[par][life_stage][i]["HSI"]).__len__() > 0:
                try:
                    # only append data pairs if both parameter and HSI are numeric (floats)
                    par_pairs.append([float(file_info[par][life_stage][i][par_dict[par]]),
                                      float(file_info[par][life_stage][i]["HSI"])]) #this is what actually creates the pair and the .append puts it in the nested list
                except ValueError:
                    logging.warning("Invalid HSI curve entry for {0} in parameter {1}.".format(life_stage, par))
        # add the nested parameter pair list as pandas DataFrame to the curve_data dictionary
        curve_data.update({par: pd.DataFrame(par_pairs, columns=[par_dict[par], "HSI"])}) #contains pandas dataframes for velocity and depth
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
def get_fuzzhsi_raster(tif_dir1,tif_dir2,fuzz_paramters):


    return ValuesRaster(tif_dir1,tif_dir2,fuzz_paramters)



@log_actions
@cache
def main():
    # get HSI curves as pandas DataFrames nested in a dictionary
    if method == "hsi":
        print("hsi")
        hsi_curve = get_hsi_curve(fish_file, life_stage=life_stage, parameters=parameters)

        # create HSI rasters for all parameters considered and store the Raster objects in a dictionary
        eco_rasters = {}
        for par in parameters:
            hsi_par_curve = [list(hsi_curve[par][par_dict[par]]),
                             list(hsi_curve[par]["HSI"])]
            eco_rasters.update({par: get_hsi_raster(tif_dir=tifs[par], hsi_curve=hsi_par_curve)})
            eco_rasters[par].save(hsi_output_dir + "hsi_%s.tif" % par)
    elif method == "fuzzy_logic":
        print("fuzzy_logic")
        eco_rasters = {}
        eco_rasters.update({"fuzz_hsi":ValuesRaster (tifs["velocity"],tifs["depth"],fuzzy_parameters)})
        eco_rasters["fuzz_hsi"].save(hsi_output_dir + "hsi_fuzzy.tif" )

    else:
        print("no method selected")

    # get and save chsi raster
    chsi_raster = combine_hsi_rasters(raster_list=list(eco_rasters.values()),
                                      method="geometric_mean")
    chsi_raster.save(hsi_output_dir + "chsi.tif")

if __name__ == '__main__':
    # define global variables for the main() function
    parameters = ["velocity", "depth"]
    life_stage = "juvenile"  # either "fry", "juvenile", "adult", or "spawning"
    #method="hsi" #fuzzy_logic or hsi
    method= "fuzzy_logic"
    trout = Fish("Rainbow Trout", "juvenile")

    # paths
    fish_file = os.path.abspath("") + "\\habitat\\trout.json"
    tifs = {"velocity": os.path.abspath("") + "\\basement\\flow_velocity.tif",
            "depth": os.path.abspath("") + "\\basement\\water_depth.tif"}
    hsi_output_dir = os.path.abspath("") + "\\habitat\\"
    fuzzy_parameters=[0,0,5],[0, 5, 10],[5,10,10]


    # run code and evaluate performance
    t0 = perf_counter()
    main()
    t1 = perf_counter()
    print("Time elapsed: " + str(t1 - t0))
