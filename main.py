import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Window(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        tk.Frame.__init__(self, master)
        self.master: tk.Tk = master
        self.screen_padding = 10
        self._geom = '200x200+0+0'
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        self.master.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.master.wm_title("Window")
        self.master.update()

        # load the background image
        self.background_image = Image.open('background.png')
        self.background_label = ttk.Label(self)
        # make background_label to fit the parent window always
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # on_resize will be executed whenever background_label is resized
        self.background_label.bind('<Configure>', self.on_resize)

        # # Configure grid row and column to center content
        # self.grid()
        # self.grid_rowconfigure(0, weight=1)  # Set row 0 to expand
        # self.grid_columnconfigure(0, weight=1)  # Set column 0 to expand
        #
        # # Sticky option centers the label/button
        # ttk.Label(self, text="Hello World!").grid(sticky="nsew")
        # ttk.Button(self, text="Quit", command=self.master.destroy).grid(sticky="nsew")

    def on_resize(self, event):
        # resize the background image to the size of label
        image = self.background_image.resize((event.width, event.height), Image.LANCZOS)
        # update the image of the label
        self.background_label.image = ImageTk.PhotoImage(image)
        self.background_label.config(image=self.background_label.image)


root = tk.Tk()
app = Window(root)

if __name__ == '__main__':
    root.mainloop()
