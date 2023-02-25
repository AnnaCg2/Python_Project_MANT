from make_rules import *


# Genera

#create json file
def plot_fuzzy(x_values, membership):
    """
    Plots an example of the fuzzified curves for depth, velocity and HSI
    :param fuzzy_plot: boolean value enabling or disabling the plotting function
    """
    # Visualize these universes and membership functions
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

    ax0.plot(x_values["x_velocity"], membership["velocity_membership"]["velocity_lo"], 'b', linewidth=1.5, label='low')
    ax0.plot(x_values["x_velocity"], membership["velocity_membership"]["velocity_md"], 'g', linewidth=1.5, label='medium')
    ax0.plot(x_values["x_velocity"], membership["velocity_membership"]["velocity_hi"], 'r', linewidth=1.5, label='high')
    ax0.set_title('Flow Velocity')
    ax0.legend()

    ax1.plot(x_values["x_depth"], membership["depth_membership"]["depth_lo"], 'b', linewidth=1.5, label='low')
    ax1.plot(x_values["x_depth"], membership["depth_membership"]["depth_md"], 'g', linewidth=1.5, label='medium')
    ax1.plot(x_values["x_depth"], membership["depth_membership"]["depth_hi"], 'r', linewidth=1.5, label='high')
    ax1.set_title('depth')
    ax1.legend()

    ax2.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_lo"], 'b', linewidth=1.5, label='Low')
    ax2.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_md"], 'g', linewidth=1.5, label='Medium')
    ax2.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_hi"], 'r', linewidth=1.5, label='High')
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
    return(fig)

def plot_defuzzy(habitat, x_values, membership, aggregated, habitat_activation_values, habitat_activation):
    #Visualize this
    fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(8, 6))

    habitat0 = np.zeros_like(x_values["x_habitat"])

    ax0.fill_between(x_values["x_habitat"], habitat0, habitat_activation_values["habitat_activation_lo"], facecolor='b', alpha=0.7)
    ax0.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_lo"], 'b', linewidth=0.5, linestyle='--', )
    ax0.fill_between(x_values["x_habitat"], habitat0, habitat_activation_values["habitat_activation_md"], facecolor='g', alpha=0.7)
    ax0.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_md"], 'g', linewidth=0.5, linestyle='--')
    ax0.fill_between(x_values["x_habitat"], habitat0, habitat_activation_values["habitat_activation_hi"], facecolor='r', alpha=0.7)
    ax0.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_hi"], 'r', linewidth=0.5, linestyle='--')
    ax0.set_title('Output membership activity')

    ax1.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_lo"], 'b', linewidth=0.5, linestyle='--', )
    ax1.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_md"], 'g', linewidth=0.5, linestyle='--')
    ax1.plot(x_values["x_habitat"], membership["habitat_membership"]["habitat_hi"], 'r', linewidth=0.5, linestyle='--')
    ax1.fill_between(x_values["x_habitat"], habitat0, aggregated, facecolor='Orange', alpha=0.7)
    ax1.plot([habitat, habitat], [0, habitat_activation], 'k', linewidth=1.5, alpha=0.9)
    ax1.set_title('Aggregated membership and result (line)')

    # Turn off top/right axes
    for ax in (ax0,ax1):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()

    plt.show()
    return(fig)

def get_fuzzy_params(file_path):

    # Generate fuzzy membership functions
    # add import capabilities from json
    txt_to_json(file_path, "fuzzy_params.json")
    fuzzy_parameters = read_json(os.path.abspath("") + "\\fuzzy_params.json")

    return(fuzzy_parameters)

