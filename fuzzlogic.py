from make_rules import *


def plot_fuzzy(x_values, membership):
    """
    Plots an example of the fuzzified curves for depth, velocity and HSI
    :param x_values: dictionary with velocity, depth, and habitat values stored as numpy arrays
    :param membership: dictionary with fuzzy membership functions as pandas dataframes
    :return fig: plot depicting fuzzy membership functions
    """
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

    # plot velocity membership functions
    ax0.plot(x_values["x_velocity"], membership["velocity_membership"]["velocity_lo"],
             'b', linewidth=1.5, label='low')
    ax0.plot(x_values["x_velocity"], membership["velocity_membership"]["velocity_md"],
             'g', linewidth=1.5, label='medium')
    ax0.plot(x_values["x_velocity"], membership["velocity_membership"]["velocity_hi"],
             'r', linewidth=1.5, label='high')
    ax0.set_title('Flow Velocity')
    ax0.legend()

    # plot depth membership functions
    ax1.plot(x_values["x_depth"], membership["depth_membership"]["depth_lo"],
             'b', linewidth=1.5, label='low')
    ax1.plot(x_values["x_depth"], membership["depth_membership"]["depth_md"],
             'g', linewidth=1.5, label='medium')
    ax1.plot(x_values["x_depth"], membership["depth_membership"]["depth_hi"],
             'r', linewidth=1.5, label='high')
    ax1.set_title('depth')
    ax1.legend()

    # plot depth membership functions
    ax2.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_lo"],
             'b', linewidth=1.5, label='Low')
    ax2.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_md"],
             'g', linewidth=1.5, label='Medium')
    ax2.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_hi"],
             'r', linewidth=1.5, label='High')
    ax2.set_title('habitat amount')
    ax2.legend()

    # Turn off top/right axes
    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    plt.show()
    return fig


def plot_defuzzy(habitat, x_values, membership, aggregated, habitat_activation_values, habitat_activation):
    """
    Plot output of membership values based on rules. Shows final defuzzification value.
    :param habitat: numpy.float64. final defuzzified habitat suitability index value
    :param x_values: dictionary with velocity, depth, and habitat values stored as numpy arrays
    :param membership: dictionary with fuzzy membership functions as pandas dataframes
    :param aggregated: numpy array. Aggregates all three output membership functions together
    :param habitat_activation_values: numpy array. Fuzzy membership functions from rules
    :param habitat_activation: numpy array. Final degree of membership for graphing
    :return fig: plot depicting membership functions with rules applied
    """

    fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(8, 6))
    habitat0 = np.zeros_like(x_values["x_habitat"])

    # plot habitat membership function
    ax0.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_lo"],
             'b', linewidth=0.5, linestyle='--', )
    ax0.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_md"],
             'g', linewidth=0.5, linestyle='--')
    ax0.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_hi"],
             'r', linewidth=0.5, linestyle='--')

    # fill in fuzzy membership functions based on rule applications
    ax0.fill_between(x_values["x_habitat"], habitat0, habitat_activation_values["habitat_activation_lo"],
                     facecolor='b', alpha=0.7)
    ax0.fill_between(x_values["x_habitat"], habitat0, habitat_activation_values["habitat_activation_md"],
                     facecolor='g', alpha=0.7)
    ax0.fill_between(x_values["x_habitat"], habitat0, habitat_activation_values["habitat_activation_hi"],
                     facecolor='r', alpha=0.7)
    ax0.set_title('Output membership activity')

    # plot habitat membership function with final defuzzified value
    ax1.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_lo"],
             'b', linewidth=0.5, linestyle='--', )
    ax1.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_md"],
             'g', linewidth=0.5, linestyle='--')
    ax1.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_hi"],
             'r', linewidth=0.5, linestyle='--')
    ax1.fill_between(x_values["x_habitat"], habitat0, aggregated, facecolor='Orange', alpha=0.7)
    ax1.plot([habitat, habitat], [0, habitat_activation], 'k', linewidth=1.5, alpha=0.9)
    ax1.set_title('Aggregated membership and result (line)')

    # Turn off top/right axes
    for ax in (ax0, ax1):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    plt.show()
    return fig


def get_fuzzy_params(file_path):
    """
    Extract fuzzy parameter information from txt file and save as .json
    :param file_path: string file location of text file with fuzzy parameters
    :return fuzzy_parameters: .json file with fuzzy parameter information
    """
    txt_to_json(file_path, "fuzzy_params.json")
    fuzzy_parameters = read_json(os.path.abspath("") + "\\fuzzy_params.json")
    return fuzzy_parameters


