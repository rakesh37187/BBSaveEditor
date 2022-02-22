from tkinter import FLAT, messagebox, Entry, X, LEFT, SUNKEN, DISABLED, INSERT
from tkinter import FLAT, messagebox, Entry, X, LEFT, SUNKEN, DISABLED, INSERT
from tkinter import Tk, Frame, Button, filedialog, Label, END

from process_save_file import process_file


class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        # Storing where the save file is located and its display name
        self.file_location = None
        self.profile_name = None

        # After processing the save file store the gems, the user and all the data extracted
        self.data = None
        self.gems = None
        self.user = None

        # All the entries and buttons used for filling in and changing the save data
        self.ent_level = None
        self.ent_echoes = None
        self.btn_save = None
        self.ent_arcane = None
        self.ent_bloodtinge = None
        self.ent_skill = None
        self.ent_strength = None
        self.ent_endurance = None
        self.ent_vitality = None
        self.ent_stamina = None
        self.ent_health = None
        self.ent_insight = None
        self.btn_reset = None
        self.btn_select = None
        self.btn_process = None
        self.display_name_ent = None
        self.file_loc_ent = None

        # All entries put in a list since it is used multiple times.
        self.all_entries = []

        # Init the GUI
        self.init_gui()

    def init_gui(self):
        self.parent.title("BB Save Editor")
        self.config(bg='#F0F0F0')
        self.pack()

        frm_form = Frame(relief=SUNKEN, borderwidth=3)
        frm_form.pack()

        all_entries = [self.ent_level, self.ent_echoes, self.ent_insight, self.ent_health, self.ent_stamina,
                       self.ent_vitality, self.ent_endurance, self.ent_strength, self.ent_skill,
                       self.ent_bloodtinge, self.ent_arcane]
        all_texts = ["Level", "Echoes", "Insight", "Health", "Stamina", "Vitality", "Endurance", "Strength",
                     "Skill", "Bloodtinge", "Arcane"]

        for i, (text, entry) in enumerate(zip(all_texts, all_entries)):
            lbl = Label(master=frm_form, text="User {}:".format(text))
            entry = Entry(master=frm_form, width=65)
            lbl.grid(row=i, column=0, sticky="e")
            entry.grid(row=i, column=1)
            self.all_entries.append(entry)

        frm_buttons1 = Frame()
        frm_buttons1.pack(fill=X, ipadx=5, ipady=5)

        self.btn_save = Button(master=frm_buttons1, text="Save Modifications", command=self._save_modified_stats)
        self.btn_save.pack(side=LEFT, padx=10, ipadx=10)
        self.btn_reset = Button(master=frm_buttons1, text="Reset Modifications", command=self._set_original_stats)
        self.btn_reset.pack(side=LEFT, ipadx=10)

        frm_form2 = Frame(relief=FLAT)
        frm_form2.pack(fill=X, ipadx=5, ipady=5)

        lbl = Label(master=frm_form2, text="Display Name:")
        self.display_name_ent = Entry(master=frm_form2, width=65)
        lbl.grid(row=0, column=0, sticky="e")
        self.display_name_ent.grid(row=0, column=1)

        lbl = Label(master=frm_form2, text="Selected Save:")
        self.file_loc_ent = Entry(master=frm_form2, width=65, state=DISABLED)
        lbl.grid(row=1, column=0, sticky="e")
        self.file_loc_ent.grid(row=1, column=1)

        frm_buttons2 = Frame()
        frm_buttons2.pack(fill=X, ipadx=5, ipady=5)

        self.btn_select = Button(master=frm_buttons2, text="Select Save", command=self._open_file_selection)
        self.btn_select.pack(side=LEFT, padx=10, ipadx=10)
        self.btn_process = Button(master=frm_buttons2, text="Process Save", command=self._process_data)
        self.btn_process.pack(side=LEFT, ipadx=10)

    def _save_modified_stats(self):
        if self.user is None:
            messagebox.showwarning("User not loaded!", "You can not reset all modifications since no user is loaded")
            return
        all_values = []
        for entry in self.all_entries:
            all_values.append(entry.get())
        self.user.set_all_stats(all_values)
        self.user.apply_changes(self.data, self.file_location)

    def _set_original_stats(self):
        if self.user is None:
            messagebox.showwarning("User not loaded!", "You can not reset all modifications since no user is loaded")
            return
        for stat, entry in zip(self.user.get_original_stats(), self.all_entries):
            entry.delete(0, END)
            entry.insert(0, stat)

    def _process_data(self):
        if self.file_location is None:
            messagebox.showwarning("User not loaded!", "No file selected")
        self.data, self.gems, self.user = process_file(self.file_location, self.display_name_ent.get())
        self._set_original_stats()

    def _open_file_selection(self):
        self.file_location = filedialog.askopenfilename(initialdir="./")
        self.file_loc_ent.config(state="normal")
        self.file_loc_ent.delete(0, END)
        self.file_loc_ent.insert(INSERT, self.file_location)
        self.file_loc_ent.config(state="disabled")


def main():
    root = Tk()
    root.geometry('500x360')
    root.configure(bg="#2D728F")
    app = GUI(root)
    app.mainloop()


if __name__ == '__main__':
    main()