def create_membership_functions(fuzzy_parameters):
    # must save x-axis values as a np array before passing into fuzz.trimf
    x_velocity = np.asarray(fuzzy_parameters["velocity"]["x_axis"], dtype=np.float32)
    x_depth = np.asarray(fuzzy_parameters["depth"]["x_axis"], dtype=np.float32)
    x_habitat = np.asarray(fuzzy_parameters["habitat"]["x_axis"], dtype=np.float32)
    x_values = {"x_velocity": x_velocity, "x_depth": x_depth, "x_habitat": x_habitat}

    # create custom membership functions for velocity, depth, and habitat
    velocity_membership = pd.DataFrame(columns=['velocity_lo', 'velocity_md', 'velocity_hi'])
    velocity_membership["velocity_lo"] = fuzz.trimf(x_velocity,
                                                    fuzzy_parameters["velocity"]["lo"])  # update parameter input
    velocity_membership["velocity_md"] = fuzz.trimf(x_velocity,
                                                    fuzzy_parameters["velocity"]["md"])  # update parameter input
    velocity_membership["velocity_hi"] = fuzz.trimf(x_velocity,
                                                    fuzzy_parameters["velocity"]["hi"])  # update parameter input

    depth_membership = pd.DataFrame(columns=['depth_lo', 'depth_md', 'depth_hi'])
    depth_membership["depth_lo"] = fuzz.trimf(x_depth, fuzzy_parameters["depth"]["lo"])  # add parameter input
    depth_membership["depth_md"] = fuzz.trimf(x_depth, fuzzy_parameters["depth"]["md"])  # add parameter input
    depth_membership["depth_hi"] = fuzz.trimf(x_depth, fuzzy_parameters["depth"]["hi"])  # add parameter input

    habitat_membership = pd.DataFrame(columns=['habitat_lo', 'habitat_md', 'habitat_hi'])
    habitat_membership["habitat_lo"] = fuzz.trimf(x_habitat, fuzzy_parameters["habitat"]["lo"])  # add parameter input
    habitat_membership["habitat_md"] = fuzz.trimf(x_habitat, fuzzy_parameters["habitat"]["md"])  # add parameter input
    habitat_membership["habitat_hi"] = fuzz.trimf(x_habitat, fuzzy_parameters["habitat"]["hi"])  # add parameter input

    membership = {"velocity_membership": velocity_membership, "depth_membership": depth_membership,
                  "habitat_membership": habitat_membership}
    return(membership,x_values)

def fuzzylogic(fuzzy_parameters,velocity_value,depth_value, fish_class):

    (membership, x_values) = create_membership_functions(fuzzy_parameters)
    #Activation of our fuzzy membership functions at these values. Saved in the end in dictionaries
    velocity_level_lo = fuzz.interp_membership(x_values["x_velocity"], membership["velocity_membership"]["velocity_lo"], velocity_value)
    velocity_level_md = fuzz.interp_membership(x_values["x_velocity"], membership["velocity_membership"]["velocity_md"], velocity_value)
    velocity_level_hi = fuzz.interp_membership(x_values["x_velocity"], membership["velocity_membership"]["velocity_hi"], velocity_value)
    fuzzy_velocity_dict = {"lo": velocity_level_lo, "md": velocity_level_md, "hi": velocity_level_hi}

    depth_level_lo = fuzz.interp_membership(x_values["x_depth"], membership["depth_membership"]["depth_lo"], depth_value)
    depth_level_md = fuzz.interp_membership(x_values["x_depth"], membership["depth_membership"]["depth_md"], depth_value)
    depth_level_hi = fuzz.interp_membership(x_values["x_depth"], membership["depth_membership"]["depth_hi"], depth_value)
    fuzzy_depth_dict = {"lo": depth_level_lo, "md": depth_level_md,
                           "hi": depth_level_hi}

    (habitat_activation_lo, habitat_activation_md, habitat_activation_hi) = fish_class.apply_rules\
        (habitat_trimf=membership["habitat_membership"], fuzzy_velocity=fuzzy_velocity_dict, fuzzy_depth=fuzzy_depth_dict)

    habitat_activation_values = {"habitat_activation_lo": habitat_activation_lo, "habitat_activation_md": habitat_activation_md, "habitat_activation_hi": habitat_activation_hi}

    # Aggregate all three output membership functions together
    aggregated = np.fmax(habitat_activation_lo, habitat_activation_md, habitat_activation_hi)

    # Calculate defuzzified result
    habitat = fuzz.defuzz(x_values["x_habitat"], aggregated, 'centroid')
    habitat_activation = fuzz.interp_membership(x_values["x_habitat"], aggregated, habitat)  # for plot

    return (habitat, x_values, membership, aggregated, habitat_activation_values, habitat_activation) #returns habitat hsi value
#x_habitat, velocity_membership, depth_membership, habitat_membership



