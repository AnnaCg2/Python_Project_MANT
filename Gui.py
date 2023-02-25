import tkinter
import tkinter as tk
from tkinter import *
from fuzzlogic import *
from create_hsi_rasters import *
from raster_hsi import *
from calculate_habitat_area import calculate_habitat_area

from PIL import ImageTk, Image
import numpy as np


class HsiApp(tk.Frame):
    def __init__(self,master=None):

        tk.Frame.__init__(self,master)
        self.grid()

        bg="light green"
        self.master.configure(bg=bg)

        Welcome_label = Label(master, text="The buttons below display HSI values for the selected lifestage:\n "
                                          "(note the values are displayed the Python IDE")
        Welcome_label.grid(column=1,row=0, columnspan=2)

        spawning_button = tk.Button(master, text = "Spawning-HSI", command=lambda: [get_hsi_curve((os.path.abspath("") + "\\habitat\\trout.json"), life_stage="spawning", parameters=["velocity", "depth"])])
        spawning_button.grid(column=1, row=1)

        fry_button = tk.Button(master, text = "Fry-HSI", command=lambda: get_hsi_curve((os.path.abspath("") + "\\habitat\\trout.json"), life_stage="fry", parameters=["velocity", "depth"]))
        fry_button.grid(column=1, row=2)

        juvenile_button = tk.Button(master,text = "Juvenile-HSI", command=lambda: get_hsi_curve((os.path.abspath("") + "\\habitat\\trout.json"), life_stage="juvenile", parameters=["velocity", "depth"]))
        juvenile_button.grid(column=2, row=1)

        adult_button = tk.Button(master, text = "Adult-HSI", command=lambda: get_hsi_curve((os.path.abspath("") + "\\habitat\\trout.json"), life_stage="adult", parameters=["velocity", "depth"]))
        adult_button.grid(column=2, row=2)

        img_size = (500, 500)
        #
        canvas = Canvas(master, width=500, height=500)
        canvas.grid(column=1, row=3, columnspan=2)
        canvas.configure(bg=bg)
        Createraster_label = Label(master, text="The buttons below create and display a .tiff file based on \n"
                                                "HSI method for the selected lifestage:")
        Createraster_label.grid(column=1, row=4, columnspan=2)

        map_button1 = tk.Button(master, text="Fry-CreateRaster", command=lambda:[Raster_Creation(life_stage="fry"), open_smth(canvas)])
        map_button1.grid(column=1, row=5)

        map_button2 = tk.Button(master, text="Spawning-CreateRaster", command=lambda:[Raster_Creation(life_stage="spawning"), open_smth(canvas)])
        map_button2.grid(column=1, row=6)
        #
        map_button3 = tk.Button(master, text="Juvenile-CreateRaster", command=lambda:[Raster_Creation(life_stage="juvenile"), open_smth(canvas)])
        map_button3.grid(column=2, row=5)
        #
        map_button4 = tk.Button(master, text="Adult-CreateRaster", command=lambda: [Raster_Creation(life_stage="adult"), open_smth(canvas)])
        map_button4.grid(column=2, row=6)

        Createraster_label = Label(master, text="The buttons below create and display a .tiff file based on \n"
                                                "Fuzzy method for the selected lifestage:")
        Createraster_label.grid(column=1, row=7, columnspan=2)

        map_button5 = tk.Button(master, text="Fry-CreateRaster", command=lambda:[Raster_Creation_Fuzzy(life_stage="fry"), open_smth(canvas)])
        map_button5.grid(column=1, row=8)

        map_button6 = tk.Button(master, text="Spawning-CreateRaster", command=lambda:[Raster_Creation_Fuzzy(life_stage="spawning"), open_smth(canvas)])
        map_button6.grid(column=1, row=9)
        #
        map_button7 = tk.Button(master, text="Juvenile-CreateRaster", command=lambda:[Raster_Creation_Fuzzy(life_stage="juvenile"), open_smth(canvas)])
        map_button7.grid(column=2, row=8)
        #
        map_button8 = tk.Button(master, text="Adult-CreateRaster", command=lambda: [Raster_Creation_Fuzzy(life_stage="adult"), open_smth(canvas)])
        map_button8.grid(column=2, row=9)

        #Arealabel = Label(master, text=print("The total habitat area is {0} {1}.".format(str(sum(poly_size)), area_unit)))
        #Arealabel.grid(column=1, row=10)

        # map_widgetlabel = Label(master, text = "The map below allows for visual comparison of the \n"
        #                                        ".Tiff created with an overview map")
        # map_widgetlabel.grid(column=3,row=0, columnspan=2,rowspan=2)
        #
        # map_widget=tkintermapview.TkinterMapView(master,width=500, height=500, corner_radius=0)
        # map_widget.set_position(48.860381, 2.338594)
        # map_widget.grid(column=3,row=3)

        def open_smth(canvas):
            '''
            :param canvas: predefined area that recieves the image that is generated from the chsi.tif
            :return:
            '''
            file = os.path.abspath("") + "\\habitat\\chsi.tif"
            global my_image
            img = Image.open(file).resize(img_size, resample=Image.NEAREST)
            my_image = ImageTk.PhotoImage(Image.fromarray((np.array(img) * 200).astype(np.uint8)))
            canvas.create_image(0, 0, image=my_image, anchor=NW)
            pass

        def Raster_Creation(life_stage, method="hsi"):
            '''
            :param life_stage: lifestage input to generate corresponding chsi.tif. selected via the different buttons.
            :param method: selected method for chsi.tif. Can select from hsi or fuzzy_logic
            :return:
            '''
            # define global variables for the main() function
            parameters = ["velocity", "depth"]
            trout = Fish("Rainbow Trout", life_stage)
            fuzzy_params = get_fuzzy_params(os.path.abspath("") + "\\habitat\\fuzzy_params.txt")
            # paths
            fish_file = os.path.abspath("") + "\\habitat\\trout.json"
            tifs = {"velocity": os.path.abspath("") + "\\basement\\flow_velocity.tif",
                    "depth": os.path.abspath("") + "\\basement\\water_depth.tif"}
            hsi_output_dir = os.path.abspath("") + "\\habitat\\"

            main(method,fish_file, tifs, hsi_output_dir,fuzzy_params,trout,parameters,life_stage)

        def Raster_Creation_Fuzzy(life_stage, method="fuzzy_logic"):
            '''
            :param life_stage: lifestage input to generate corresponding chsi.tif. selected via the different buttons.
            :param method: selected method for chsi.tif.  Can select from hsi or fuzzy_logic
            :return:
            '''
            # define global variables for the main() function
            parameters = ["velocity", "depth"]
            trout = Fish("Rainbow Trout", life_stage)
            fuzzy_params = get_fuzzy_params(os.path.abspath("") + "\\habitat\\fuzzy_params.txt")
            # paths
            fish_file = os.path.abspath("") + "\\habitat\\trout.json"
            tifs = {"velocity": os.path.abspath("") + "\\basement\\flow_velocity.tif",
                    "depth": os.path.abspath("") + "\\basement\\water_depth.tif"}
            hsi_output_dir = os.path.abspath("") + "\\habitat\\"

            main(method,fish_file, tifs, hsi_output_dir,fuzzy_params,trout,parameters,life_stage)

        def calculate_habitat_area(layer, epsg):
            """
            Calculate the usable habitat area
            :param layer: osgeo.ogr.Layer
            :param epsg: int (Authority code drives area units)
            :return: None
            """
            # retrieve units
            srs = geo.osr.SpatialReference()
            srs.ImportFromEPSG(epsg)
            area_unit = "square %s" % str(srs.GetLinearUnitsName())

            # add area field
            layer.CreateField(geo.ogr.FieldDefn("area", geo.ogr.OFTReal))

            # create list to store polygon sizes
            poly_size = []

            # iterate through geometries (polygon features) of the layer
            for feature in layer:
                # retrieve polygon geometry
                polygon = feature.GetGeometryRef()
                # add polygon size if field "value" is one (determined by chsi_treshold)
                if int(feature.GetField(0)):
                    poly_size.append(polygon.GetArea())
                # write area to area field
                feature.SetField("area", polygon.GetArea())
                # add the feature modifications to the layer
                layer.SetFeature(feature)

            # calculate and print habitat area
            print("The total habitat area is {0} {1}.".format(str(sum(poly_size)), area_unit))
            return (poly_size, area_unit)

if __name__ == "__main__":
    HsiApp().mainloop()