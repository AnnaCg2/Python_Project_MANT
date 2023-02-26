import tkinter
import tkinter as tk
from tkinter import *
from create_hsi_rasters import *
from raster_hsi import *
from PIL import ImageTk, Image
import numpy as np


class HsiApp(tk.Frame):
    def __init__(self,master=None):

        tk.Frame.__init__(self,master)
        self.grid()

        bg="light blue"
        self.master.configure(bg=bg)

        Welcome_label = Label(master, text="The buttons below display HSI values for the selected lifestage:\n "
                                          "(note the values are displayed in the Python IDE")
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

        canvas = Canvas(master, width=500, height=500)
        canvas.grid(column=1, row=3, columnspan=2)
        canvas.configure(bg=bg)
        Createraster_label = Label(master, text="The buttons below create and display a .tiff file based on \n"
                                                "HSI method for the selected lifestage:")
        Createraster_label.grid(column=1, row=4, columnspan=2)

        map_button1 = tk.Button(master, text="Fry-CreateRaster", command=lambda: (open_smth(life_stage="fry", method="hsi", canvas=canvas)))
        map_button1.grid(column=1, row=5)

        map_button2 = tk.Button(master, text="Spawning-CreateRaster", command=lambda:(open_smth(life_stage="spawning", method="hsi", canvas=canvas)))
        map_button2.grid(column=1, row=6)
        #
        map_button3 = tk.Button(master, text="Juvenile-CreateRaster", command=lambda:(open_smth(life_stage="juvenile", method="hsi", canvas=canvas)))
        map_button3.grid(column=2, row=5)
        #
        map_button4 = tk.Button(master, text="Adult-CreateRaster", command=lambda: (open_smth(life_stage="adult", method="hsi", canvas=canvas)))
        map_button4.grid(column=2, row=6)

        Createraster_label = Label(master, text="The buttons below create and display a .tiff file based on \n"
                                                "Fuzzy method for the selected lifestage:" \n)
        Createraster_label.grid(column=1, row=7, columnspan=2)

        map_button5 = tk.Button(master, text="Fry-CreateRaster", command=lambda: (open_smth(life_stage="fry", method="fuzzy_logic", canvas=canvas)))
        map_button5.grid(column=1, row=8)

        map_button6 = tk.Button(master, text="Spawning-CreateRaster", command=lambda: (open_smth(life_stage="spawning", method="fuzzy_logic", canvas=canvas)))
        map_button6.grid(column=1, row=9)
        #
        map_button7 = tk.Button(master, text="Juvenile-CreateRaster", command=lambda: (open_smth(life_stage="juvenile", method="fuzzy_logic", canvas=canvas)))
        map_button7.grid(column=2, row=8)
        #
        map_button8 = tk.Button(master, text="Adult-CreateRaster", command=lambda: (open_smth(life_stage="adult", method="fuzzy_logic", canvas=canvas)))
        map_button8.grid(column=2, row=9)

        # map_widgetlabel = Label(master, text = "The map below allows for visual comparison of the \n"
        #                                        ".Tiff created with an overview map")
        # map_widgetlabel.grid(column=3,row=0, columnspan=2,rowspan=2)
        #
        # map_widget=tkintermapview.TkinterMapView(master,width=500, height=500, corner_radius=0)
        # map_widget.set_position(48.860381, 2.338594)
        # map_widget.grid(column=3,row=3)

        def open_smth(life_stage, method, canvas):
            '''
            :param canvas: predefined area that recieves the image that is generated from the chsi.tif
            :return:
            '''

            Raster_Creation(life_stage, method)

            file = os.path.abspath("") + "\\habitat\\chsi.tif"
            global my_image
            img = Image.open(file).resize(img_size, resample=Image.NEAREST)
            my_image = ImageTk.PhotoImage(Image.fromarray((np.array(img) * 200).astype(np.uint8)))
            canvas.create_image(0, 0, image=my_image, anchor=NW)

            pass

        def Raster_Creation(life_stage, method):
            '''
            :param life_stage: lifestage input to generate corresponding chsi.tif. selected via the different buttons.
            :param method: selected method for chsi.tif.  Can select from hsi or fuzzy_logic
            :return:
            '''
            # define global variables for the main() function
            parameters = ["velocity", "depth"]
            life_stage = life_stage
            trout = Fish("Rainbow Trout", life_stage)
            fuzzy_params = get_fuzzy_params(os.path.abspath("") + "\\habitat\\fuzzy_params.txt")

            # paths
            fish_file = os.path.abspath("") + "\\habitat\\trout.json"
            tifs = {"velocity": os.path.abspath("") + "\\basement\\flow_velocity.tif",
                    "depth": os.path.abspath("") + "\\basement\\water_depth.tif"}
            hsi_output_dir = os.path.abspath("") + "\\habitat\\"

            plot_fuzzy_example = False

            main(method,fish_file, tifs, hsi_output_dir,fuzzy_params,trout,parameters,life_stage,plot_fuzzy_example)

        def Raster_Creation_Fuzzy(life_stage, method):
            '''
            :param life_stage: lifestage input to generate corresponding chsi.tif. selected via the different buttons.
            :param method: selected method for chsi.tif.  Can select from hsi or fuzzy_logic
            :return:
            '''
            # define global variables for the main() function
            parameters = ["velocity", "depth"]
            life_stage = life_stage
            trout = Fish("Rainbow Trout", life_stage)
            fuzzy_params = get_fuzzy_params(os.path.abspath("") + "\\habitat\\fuzzy_params.txt")

            # paths
            fish_file = os.path.abspath("") + "\\habitat\\trout.json"
            tifs = {"velocity": os.path.abspath("") + "\\basement\\flow_velocity.tif",
                    "depth": os.path.abspath("") + "\\basement\\water_depth.tif"}
            hsi_output_dir = os.path.abspath("") + "\\habitat\\"

            main(method,fish_file, tifs, hsi_output_dir,fuzzy_params,trout,parameters,life_stage)



if __name__ == "__main__":
    HsiApp().mainloop()