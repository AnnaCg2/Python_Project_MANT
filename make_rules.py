from fun import *


class Fish:
    def __init__(self, *args, **kwargs):
        Fish.__init__(self)
        self.__family = ""
        self.__species = ""
        self.__common_name = ""


    def make_lo_belonging(self, velocity_level, depth_level, habitat_lo):
        active_rule1 = np.fmax(velocity_level, depth_level)
        habitat_activation_lo = np.fmin(active_rule1, habitat_lo)
        return(habitat_activation_lo)

    def make_md_belonging(self, velocity_level, depth_level, habitat_md):
        habitat_activation_md = np.fmin(depth_level, habitat_md)
        return(habitat_activation_md)

    def make_hi_belonging(self, velocity_level, depth_level, habitat_hi):
        active_rule3 = np.fmax(velocity_level, depth_level)
        habitat_activation_hi = np.fmin(active_rule3, habitat_hi)
        return(habitat_activation_hi)

    def __call__(self, *args, **kwargs):
        # example prints class structure information to console
        print("Class Info: <type> = NewClass (%s)" % os.path.dirname(__file__))
        print(dir(self))

class Fry(Fish):
    def __init__(self, *args, **kwargs):

    def make_lo_belonging(self, velocity_level, depth_level, habitat_lo):
        active_rule1 = np.fmax(velocity_level, depth_level)
        habitat_activation_lo = np.fmin(active_rule1, habitat_lo)
        return (habitat_activation_lo)

    def make_md_belonging(self, velocity_level, depth_level, habitat_md):
        habitat_activation_md = np.fmin(depth_level, habitat_md)
        return (habitat_activation_md)

    def make_hi_belonging(self, velocity_level, depth_level, habitat_hi):
        active_rule3 = np.fmax(velocity_level, depth_level)
        habitat_activation_hi = np.fmin(active_rule3, habitat_hi)
        return (habitat_activation_hi)

    def __call__(self, *args, **kwargs):
        # example prints class structure information to console
        print("Class Info: <type> = NewClass (%s)" % os.path.dirname(__file__))
        print(dir(self))

class Juvenile(Fish):
    def __init__(self, *args, **kwargs):

    def make_lo_belonging(self, velocity_level, depth_level, habitat_lo):
        active_rule1 = np.fmax(velocity_level, depth_level)
        habitat_activation_lo = np.fmin(active_rule1, habitat_lo)
        return (habitat_activation_lo)

    def make_md_belonging(self, depth_level, habitat_md):
        habitat_activation_md = np.fmin(depth_level, habitat_md)
        return (habitat_activation_md)

    def make_hi_belonging(self, velocity_level, depth_level, habitat_hi):
        active_rule3 = np.fmax(velocity_level, depth_level)
        habitat_activation_hi = np.fmin(active_rule3, habitat_hi)
        return (habitat_activation_hi)

    def __call__(self, *args, **kwargs):
        # example prints class structure information to console
        print("Class Info: <type> = NewClass (%s)" % os.path.dirname(__file__))
        print(dir(self))

class Adult(Fish):
    def __init__(self, *args, **kwargs):

    def make_lo_belonging(self, velocity_level, depth_level, habitat_lo):
        active_rule1 = np.fmax(velocity_level, depth_level)
        habitat_activation_lo = np.fmin(active_rule1, habitat_lo)
        return (habitat_activation_lo)

    def make_md_belonging(self, velocity_level, depth_level, habitat_md):
        habitat_activation_md = np.fmin(depth_level, habitat_md)
        return (habitat_activation_md)

    def make_hi_belonging(self, velocity_level, depth_level, habitat_hi):
        active_rule3 = np.fmax(velocity_level, depth_level)
        habitat_activation_hi = np.fmin(active_rule3, habitat_hi)
        return (habitat_activation_hi)

class Spawning(Fish):
    def __init__(self, *args, **kwargs):

    def make_lo_belonging(self, velocity_level, depth_level, habitat_lo):
        active_rule1 = np.fmax(velocity_level, depth_level)
        habitat_activation_lo = np.fmin(active_rule1, habitat_lo)
        return (habitat_activation_lo)

    def make_md_belonging(self, velocity_level, depth_level, habitat_md):
        habitat_activation_md = np.fmin(depth_level, habitat_md)
        return (habitat_activation_md)

    def make_hi_belonging(self, velocity_level, depth_level, habitat_hi):
        active_rule3 = np.fmax(velocity_level, depth_level)
        habitat_activation_hi = np.fmin(active_rule3, habitat_hi)
        return (habitat_activation_hi)

