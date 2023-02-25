from fun import *


class Fish:
    def __init__(self, common_name, life_stage):
        self.common_name = common_name
        self.life_stage = life_stage
    #
    # def check_life_stage(self, func):
    #     def wrapper(*args, **kwargs):
    #         if
    #
    #         except ValueError:
    #             print("ERROR: Life stage must be set as fry, juvenile, adult, or spawning")
    #     return wrapper

    def make_fuzzy_rules(self, fuzzy_velocity, fuzzy_depth):
        """
        Defines and applies rules to create fuzzy HSI membership values
        :param life_stage: STR with life_stage (defined by user)
        :param habitat_trimf: pd data frame with results of skfuzz triangular membership function generator
                        column names: "habitat_lo", "habitat_md", "habitat_hi"
        :param fuzzy_velocity: dictionary with low, medium, and high fuzzy velocity membership
                            dictionary keys: "lo", "md", "hi"
        :param fuzzy_depth: dictionary with low, medium, and high fuzzy depth membership
                            dictionary keys: "lo", "md", "hi"
        :return: habitat_activation_lo: pandas series with fuzzy membership values for lo habitat
                 habitat_activation_md: pandas series with fuzzy membership values for md habitat
                 habitat_activation_hi: pandas series with fuzzy membership values for hi habitat

        """
        if self.life_stage == "fry":
            active_rule1 = np.fmin(fuzzy_velocity["hi"], fuzzy_depth["hi"])
            active_rule2 = np.fmax(fuzzy_velocity["hi"], fuzzy_depth["md"])
            active_rule3 = np.fmin(fuzzy_velocity["md"], fuzzy_depth["lo"])

        if self.life_stage == "juvenile":
            active_rule1 = np.fmax(fuzzy_velocity["hi"], fuzzy_depth["lo"])
            active_rule2 = np.fmax(fuzzy_velocity["md"], fuzzy_depth["md"])
            active_rule3 = np.fmax(fuzzy_velocity["md"], fuzzy_depth["md"])


        if self.life_stage == "adult":
            active_rule1 = np.fmin(fuzzy_velocity["hi"], fuzzy_depth["hi"])
            active_rule2 = np.fmax(fuzzy_velocity["md"], fuzzy_depth["md"])
            active_rule3 = np.fmax(fuzzy_velocity["md"], fuzzy_depth["hi"])


        if self.life_stage == "spawning":
            active_rule1 = np.fmax(fuzzy_velocity["lo"], fuzzy_depth["hi"])
            active_rule2 = np.fmax(fuzzy_velocity["md"], fuzzy_depth["md"])
            active_rule3 = np.fmax(fuzzy_velocity["md"], fuzzy_depth["lo"])

        return (active_rule1, active_rule2, active_rule3)

    def apply_rules(self, habitat_trimf, fuzzy_velocity, fuzzy_depth):

        (active_rule1, active_rule2, active_rule3) = self.make_fuzzy_rules(fuzzy_velocity, fuzzy_depth)
        if self.life_stage == "fry":
            habitat_activation_lo = np.fmax(active_rule1, habitat_trimf["habitat_lo"])
            habitat_activation_md = np.fmax(fuzzy_depth["md"], habitat_trimf["habitat_md"])
            habitat_activation_hi = np.fmax(active_rule3, habitat_trimf["habitat_hi"])

        if self.life_stage == "juvenile":
            habitat_activation_lo = np.fmin(active_rule1, habitat_trimf["habitat_lo"])
            habitat_activation_md = np.fmax(fuzzy_depth["md"], habitat_trimf["habitat_md"])
            habitat_activation_hi = np.fmin(active_rule3, habitat_trimf["habitat_hi"])

        if self.life_stage == "adult":
            habitat_activation_lo = np.fmax(active_rule1, habitat_trimf["habitat_lo"])
            habitat_activation_md = np.fmax(active_rule2, habitat_trimf["habitat_md"])
            habitat_activation_hi = np.fmin(active_rule3, habitat_trimf["habitat_hi"])

        if self.life_stage == "spawning":
            habitat_activation_lo = np.fmin(active_rule1, habitat_trimf["habitat_lo"])
            habitat_activation_md = np.fmax(active_rule2, habitat_trimf["habitat_md"])
            habitat_activation_hi = np.fmin(active_rule3, habitat_trimf["habitat_hi"])

        return (habitat_activation_lo, habitat_activation_md, habitat_activation_hi)

    def __call__(self, *args, **kwargs):
        # example prints class structure information to console
        print("Class Info: <type> = NewClass (%s)" % os.path.dirname(__file__))
        print(dir(self))

