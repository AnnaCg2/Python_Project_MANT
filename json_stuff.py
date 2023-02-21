import csv
import json
from fun import *



#written dictionary method
# data_for_json = ["velocity", {"lo": [0,0,5], "med": [0,5,10], "hi": [5,10,10]}, "depth", {"lo": [0,0,5], "med": [0,5,10], "hi": [5,10,10]}, "HSI", {"lo": [0,0,5], "med": [0,5,10], "hi": [5,10,10]}]
#
# with open("shape_parameters2.json", "w") as write_file:
#     json.dump(data_for_json, write_file, indent=4)
#

#
# def line_to_dict(split_line):
#     line_dict = {}
#     for part in split_line:
#         key, value = part.split(":", maxsplit=1)
#         line_dict[key] = value
#
#     return line_dict
#
# def convert():
#     f=open("")


with open(os.path.abspath("") + "\\habitat\\shape_params.txt", 'r') as input_file:
    file_info = input_file.read()

    shape_data = json.loads(file_info)

with open('shape_params3.json', 'w') as output_file:
    json.dump(shape_data, output_file, indent=4)

input_file.close()
output_file.close()

please_work = read_json(os.path.abspath("") + "\\shape_params3.json")
print(please_work["velocity"]["lo"])


