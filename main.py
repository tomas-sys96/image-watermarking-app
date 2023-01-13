import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageGrab


class ImageWatermarkingApp:

    def __init__(self, window):
        self.WIDTH = 960
        self.HEIGHT = 540
        self.window = window
        self.window.resizable(width=False, height=False)
        self.window.title("Image Watermarking App")

        self.file_path = None
        self.file_types = [("All Files", "*.*"),
                           ("PNG", "*.png"),
                           ("JPG", "*.jpg"),
                           ("JPEG", "*.jpeg"),
                           ("GIF", "*.gif")]

        # Styling
        self.style = ttk.Style()
        self.style.configure("Frame1.TFrame", background="#f0f8ff")

        # Frame
        self.button_frame = ttk.Frame(self.window)
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.description_frame = ttk.Frame(self.window)
        self.description_frame.grid(row=0, column=2, columnspan=2, sticky="nsew")

        self.text_frame = ttk.LabelFrame(self.window, text="Text Options")
        self.text_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.font_frame = ttk.LabelFrame(self.window, text="Font Options")
        self.font_frame.grid(row=2, column=2, columnspan=2, sticky="nsew")

        # Button
        self.open_button = ttk.Button(self.button_frame, text="Open...", command=self.open_file)
        self.open_button.pack(side="left")

        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_file)
        self.save_button["state"] = "disabled"
        self.save_button.pack(side="left")

        self.apply_button = ttk.Button(self.text_frame, text="Apply", command=self.change_text)
        self.apply_button["state"] = "disabled"
        self.apply_button.grid(row=0, column=2)

        # Checkbutton
        self.bold_button_clicked = tk.IntVar()
        self.bold_button = ttk.Checkbutton(self.font_frame,
                                           text="Bold",
                                           variable=self.bold_button_clicked,
                                           offvalue=0,
                                           onvalue=1,
                                           command=self.change_weight_and_slant)
        self.bold_button["state"] = "disabled"
        self.bold_button.grid(row=0, column=3, sticky="w", padx=(30, 0))

        self.italic_button_clicked = tk.IntVar()
        self.italic_button = ttk.Checkbutton(self.font_frame,
                                             text="Italic",
                                             variable=self.italic_button_clicked,
                                             offvalue=0,
                                             onvalue=1,
                                             command=self.change_weight_and_slant)
        self.italic_button["state"] = "disabled"
        self.italic_button.grid(row=1, column=3, sticky="w", padx=(30, 0))

        # Canvas
        self.canvas = tk.Canvas(width=self.WIDTH, height=self.HEIGHT, bd=0, highlightthickness=0)
        self.image = None
        self.image_photo = None
        self.canvas_image = None
        self.canvas.grid(row=1, column=0, columnspan=4)

        # Label
        self.description_label = tk.Label(self.description_frame,
                                          text="Dimensions of the output image will be at most 960px x 540px.")
        self.description_label.pack(side="right")

        self.text_label = tk.Label(self.text_frame, text="Text")
        self.text_label.grid(row=0, column=0, sticky="w")

        self.text_position_label = tk.Label(self.text_frame, text="Text Position")
        self.text_position_label.grid(row=1, column=0, sticky="w")

        self.font_style_label = tk.Label(self.font_frame, text="Font Style")
        self.font_style_label.grid(row=0, column=0, sticky="w")

        self.font_size_label = tk.Label(self.font_frame, text="Font Size")
        self.font_size_label.grid(row=1, column=0, sticky="w")

        self.font_color_label = tk.Label(self.font_frame, text="Font Color")
        self.font_color_label.grid(row=2, column=0, sticky="w")

        # Entry
        self.text_entry = ttk.Entry(self.text_frame, width=47)
        self.text_entry["state"] = "disabled"
        self.text_entry.grid(row=0, column=1, sticky="w", padx=(30, 0))

        # Dropdown menu
        self.text_position_options = ["Top Left", "Top Center", "Top Right", "Middle Left", "Middle Center",
                                      "Middle Right", "Bottom Left", "Bottom Center", "Bottom Right"]
        self.text_position_clicked = tk.StringVar()
        self.text_position_menu = ttk.OptionMenu(
            self.text_frame,
            self.text_position_clicked,
            self.text_position_options[4],
            *self.text_position_options,
            command=self.change_text_position
        )
        self.text_position_menu.config(width=14)
        self.text_position_menu["state"] = "disabled"
        self.text_position_menu.grid(row=1, column=1, sticky="w", padx=(30, 0))

        self.font_size_options = ["8 pt", "10 pt", "12 pt", "14 pt", "16 pt", "18 pt", "20 pt", "22 pt", "24 pt",
                                  "26 pt", "28 pt", "32 pt", "36 pt", "40 pt"]
        self.font_size_clicked = tk.StringVar()
        self.font_size_menu = ttk.OptionMenu(
            self.font_frame,
            self.font_size_clicked,
            self.font_size_options[2],
            *self.font_size_options,
            command=self.change_font_size
        )
        self.font_size_menu.config(width=14)
        self.font_size_menu["state"] = "disabled"
        self.font_size_menu.grid(row=1, column=1, sticky="w", padx=(30, 0))

        self.font_color_options = ["Black", "Dark Grey", "Light Grey", "White"]
        self.font_color_clicked = tk.StringVar()
        self.font_color_menu = ttk.OptionMenu(
            self.font_frame,
            self.font_color_clicked,
            self.font_color_options[3],
            *self.font_color_options,
            command=self.change_font_color
        )
        self.font_color_menu.config(width=14)
        self.font_color_menu["state"] = "disabled"
        self.font_color_menu.grid(row=2, column=1, sticky="w", padx=(30, 0))

        # Combobox
        self.font_style_clicked = tk.StringVar()
        self.font_style_combobox = ttk.Combobox(
            self.font_frame,
            width=25,
            textvariable=self.font_style_clicked
        )
        self.font_style_combobox.bind("<<ComboboxSelected>>", self.change_font_style)
        self.font_style_combobox["values"] = ("Arial",
                                              "Arial Black",
                                              "Banschrift",
                                              "Calibri",
                                              "Cambria",
                                              "Candara",
                                              "Comic Sans MS",
                                              "Consolas",
                                              "Constantia",
                                              "Corbel",
                                              "Courier New",
                                              "Ebrima",
                                              "Franklin Gothic Medium",
                                              "Gabriola",
                                              "Gadugi",
                                              "Georgia",
                                              "Impact",
                                              "Ink Free",
                                              "Javanese Text",
                                              "Leelawadee UI",
                                              "Lucida Console",
                                              "Lucida Sans Unicode",
                                              "Malgun Gothic",
                                              "MS Gothic",
                                              "MV Boli",
                                              "Myanmar Text",
                                              "Palatino Linotype",
                                              "Segoe MDL2 Assets",
                                              "Segoe Print",
                                              "Segoe Script",
                                              "Segoe UI",
                                              "Simsun",
                                              "Sitka",
                                              "Sylfaen",
                                              "Tahoma",
                                              "Times New Roman",
                                              "Trebuchet MS",
                                              "Verdana",
                                              "YU Gothic")
        self.font_style_combobox.current(3)
        self.font_style_combobox["state"] = "disabled"
        self.font_style_combobox.grid(row=0, column=1, sticky="w", padx=(30, 0))

        # Watermark
        self.canvas_watermark = None

    def initialize_canvas(self):
        # self.canvas.config(background="SystemButtonFace")
        self.canvas_image = self.canvas.create_image(self.WIDTH / 2,
                                                     self.HEIGHT / 2,
                                                     anchor="center",
                                                     image=self.image_photo)

        self.save_button["state"] = "enable"
        self.text_entry["state"] = "enable"
        self.text_entry.insert(0, "Sample text")
        self.apply_button["state"] = "enable"
        self.text_position_menu["state"] = "enable"
        self.font_style_combobox["state"] = "enable"
        self.font_size_menu["state"] = "enable"
        self.font_color_menu["state"] = "enable"
        self.bold_button["state"] = "enable"
        self.italic_button["state"] = "enable"

        text_position = self.get_text_position()
        self.canvas_watermark = self.canvas.create_text(*text_position["positions"],
                                                        anchor=text_position["anchor"],
                                                        text=self.text_entry.get(),
                                                        font=(self.get_font_style(), self.get_font_size()),
                                                        fill=self.get_font_color())

    def open_file(self):
        file_name = filedialog.askopenfilename(
            initialdir="/",
            filetypes=self.file_types
        )
        self.file_path = file_name

        image_types = [ext[1].replace("*.", "") for ext in self.file_types[1:]]
        try:
            file_extension = file_name.split("/")[-1].split(".")[1].lower()
        except IndexError:
            return
        else:
            if file_extension in image_types:
                self.image = Image.open(file_name)
                if self.image.width > self.WIDTH or self.image.height > self.HEIGHT:
                    self.image = self.resize_image(self.image)
                self.image_photo = ImageTk.PhotoImage(self.image)
                if self.canvas_image is None:
                    self.initialize_canvas()
                else:
                    self.canvas.itemconfig(self.canvas_image, image=self.image_photo)
                    self.change_text_position()

    def save_file(self):
        x0 = self.window.winfo_rootx() + self.canvas.winfo_x() + self.WIDTH / 2 - self.image.width / 2
        y0 = self.window.winfo_rooty() + self.canvas.winfo_y() + self.HEIGHT / 2 - self.image.height / 2
        x1 = x0 + self.image.width
        y1 = y0 + self.image.height

        name = self.file_path.split("/")[-1]
        directory = self.file_path.replace(name, "")

        file_name = filedialog.asksaveasfile(
            initialdir=directory,
            filetypes=self.file_types
        )

        try:
            ImageGrab.grab().crop((x0, y0, x1, y1)).save(file_name.name)
        except AttributeError:
            return

    def resize_image(self, image):
        width_ratio = image.width / self.WIDTH
        height_ratio = image.height / self.HEIGHT
        if width_ratio >= height_ratio:
            driving_ratio = width_ratio
        else:
            driving_ratio = height_ratio
        new_width = round(image.width / driving_ratio)
        new_height = round(image.height / driving_ratio)
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        return resized_image

    def change_text(self):
        updated_text = self.text_entry.get()
        self.canvas.itemconfig(self.canvas_watermark, text=updated_text)

    def get_text_position(self):
        ratio = 0.95
        if min(self.image.width, self.image.height) == self.image.width:
            left_border = (self.WIDTH / 2) - round((self.image.width / 2) * ratio)
            right_border = (self.WIDTH / 2) + round((self.image.width / 2) * ratio)
            gap = round((self.image.width / 2) * (1 - ratio))
            top_border = (self.HEIGHT / 2) - round(self.image.height / 2) + gap
            bottom_border = (self.HEIGHT / 2) + round(self.image.height / 2) - gap
        else:
            top_border = (self.HEIGHT / 2) - round((self.image.height / 2) * ratio)
            bottom_border = (self.HEIGHT / 2) + round((self.image.height / 2) * ratio)
            gap = round((self.image.height / 2) * (1 - ratio))
            left_border = (self.WIDTH / 2) - round(self.image.width / 2) + gap
            right_border = (self.WIDTH / 2) + round(self.image.width / 2) - gap
        text_positions = {
            "Top Left": {
                "positions": (left_border, top_border),
                "anchor": "nw"
            },
            "Top Center": {
                "positions": (self.WIDTH / 2, top_border),
                "anchor": "n"
            },
            "Top Right": {
                "positions": (right_border, top_border),
                "anchor": "ne"
            },
            "Middle Left": {
                "positions": (left_border, self.HEIGHT / 2),
                "anchor": "w"
            },
            "Middle Center": {
                "positions": (self.WIDTH / 2, self.HEIGHT / 2),
                "anchor": "center"
            },
            "Middle Right": {
                "positions": (right_border, self.HEIGHT / 2),
                "anchor": "e"
            },
            "Bottom Left": {
                "positions": (left_border, bottom_border),
                "anchor": "sw"
            },
            "Bottom Center": {
                "positions": (self.WIDTH / 2, bottom_border),
                "anchor": "s"
            },
            "Bottom Right": {
                "positions": (right_border, bottom_border),
                "anchor": "se"
            }
        }

        text_position = self.text_position_clicked.get()
        return text_positions[text_position]

    def change_text_position(self, *args):
        text_position = self.get_text_position()
        self.canvas.itemconfig(self.canvas_watermark, anchor=text_position["anchor"])
        self.canvas.coords(self.canvas_watermark,
                         text_position["positions"][0],
                         text_position["positions"][1])

    def get_font_modifications(self):
        font_weight = self.bold_button_clicked.get()
        font_slant = self.italic_button_clicked.get()

        if font_weight == 1 and font_slant == 1:
            font_modifications = ["bold", "italic"]
        elif font_weight == 1 and font_slant == 0:
            font_modifications = ["bold"]
        elif font_weight == 0 and font_slant == 1:
            font_modifications = ["italic"]
        else:
            font_modifications = []
        return font_modifications

    def change_weight_and_slant(self):
        self.canvas.itemconfig(self.canvas_watermark,
                               font=(self.get_font_style(), self.get_font_size(), *self.get_font_modifications()))

    def get_font_style(self):
        font_style = self.font_style_clicked.get()
        return font_style

    def change_font_style(self, *args):
        font_style = self.get_font_style()
        self.canvas.itemconfig(self.canvas_watermark,
                               font=(font_style, self.get_font_size(), *self.get_font_modifications()))

    def get_font_size(self):
        font_size = int(self.font_size_clicked.get().split()[0])
        return font_size

    def change_font_size(self, *args):
        font_size = self.get_font_size()
        self.canvas.itemconfig(self.canvas_watermark,
                               font=(self.get_font_style(), font_size, *self.get_font_modifications()))

    def get_font_color(self):
        font_color = self.font_color_clicked.get()
        if font_color == "Black":
            hex_code = "#000000"
        elif font_color == "Dark Grey":
            hex_code = "#5b5b5b"
        elif font_color == "Light Grey":
            hex_code = "#bcbcbc"
        else:
            hex_code = "#ffffff"
        return hex_code

    def change_font_color(self, *args):
        font_color = self.get_font_color()
        self.canvas.itemconfig(self.canvas_watermark, fill=font_color)


if __name__ == "__main__":
    root = tk.Tk()
    image_watermarking_app = ImageWatermarkingApp(root)
    image_watermarking_app.window.mainloop()
