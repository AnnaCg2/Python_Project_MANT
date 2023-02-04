import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


# Genera
def plotfuzzylogic()
    # # Visualize these universes and membership functions
    # fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
    #
    # ax0.plot(velocity, velocity_lo, 'b', linewidth=1.5, label='low')
    # ax0.plot(velocity, velocity_md, 'g', linewidth=1.5, label='medium')
    # ax0.plot(velocity, velocity_hi, 'r', linewidth=1.5, label='high')
    # ax0.set_title('Flow Velocity')
    # ax0.legend()
    #
    # ax1.plot(depth, depth_lo, 'b', linewidth=1.5, label='low')
    # ax1.plot(depth, depth_md, 'g', linewidth=1.5, label='medium')
    # ax1.plot(depth, depth_hi, 'r', linewidth=1.5, label='high')
    # ax1.set_title('depth velocity')
    # ax1.legend()
    #
    # ax2.plot(x_habitat, habitat_lo, 'b', linewidth=1.5, label='Low')
    # ax2.plot(x_habitat, habitat_md, 'g', linewidth=1.5, label='Medium')
    # ax2.plot(x_habitat, habitat_hi, 'r', linewidth=1.5, label='High')
    # ax2.set_title('habitat amount')
    # ax2.legend()
    #
    # # Turn off top/right axes
    # for ax in (ax0, ax1, ax2):
    #     ax.spines['top'].set_visible(False)
    #     ax.spines['right'].set_visible(False)
    #     ax.get_xaxis().tick_bottom()
    #     ax.get_yaxis().tick_left()
    #
    # plt.tight_layout()

    # Visualize this
    # fig, ax0 = plt.subplots(figsize=(8, 3))
    #
    # ax0.fill_between(x_habitat, habitat0, habitat_activation_lo, facecolor='b', alpha=0.7)
    # ax0.plot(x_habitat, habitat_lo, 'b', linewidth=0.5, linestyle='--', )
    # ax0.fill_between(x_habitat, habitat0, habitat_activation_md, facecolor='g', alpha=0.7)
    # ax0.plot(x_habitat, habitat_md, 'g', linewidth=0.5, linestyle='--')
    # ax0.fill_between(x_habitat, habitat0, habitat_activation_hi, facecolor='r', alpha=0.7)
    # ax0.plot(x_habitat, habitat_hi, 'r', linewidth=0.5, linestyle='--')
    # ax0.set_title('Output membership activity')
    #
    # # Turn off top/right axes
    # for ax in (ax0,):
    #     ax.spines['top'].set_visible(False)
    #     ax.spines['right'].set_visible(False)
    #     ax.get_xaxis().tick_bottom()
    #     ax.get_yaxis().tick_left()
    #
    # plt.tight_layout()

    # # Visualize this
    # fig, ax0 = plt.subplots(figsize=(8, 3))
    #
    # ax0.plot(x_habitat, habitat_lo, 'b', linewidth=0.5, linestyle='--', )
    # ax0.plot(x_habitat, habitat_md, 'g', linewidth=0.5, linestyle='--')
    # ax0.plot(x_habitat, habitat_hi, 'r', linewidth=0.5, linestyle='--')
    # ax0.fill_between(x_habitat, habitat0, aggregated, facecolor='Orange', alpha=0.7)
    # ax0.plot([habitat, habitat], [0, habitat_activation], 'k', linewidth=1.5, alpha=0.9)
    # ax0.set_title('Aggregated membership and result (line)')
    #
    # # Turn off top/right axes
    # for ax in (ax0,):
    #     ax.spines['top'].set_visible(False)
    #     ax.spines['right'].set_visible(False)
    #     ax.get_xaxis().tick_bottom()
    #     ax.get_yaxis().tick_left()
    #
    # plt.tight_layout()
    #
    # plt.show()
    # print(habitat)
    pass
def fuzzylogic(parameters,velocity_value,depth_value):

    # a range of parameters (needs updating with parameter input)
    velocity = np.arange(0, 11, 1) #add parameter input
    depth = np.arange(0, 11, 1) #add parameter input
    x_habitat = np.arange(0, 1.05, .05) #add parameter input


    # Generate fuzzy membership functions

    #add import capabilities from json

    velocity_lo = fuzz.trimf(velocity, parameters[0]) #update parameter input
    velocity_md = fuzz.trimf(velocity, parameters[1]) #update parameter input
    velocity_hi = fuzz.trimf(velocity, parameters[2]) #update parameter input

    depth_lo = fuzz.trimf(depth, [0, 0, 5]) #add parameter input
    depth_md = fuzz.trimf(depth, [0, 5, 10]) #add parameter input
    depth_hi = fuzz.trimf(depth, [5, 10, 10]) #add parameter input

    habitat_lo = fuzz.trimf(x_habitat, [0, 0, .5]) #add parameter input
    habitat_md = fuzz.trimf(x_habitat, [.3, .5, .8]) #add parameter input
    habitat_hi = fuzz.trimf(x_habitat, [.7, 1, 1]) #add parameter input




    # We need the activation of our fuzzy membership functions at these values.
    # The exact values velocity_value and 9.8 do not exist on our universes...
    # This is what fuzz.interp_membership exists for!
    velocity_level_lo = fuzz.interp_membership(velocity, velocity_lo, velocity_value)
    velocity_level_md = fuzz.interp_membership(velocity, velocity_md, velocity_value)
    velocity_level_hi = fuzz.interp_membership(velocity, velocity_hi, velocity_value)

    depth_level_lo = fuzz.interp_membership(depth, depth_lo, depth_value)
    depth_level_md = fuzz.interp_membership(depth, depth_md, depth_value)
    depth_level_hi = fuzz.interp_membership(depth, depth_hi, depth_value)

    # Now we take our rules and apply them. Rule 1 concerns bad food OR depthice.
    # The OR operator means we take the maximum of these two.

    # rules ( need updating with class)
    active_rule1 = np.fmax(velocity_level_lo, depth_level_lo)

    # Now we apply this by clipping the top off the corresponding output
    # membership function with `np.fmin`
    habitat_activation_lo = np.fmin(active_rule1, habitat_lo)  # removed entirely to 0

    # For rule 2 we connect acceptable depthice to medium habitatping
    habitat_activation_md = np.fmin(depth_level_md, habitat_md)

    # For rule 3 we connect high depthice OR high food with high habitatping
    active_rule3 = np.fmax(velocity_level_hi, depth_level_hi)
    habitat_activation_hi = np.fmin(active_rule3, habitat_hi)
    habitat0 = np.zeros_like(x_habitat)


    # Aggregate all three output membership functions together
    aggregated = np.fmax(habitat_activation_lo,
                         np.fmax(habitat_activation_md, habitat_activation_hi))

    # Calculate defuzzified result
    habitat = fuzz.defuzz(x_habitat, aggregated, 'centroid')
    habitat_activation = fuzz.interp_membership(x_habitat, aggregated, habitat)  # for plot


    return habitat #returns habitat hsi value