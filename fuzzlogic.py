from make_rules import *


# Genera

#create json file
def get_fuzzy_params(file_path):

    # Generate fuzzy membership functions
    # add import capabilities from json
    txt_to_json(file_path, "fuzzy_params.json")
    fuzzy_parameters = read_json(os.path.abspath("") + "\\fuzzy_params.json")

    return(fuzzy_parameters)

def fuzzylogic(fuzzy_parameters,velocity_value,depth_value, fish_class):

    #must save x-axis values as a np array before passing into fuzz.trimf
    x_velocity = np.asarray(fuzzy_parameters["velocity"]["x_axis"], dtype=np.float32)
    x_depth = np.asarray(fuzzy_parameters["depth"]["x_axis"], dtype=np.float32)
    x_habitat = np.asarray(fuzzy_parameters["habitat"]["x_axis"], dtype=np.float32)

    #create custom membership functions for velocity, depth, and habitat
    velocity_membership = pd.DataFrame(columns=['velocity_lo', 'velocity_md', 'velocity_hi'])
    velocity_membership["velocity_lo"] = fuzz.trimf(x_velocity, fuzzy_parameters["velocity"]["lo"]) #update parameter input
    velocity_membership["velocity_md"] = fuzz.trimf(x_velocity, fuzzy_parameters["velocity"]["md"]) #update parameter input
    velocity_membership["velocity_hi"] = fuzz.trimf(x_velocity, fuzzy_parameters["velocity"]["hi"]) #update parameter input

    depth_membership = pd.DataFrame(columns=['depth_lo', 'depth_md', 'depth_hi'])
    depth_membership["depth_lo"] = fuzz.trimf(x_depth, fuzzy_parameters["depth"]["lo"]) #add parameter input
    depth_membership["depth_md"] = fuzz.trimf(x_depth, fuzzy_parameters["depth"]["md"]) #add parameter input
    depth_membership["depth_hi"] = fuzz.trimf(x_depth, fuzzy_parameters["depth"]["hi"]) #add parameter input

    habitat_membership = pd.DataFrame(columns = ['habitat_lo','habitat_md','habitat_hi'])
    habitat_membership["habitat_lo"] = fuzz.trimf(x_habitat, fuzzy_parameters["habitat"]["lo"]) #add parameter input
    habitat_membership["habitat_md"] = fuzz.trimf(x_habitat, fuzzy_parameters["habitat"]["md"]) #add parameter input
    habitat_membership["habitat_hi"] = fuzz.trimf(x_habitat, fuzzy_parameters["habitat"]["hi"]) #add parameter input



    #Activation of our fuzzy membership functions at these values. Saved in the end in dictionaries
    # The exact values velocity_value and 9.8 do not exist on our universes...
    # This is what fuzz.interp_membership exists for!
    velocity_level_lo = fuzz.interp_membership(x_velocity, velocity_membership["velocity_lo"], velocity_value)
    velocity_level_md = fuzz.interp_membership(x_velocity, velocity_membership["velocity_md"], velocity_value)
    velocity_level_hi = fuzz.interp_membership(x_velocity, velocity_membership["velocity_hi"], velocity_value)
    fuzzy_velocity_dict = {"lo": velocity_level_lo, "md": velocity_level_md, "hi": velocity_level_hi}

    depth_level_lo = fuzz.interp_membership(x_depth, depth_membership["depth_lo"], depth_value)
    depth_level_md = fuzz.interp_membership(x_depth, depth_membership["depth_md"], depth_value)
    depth_level_hi = fuzz.interp_membership(x_depth, depth_membership["depth_hi"], depth_value)
    fuzzy_depth_dict = {"lo": depth_level_lo, "md": depth_level_md,
                           "hi": depth_level_hi}

    (habitat_activation_lo, habitat_activation_md, habitat_activation_hi) = fish_class.apply_rules\
        (habitat_trimf=habitat_membership, fuzzy_velocity=fuzzy_velocity_dict, fuzzy_depth=fuzzy_depth_dict)

    # Aggregate all three output membership functions together
    aggregated = np.fmax(habitat_activation_lo, habitat_activation_md, habitat_activation_hi)

    # Calculate defuzzified result
    habitat = fuzz.defuzz(x_habitat, aggregated, 'centroid')
    habitat_activation = fuzz.interp_membership(x_habitat, aggregated, habitat)  # for plot


    return habitat #returns habitat hsi value

