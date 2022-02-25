from tkinter import FLAT, messagebox, Entry, X, LEFT, DISABLED, INSERT, BOTH, StringVar
from tkinter import Tk, Frame, Button, filedialog, Label, END
from tkinter.ttk import Combobox

from gem_data_conversion import gem_effects, gem_shapes
from process_save_file import process_user, process_gems


class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        # Storing where the save file is located and its display name
        self.file_location = None

        # Default colour options for labels, buttons and possibly other widgets
        self.button_settings = {"bg": "#0B5351", "fg": "white", "font": ('Helvetica', 10, 'bold')}
        self.label_settings = {"bg": "#00A9A5", "fg": "white", "font": ('Helvetica', 9, 'bold')}

        # After processing the save file store the gems, the user and all the data extracted
        self.data = None
        self.gems = None
        self.user = None

        # All the entries and buttons used for filling in and changing the save data
        self.ent_level = None
        self.ent_echoes = None
        self.ent_arcane = None
        self.ent_bloodtinge = None
        self.ent_skill = None
        self.ent_strength = None
        self.ent_endurance = None
        self.ent_vitality = None
        self.ent_stamina = None
        self.ent_health = None
        self.ent_insight = None
        self.display_name_ent = None
        self.file_loc_ent = None
        self.selected_gem = None

        self.combobox_all_gems = None
        self.ent_gem_id = None
        self.ent_gem_source = None
        self.ent_gem_quantity = None
        self.ent_gem_shape = None
        self.ent_gem_effect_1 = None
        self.ent_gem_effect_2 = None
        self.ent_gem_effect_3 = None

        self.btn_save = None
        self.btn_reset = None
        self.btn_select = None
        self.btn_process = None

        # All entries, buttons and menus put in a list since it is used multiple times.
        self.all_gem_menu = []
        self.all_user_entries = []
        self.all_gem_btns = []
        self.all_user_btns = []
        self.gem_effects_values = ["{}, {}".format(gem.decode("utf-8"), gem_effects.get(gem)) for gem in gem_effects]
        self.gem_shape_values = ["{}, {}".format(gem.decode("utf-8"), gem_shapes.get(gem)) for gem in gem_shapes]

        # Init the GUI
        self.parent.title("BB Save Editor")
        self.pack()
        self.init_main_screen()

    def init_main_screen(self):
        main_screen = Frame(relief=FLAT, borderwidth=3, bg="#00A9A5")
        main_screen.pack(fill=BOTH)
        main_screen_text = ("Welcome to the BB Save Editor!\n"
                            "This is still a W.I.P.\n"
                            "Please feel free to report any bugs.\n"
                            "Made by Rakesh37187")
        welcome = Label(master=main_screen, text=main_screen_text, bg="#00A9A5", fg="white",
                        font=('Helvetica', 22, 'bold'))
        welcome.pack(pady=50, ipady=10)
        main_menu_options = Frame(relief=FLAT, borderwidth=3, bg="#00A9A5")
        main_menu_options.pack(fill=BOTH, side=LEFT)

        btn_user = Button(master=main_menu_options, text="Open User Editor",
                          command=lambda: self.init_user_gui(main_screen, main_menu_options),
                          relief=FLAT, **self.button_settings)
        btn_user.pack(side=LEFT, padx=10, ipadx=10)

        btn_gem = Button(master=main_menu_options, text="Open Gem Editor",
                         command=lambda: self.init_gem_gui(main_screen, main_menu_options),
                         relief=FLAT, **self.button_settings)
        btn_gem.pack(side=LEFT, padx=10, ipadx=10)

        btn_inv = Button(master=main_menu_options, text="Open Inventory Editor",
                         command=lambda: self.init_user_gui(main_screen, main_menu_options),
                         relief=FLAT, **self.button_settings)
        btn_inv.pack(side=LEFT, padx=10, ipadx=10)
        self.make_buttons_responsive([btn_user, btn_gem, btn_inv])

    def add_save_select_and_process(self, to_process):
        frm_form = Frame(relief=FLAT, borderwidth=3, bg="#00A9A5")
        frm_form.pack(fill=X)

        lbl = Label(master=frm_form, text="Selected Save:", **self.label_settings)
        self.file_loc_ent = Entry(master=frm_form, width=65, state=DISABLED)
        lbl.grid(row=0, column=0, sticky="e")
        self.file_loc_ent.grid(row=0, column=1)

        frm_buttons1 = Frame(relief=FLAT, bg="#00A9A5")
        frm_buttons1.pack(fill=X, ipadx=5, ipady=5)

        self.btn_select = Button(master=frm_buttons1, text="Select Save", command=self._open_file_selection,
                                 relief=FLAT, **self.button_settings)
        self.btn_select.pack(side=LEFT, padx=10, ipadx=10)
        self.btn_process = Button(master=frm_buttons1, text="Process Save", command=to_process,
                                  relief=FLAT, **self.button_settings)
        self.btn_process.pack(side=LEFT, padx=10, ipadx=10)

    def make_buttons_responsive(self, all_buttons):
        for btn in all_buttons:
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

    def init_gem_gui(self, e1=None, e2=None):
        self.delete_previous_screen(*(e1, e2))
        frm_select = Frame(relief=FLAT, borderwidth=3, bg="#00A9A5")
        self.combobox_all_gems = Combobox(master=frm_select)
        self.combobox_all_gems.config(width=65)
        lbl = Label(master=frm_select, text="Select Gem:", bg="#00A9A5", fg="white", font=('Helvetica', 9, 'bold'))
        lbl.grid(row=0, column=0)
        self.combobox_all_gems.grid(row=0, column=1)
        frm_select.pack(fill=X)
        self.combobox_all_gems.bind("<<ComboboxSelected>>", self._set_original_gem_stats)

        filler_frm = Frame(relief=FLAT, bg="#00A9A5")
        filler_frm.config(height=40)
        filler_frm.pack(fill=BOTH)

        frm_form = Frame(relief=FLAT, borderwidth=3, bg="#00A9A5")
        frm_form.pack(fill=X)

        filler_frm = Frame(relief=FLAT, bg="#00A9A5")
        filler_frm.config(height=40)
        filler_frm.pack(fill=BOTH)

        frm_buttons1 = Frame(relief=FLAT, bg="#00A9A5")
        self.btn_save = Button(master=frm_buttons1, text="Save Modifications", command=self._save_modified_gem_stats,
                               relief=FLAT, **self.button_settings)
        self.btn_save.pack(side=LEFT, padx=10, ipadx=10)
        self.btn_reset = Button(master=frm_buttons1, text="Reset Modifications", command=self._set_original_gem_stats,
                                relief=FLAT, **self.button_settings)
        self.btn_reset.pack(side=LEFT, ipadx=10)
        frm_buttons1.pack(fill=X, ipadx=5, ipady=5)
        all_gem_menu = [self.ent_gem_id, self.ent_gem_source, self.ent_gem_quantity, self.ent_gem_shape,
                        self.ent_gem_effect_1, self.ent_gem_effect_2, self.ent_gem_effect_3]
        all_texts = ["ID", "Source", "Quantity", "Shape", "Effect 1", "Effect 2", "Effect 3"]
        for i, (text, entry) in enumerate(zip(all_texts, all_gem_menu)):
            lbl = Label(master=frm_form, text="Gem {}:".format(text), bg="#00A9A5", fg="white",
                        font=('Helvetica', 9, 'bold'))
            clicked = StringVar()
            clicked.set(list(self.gem_effects_values)[0])
            if i > 3:
                entry = Combobox(master=frm_form, textvariable=clicked, values=self.gem_effects_values)
                entry.config(width=62)
            elif i == 3:
                entry = Combobox(master=frm_form, textvariable=clicked, values=self.gem_shape_values)
                entry.config(width=62)
            else:
                entry = Entry(master=frm_form, width=65, state='disabled')
                lbl.grid(row=i, column=0, sticky="e")
                entry.grid(row=i, column=1)
            lbl.grid(row=i, column=0, sticky="e")
            entry.grid(row=i, column=1)
            self.all_gem_menu.append(entry)

        self.add_save_select_and_process(self._process_data_gems)

        filler_frm = Frame(relief=FLAT, bg="#00A9A5")
        filler_frm.config(height=40)
        filler_frm.pack(fill=BOTH)

    def init_user_gui(self, e1=None, e2=None):
        self.delete_previous_screen(*(e1, e2))
        frm_form = Frame(relief=FLAT, borderwidth=3, bg="#00A9A5")
        frm_form.pack(fill=X)

        all_entries = [self.ent_level, self.ent_echoes, self.ent_insight, self.ent_health, self.ent_stamina,
                       self.ent_vitality, self.ent_endurance, self.ent_strength, self.ent_skill,
                       self.ent_bloodtinge, self.ent_arcane]
        all_texts = ["Level", "Echoes", "Insight", "Health", "Stamina", "Vitality", "Endurance", "Strength",
                     "Skill", "Bloodtinge", "Arcane"]

        for i, (text, entry) in enumerate(zip(all_texts, all_entries)):
            lbl = Label(master=frm_form, text="User {}:".format(text), bg="#00A9A5", fg="white",
                        font=('Helvetica', 9, 'bold'))
            entry = Entry(master=frm_form, width=65)
            lbl.grid(row=i, column=0, sticky="e")
            entry.grid(row=i, column=1)
            self.all_user_entries.append(entry)

        frm_buttons1 = Frame(relief=FLAT, bg="#00A9A5")

        self.btn_save = Button(master=frm_buttons1, text="Save Modifications", command=self._save_modified_user_stats,
                               relief=FLAT, **self.button_settings)
        self.btn_save.pack(side=LEFT, padx=10, ipadx=10)
        self.btn_reset = Button(master=frm_buttons1, text="Reset Modifications", command=self._set_original_users_stats,
                                relief=FLAT, **self.button_settings)
        self.btn_reset.pack(side=LEFT, ipadx=10)

        frm_form2 = Frame(relief=FLAT, borderwidth=3, bg="#00A9A5")

        lbl = Label(master=frm_form2, text="Display Name:", **self.label_settings)
        self.display_name_ent = Entry(master=frm_form2, width=65, state="disabled")
        lbl.grid(row=0, column=0, sticky="e")
        self.display_name_ent.grid(row=0, column=1, padx=4)

        frm_buttons1.pack(fill=X, ipadx=5, ipady=5)
        frm_form2.pack(fill=X, ipadx=5)
        self.add_save_select_and_process(self._process_data_user)
        self.btn_process.pack(side=LEFT, ipadx=10)
        self.make_buttons_responsive([self.btn_save, self.btn_reset, self.btn_select, self.btn_process])

    @staticmethod
    def delete_previous_screen(*args):
        for arg in args:
            for widget in arg.winfo_children():
                widget.destroy()
            arg.destroy()

    @staticmethod
    def on_enter(e):
        e.widget['background'] = '#4E8098'

    @staticmethod
    def on_leave(e):
        e.widget['background'] = '#0B5351'

    def _save_modified_user_stats(self):
        if self.user is None:
            messagebox.showwarning("User not loaded!", "You can not reset all modifications since no user is loaded")
            return
        all_values = []
        for entry in self.all_user_entries:
            all_values.append(entry.get())
        self.user.set_all_stats(all_values)
        self.user.apply_changes(self.data, self.file_location)

    def _save_modified_gem_stats(self):
        if self.gems is None:
            messagebox.showwarning("File not loaded!", "You can not reset all modifications since no file is loaded")
            return
        all_values = []
        for entry in self.all_gem_menu:
            all_values.append(entry.get())
        self.selected_gem.set_all_stats(all_values)
        self.selected_gem.apply_changes(self.data, self.file_location)

    def _set_original_users_stats(self):
        if self.user is None:
            messagebox.showwarning("User not loaded!", "You can not reset all modifications since no user is loaded")
            return
        for stat, entry in zip(self.user.get_original_stats(), self.all_user_entries):
            entry.delete(0, END)
            entry.insert(0, stat)
        self.display_name_ent.config(state="normal")
        self.display_name_ent.delete(0, END)
        self.display_name_ent.insert(INSERT, self.user.get_display_name())
        self.display_name_ent.config(state="disabled")

    def _load_all_gems(self):
        if self.gems is None:
            messagebox.showwarning("File not loaded!", "You can not reset all modifications since no file is loaded")
            return
        self.combobox_all_gems['values'] = [list(gem.get_original_stats())[0] for gem in self.gems]

    def _set_original_gem_stats(self, e=None):
        if e is not None:
            for gem in self.gems:
                if list(gem.get_original_stats())[0] == e.widget.get():
                    self.selected_gem = gem
        for i, (gem_menu, value) in enumerate(zip(self.all_gem_menu, list(self.selected_gem.get_original_stats()))):
            if i > 2:
                gem_menu.set(value)
            else:
                gem_menu.config(state="normal")
                gem_menu.delete(0, END)
                gem_menu.insert(INSERT, value)
                gem_menu.config(state="disabled")

    def _process_data_user(self):
        if self.file_location is None:
            messagebox.showwarning("User not loaded!", "No file selected")
        self.data, self.user = process_user(self.file_location)
        self._set_original_users_stats()

    def _process_data_gems(self):
        if self.file_location is None:
            messagebox.showwarning("File not loaded!", "No file selected")
        self.data, self.gems = process_gems(self.file_location)
        self._load_all_gems()

    def _open_file_selection(self):
        self.file_location = filedialog.askopenfilename(initialdir="./")
        self.file_loc_ent.config(state="normal")
        self.file_loc_ent.delete(0, END)
        self.file_loc_ent.insert(INSERT, self.file_location)
        self.file_loc_ent.config(state="disabled")


def main():
    root = Tk()
    root.geometry('500x365')
    app = GUI(root)
    app.mainloop()


if __name__ == '__main__':
    main()
