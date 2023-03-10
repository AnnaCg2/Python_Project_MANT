try:
    import os
    import logging
    import random
    import shutil
    import string
except ImportError:
    print("ERROR: Cannot import basic Python libraries.")

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("ERROR: Cannot import SciPy libraries.")

try:
    import json
except ImportError:
    print("ERROR: Cannot import json package.")

try:
    import skfuzzy as fuzz

except ImportError:
    print("ERROR: Cannot import skfuzzy package")

try:
    import matplotlib.pyplot as plt

except ImportError:
    print("ERROR: Cannot import matplotlib package")

try:
    from flusstools import geotools as geo
except ImportError:
    print("ERROR: Cannot import geotools.")

cache_folder = os.path.abspath("") + "\\__cache__\\"
par_dict = {"velocity": "u",
            "depth": "h",
            "grain_size": "d"}
nan_value = 0