# file_path = os.path.abspath("") + "\\habitat\\shape_params.txt"
# fuzzy_parameters = get_fuzzy_params(os.path.abspath("") + "\\habitat\\shape_params.txt")
# trout = Fish("Rainbow Trout","juvenile")
# velocity_array = [[0, 0, 5],[0, 5, 10],[5, 10, 10]]
# test = fuzzylogic(fuzzy_parameters,9.8,6.5, trout)


# def plot_fuzzy_logic(fuzzy_plot,velocity_membership, depth_membership, habitat_membership, habitat):
#     """
#     Plots an example of the fuzzified curves for depth, velocity and HSI
#     :param fuzzy_plot: boolean value enabling or disabling the plotting function
#     """
#     # Visualize these universes and membership functions
#     fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
#
#     ax0.plot(velocity, velocity_membership["velocity_lo"], 'b', linewidth=1.5, label='low')
#     ax0.plot(velocity, velocity_membership["velocity_md"], 'g', linewidth=1.5, label='medium')
#     ax0.plot(velocity, velocity_membership["velocity_hi"], 'r', linewidth=1.5, label='high')
#     ax0.set_title('Flow Velocity')
#     ax0.legend()
#
#     ax1.plot(depth, depth_memberhsip["depth_lo"], 'b', linewidth=1.5, label='low')
#     ax1.plot(depth, depth_membership["depth_md"], 'g', linewidth=1.5, label='medium')
#     ax1.plot(depth, depth_membership["depth_hi"], 'r', linewidth=1.5, label='high')
#     ax1.set_title('depth velocity')
#     ax1.legend()
#
#     ax2.plot(x_habitat, habitat_membership["habitat_lo"], 'b', linewidth=1.5, label='Low')
#     ax2.plot(x_habitat, habitat_membership["habitat_md"], 'g', linewidth=1.5, label='Medium')
#     ax2.plot(x_habitat, habitat_membership["habitat_hi"], 'r', linewidth=1.5, label='High')
#     ax2.set_title('habitat amount')
#     ax2.legend()
#
#     # Turn off top/right axes
#     for ax in (ax0, ax1, ax2):
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.get_xaxis().tick_bottom()
#         ax.get_yaxis().tick_left()
#
#     plt.tight_layout()
#
#     #Visualize this
#     fig, ax0 = plt.subplots(figsize=(8, 3))
#
#     ax0.fill_between(x_habitat, habitat0, habitat_activation_lo, facecolor='b', alpha=0.7)
#     ax0.plot(x_habitat, habitat_lo, 'b', linewidth=0.5, linestyle='--', )
#     ax0.fill_between(x_habitat, habitat0, habitat_activation_md, facecolor='g', alpha=0.7)
#     ax0.plot(x_habitat, habitat_md, 'g', linewidth=0.5, linestyle='--')
#     ax0.fill_between(x_habitat, habitat0, habitat_activation_hi, facecolor='r', alpha=0.7)
#     ax0.plot(x_habitat, habitat_hi, 'r', linewidth=0.5, linestyle='--')
#     ax0.set_title('Output membership activity')
#
#     # Turn off top/right axes
#     for ax in (ax0,):
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.get_xaxis().tick_bottom()
#         ax.get_yaxis().tick_left()
#
#     plt.tight_layout()
#
#     # Visualize this
#     fig, ax0 = plt.subplots(figsize=(8, 3))
#
#     ax0.plot(x_habitat, habitat_lo, 'b', linewidth=0.5, linestyle='--', )
#     ax0.plot(x_habitat, habitat_md, 'g', linewidth=0.5, linestyle='--')
#     ax0.plot(x_habitat, habitat_hi, 'r', linewidth=0.5, linestyle='--')
#     ax0.fill_between(x_habitat, habitat0, aggregated, facecolor='Orange', alpha=0.7)
#     ax0.plot([habitat, habitat], [0, habitat_activation], 'k', linewidth=1.5, alpha=0.9)
#     ax0.set_title('Aggregated membership and result (line)')
#
#     # Turn off top/right axes
#     for ax in (ax0,):
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.get_xaxis().tick_bottom()
#         ax.get_yaxis().tick_left()
#
#     plt.tight_layout()
#
#     plt.show()
#     print(habitat)
#     pass
