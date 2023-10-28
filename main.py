import tkinter as tk
from tkinter import ttk


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

        self.grid()
        ttk.Label(self, text="Hello World!").grid(column=0, row=0)
        ttk.Button(self, text="Quit", command=self.master.destroy).grid(column=0, row=1)


root = tk.Tk()
app = Window(root)

if __name__ == '__main__':
    root.mainloop()
