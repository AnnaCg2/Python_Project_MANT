import tkinter as tk
from tkinter import *
from create_hsi_rasters import *
from PIL import ImageTk
from PIL import Image
import numpy as np
from calculate_habitat_area import *


class HsiApp(tk.Frame):  # Creates a class for the GUI, created by Murat
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)  # Defines the frame for the GUI
        self.grid()

        bg = "light blue"  # Input of a background color
        self.master.configure(bg=bg)

        Welcome_label = Label(master, text="Thank you for using our program \n"  # Defines welcome label
                                           "The .tif of the habitat will display below based on which button is pressed")
        Welcome_label.grid(column=1, row=0, columnspan=2)

        # Creation of the canvas to be able to show images of the generated .tif files.
        img_size = (500, 500)  # define image size to later be displayed on a canvas.
        canvas = Canvas(master, width=500, height=500)  # define canvas size.
        canvas.grid(column=1, row=3, columnspan=2)
        canvas.configure(bg=bg)  # ensures background matches the background of the master window.

        # Creation of the buttons to show different .tif files based on lifestage and HSI method.
        Createraster_label = Label(master, text="The buttons below create and display a .tiff file based on \n"
                                                "HSI method for the selected lifestage:")
        Createraster_label.grid(column=1, row=4, columnspan=2, pady=10)

        map_button1 = tk.Button(master, text="Fry-HSI",
                                command=lambda: (open_smth(life_stage="fry", method="hsi", canvas=canvas)))
        map_button1.grid(column=1, row=5)
        map_button2 = tk.Button(master, text="Spawning-HSI",
                                command=lambda: (open_smth(life_stage="spawning", method="hsi", canvas=canvas)))
        map_button2.grid(column=1, row=6)
        map_button3 = tk.Button(master, text="Juvenile-HSI",
                                command=lambda: (open_smth(life_stage="juvenile", method="hsi", canvas=canvas)))
        map_button3.grid(column=2, row=5)
        map_button4 = tk.Button(master, text="Adult-HSI",
                                command=lambda: (open_smth(life_stage="adult", method="hsi", canvas=canvas)))
        map_button4.grid(column=2, row=6)

        # Creation of the buttons to show different .tif files based on lifestage and Fuzzy method.
        Createraster_label = Label(master, text="The buttons below create and display a .tiff file based on \n"
                                                "Fuzzy method for the selected lifestage: \n"
                                                "IMPORTANT: THIS FUNCTION TAKES A LONG TIME TO RUN - CLICK BUTTONS ONCE THEN WAIT")
        Createraster_label.grid(column=1, row=7, columnspan=2, pady=10)
        map_button5 = tk.Button(master, text="Fry-FuzzyLogic",
                                command=lambda: (open_smth(life_stage="fry", method="fuzzy_logic", canvas=canvas)))
        map_button5.grid(column=1, row=8)
        map_button6 = tk.Button(master, text="Spawning-FuzzyLogic",
                                command=lambda: (open_smth(life_stage="spawning", method="fuzzy_logic", canvas=canvas)))
        map_button6.grid(column=1, row=9)
        map_button7 = tk.Button(master, text="Juvenile-FuzzyLogic",
                                command=lambda: (open_smth(life_stage="juvenile", method="fuzzy_logic", canvas=canvas)))
        map_button7.grid(column=2, row=8)
        map_button8 = tk.Button(master, text="Adult-FuzzyLogic",
                                command=lambda: (open_smth(life_stage="adult", method="fuzzy_logic", canvas=canvas)))
        map_button8.grid(column=2, row=9)

        # Creation of the buttons to calculate area of the shown .tif file.
        Area_label = Label(master, text="The button below calculates suitable habitat area \n"
                                        "based on which option you selected above")
        Area_label.grid(column=1, row=10, columnspan=2, pady=10)
        Area_button1 = tk.Button(master, text="Calculate Area", command=lambda: (
            Area_Creation(chsi_raster_name=os.path.abspath("") + "\\habitat\\chsi.tif", chsi_threshold=0.4)))
        Area_button1.grid(column=1, row=11, columnspan=2)

        # Thank you message
        Thank_youlabel = Label(master, text="Thank you for using our program\n"
                                            "Anna, Niklas, Murat (Team MANT)")
        Thank_youlabel.grid(column=1, row=13, columnspan=2, pady=10)

        def open_smth(life_stage, method, canvas):  # Function to open .tif images.
            '''
            :param life_stage: lifestage input to generate corresponding chsi.tif. selected via the different buttons.
            :param method: Selected method for generation of hsi.tif.  Can select from hsi or fuzzy_logic
            :param canvas: predefined area that recieves the image that is generated from the chsi.tif
            :return:
            '''

            Raster_Creation(life_stage, method)

            file = os.path.abspath("") + "\\habitat\\chsi.tif"
            global my_image  # Makes my_image variable global
            img = Image.open(file).resize(img_size, resample=Image.NEAREST)
            my_image = ImageTk.PhotoImage(Image.fromarray((np.array(img) * 200).astype(np.uint8)))
            canvas.create_image(0, 0, image=my_image, anchor=NW)

            pass

        def Raster_Creation(life_stage, method): #Function pulled from Create_hsi_raster.py to generate the .tif file based on button selection.
            '''
            :param life_stage: lifestage input to generate corresponding chsi.tif. selected via the different buttons.
            :param method: selected method for generation of chsi.tif.  Can select from hsi or fuzzy_logic
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

            main(method, fish_file, tifs, hsi_output_dir, fuzzy_params, trout, parameters, life_stage,
                 plot_fuzzy_example)

        def Area_Creation(chsi_raster_name, chsi_threshold): #Function pulled from Calculate_habitat_area to calculate the area of the displayed .tif file.
            '''
            :param chsi_raster_name:  Name of the .tif that you would like to calculate area for.
            :param chsi_threshold: Threshold value utilized in Fuzzy Logic
            :return:
            '''
            chsi_raster_name = os.path.abspath("") + "\\habitat\\chsi.tif"
            chsi_threshold = 0.4

            # launch main function
            main1(chsi_raster_name, chsi_threshold)


if __name__ == "__main__":
    HsiApp().mainloop()