def create_membership_functions(fuzzy_parameters):
    """
    Generates triangle membership functions and saves in dictionary
    :param fuzzy_parameters: .json file with fuzzy parameter information
    :return membership: dictionary with fuzzy membership functions as pandas dataframes
    :return x_values: dictionary with velocity, depth, and habitat values stored as numpy arrays
    """
    # must save x-axis values as a np array before passing into fuzz.trimf
    x_velocity = np.asarray(fuzzy_parameters["velocity"]["x_axis"], dtype=np.float16)
    x_depth = np.asarray(fuzzy_parameters["depth"]["x_axis"], dtype=np.float16)
    x_habitat = np.asarray(fuzzy_parameters["habitat"]["x_axis"], dtype=np.float16)
    x_values = {"x_velocity": x_velocity, "x_depth": x_depth, "x_habitat": x_habitat}

    # create custom membership functions for velocity
    velocity_membership = pd.DataFrame(columns=['velocity_lo', 'velocity_md', 'velocity_hi'])
    velocity_membership["velocity_lo"] = fuzz.trimf(x_velocity,
                                                    fuzzy_parameters["velocity"]["lo"])
    velocity_membership["velocity_md"] = fuzz.trimf(x_velocity,
                                                    fuzzy_parameters["velocity"]["md"])
    velocity_membership["velocity_hi"] = fuzz.trimf(x_velocity,
                                                    fuzzy_parameters["velocity"]["hi"])

    # create custom membership functions for depth
    depth_membership = pd.DataFrame(columns=['depth_lo', 'depth_md', 'depth_hi'])
    depth_membership["depth_lo"] = fuzz.trimf(x_depth, fuzzy_parameters["depth"]["lo"])
    depth_membership["depth_md"] = fuzz.trimf(x_depth, fuzzy_parameters["depth"]["md"])
    depth_membership["depth_hi"] = fuzz.trimf(x_depth, fuzzy_parameters["depth"]["hi"])

    # create custom membership functions for habitat
    habitat_membership = pd.DataFrame(columns=['habitat_lo', 'habitat_md', 'habitat_hi'])
    habitat_membership["habitat_lo"] = fuzz.trimf(x_habitat, fuzzy_parameters["habitat"]["lo"])
    habitat_membership["habitat_md"] = fuzz.trimf(x_habitat, fuzzy_parameters["habitat"]["md"])
    habitat_membership["habitat_hi"] = fuzz.trimf(x_habitat, fuzzy_parameters["habitat"]["hi"])

    membership = {"velocity_membership": velocity_membership, "depth_membership": depth_membership,
                  "habitat_membership": habitat_membership}
    return membership, x_values


def fuzzylogic(velocity_value, depth_value, fish_class, membership, x_values):
    """
    Applies fuzzy logic and defuzification to provide final habitat suitability number
    for given velocity and depth value
    :param velocity_value:numpy.float64 given velocity value
    :param depth_value: numpy.float64 given velocity value
    :param fish_class: class object. contains functions for making rules
    :param membership: dictionary with fuzzy membership functions as pandas dataframes
    :param x_values: dictionary with velocity, depth, and habitat values stored as numpy arrays
    :return habitat: numpy.float64. final defuzzified habitat suitability index value
    :return aggregated: numpy array. Aggregates all three output membership functions together
    :return habitat_activation_values: numpy array. Fuzzy membership functions from rules
    :return habitat_activation: numpy array. Final degree of membership for graphing

    Skyfuzz's tipping example used as template
     https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem.html
    """
    # Activation of our fuzzy membership functions at these values.
    # Saved in dictionary
    param = ["lo", "md", "hi"]
    fuzzy_velocity_dict = {}
    fuzzy_depth_dict = {}
    for par in param:
        fuzzy_velocity_dict.update({par :fuzz.interp_membership(x_values["x_velocity"],
                                                               membership["velocity_membership"]["velocity_"+par],
                                                               velocity_value) })
        fuzzy_depth_dict.update({par :fuzz.interp_membership(x_values["x_depth"],
                                                            membership["depth_membership"]["depth_"+par],
                                                            depth_value)})

    # call fish class to apply rules
    habitat_activation_lo, habitat_activation_md, habitat_activation_hi = \
        fish_class.make_fuzzy_rules(habitat_trimf=membership["habitat_membership"],
                                    fuzzy_velocity=fuzzy_velocity_dict,
                                    fuzzy_depth=fuzzy_depth_dict)

    habitat_activation_values = {"habitat_activation_lo": habitat_activation_lo,
                                 "habitat_activation_md": habitat_activation_md,
                                 "habitat_activation_hi": habitat_activation_hi}

    # Aggregate all three output membership functions together
    aggregated = np.fmax(habitat_activation_lo, habitat_activation_md, habitat_activation_hi)

    # Calculate defuzzified result
    habitat = fuzz.defuzz(x_values["x_habitat"], aggregated, 'centroid')
    habitat_activation = fuzz.interp_membership(x_values["x_habitat"], aggregated, habitat)
    return habitat, aggregated, habitat_activation_values, habitat_activation



