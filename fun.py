from config import *
from bisect import bisect_left
#


def cache(fun):
    def wrapper(*args, **kwargs):
        check_cache()
        fun(*args, **kwargs)
        remove_directory(cache_folder)
    return wrapper


def check_cache():
    try:
        os.makedirs(cache_folder)
    except OSError:
        pass


def create_random_string(length):
    """
    Create a random alphabetic string with a given length (used as file name for temporary (cached) dataset
    :param length: integer (number of characters)
    :return: string
    """
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


def interpolate_from_list(x_values, y_values, xi_values):
    """
    Calculate y_i value from a list of x and y values for a list of given x_i
    if one of x_i values is beyond value range of x_i values, function appends nan_value (b/c we're interpolating not extrapolating)
    :param x_values: sorted list (smallest to largest)
    :param y_values: sorted list (smallest to largest, must match x_values)
    :param xi_values: n x 1 numpy.ndarray of floats
    :return: n x 1 numpy.ndarray of floats (yi_values)
    """
    yi_values = []
    max_position = x_values.__len__()
    for xi in xi_values:
        position = bisect_left(x_values, xi)
        try:
            if position > 0:
                if position < max_position:
                    yi_values.append(interpolate_y(x1=x_values[position-1], x2=x_values[position],
                                                   y1=y_values[position-1], y2=y_values[position],
                                                   xi=xi))
                else:
                    yi_values.append(nan_value)
            else:
                yi_values.append(nan_value)
        except TypeError:
            yi_values.append(nan_value)
    return np.array(yi_values)


def interpolate_y(x1, x2, y1, y2, xi):
    """
    Linear interpolation of yi for xi between two points x1/y1 and x2/y2
    Called by interpolate_from_list - this is the function that does the actual initerpolation
    :param x1: float (x-value of point 1)
    :param x2: float (y-value of point 1)
    :param y1: float (x-value of point 2)
    :param y2: float (y-value of point 2)
    :param xi: float (x value of point to interpolate)
    :return: float (yi)
    """
    try:
        return y1 + ((xi - x1) / (x2 - x1) * (y2 - y1))
    except ValueError:
        return nan_value
    except ZeroDivisionError:
        return nan_value


def log_actions(fun):
    def wrapper(*args, **kwargs):
        start_logging()
        fun(*args, **kwargs)
        logging.shutdown()
    return wrapper


def read_json(file_name):
    """
    Open a json file with habitat suitability curves for a fish. Returns it as Python object
    :param file_name: string of the file name including the directory.
    :return: JSON object - in the case of trout.json, the return object
                can be called like this: trout["velocity"]["spawning"][0]["u"] = 0.0198
    """
    with open(file_name, mode="r") as file:
        return json.load(file)

def txt_to_json(file_path, save_path):
    """
    Reads data from .txt file and loads into and saves .json file
    :param file_path: string of the file path to the .txt file including the directory
    :param save_path: string of the .json file name
    """
    with open(file_path) as file:
        file_data = file.read()
        txt_data = json.loads(file_data)

    with open(save_path, 'w') as json_file:
        json.dump(txt_data, json_file, indent=4)

    file.close()
    json_file.close()
    return()



def remove_directory(directory):
    """
    Remove directory and all its contents - be careful!
    :param directory: string
    :return: None
    """
    try:
        for root, dirs, files in os.walk(directory):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        shutil.rmtree(directory)
    except PermissionError:
        print("WARNING: Could not remove %s (files locked by other program)." % directory)
    except FileNotFoundError:
        print("WARNING: The directory %s does not exist." % directory)
    except NotADirectoryError:
        print("WARNING: %s is not a directory." % directory)


def start_logging(): #starts logging to a logfile (logfile.log) and the Python console at the logging.DEBUG level
    logging.basicConfig(filename="logfile.log", format="[%(asctime)s] %(message)s",
                        filemode="w", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
