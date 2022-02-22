from tkinter import TOP, FLAT, messagebox, CENTER
from tkinter import Tk, Canvas, Frame, Button, filedialog, Text, Label

from process_save_file import process_file


class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.file_location = None
        self.profile_name = None
        self.data = None
        self.gems = None
        self.user = None
        self.canvas = None
        self.parent = parent
        self.init_gui()

    def init_gui(self):
        self.parent.title("BB Save Editor")
        self.config(bg='#F0F0F0')
        self.pack()
        canvas = Canvas(self, bg="#3B8EA5", height=375, width=900, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_text(143.0, 130.0, anchor="nw",
                           text="This is a W.I.P Bloodborne\nSave Editor made by\n/u/Rakesh37187",
                           fill="#FFFFFF",
                           font=("Roboto", 48 * -1),
                           justify="center"
                           )
        canvas.pack()

        canvas1 = Canvas(self, relief=FLAT, bg="#3B8EA5", width=100, height=100)
        canvas1.pack(side=TOP, anchor=CENTER)

        self.add_profile_name_text(canvas1)
        self.add_select_file_button(canvas1)
        self.add_process_button(canvas1)

    def _open_file_selection(self):
        self.file_location = filedialog.askopenfilename(initialdir="./")

    def _process_data(self):
        try:
            self.data, self.gems, self.user = process_file(self.file_location, self.profile_name.get("1.0", "end-1c"))
            messagebox.showinfo("Success", "User profile and gems loaded!")
            self.add_user_name_and_stats()
        except TypeError:
            messagebox.showerror("Error!", "You probably have not selected a file!")

    def add_user_name_and_stats(self):
        user_info = Label(text=self.user.get_original_stats())
        user_info.pack()

    def add_process_button(self, canvas):
        process_button = Button(canvas, text="Process Data", command=self._process_data)
        process_button.pack()

    def add_profile_name_text(self, canvas):
        self.profile_name = Text(canvas, height=1, width=15)
        self.profile_name.pack()

    def add_select_file_button(self, canvas):
        process_button = Button(canvas, text="Select File", command=self._open_file_selection)
        process_button.pack()


def main():
    root = Tk()
    root.geometry('900x450')
    root.configure(bg="#2D728F")
    app = GUI(root)
    app.mainloop()


if __name__ == '__main__':
    main()
