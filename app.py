import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class CollapsibleFrame(ttk.LabelFrame):
    def __init__(self, parent, title="", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.is_expanded = True
        self.title = title

        self.toggle_btn = ttk.Button(
            self,
            text=f"▼ {self.title}",
            command=self.toggle,
            style="Toolbutton"
        )
        self.toggle_btn.pack(fill="x", padx=5, pady=2)

        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, padx=5, pady=2)

    def toggle(self):
        if self.is_expanded:
            self.content_frame.pack_forget()
            self.toggle_btn.configure(text=f"► {self.title}")
            self.is_expanded = False
        else:
            self.content_frame.pack(fill="both", expand=True, padx=5, pady=2)
            self.toggle_btn.configure(text=f"▼ {self.title}")
            self.is_expanded = True

class UESRPGCharacterSheet(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CHARACTER SHEET - 3ev4")
        self.geometry("1280x720")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        tab4 = ttk.Frame(notebook)
        tab5 = ttk.Frame(notebook)
        tab6 = ttk.Frame(notebook)

        notebook.add(tab1, text="Page 1: Character and Attributes")
        notebook.add(tab2, text="Page 2: Skills")
        notebook.add(tab3, text="Page 3: Armor and Weapons")
        notebook.add(tab4, text="Page 4: Items & Equipment")
        notebook.add(tab5, text="Page 5: Talents, Traits, & Powers")
        notebook.add(tab6, text="Page 6: Spellcasting")

        self.setup_tab1(tab1)
        self.setup_tab2(tab2)
        self.setup_tab3(tab3)
        self.setup_tab4(tab4)
        self.setup_tab5(tab5)
        self.setup_tab6(tab6)
        self.setup_menu()

# ---------------PAGE1------------------
    def setup_tab1(self, parent):
        self.tab1_entries = {}
        self.derived_attr_vars = {}

        header_frame = ttk.LabelFrame(parent, text="Character Sheet")
        header_frame.pack(fill="x", padx=10, pady=5)

        row1_fields = [
            ("Name:", 35),
            ("Race:", 35),
            ("Birthsign:", 35),
            ("Elite Advances:", 35)
        ]

        for i, (field_label, width_val) in enumerate(row1_fields):
            key = field_label.rstrip(":")
            ttk.Label(header_frame, text=field_label).grid(row=0, column=i * 2, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(header_frame, width=width_val)
            entry.grid(row=0, column=i * 2 + 1, padx=5, pady=5, sticky="w")
            self.tab1_entries[key] = entry

        row2_fields = [
            ("Size:", 20),
            ("XP:", 20),
            ("Total XP:", 20)
        ]

        for i, (field_label, width_val) in enumerate(row2_fields):
            key = field_label.rstrip(":")
            ttk.Label(header_frame, text=field_label).grid(row=1, column=i * 2, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(header_frame, width=width_val)
            entry.grid(row=1, column=i * 2 + 1, padx=5, pady=5, sticky="w")
            self.tab1_entries[key] = entry

        # Characteristics
        attr_frame = ttk.LabelFrame(parent, text="Characteristics")
        attr_frame.pack(fill="x", padx=10, pady=5)

        attributes = ["Str", "End", "Ag", "Int", "Wp", "Prc", "Prs", "Lck"]
        bonus_names = ["SB", "EB", "AB", "IB", "WB", "PcB", "PsB", "LB"]

        self.attr_vars = {}
        self.bonus_vars = {}
        self.favored_vars = {}

        # Favored
        ttk.Label(attr_frame, text="Favored", font=('Helvetica', 9, 'bold')).grid(row=2, column=0, padx=(10, 5), pady=2,
                                                                                  sticky="e")

        for i, (attr, bonus_name) in enumerate(zip(attributes, bonus_names), start=1):
            ttk.Label(attr_frame, text=attr, font=('Helvetica', 9, 'bold')).grid(row=0, column=i, padx=12, pady=2)

            var = tk.StringVar(value="0")
            self.attr_vars[attr] = var
            entry = ttk.Entry(attr_frame, textvariable=var, width=5, justify="center")
            entry.grid(row=1, column=i, padx=5, pady=2)

            # Checkbutton (Favored)
            if attr != "Lck":
                cb_var = tk.BooleanVar(value=False)
                self.favored_vars[attr] = cb_var

                cb = ttk.Checkbutton(
                    attr_frame,
                    variable=cb_var,
                    command=lambda a=attr: self.on_favored_toggle(a) if hasattr(self, "on_favored_toggle") else None
                )
                cb.grid(row=2, column=i, padx=5, pady=2)
            else:
                ttk.Label(attr_frame, text="-").grid(row=2, column=i, padx=5, pady=2)

            b_var = tk.StringVar(value="0")
            self.bonus_vars[bonus_name] = b_var
            bonus_entry = ttk.Entry(attr_frame, textvariable=b_var, width=5, justify="center", state="readonly")
            bonus_entry.grid(row=3, column=i, padx=5, pady=2)

            ttk.Label(attr_frame, text=bonus_name, foreground="gray").grid(row=4, column=i, padx=12, pady=2)

            var.trace_add("write", lambda *args, a=attr, b=bonus_name: self.calculate_bonus(a, b))

        lucky_frame = ttk.Frame(attr_frame)
        lucky_frame.grid(row=5, column=0, columnspan=9, pady=(10, 5), sticky="w", padx=10)

        for i, field in enumerate(["Lucky Numbers:", "Unlucky Numbers:"]):
            key = field.rstrip(":")
            ttk.Label(lucky_frame, text=field, font=('Helvetica', 9, 'bold')).grid(row=0, column=i * 2, padx=(10, 5),
                                                                                   pady=5, sticky="e")
            entry = ttk.Entry(lucky_frame, width=25)
            entry.grid(row=0, column=i * 2 + 1, padx=(0, 15), pady=5, sticky="w")
            self.tab1_entries[key] = entry

        # Attributes
        attributes_frame = ttk.LabelFrame(parent, text="Attributes")
        attributes_frame.pack(fill="x", padx=10, pady=5)

        # Current / Max
        def create_dual_entry(parent_widget, row, col, label_text):
            ttk.Label(parent_widget, text=label_text, font=('Helvetica', 9, 'bold')).grid(row=row, column=col,
                                                                                          padx=(20 if col > 0 else 5,
                                                                                                5), pady=2, sticky="e")
            frame = ttk.Frame(parent_widget)
            frame.grid(row=row, column=col + 1, padx=5, pady=2, sticky="w")
            e1 = ttk.Entry(frame, width=5, justify="center")
            e1.pack(side="left")
            ttk.Label(frame, text="/").pack(side="left", padx=2)
            e2 = ttk.Entry(frame, width=5, justify="center")
            e2.pack(side="left")
            return (e1, e2)

        def create_single_entry(parent_widget, row, col, label_text, width=13):
            ttk.Label(parent_widget, text=label_text, font=('Helvetica', 9, 'bold')).grid(row=row, column=col,
                                                                                          padx=(20 if col > 0 else 5,
                                                                                                5), pady=2, sticky="e")
            e = ttk.Entry(parent_widget, width=width, justify="center" if width < 20 else "left")
            e.grid(row=row, column=col + 1, padx=5, pady=2, sticky="w")
            return e

        # HP, WT, Speed, IR, Linguistics
        self.derived_attr_vars["HP"] = create_dual_entry(attributes_frame, 0, 0, "HP")
        self.derived_attr_vars["WT"] = create_single_entry(attributes_frame, 1, 0, "WT")
        self.derived_attr_vars["Speed"] = create_single_entry(attributes_frame, 2, 0, "Speed")
        self.derived_attr_vars["IR"] = create_single_entry(attributes_frame, 3, 0, "IR")

        ling_entry = ttk.Entry(attributes_frame, width=25)
        ttk.Label(attributes_frame, text="Linguistics", font=('Helvetica', 9, 'bold')).grid(row=4, column=0, padx=5,
                                                                                            pady=2, sticky="e")
        ling_entry.grid(row=4, column=1, padx=5, pady=2, sticky="w")
        self.tab1_entries["Linguistics"] = ling_entry

        # MP, SP, LP, AP, ENC / CR
        self.derived_attr_vars["MP"] = create_dual_entry(attributes_frame, 0, 2, "MP")
        self.derived_attr_vars["SP"] = create_dual_entry(attributes_frame, 1, 2, "SP")
        self.derived_attr_vars["LP"] = create_dual_entry(attributes_frame, 2, 2, "LP")
        self.derived_attr_vars["AP"] = create_dual_entry(attributes_frame, 3, 2, "AP")
        self.derived_attr_vars["ENC / CR"] = create_dual_entry(attributes_frame, 4, 2, "ENC / CR")

        #Languages
        ttk.Label(attributes_frame, text="Languages", font=('Helvetica', 9, 'bold')).grid(row=5, column=0, padx=5,
                                                                                          pady=(5, 10), sticky="e")
        langs_entry = ttk.Entry(attributes_frame, width=65)
        langs_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=(5, 10), sticky="w")
        self.tab1_entries["Languages"] = langs_entry

        #BONDS
        bonds_frame = ttk.LabelFrame(parent, text="Bonds")
        bonds_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.bonds_text = tk.Text(bonds_frame, height=5, wrap="word")
        bonds_scrollbar = ttk.Scrollbar(bonds_frame, orient="vertical", command=self.bonds_text.yview)
        self.bonds_text.configure(yscrollcommand=bonds_scrollbar.set)

        self.bonds_text.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        bonds_scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=5)

    def on_favored_toggle(self, changed_attr):
        favored_count = sum(1 for var in self.favored_vars.values() if var.get())

        if favored_count > 2:
            self.favored_vars[changed_attr].set(False)

            messagebox.showwarning(
                "Limit Favored",
                "Max 2 Favored Attributes!"
            )
        else:
            if hasattr(self, "calculate_derived"):
                self.calculate_derived()
#---------------PAGE2------------------
    def setup_tab2(self, parent):
        self.skill_ranks_info = {
            "Untrained": (-1, -20),
            "Novice": (0, 0),
            "Apprentice": (1, 10),
            "Journeyman": (2, 20),
            "Adept": (3, 30),
            "Expert": (4, 40),
            "Master": (5, 50)
        }

        def update_skill_values(skill_name):
            data = self.skill_vars[skill_name]
            selected_level = data["level_cb"].get()
            rank, bonus = self.skill_ranks_info.get(selected_level, (-1, -20))

            data["rank_var"].set(str(rank))
            data["bonus_var"].set(f"+{bonus}" if bonus >= 0 else str(bonus))

            for stat, tn_var in data["tn_vars"]:
                stat_val_str = getattr(self, "attr_vars", {}).get(stat, tk.StringVar(value="0")).get()
                try:
                    stat_val = int(stat_val_str)
                except ValueError:
                    stat_val = 0
                tn_var.set(str(stat_val + bonus))

        def update_single_prof_row(row_data):
            selected_level = row_data["level_cb"].get()
            rank, bonus = self.skill_ranks_info.get(selected_level, (-1, -20))

            row_data["rank_var"].set(str(rank))
            row_data["bonus_var"].set(f"+{bonus}" if bonus >= 0 else str(bonus))

            for widget in row_data["tn_container"].winfo_children():
                widget.destroy()

            row_data["tn_entries"] = []
            selected_attrs = [cb.get() for cb in row_data["attr_cbs"] if cb.get() != "None"]

            for idx, stat in enumerate(selected_attrs):
                if idx > 0:
                    ttk.Label(row_data["tn_container"], text=",").pack(side="left", padx=1)

                stat_val_str = getattr(self, "attr_vars", {}).get(stat, tk.StringVar(value="0")).get()
                try:
                    stat_val = int(stat_val_str)
                except ValueError:
                    stat_val = 0

                tn_val = stat_val + bonus
                tn_var = tk.StringVar(value=str(tn_val))
                tn_entry = ttk.Entry(row_data["tn_container"], textvariable=tn_var, width=4, justify="center",
                                     state="readonly")
                tn_entry.pack(side="left")

                row_data["tn_entries"].append((stat, tn_var))

        def update_cs_values():
            selected_level = self.cs_level_cb.get()
            rank, bonus = self.skill_ranks_info.get(selected_level, (-1, -20))

            self.cs_rank_var.set(str(rank))
            self.cs_bonus_var.set(f"+{bonus}" if bonus >= 0 else str(bonus))

            str_val = int(getattr(self, "attr_vars", {}).get("Str", tk.StringVar(value="0")).get() or 0)
            ag_val = int(getattr(self, "attr_vars", {}).get("Ag", tk.StringVar(value="0")).get() or 0)

            self.cs_tn_str_var.set(str(str_val + bonus))
            self.cs_tn_ag_var.set(str(ag_val + bonus))

        def recalculate_all_tns():
            if hasattr(self, 'skill_vars'):
                for skill_name in self.skill_vars:
                    update_skill_values(skill_name)
            if hasattr(self, 'prof_rows'):
                for row_data in self.prof_rows:
                    update_single_prof_row(row_data)
            if hasattr(self, 'cs_level_cb'):
                update_cs_values()

        self.recalculate_all_tns = recalculate_all_tns

        #Canvas + Scrollbar
        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)

        main_container = ttk.Frame(canvas)

        main_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=main_container, anchor="nw")

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind('<Configure>', _on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        skills_frame = ttk.LabelFrame(main_container, text="Skills")
        skills_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=5)

        right_container = ttk.Frame(main_container)
        right_container.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=5)

        skills_data = [
            ("Acrobatics", ["Str", "Ag"]),
            ("Alchemy", ["Int"]),
            ("Athletics", ["Str", "End"]),
            ("Command", ["Str", "Int", "Prs"]),
            ("Commerce", ["Int", "Prs"]),
            ("Deceive", ["Int", "Prs"]),
            ("Enchant", ["Int"]),
            ("Evade", ["Ag"]),
            ("Investigate", ["Int", "Prc"]),
            ("Logic", ["Int", "Prc"]),
            ("Lore", ["Int"]),
            ("Navigate", ["Int", "Prc"]),
            ("Observe", ["Prc"]),
            ("Persuade", ["Str", "Prs"]),
            ("Ride", ["Ag"]),
            ("Stealth", ["Ag", "Prc"]),
            ("Subterfuge", ["Ag", "Int"]),
            ("Survival", ["Int", "Prc"])
        ]

        headers = ["Skill", "Level", "Rank", "Bonus", "TN"]
        for i, h in enumerate(headers):
            sticky_val = "w" if i in [0, 4] else ""
            ttk.Label(skills_frame, text=h, font=('Helvetica', 9, 'bold')).grid(row=0, column=i, padx=5, pady=5,
                                                                                sticky=sticky_val)

        self.skill_vars = {}

        for row_idx, (skill_name, stats) in enumerate(skills_data, start=1):
            stats_str = f" ({', '.join(stats)})"
            ttk.Label(skills_frame, text=f"{skill_name}{stats_str}").grid(row=row_idx, column=0, padx=5, pady=2,
                                                                          sticky="w")

            level_cb = ttk.Combobox(skills_frame, values=list(self.skill_ranks_info.keys()), state="readonly",
                                    width=10)
            level_cb.set("Untrained")
            level_cb.grid(row=row_idx, column=1, padx=2, pady=2)

            rank_var = tk.StringVar(value="-1")
            bonus_var = tk.StringVar(value="-20")

            ttk.Entry(skills_frame, textvariable=rank_var, width=4, justify="center", state="readonly").grid(
                row=row_idx, column=2, padx=2, pady=2)
            ttk.Entry(skills_frame, textvariable=bonus_var, width=5, justify="center", state="readonly").grid(
                row=row_idx, column=3, padx=2, pady=2)

            tn_container = ttk.Frame(skills_frame)
            tn_container.grid(row=row_idx, column=4, padx=2, pady=2, sticky="w")

            tn_vars = []
            for stat_idx, stat in enumerate(stats):
                if stat_idx > 0:
                    ttk.Label(tn_container, text=",").pack(side="left", padx=1)

                tn_v = tk.StringVar(value="0")
                tn_vars.append((stat, tn_v))
                ttk.Entry(tn_container, textvariable=tn_v, width=4, justify="center", state="readonly").pack(
                    side="left")

            self.skill_vars[skill_name] = {
                "level_cb": level_cb,
                "rank_var": rank_var,
                "bonus_var": bonus_var,
                "tn_vars": tn_vars,
                "stats": stats
            }

            level_cb.bind("<<ComboboxSelected>>", lambda event, s=skill_name: update_skill_values(s))
            update_skill_values(skill_name)

        # --- PROFESSIONS ---
        prof_frame = ttk.LabelFrame(right_container, text="Professions / Custom Skills")
        prof_frame.pack(fill="x", padx=0, pady=(0, 5))

        prof_headers_frame = ttk.Frame(prof_frame)
        prof_headers_frame.pack(fill="x", padx=2, pady=(5, 2))

        ttk.Label(prof_headers_frame, text="Custom Skill / Profession", font=('Helvetica', 9, 'bold'),
                  width=22).pack(
            side="left", padx=2)
        ttk.Label(prof_headers_frame, text="Level", font=('Helvetica', 9, 'bold'), width=12).pack(side="left",
                                                                                                  padx=2)
        ttk.Label(prof_headers_frame, text="Attributes", font=('Helvetica', 9, 'bold'), width=18).pack(side="left",
                                                                                                       padx=2)
        ttk.Label(prof_headers_frame, text="Rank", font=('Helvetica', 9, 'bold'), width=5).pack(side="left", padx=2)
        ttk.Label(prof_headers_frame, text="Bonus", font=('Helvetica', 9, 'bold'), width=6).pack(side="left",
                                                                                                 padx=2)
        ttk.Label(prof_headers_frame, text="TN", font=('Helvetica', 9, 'bold')).pack(side="left", padx=2)

        prof_rows_container = ttk.Frame(prof_frame)
        prof_rows_container.pack(fill="x", padx=2, pady=2)

        self.prof_rows = []
        attr_options = ["None", "Str", "End", "Ag", "Int", "Wp", "Prc", "Prs"]

        def add_prof_row():
            r_frame = ttk.Frame(prof_rows_container)
            r_frame.pack(fill="x", pady=2)

            name_entry = ttk.Entry(r_frame, width=20)
            name_entry.pack(side="left", padx=2)

            level_cb = ttk.Combobox(r_frame, values=list(self.skill_ranks_info.keys()), state="readonly", width=10)
            level_cb.set("Untrained")
            level_cb.pack(side="left", padx=2)

            attr_cb_frame = ttk.Frame(r_frame)
            attr_cb_frame.pack(side="left", padx=2)

            attr_cbs = []
            for _ in range(3):
                cb = ttk.Combobox(attr_cb_frame, values=attr_options, state="readonly", width=4)
                cb.set("None")
                cb.pack(side="left", padx=1)
                attr_cbs.append(cb)

            rank_var = tk.StringVar(value="-1")
            bonus_var = tk.StringVar(value="-20")

            ttk.Entry(r_frame, textvariable=rank_var, width=4, justify="center", state="readonly").pack(side="left",
                                                                                                        padx=2)
            ttk.Entry(r_frame, textvariable=bonus_var, width=5, justify="center", state="readonly").pack(
                side="left",
                padx=2)

            tn_container = ttk.Frame(r_frame)
            tn_container.pack(side="left", padx=2)

            row_data = {
                "frame": r_frame,
                "name_entry": name_entry,
                "level_cb": level_cb,
                "attr_cbs": attr_cbs,
                "rank_var": rank_var,
                "bonus_var": bonus_var,
                "tn_container": tn_container,
                "tn_entries": []
            }

            def update_this_prof():
                update_single_prof_row(row_data)

            level_cb.bind("<<ComboboxSelected>>", lambda e: update_this_prof())
            for cb in attr_cbs:
                cb.bind("<<ComboboxSelected>>", lambda e: update_this_prof())

            del_btn = ttk.Button(r_frame, text="✕", width=2, command=lambda: remove_prof_row(row_data))
            del_btn.pack(side="right", padx=2)

            self.prof_rows.append(row_data)
            update_this_prof()

        def remove_prof_row(row_data):
            row_data["frame"].destroy()
            if row_data in self.prof_rows:
                self.prof_rows.remove(row_data)

        self.add_prof_row = add_prof_row
        for _ in range(3):
            self.add_prof_row()

        add_prof_btn = ttk.Button(prof_frame, text="+ Add Profession", command=add_prof_row)
        add_prof_btn.pack(anchor="w", padx=5, pady=5)

        # --- COMBAT STYLE (Str, Ag) ---
        cs_frame = ttk.LabelFrame(right_container, text="Combat Style (Str, Ag)")
        cs_frame.pack(fill="x", padx=0, pady=5)

        cs_top = ttk.Frame(cs_frame)
        cs_top.pack(fill="x", padx=5, pady=5)

        ttk.Label(cs_top, text="Style Name:").pack(side="left", padx=(0, 5))
        self.cs_name_entry = ttk.Entry(cs_top, width=18)
        self.cs_name_entry.pack(side="left", padx=(0, 10))

        ttk.Label(cs_top, text="Level:").pack(side="left", padx=(0, 5))
        self.cs_level_cb = ttk.Combobox(cs_top, values=list(self.skill_ranks_info.keys()), state="readonly",
                                        width=10)
        self.cs_level_cb.set("Untrained")
        self.cs_level_cb.pack(side="left", padx=(0, 10))

        ttk.Label(cs_top, text="Rank:").pack(side="left", padx=(0, 2))
        self.cs_rank_var = tk.StringVar(value="-1")
        ttk.Entry(cs_top, textvariable=self.cs_rank_var, width=4, justify="center", state="readonly").pack(
            side="left",
            padx=(0, 10))

        ttk.Label(cs_top, text="Bonus:").pack(side="left", padx=(0, 2))
        self.cs_bonus_var = tk.StringVar(value="-20")
        ttk.Entry(cs_top, textvariable=self.cs_bonus_var, width=5, justify="center", state="readonly").pack(
            side="left",
            padx=(0,
                  10))

        ttk.Label(cs_top, text="TN:").pack(side="left", padx=(0, 2))
        self.cs_tn_str_var = tk.StringVar(value="0")
        self.cs_tn_ag_var = tk.StringVar(value="0")
        ttk.Entry(cs_top, textvariable=self.cs_tn_str_var, width=4, justify="center", state="readonly").pack(
            side="left")
        ttk.Label(cs_top, text=",").pack(side="left", padx=1)
        ttk.Entry(cs_top, textvariable=self.cs_tn_ag_var, width=4, justify="center", state="readonly").pack(
            side="left")

        ttk.Label(cs_frame, text="Weapons / Armor:", font=('Helvetica', 9, 'bold')).pack(anchor="w", padx=5,
                                                                                         pady=(5, 2))

        cs_lines_container = ttk.Frame(cs_frame)
        cs_lines_container.pack(fill="x", padx=5, pady=(0, 5))

        self.cs_lines = []

        def add_cs_line_row():
            r_frame = ttk.Frame(cs_lines_container)
            r_frame.pack(fill="x", pady=1)

            entry = ttk.Entry(r_frame)
            entry.pack(side="left", fill="x", expand=True, padx=(0, 2))

            row_data = {"frame": r_frame, "entry": entry}

            del_btn = ttk.Button(r_frame, text="✕", width=2, command=lambda: remove_cs_line_row(row_data))
            del_btn.pack(side="right")

            self.cs_lines.append(row_data)

        def remove_cs_line_row(row_data):
            row_data["frame"].destroy()
            if row_data in self.cs_lines:
                self.cs_lines.remove(row_data)

        self.add_cs_line_row = add_cs_line_row
        for _ in range(5):
            self.add_cs_line_row = add_cs_line_row

        add_cs_line_btn = ttk.Button(cs_frame, text="+ Add Weapon / Armor", command=add_cs_line_row)
        add_cs_line_btn.pack(anchor="w", padx=5, pady=(0, 5))

        self.cs_level_cb.bind("<<ComboboxSelected>>", lambda event: update_cs_values())
        update_cs_values()

        # --- SPECIALIZATIONS ---
        spec_frame = ttk.LabelFrame(right_container, text="Specializations")
        spec_frame.pack(fill="both", expand=True, padx=0, pady=(5, 0))

        spec_lines_container = ttk.Frame(spec_frame)
        spec_lines_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.spec_lines = []

        def add_spec_line_row():
            r_frame = ttk.Frame(spec_lines_container)
            r_frame.pack(fill="x", pady=1)

            entry = ttk.Entry(r_frame)
            entry.pack(side="left", fill="x", expand=True, padx=(0, 2))

            row_data = {"frame": r_frame, "entry": entry}

            del_btn = ttk.Button(r_frame, text="✕", width=2, command=lambda: remove_spec_line_row(row_data))
            del_btn.pack(side="right")

            self.spec_lines.append(row_data)

        def remove_spec_line_row(row_data):
            row_data["frame"].destroy()
            if row_data in self.spec_lines:
                self.spec_lines.remove(row_data)

        self.add_spec_line_row = add_spec_line_row
        for _ in range(2):
            self.add_spec_line_row = add_spec_line_row

        add_spec_btn = ttk.Button(spec_frame, text="+ Add Specialization", command=add_spec_line_row)
        add_spec_btn.pack(anchor="w", padx=5, pady=(0, 5))
#---------------PAGE3------------------
    def setup_tab3(self, parent):
        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)

        main_container = ttk.Frame(canvas)

        main_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=main_container, anchor="nw")

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind('<Configure>', _on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        left_side = ttk.Frame(main_container)
        left_side.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=5)

        right_side = ttk.Frame(main_container)
        right_side.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=5)

        # ARMOR, SHIELD, NOTES
        armor_frame = ttk.LabelFrame(left_side, text="Armor")
        armor_frame.pack(fill="x", padx=0, pady=(0, 5))

        armor_frame.columnconfigure(0, weight=1)
        armor_frame.columnconfigure(1, weight=1)
        armor_frame.columnconfigure(2, weight=1)

        left_zones = [
            ("Head (0)", "head"),
            ("Right Arm (8)", "r_arm"),
            ("Right Leg (6)", "r_leg")
        ]

        right_zones = [
            ("Body (1-5)", "body"),
            ("Left Arm (9)", "l_arm"),
            ("Left Leg (7)", "l_leg")
        ]

        self.armor_vars = {}

        left_arm_container = ttk.Frame(armor_frame)
        left_arm_container.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        for label_text, zone_key in left_zones:
            z_frame = ttk.LabelFrame(left_arm_container, text=label_text)
            z_frame.pack(fill="x", pady=2)

            self.armor_vars[zone_key] = {
                "ar": tk.StringVar(),
                "enc": tk.StringVar(),
                "type": tk.StringVar()
            }

            ttk.Label(z_frame, text="AR:").grid(row=0, column=0, padx=2, pady=1, sticky="e")
            ttk.Entry(z_frame, textvariable=self.armor_vars[zone_key]["ar"], width=8).grid(row=0, column=1, padx=2,
                                                                                           pady=1)

            ttk.Label(z_frame, text="ENC:").grid(row=1, column=0, padx=2, pady=1, sticky="e")
            ttk.Entry(z_frame, textvariable=self.armor_vars[zone_key]["enc"], width=8).grid(row=1, column=1, padx=2,
                                                                                            pady=1)

            ttk.Label(z_frame, text="Type:").grid(row=2, column=0, padx=2, pady=1, sticky="e")
            ttk.Entry(z_frame, textvariable=self.armor_vars[zone_key]["type"], width=8).grid(row=2, column=1, padx=2,
                                                                                             pady=1)

        center_arm_container = ttk.Frame(armor_frame)
        center_arm_container.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        body_canvas = tk.Canvas(center_arm_container, width=120, height=240, bg="#f0f0f0", highlightthickness=1,
                                highlightbackground="#ccc")
        body_canvas.pack(expand=True)
        body_canvas.create_text(60, 120, text="[ Character ]", fill="#888888", justify="center")

        right_arm_container = ttk.Frame(armor_frame)
        right_arm_container.grid(row=0, column=2, padx=5, pady=5, sticky="n")

        for label_text, zone_key in right_zones:
            z_frame = ttk.LabelFrame(right_arm_container, text=label_text)
            z_frame.pack(fill="x", pady=2)

            self.armor_vars[zone_key] = {
                "ar": tk.StringVar(),
                "enc": tk.StringVar(),
                "type": tk.StringVar()
            }

            ttk.Label(z_frame, text="AR:").grid(row=0, column=0, padx=2, pady=1, sticky="e")
            ttk.Entry(z_frame, textvariable=self.armor_vars[zone_key]["ar"], width=8).grid(row=0, column=1, padx=2,
                                                                                           pady=1)

            ttk.Label(z_frame, text="ENC:").grid(row=1, column=0, padx=2, pady=1, sticky="e")
            ttk.Entry(z_frame, textvariable=self.armor_vars[zone_key]["enc"], width=8).grid(row=1, column=1, padx=2,
                                                                                            pady=1)

            ttk.Label(z_frame, text="Type:").grid(row=2, column=0, padx=2, pady=1, sticky="e")
            ttk.Entry(z_frame, textvariable=self.armor_vars[zone_key]["type"], width=8).grid(row=2, column=1, padx=2,
                                                                                             pady=1)

        # 4. Shield
        shield_frame = ttk.Frame(armor_frame)
        shield_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=(2, 5), sticky="ew")

        ttk.Label(shield_frame, text="Shield (BR/Type/ENC):", font=('Helvetica', 8, 'bold')).pack(side="left",
                                                                                                  padx=(0, 2))
        self.shield_var = tk.StringVar()
        ttk.Entry(shield_frame, textvariable=self.shield_var).pack(side="left", fill="x", expand=True)

        notes_frame = ttk.LabelFrame(left_side, text="Armor Notes")
        notes_frame.pack(fill="x", pady=2)
        self.armor_notes_text = tk.Text(notes_frame, height=4, wrap="word")
        self.armor_notes_text.pack(fill="both", expand=True, padx=2, pady=2)

        wounds_frame = ttk.LabelFrame(left_side, text="Wounds")
        wounds_frame.pack(fill="x", pady=2)
        self.wounds_text = tk.Text(wounds_frame, height=4, wrap="word")
        self.wounds_text.pack(fill="both", expand=True, padx=2, pady=2)

        conditions_frame = ttk.LabelFrame(left_side, text="Conditions")
        conditions_frame.pack(fill="x", pady=2)
        self.conditions_text = tk.Text(conditions_frame, height=4, wrap="word")
        self.conditions_text.pack(fill="both", expand=True, padx=2, pady=2)

        # PRAWA STRONA: WEAPONS & AMMUNITION
        dmg_options = ["1d4", "1d6", "1d8", "1d10", "1d12", "2d8", "2d10", "2d12"]
        bonus_mat_options = [f"+{i}" for i in range(0, 11)]
        h_options = ["1H", "2H"]

        self.weapons_vars = {"melee": [], "ranged": [], "ammo": []}

        def build_dynamic_weapon_table(parent_frame, title, category_key):
            frame = ttk.LabelFrame(parent_frame, text=title)
            frame.pack(fill="x", pady=(0, 5))

            headers_frame = ttk.Frame(frame)
            headers_frame.pack(fill="x", padx=2, pady=(2, 0))

            rows_container = ttk.Frame(frame)
            rows_container.pack(fill="x", padx=2, pady=2)

            if category_key == "melee":
                headers = [("Name", 0), ("Dmg", 8), ("Mat. Bonus", 10), ("H", 6), ("Reach", 6), ("ENC", 5)]
                for text, w in headers:
                    if w == 0:
                        ttk.Label(headers_frame, text=text, font=('Helvetica', 8, 'bold')).pack(side="left", fill="x", expand=True, padx=2)
                    else:
                        ttk.Label(headers_frame, text=text, font=('Helvetica', 8, 'bold'), width=w).pack(side="left", padx=2)
                ttk.Label(headers_frame, text="", width=3).pack(side="right")

                def add_melee_row():
                    row_frame = ttk.Frame(rows_container)
                    row_frame.pack(fill="x", pady=2)

                    top_row = ttk.Frame(row_frame)
                    top_row.pack(fill="x")

                    del_btn = ttk.Button(top_row, text="✕", width=2, command=lambda: remove_row(item_data))
                    del_btn.pack(side="right", padx=(2, 0))

                    enc_entry = ttk.Entry(top_row, width=5, justify="center")
                    enc_entry.pack(side="right", padx=2)

                    reach_entry = ttk.Entry(top_row, width=6, justify="center")
                    reach_entry.pack(side="right", padx=2)

                    h_cb = ttk.Combobox(top_row, values=h_options, state="readonly", width=4)
                    h_cb.set("1H")
                    h_cb.pack(side="right", padx=2)

                    mat_cb = ttk.Combobox(top_row, values=bonus_mat_options, state="readonly", width=5)
                    mat_cb.set("+0")
                    mat_cb.pack(side="right", padx=2)

                    dmg_cb = ttk.Combobox(top_row, values=dmg_options, state="readonly", width=6)
                    dmg_cb.set("1d4")
                    dmg_cb.pack(side="right", padx=2)

                    name_entry = ttk.Entry(top_row)
                    name_entry.pack(side="left", fill="x", expand=True, padx=2)

                    qualities_frame = ttk.Frame(row_frame)
                    qualities_frame.pack(fill="x", padx=2, pady=(2, 0))

                    crushing_var = tk.BooleanVar()
                    splitting_var = tk.BooleanVar()
                    slashing_var = tk.BooleanVar()

                    ttk.Checkbutton(qualities_frame, text="Crushing", variable=crushing_var).pack(side="left", padx=(0, 4))
                    ttk.Checkbutton(qualities_frame, text="Splitting", variable=splitting_var).pack(side="left", padx=4)
                    ttk.Checkbutton(qualities_frame, text="Slashing", variable=slashing_var).pack(side="left", padx=4)

                    ttk.Label(qualities_frame, text="Other:").pack(side="left", padx=(8, 2))
                    other_qualities_entry = ttk.Entry(qualities_frame)
                    other_qualities_entry.pack(side="left", fill="x", expand=True, padx=(0, 2))

                    sep = ttk.Separator(row_frame, orient="horizontal")
                    sep.pack(fill="x", pady=4)

                    item_data = {
                        "frame": row_frame,
                        "name": name_entry,
                        "dmg": dmg_cb,
                        "mat_bonus": mat_cb,
                        "h": h_cb,
                        "reach": reach_entry,
                        "enc": enc_entry,
                        "qualities": {
                            "crushing": crushing_var,
                            "splitting": splitting_var,
                            "slashing": slashing_var,
                            "other": other_qualities_entry
                        }
                    }

                    self.weapons_vars["melee"].append(item_data)
                    self.add_melee_row = add_melee_row

                def remove_row(item_data):
                    item_data["frame"].destroy()
                    if item_data in self.weapons_vars["melee"]:
                        self.weapons_vars["melee"].remove(item_data)

                for _ in range(3):
                    add_melee_row()

                btn = ttk.Button(frame, text="+ Add Melee Weapon", command=add_melee_row)
                btn.pack(anchor="w", padx=5, pady=5)

            elif category_key == "ranged":
                headers = [("Type", 0), ("Dmg", 8), ("H", 6), ("Range (Short / Med / Long)", 24), ("ENC", 5)]
                for text, w in headers:
                    if w == 0:
                        ttk.Label(headers_frame, text=text, font=('Helvetica', 8, 'bold')).pack(side="left", fill="x", expand=True, padx=2)
                    else:
                        ttk.Label(headers_frame, text=text, font=('Helvetica', 8, 'bold'), width=w).pack(side="left", padx=2)
                ttk.Label(headers_frame, text="", width=3).pack(side="right")

                def add_ranged_row():
                    row_frame = ttk.Frame(rows_container)
                    row_frame.pack(fill="x", pady=2)

                    top_row = ttk.Frame(row_frame)
                    top_row.pack(fill="x")

                    del_btn = ttk.Button(top_row, text="✕", width=2, command=lambda: remove_row(item_data))
                    del_btn.pack(side="right", padx=(2, 0))

                    enc_entry = ttk.Entry(top_row, width=5, justify="center")
                    enc_entry.pack(side="right", padx=2)

                    range_frame = ttk.Frame(top_row)
                    range_frame.pack(side="right", padx=2)

                    r1_entry = ttk.Entry(range_frame, width=4, justify="center")
                    r1_entry.pack(side="left")
                    ttk.Label(range_frame, text="/").pack(side="left")

                    r2_entry = ttk.Entry(range_frame, width=4, justify="center")
                    r2_entry.pack(side="left")
                    ttk.Label(range_frame, text="/").pack(side="left")

                    r3_entry = ttk.Entry(range_frame, width=4, justify="center")
                    r3_entry.pack(side="left")

                    h_cb = ttk.Combobox(top_row, values=h_options, state="readonly", width=4)
                    h_cb.set("2H")
                    h_cb.pack(side="right", padx=2)

                    dmg_cb = ttk.Combobox(top_row, values=dmg_options, state="readonly", width=6)
                    dmg_cb.set("1d4")
                    dmg_cb.pack(side="right", padx=2)

                    type_entry = ttk.Entry(top_row)
                    type_entry.pack(side="left", fill="x", expand=True, padx=2)

                    qualities_frame = ttk.Frame(row_frame)
                    qualities_frame.pack(fill="x", padx=2, pady=(2, 0))

                    ttk.Label(qualities_frame, text="Qualities:").pack(side="left", padx=(0, 5))
                    qualities_entry = ttk.Entry(qualities_frame)
                    qualities_entry.pack(side="left", fill="x", expand=True, padx=(0, 2))

                    sep = ttk.Separator(row_frame, orient="horizontal")
                    sep.pack(fill="x", pady=4)

                    item_data = {
                        "frame": row_frame,
                        "type": type_entry,
                        "dmg": dmg_cb,
                        "h": h_cb,
                        "range_short": r1_entry,
                        "range_med": r2_entry,
                        "range_long": r3_entry,
                        "qualities": qualities_entry,
                        "enc": enc_entry
                    }

                    self.weapons_vars["ranged"].append(item_data)
                    self.add_ranged_row = add_ranged_row

                def remove_row(item_data):
                    item_data["frame"].destroy()
                    if item_data in self.weapons_vars["ranged"]:
                        self.weapons_vars["ranged"].remove(item_data)

                for _ in range(3):
                    add_ranged_row()

                btn = ttk.Button(frame, text="+ Add Ranged Weapon", command=add_ranged_row)
                btn.pack(anchor="w", padx=5, pady=5)

            elif category_key == "ammo":
                headers = [("Qty", 6), ("Name", 0), ("Dam Mod", 10), ("Qualities", 0), ("ENC", 5)]
                for text, w in headers:
                    if w == 0:
                        ttk.Label(headers_frame, text=text, font=('Helvetica', 8, 'bold')).pack(side="left", fill="x", expand=True, padx=2)
                    else:
                        ttk.Label(headers_frame, text=text, font=('Helvetica', 8, 'bold'), width=w).pack(side="left", padx=2)
                ttk.Label(headers_frame, text="", width=3).pack(side="right")

                def add_ammo_row():
                    row_frame = ttk.Frame(rows_container)
                    row_frame.pack(fill="x", pady=2)

                    del_btn = ttk.Button(row_frame, text="✕", width=2, command=lambda: remove_row(item_data))
                    del_btn.pack(side="right", padx=(2, 0))

                    enc_entry = ttk.Entry(row_frame, width=5, justify="center")
                    enc_entry.pack(side="right", padx=2)

                    qualities_entry = ttk.Entry(row_frame)
                    qualities_entry.pack(side="right", fill="x", expand=True, padx=2)

                    dam_mod_entry = ttk.Entry(row_frame, width=8, justify="center")
                    dam_mod_entry.pack(side="right", padx=2)

                    qty_entry = ttk.Entry(row_frame, width=5, justify="center")
                    qty_entry.pack(side="left", padx=2)

                    name_entry = ttk.Entry(row_frame)
                    name_entry.pack(side="left", fill="x", expand=True, padx=2)

                    item_data = {
                        "frame": row_frame,
                        "qty": qty_entry,
                        "name": name_entry,
                        "dam_mod": dam_mod_entry,
                        "qualities": qualities_entry,
                        "enc": enc_entry
                    }

                    self.weapons_vars["ammo"].append(item_data)
                    self.add_ammo_row = add_ammo_row

                def remove_row(item_data):
                    item_data["frame"].destroy()
                    if item_data in self.weapons_vars["ammo"]:
                        self.weapons_vars["ammo"].remove(item_data)

                for _ in range(3):
                    add_ammo_row()

                btn = ttk.Button(frame, text="+ Add Ammunition", command=add_ammo_row)
                btn.pack(anchor="w", padx=5, pady=5)

        build_dynamic_weapon_table(right_side, "Melee Weapons", "melee")
        build_dynamic_weapon_table(right_side, "Ranged Weapons", "ranged")
        build_dynamic_weapon_table(right_side, "Ammunition", "ammo")

# ---------------PAGE4------------------
    def setup_tab4(self, parent):
        #Items & Equipment
        main_container = ttk.Frame(parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        eq_frame = ttk.LabelFrame(main_container, text="Items & Equipment")
        eq_frame.pack(fill="both", expand=True, padx=5, pady=5)

        eq_frame.columnconfigure(0, weight=1)
        eq_frame.columnconfigure(1, weight=1)

        self.equipment_vars = []
        self.equipment_rows = []  # Przechowuje pełne obiekty wierszy do zapisu/odczytu

        #Items & Equipment
        left_eq_frame = ttk.Frame(eq_frame)
        left_eq_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        left_eq_frame.columnconfigure(1, weight=1)

        ttk.Label(left_eq_frame, text="Qty", font=('Helvetica', 9, 'bold')).grid(row=0, column=0, padx=2, pady=2)
        ttk.Label(left_eq_frame, text="Items & Equipment", font=('Helvetica', 9, 'bold')).grid(row=0, column=1, padx=2,
                                                                                               pady=2, sticky="w")
        ttk.Label(left_eq_frame, text="ENC", font=('Helvetica', 9, 'bold')).grid(row=0, column=2, padx=2, pady=2)

        for i in range(1, 15):
            qty_entry = ttk.Entry(left_eq_frame, width=4, justify="center")
            qty_entry.grid(row=i, column=0, padx=2, pady=1)

            item_entry = ttk.Entry(left_eq_frame)
            item_entry.grid(row=i, column=1, padx=2, pady=1, sticky="ew")

            enc_var = tk.StringVar()
            enc_entry = ttk.Entry(left_eq_frame, textvariable=enc_var, width=6, justify="center")
            enc_entry.grid(row=i, column=2, padx=2, pady=1)

            enc_var.trace_add("write", self.calculate_total_enc)
            self.equipment_vars.append(enc_var)
            self.equipment_rows.append({
                "qty": qty_entry,
                "item": item_entry,
                "enc_var": enc_var
            })

        right_eq_frame = ttk.Frame(eq_frame)
        right_eq_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        right_eq_frame.columnconfigure(1, weight=1)

        ttk.Label(right_eq_frame, text="Qty", font=('Helvetica', 9, 'bold')).grid(row=0, column=0, padx=2, pady=2)
        ttk.Label(right_eq_frame, text="Items & Equipment (Cont.)", font=('Helvetica', 9, 'bold')).grid(row=0, column=1,
                                                                                                        padx=2, pady=2,
                                                                                                        sticky="w")
        ttk.Label(right_eq_frame, text="ENC", font=('Helvetica', 9, 'bold')).grid(row=0, column=2, padx=2, pady=2)

        for i in range(1, 13):
            qty_entry = ttk.Entry(right_eq_frame, width=4, justify="center")
            qty_entry.grid(row=i, column=0, padx=2, pady=1)

            item_entry = ttk.Entry(right_eq_frame)
            item_entry.grid(row=i, column=1, padx=2, pady=1, sticky="ew")

            enc_var = tk.StringVar()
            enc_entry = ttk.Entry(right_eq_frame, textvariable=enc_var, width=6, justify="center")
            enc_entry.grid(row=i, column=2, padx=2, pady=1)

            enc_var.trace_add("write", lambda *args: self.calculate_total_enc())
            self.equipment_vars.append(enc_var)
            self.equipment_rows.append({
                "qty": qty_entry,
                "item": item_entry,
                "enc_var": enc_var
            })

        # 3. Total ENC & Drakes
        summary_frame = ttk.Frame(right_eq_frame)
        summary_frame.grid(row=13, column=0, columnspan=3, padx=2, pady=(15, 5), sticky="e")

        ttk.Label(summary_frame, text="Total ENC:", font=('Helvetica', 9, 'bold')).grid(row=0, column=0, padx=5, pady=2,
                                                                                        sticky="e")
        self.total_enc_var = tk.StringVar(value="0")
        ttk.Entry(summary_frame, textvariable=self.total_enc_var, width=8, justify="center", state="readonly").grid(
            row=0, column=1, padx=2, pady=2)

        ttk.Label(summary_frame, text="Drakes:", font=('Helvetica', 9, 'bold')).grid(row=1, column=0, padx=5, pady=2,
                                                                                     sticky="e")
        self.drakes_var = tk.StringVar(value="0")
        ttk.Entry(summary_frame, textvariable=self.drakes_var, width=10, justify="center").grid(row=1, column=1, padx=2,
                                                                                                pady=2)

    def calculate_total_enc(self, *args):
        total = 0.0
        if hasattr(self, "equipment_vars"):
            for enc_var in self.equipment_vars:
                val_str = enc_var.get().strip().replace(',', '.')
                if val_str:
                    try:
                        total += float(val_str)
                    except ValueError:
                        pass

        if hasattr(self, "total_enc_var"):
            if total.is_integer():
                self.total_enc_var.set(str(int(total)))
            else:
                self.total_enc_var.set(f"{total:.1f}")
# ---------------PAGE5------------------
    def setup_tab5(self, parent):
        main_canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=main_canvas.yview)

        scrollable_frame = ttk.Frame(main_canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        self.ttp_data = {
            "talents": [],
            "traits": [],
            "powers": []
        }
        self.ttp_containers = {}

        self._build_collapsible_section(scrollable_frame, "Talents", "talents")
        self._build_collapsible_section(scrollable_frame, "Traits", "traits")
        self._build_collapsible_section(scrollable_frame, "Powers", "powers")

    def _build_collapsible_section(self, parent, section_title, category_key):
        collapsible = CollapsibleFrame(parent, title=section_title)
        collapsible.pack(fill="x", expand=True, padx=5, pady=5)

        container = collapsible.content_frame

        headers_frame = ttk.Frame(container)
        headers_frame.pack(fill="x", pady=(0, 2))

        ttk.Label(headers_frame, text=f"{section_title} Name", font=('Helvetica', 9, 'bold'), width=100).pack(
            side="left", padx=2)
        ttk.Label(headers_frame, text="Effects / Notes", font=('Helvetica', 9, 'bold')).pack(side="left", padx=5)

        rows_container = ttk.Frame(container)
        rows_container.pack(fill="x", expand=True)

        self.ttp_containers[category_key] = rows_container

        add_btn = ttk.Button(
            container,
            text=f"+ Add {section_title[:-1] if section_title.endswith('s') else section_title}",
            command=lambda: self._add_ttp_row(rows_container, category_key)
        )
        add_btn.pack(anchor="w", pady=5, padx=2)

        for _ in range(3):
            self._add_ttp_row(rows_container, category_key)

    def _add_ttp_row(self, container, category_key):
        row_frame = ttk.Frame(container)
        row_frame.pack(fill="x", pady=2)

        name_entry = ttk.Entry(row_frame, width=25)
        name_entry.pack(side="left", padx=2)

        effect_entry = ttk.Entry(row_frame)
        effect_entry.pack(side="left", fill="x", expand=True, padx=2)

        row_data = {
            "frame": row_frame,
            "name": name_entry,
            "effect": effect_entry
        }

        remove_btn = ttk.Button(
            row_frame,
            text="✕",
            width=3,
            command=lambda: self._remove_ttp_row(category_key, row_data)
        )
        remove_btn.pack(side="right", padx=2)

        self.ttp_data[category_key].append(row_data)

    def _remove_ttp_row(self, category_key, row_data):
        row_data["frame"].destroy()
        self.ttp_data[category_key].remove(row_data)

    def _add_ttp_row_with_data(self, category_key, name_text="", effect_text=""):
        if category_key in self.ttp_containers:
            container = self.ttp_containers[category_key]
            self._add_ttp_row(container, category_key)
            last_row = self.ttp_data[category_key][-1]
            last_row["name"].insert(0, str(name_text))
            last_row["effect"].insert(0, str(effect_text))
# ---------------PAGE6------------------
    def setup_tab6(self, parent):
        main_canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=main_canvas.yview)

        scrollable_frame = ttk.Frame(main_canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        container = ttk.Frame(scrollable_frame)
        container.pack(fill="both", expand=True, padx=5, pady=5)

        left_side = ttk.Frame(container)
        left_side.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_side = ttk.Frame(container)
        right_side.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.spellcasting_vars = {}
        self.custom_magic_skills = []
        self.specializations_vars = []
        self.rituals_vars = []
        self.spells_vars = []

        # 1. SPELLCASTING SKILLS
        spell_frame = ttk.LabelFrame(left_side, text="Spellcasting Skills")
        spell_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(spell_frame, text="Skill", font=('Helvetica', 8, 'bold')).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        ttk.Label(spell_frame, text="Level", font=('Helvetica', 8, 'bold')).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(spell_frame, text="Rank", font=('Helvetica', 8, 'bold')).grid(row=0, column=2, padx=2, pady=2)
        ttk.Label(spell_frame, text="Bonus", font=('Helvetica', 8, 'bold')).grid(row=0, column=3, padx=2, pady=2)
        ttk.Label(spell_frame, text="TN", font=('Helvetica', 8, 'bold')).grid(row=0, column=4, padx=2, pady=2)

        magic_schools = [
            ("Alteration (Wp)", "alteration", "Wp"),
            ("Conjuration (Wp)", "conjuration", "Wp"),
            ("Destruction (Wp)", "destruction", "Wp"),
            ("Illusion (Wp)", "illusion", "Wp"),
            ("Mysticism (Wp)", "mysticism", "Wp"),
            ("Necromancy (Int)", "necromancy", "Int"),
            ("Restoration (Wp)", "restoration", "Wp")
        ]

        current_row = 1
        for label_text, school_key, main_attr in magic_schools:
            ttk.Label(spell_frame, text=label_text).grid(row=current_row, column=0, padx=5, pady=2, sticky="w")

            level_cb = ttk.Combobox(spell_frame, values=list(getattr(self, 'skill_ranks_info', {}).keys()), state="readonly", width=10)
            level_cb.set("Untrained")
            level_cb.grid(row=current_row, column=1, padx=2, pady=2)

            rank_var = tk.StringVar(value="-1")
            bonus_var = tk.StringVar(value="-20")
            tn_var = tk.StringVar(value="0")

            ttk.Entry(spell_frame, textvariable=rank_var, width=4, justify="center", state="readonly").grid(
                row=current_row, column=2, padx=2, pady=2)
            ttk.Entry(spell_frame, textvariable=bonus_var, width=5, justify="center", state="readonly").grid(
                row=current_row, column=3, padx=2, pady=2)
            ttk.Entry(spell_frame, textvariable=tn_var, width=5, justify="center", state="readonly").grid(
                row=current_row, column=4, padx=2, pady=2)

            self.spellcasting_vars[school_key] = {
                "level_cb": level_cb,
                "rank_var": rank_var,
                "bonus_var": bonus_var,
                "tn_var": tn_var,
                "attr": main_attr
            }

            level_cb.bind("<<ComboboxSelected>>", lambda event, k=school_key: self.update_magic_skill_values(k))
            self.update_magic_skill_values(school_key)
            current_row += 1

        # Custom Magic Skills
        ttk.Separator(spell_frame, orient="horizontal").grid(row=current_row, column=0, columnspan=5, sticky="ew", pady=5)
        current_row += 1

        ttk.Label(spell_frame, text="Custom Magic Skills", font=('Helvetica', 8, 'bold')).grid(row=current_row, column=0, columnspan=5, padx=5, pady=2, sticky="w")
        current_row += 1

        custom_skills_container = ttk.Frame(spell_frame)
        custom_skills_container.grid(row=current_row, column=0, columnspan=5, sticky="ew", padx=2)

        def add_custom_skill_row():
            r_frame = ttk.Frame(custom_skills_container)
            r_frame.pack(fill="x", pady=1)

            name_e = ttk.Entry(r_frame, width=15)
            name_e.pack(side="left", padx=2)

            attr_cb = ttk.Combobox(r_frame, values=["Wp", "Int"], width=3, state="readonly")
            attr_cb.set("Wp")
            attr_cb.pack(side="left", padx=2)

            level_cb = ttk.Combobox(r_frame, values=list(getattr(self, 'skill_ranks_info', {}).keys()), state="readonly", width=10)
            level_cb.set("Untrained")
            level_cb.pack(side="left", padx=2)

            rank_var = tk.StringVar(value="-1")
            bonus_var = tk.StringVar(value="-20")
            tn_var = tk.StringVar(value="0")

            ttk.Entry(r_frame, textvariable=rank_var, width=4, justify="center", state="readonly").pack(side="left", padx=2)
            ttk.Entry(r_frame, textvariable=bonus_var, width=5, justify="center", state="readonly").pack(side="left", padx=2)
            ttk.Entry(r_frame, textvariable=tn_var, width=5, justify="center", state="readonly").pack(side="left", padx=2)

            row_data = {
                "frame": r_frame,
                "name": name_e,
                "attr_cb": attr_cb,
                "level_cb": level_cb,
                "rank_var": rank_var,
                "bonus_var": bonus_var,
                "tn_var": tn_var
            }

            def update_custom_row():
                lvl = level_cb.get()
                rank, bonus = getattr(self, 'skill_ranks_info', {}).get(lvl, (-1, -20))
                rank_var.set(str(rank))
                bonus_var.set(f"+{bonus}" if bonus >= 0 else str(bonus))

                selected_attr = attr_cb.get()
                attr_val_str = getattr(self, "attr_vars", {}).get(selected_attr, tk.StringVar(value="0")).get()
                try:
                    attr_val = int(attr_val_str)
                except ValueError:
                    attr_val = 0
                tn_var.set(str(attr_val + bonus))

            level_cb.bind("<<ComboboxSelected>>", lambda e: update_custom_row())
            attr_cb.bind("<<ComboboxSelected>>", lambda e: update_custom_row())
            update_custom_row()

            del_btn = ttk.Button(r_frame, text="✕", width=2, command=lambda: remove_custom_skill(row_data))
            del_btn.pack(side="right", padx=2)

            self.custom_magic_skills.append(row_data)

        def remove_custom_skill(row_data):
            row_data["frame"].destroy()
            if row_data in self.custom_magic_skills:
                self.custom_magic_skills.remove(row_data)

        self.add_custom_skill_row = add_custom_skill_row
        self.add_custom_skill_row()

        add_skill_btn = ttk.Button(spell_frame, text="+ Add Custom Skill", command=self.add_custom_skill_row)
        add_skill_btn.grid(row=current_row + 1, column=0, columnspan=5, pady=5, padx=5, sticky="w")

        # 2. SPECIALIZATIONS
        spec_frame = ttk.LabelFrame(left_side, text="Specializations")
        spec_frame.pack(fill="x", pady=(5, 10))

        spec_container = ttk.Frame(spec_frame)
        spec_container.pack(fill="x", expand=True, padx=5, pady=2)

        def add_spec_row():
            r_frame = ttk.Frame(spec_container)
            r_frame.pack(fill="x", pady=1)

            spec_entry = ttk.Entry(r_frame)
            spec_entry.pack(side="left", fill="x", expand=True, padx=2)

            row_data = {"frame": r_frame, "entry": spec_entry}

            del_btn = ttk.Button(r_frame, text="✕", width=2, command=lambda: remove_spec_row(row_data))
            del_btn.pack(side="right", padx=2)

            self.specializations_vars.append(row_data)

        def remove_spec_row(row_data):
            row_data["frame"].destroy()
            if row_data in self.specializations_vars:
                self.specializations_vars.remove(row_data)

        self.add_spec_row = add_spec_row
        self.add_spec_row()

        add_spec_btn = ttk.Button(spec_frame, text="+ Add Specialization", command=self.add_spec_row)
        add_spec_btn.pack(anchor="w", padx=5, pady=5)

        # 3. RITUALS
        rituals_frame = ttk.LabelFrame(left_side, text="Rituals")
        rituals_frame.pack(fill="x", pady=(0, 10))

        rituals_container = ttk.Frame(rituals_frame)
        rituals_container.pack(fill="x", expand=True, padx=5, pady=2)

        r_header = ttk.Frame(rituals_container)
        r_header.pack(fill="x", pady=(0, 2))
        ttk.Label(r_header, text="Ritual Name", font=('Helvetica', 8, 'bold'), width=22).pack(side="left", padx=2)
        ttk.Label(r_header, text="Effects / Notes", font=('Helvetica', 8, 'bold')).pack(side="left", padx=5)

        r_rows_frame = ttk.Frame(rituals_container)
        r_rows_frame.pack(fill="x", expand=True)

        def add_ritual_row():
            r_frame = ttk.Frame(r_rows_frame)
            r_frame.pack(fill="x", pady=2)

            name_entry = ttk.Entry(r_frame, width=22)
            name_entry.pack(side="left", padx=2)

            notes_entry = ttk.Entry(r_frame)
            notes_entry.pack(side="left", fill="x", expand=True, padx=2)

            row_data = {"frame": r_frame, "name": name_entry, "notes": notes_entry}

            del_btn = ttk.Button(r_frame, text="✕", width=2, command=lambda: remove_ritual_row(row_data))
            del_btn.pack(side="right", padx=2)

            self.rituals_vars.append(row_data)

        def remove_ritual_row(row_data):
            row_data["frame"].destroy()
            if row_data in self.rituals_vars:
                self.rituals_vars.remove(row_data)

        self.add_ritual_row = add_ritual_row
        self.add_ritual_row()

        add_ritual_btn = ttk.Button(rituals_frame, text="+ Add Ritual", command=self.add_ritual_row)
        add_ritual_btn.pack(anchor="w", padx=5, pady=5)

        # 4. SPELLS
        spells_main_frame = ttk.LabelFrame(right_side, text="Spells")
        spells_main_frame.pack(fill="both", expand=True, pady=(0, 10))

        spells_grid_container = ttk.Frame(spells_main_frame)
        spells_grid_container.pack(fill="both", expand=True, padx=2, pady=5)

        def create_single_spell_card(parent_frame, row_ref):
            card = ttk.LabelFrame(parent_frame, text="Spell")

            header_frame = ttk.Frame(card)
            header_frame.pack(fill="x", padx=2, pady=2)

            del_btn = ttk.Button(header_frame, text="✕", width=2)
            del_btn.pack(side="right")

            top_info = ttk.Frame(header_frame)
            top_info.pack(side="left", fill="x", expand=True)

            ttk.Label(top_info, text="Name:", font=('Helvetica', 8, 'bold')).pack(side="left", padx=(0, 1))
            name_entry = ttk.Entry(top_info, width=10)
            name_entry.pack(side="left", padx=(0, 2), fill="x", expand=True)

            ttk.Label(top_info, text="Attr.:", font=('Helvetica', 8, 'bold')).pack(side="left", padx=(1, 1))
            attr_entry = ttk.Entry(top_info, width=15)
            attr_entry.pack(side="left", padx=(0, 2), fill="x", expand=True)

            body_frame = ttk.Frame(card)
            body_frame.pack(fill="both", expand=True, padx=2, pady=2)

            table_frame = ttk.Frame(body_frame)
            table_frame.pack(fill="x", pady=2)

            grid_entries = {
                "Level": [],
                "Cost": [],
                "Spell Str.": []
            }

            rows_labels = ["Level", "Cost", "Spell Str."]
            for r_idx, label_name in enumerate(rows_labels):
                ttk.Label(table_frame, text=label_name, font=('Helvetica', 7, 'bold'), width=8, anchor="e").grid(
                    row=r_idx, column=0, padx=(0, 2), pady=1, sticky="e"
                )
                for c_idx in range(7):
                    e = ttk.Entry(table_frame, width=2, justify="center")
                    e.grid(row=r_idx, column=c_idx + 1, padx=1, pady=1)
                    grid_entries[label_name].append(e)

            desc_frame = ttk.Frame(body_frame)
            desc_frame.pack(fill="both", expand=True, pady=(2, 0))

            ttk.Label(desc_frame, text="Description:", font=('Helvetica', 8, 'bold')).pack(anchor="w")
            desc_text = tk.Text(desc_frame, height=3, width=18, wrap="word")
            desc_text.pack(fill="both", expand=True, pady=1)

            card_data = {
                "card_frame": card,
                "del_btn": del_btn,
                "name": name_entry,
                "attr": attr_entry,
                "grid": grid_entries,
                "description": desc_text
            }

            def remove_this_card():
                card.destroy()
                row_ref["active_cards"] -= 1
                if row_ref["active_cards"] <= 0:
                    row_ref["row_frame"].destroy()
                    if row_ref in self.spells_vars:
                        self.spells_vars.remove(row_ref)

            del_btn.config(command=remove_this_card)
            return card_data

        def add_spell_trio_row():
            row_frame = ttk.Frame(spells_grid_container)
            row_frame.pack(fill="x", pady=4)

            row_data = {
                "row_frame": row_frame,
                "active_cards": 3,
                "cards": []
            }

            for _ in range(3):
                card_data = create_single_spell_card(row_frame, row_data)
                card_data["card_frame"].pack(side="left", fill="both", expand=True, padx=2)
                row_data["cards"].append(card_data)

            self.spells_vars.append(row_data)

        self.add_spell_trio_row = add_spell_trio_row

        for _ in range(2):
            self.add_spell_trio_row()

        add_spell_btn = ttk.Button(spells_main_frame, text="+ Add Spells", command=self.add_spell_trio_row)
        add_spell_btn.pack(anchor="w", padx=5, pady=5)

    def update_magic_skill_values(self, school_key):
        if not hasattr(self, 'spellcasting_vars') or school_key not in self.spellcasting_vars:
            return

        data = self.spellcasting_vars[school_key]
        selected_level = data["level_cb"].get()

        rank, bonus = getattr(self, 'skill_ranks_info', {}).get(selected_level, (-1, -20))

        data["rank_var"].set(str(rank))
        data["bonus_var"].set(f"+{bonus}" if bonus >= 0 else str(bonus))

        attr_key = data["attr"]
        attr_val_str = getattr(self, "attr_vars", {}).get(attr_key, tk.StringVar(value="0")).get()
        try:
            attr_val = int(attr_val_str)
        except ValueError:
            attr_val = 0

        data["tn_var"].set(str(attr_val + bonus))
# ---------------SAVE&LOAD------------------
    def setup_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Save Character...", command=self.save_to_json, accelerator="Ctrl+S")
        file_menu.add_command(label="Open Character...", command=self.load_from_json, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        self.bind("<Control-s>", lambda e: self.save_to_json())
        self.bind("<Control-o>", lambda e: self.load_from_json())

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save character data to json file"
        )
        if not filename:
            return

        entries = getattr(self, "tab1_entries", {})
        get_entry = lambda key: entries[key].get() if key in entries else ""

        derived = getattr(self, "derived_attr_vars", {})
        attributes_data = {}
        attributes_max_data = {}

        for k, widget in derived.items():
            if isinstance(widget, tuple):
                attributes_data[k] = widget[0].get()
                attributes_max_data[k] = widget[1].get()
            else:
                attributes_data[k] = widget.get()

        data = {
            "header": {
                "name": get_entry("Name"),
                "race": get_entry("Race"),
                "birthsign": get_entry("Birthsign"),
                "elite_advances": get_entry("Elite Advances"),
                "size": get_entry("Size"),
                "xp": get_entry("XP"),
                "total_xp": get_entry("Total XP")
            },
            "characteristics": {k: v.get() for k, v in getattr(self, "attr_vars", {}).items()},
            "favored": {k: v.get() for k, v in getattr(self, "favored_vars", {}).items()},
            "lucky_numbers": get_entry("Lucky Numbers"),
            "unlucky_numbers": get_entry("Unlucky Numbers"),
            "attributes": attributes_data,
            "attributes_max": attributes_max_data,
            "linguistics": get_entry("Linguistics"),
            "languages": get_entry("Languages"),
            "bonds": self.bonds_text.get("1.0", tk.END).strip() if hasattr(self, "bonds_text") else "",

            "skills": {name: info["level_cb"].get() for name, info in getattr(self, "skill_vars", {}).items()},
            "professions": [
                {
                    "name": row["name_entry"].get(),
                    "level": row["level_cb"].get(),
                    "attrs": [cb.get() for cb in row["attr_cbs"]]
                }
                for row in getattr(self, "prof_rows", [])
            ],
            "combat_style": {
                "name": self.cs_name_entry.get() if hasattr(self, "cs_name_entry") else "",
                "level": self.cs_level_cb.get() if hasattr(self, "cs_level_cb") else "",
                "items": [line["entry"].get() for line in getattr(self, "cs_lines", [])]
            },
            "specializations": [line["entry"].get() for line in getattr(self, "spec_lines", [])],

            "armor": {
                zone: {
                    "ar": vars_dict["ar"].get(),
                    "enc": vars_dict["enc"].get(),
                    "type": vars_dict["type"].get()
                }
                for zone, vars_dict in getattr(self, "armor_vars", {}).items()
            } if hasattr(self, "armor_vars") else {},
            "shield": self.shield_var.get() if hasattr(self, "shield_var") else "",
            "armor_notes": self.armor_notes_text.get("1.0", tk.END).strip() if hasattr(self,
                                                                                       "armor_notes_text") else "",
            "wounds": self.wounds_text.get("1.0", tk.END).strip() if hasattr(self, "wounds_text") else "",
            "conditions": self.conditions_text.get("1.0", tk.END).strip() if hasattr(self, "conditions_text") else "",

            "weapons": {
                "melee": [
                    {
                        "name": item["name"].get(),
                        "dmg": item["dmg"].get(),
                        "mat_bonus": item["mat_bonus"].get(),
                        "h": item["h"].get(),
                        "reach": item["reach"].get(),
                        "enc": item["enc"].get(),
                        "qualities": {
                            "crushing": item["qualities"]["crushing"].get(),
                            "splitting": item["qualities"]["splitting"].get(),
                            "slashing": item["qualities"]["slashing"].get(),
                            "other": item["qualities"]["other"].get()
                        }
                    }
                    for item in getattr(self, "weapons_vars", {}).get("melee", [])
                ],
                "ranged": [
                    {
                        "type": item["type"].get(),
                        "dmg": item["dmg"].get(),
                        "h": item["h"].get(),
                        "range_short": item["range_short"].get(),
                        "range_med": item["range_med"].get(),
                        "range_long": item["range_long"].get(),
                        "qualities": item["qualities"].get(),
                        "enc": item["enc"].get()
                    }
                    for item in getattr(self, "weapons_vars", {}).get("ranged", [])
                ],
                "ammo": [
                    {
                        "qty": item["qty"].get(),
                        "name": item["name"].get(),
                        "dam_mod": item["dam_mod"].get(),
                        "qualities": item["qualities"].get(),
                        "enc": item["enc"].get()
                    }
                    for item in getattr(self, "weapons_vars", {}).get("ammo", [])
                ]
            }
        }
        # Items & Equipment
        equipment_data = []
        if hasattr(self, "equipment_rows"):
            for row in self.equipment_rows:
                qty = row["qty"].get().strip()
                item = row["item"].get().strip()
                enc = row["enc_var"].get().strip()

                if qty or item or enc:
                    equipment_data.append({
                        "qty": qty,
                        "item": item,
                        "enc": enc
                    })


        data["equipment"] = equipment_data
        data["drakes"] = self.drakes_var.get().strip() if hasattr(self, "drakes_var") else "0"
        # Talents, Traits, Powers
        ttp_saved = {}
        if hasattr(self, "ttp_data"):
            for category, rows in self.ttp_data.items():
                cat_list = []
                for row in rows:
                    name = row["name"].get().strip()
                    effect = row["effect"].get().strip()

                    if name or effect:
                        cat_list.append({
                            "name": name,
                            "effect": effect
                        })
                ttp_saved[category] = cat_list

        data["ttp_data"] = ttp_saved
        # Spellcasting, Custom Skills, Specializations, Rituals, Spells
        magic_data = {}

        # Spellcasting Skills
        spellcasting_skills = {}
        if hasattr(self, "spellcasting_vars"):
            for school_key, widgets in self.spellcasting_vars.items():
                spellcasting_skills[school_key] = {
                    "level": widgets["level_cb"].get(),
                    "rank": widgets["rank_var"].get(),
                    "bonus": widgets["bonus_var"].get(),
                    "tn": widgets["tn_var"].get()
                }
        magic_data["spellcasting_skills"] = spellcasting_skills

        # Custom Magic Skills
        custom_magic = []
        if hasattr(self, "custom_magic_skills"):
            for row in self.custom_magic_skills:
                name = row["name"].get().strip()
                if name:
                    custom_magic.append({
                        "name": name,
                        "attr": row["attr_cb"].get(),
                        "level": row["level_cb"].get(),
                        "rank": row["rank_var"].get(),
                        "bonus": row["bonus_var"].get(),
                        "tn": row["tn_var"].get()
                    })
        magic_data["custom_skills"] = custom_magic

        # Specializations
        specializations = []
        if hasattr(self, "specializations_vars"):
            for row in self.specializations_vars:
                spec_text = row["entry"].get().strip()
                if spec_text:
                    specializations.append(spec_text)
        magic_data["specializations"] = specializations

        # Rituals
        rituals = []
        if hasattr(self, "rituals_vars"):
            for row in self.rituals_vars:
                r_name = row["name"].get().strip()
                r_notes = row["notes"].get().strip()
                if r_name or r_notes:
                    rituals.append({
                        "name": r_name,
                        "notes": r_notes
                    })
        magic_data["rituals"] = rituals

        # Spells
        saved_spells = []
        if hasattr(self, "spells_vars"):
            for row in self.spells_vars:
                for card in row["cards"]:
                    if card["card_frame"].winfo_exists():
                        name = card["name"].get().strip()
                        desc = card["description"].get("1.0", tk.END).strip()

                        grid_values = {
                            "level": [e.get().strip() for e in card["grid"]["Level"]],
                            "cost": [e.get().strip() for e in card["grid"]["Cost"]],
                            "spell_str": [e.get().strip() for e in card["grid"]["Spell Str."]]
                        }

                        has_grid_data = any(any(v) for v in grid_values.values())
                        if name or desc or has_grid_data:
                            saved_spells.append({
                                "name": name,
                                "attr": card["attr"].get().strip(),
                                "grid": grid_values,
                                "description": desc
                            })
        magic_data["spells"] = saved_spells

        data["magic"] = magic_data

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Success", "The character sheet has been saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the file:\n{e}")

    def load_from_json(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load character sheet"
        )
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Name, Race, Birthsign
            header = data.get("header", {})
            header_mapping = {
                "Name": header.get("name", ""),
                "Race": header.get("race", ""),
                "Birthsign": header.get("birthsign", ""),
                "Elite Advances": header.get("elite_advances", ""),
                "Size": header.get("size", ""),
                "XP": header.get("xp", ""),
                "Total XP": header.get("total_xp", "")
            }
            for k, val in header_mapping.items():
                if hasattr(self, "tab1_entries") and k in self.tab1_entries:
                    self.tab1_entries[k].delete(0, tk.END)
                    self.tab1_entries[k].insert(0, str(val))

            # Characteristics & Favored
            for k, val in data.get("characteristics", {}).items():
                if hasattr(self, "attr_vars") and k in self.attr_vars:
                    self.attr_vars[k].set(val)

            for k, val in data.get("favored", {}).items():
                if hasattr(self, "favored_vars") and k in self.favored_vars:
                    self.favored_vars[k].set(val)

            # Lucky / Unlucky Numbers & Languages
            if hasattr(self, "tab1_entries"):
                for key_json, key_dict in [("lucky_numbers", "Lucky Numbers"),
                                           ("unlucky_numbers", "Unlucky Numbers"),
                                           ("linguistics", "Linguistics"),
                                           ("languages", "Languages")]:
                    if key_dict in self.tab1_entries:
                        self.tab1_entries[key_dict].delete(0, tk.END)
                        self.tab1_entries[key_dict].insert(0, str(data.get(key_json, "")))

            # Atrybuty pochodne (HP, MP, WT, itp.)
            attrs = data.get("attributes", {})
            attrs_max = data.get("attributes_max", {})
            if hasattr(self, "derived_attr_vars"):
                for attr_key, widget in self.derived_attr_vars.items():
                    if isinstance(widget, tuple):  # Pola z podwójnym wpisem (Current / Max)
                        widget[0].delete(0, tk.END)
                        widget[0].insert(0, str(attrs.get(attr_key, "")))
                        widget[1].delete(0, tk.END)
                        widget[1].insert(0, str(attrs_max.get(attr_key, "")))
                    else:  # Pola z pojedynczym wpisem (WT, Speed, IR)
                        widget.delete(0, tk.END)
                        widget.insert(0, str(attrs.get(attr_key, "")))

            # Bonds
            if hasattr(self, "bonds_text"):
                self.bonds_text.delete("1.0", tk.END)
                self.bonds_text.insert("1.0", data.get("bonds", ""))

            # --- PAGE 2: SKILLS ---
            skills_data = data.get("skills", {})
            if hasattr(self, "skill_vars"):
                for skill_name, level_val in skills_data.items():
                    if skill_name in self.skill_vars:
                        self.skill_vars[skill_name]["level_cb"].set(level_val)

            # --- PAGE 2: PROFESSIONS ---
            professions_data = data.get("professions", [])
            if hasattr(self, "prof_rows"):
                for row in list(self.prof_rows):
                    row["frame"].destroy()
                self.prof_rows.clear()
                for prof in professions_data:
                    if hasattr(self, "add_prof_row"):
                        self.add_prof_row()
                        last_row = self.prof_rows[-1]

                        last_row["name_entry"].delete(0, tk.END)
                        last_row["name_entry"].insert(0, prof.get("name", ""))

                        last_row["level_cb"].set(prof.get("level", "Untrained"))

                        attrs = prof.get("attrs", ["None", "None", "None"])
                        for idx, cb in enumerate(last_row["attr_cbs"]):
                            if idx < len(attrs):
                                cb.set(attrs[idx])

                # --- PAGE 2: COMBAT STYLE ---
                cs_data = data.get("combat_style", {})
                if hasattr(self, "cs_name_entry"):
                    self.cs_name_entry.delete(0, tk.END)
                    self.cs_name_entry.insert(0, cs_data.get("name", ""))
                    self.cs_level_cb.set(cs_data.get("level", "Untrained"))

                    for line in list(self.cs_lines):
                        line["frame"].destroy()
                    self.cs_lines.clear()

                    items_list = cs_data.get("items", cs_data.get("lines", []))

                    for line_text in items_list:
                        if hasattr(self, "add_cs_line_row"):
                            self.add_cs_line_row()
                            last_entry = self.cs_lines[-1]["entry"]
                            last_entry.delete(0, tk.END)
                            last_entry.insert(0, str(line_text))

            # --- PAGE 2: SPECIALIZATIONS ---
            spec_data = data.get("specializations", [])
            if hasattr(self, "spec_lines"):
                for line in list(self.spec_lines):
                    line["frame"].destroy()
                self.spec_lines.clear()

                for spec_text in spec_data:
                    if hasattr(self, "add_spec_line_row"):
                        self.add_spec_line_row()
                        self.spec_lines[-1]["entry"].insert(0, spec_text)

            if hasattr(self, "recalculate_all_tns"):
                self.recalculate_all_tns()
            # --- ARMOR---
            armor_data = data.get("armor", {})
            if hasattr(self, "armor_vars") and isinstance(self.armor_vars, dict):
                for zone_key, zone_data in armor_data.items():
                    if zone_key in self.armor_vars and isinstance(zone_data, dict):
                        # AR
                        self.armor_vars[zone_key]["ar"].set(str(zone_data.get("ar", "")))
                        # ENC
                        self.armor_vars[zone_key]["enc"].set(str(zone_data.get("enc", "")))
                        # Type
                        self.armor_vars[zone_key]["type"].set(str(zone_data.get("type", "")))

            # --- SHIELD ---
            if hasattr(self, "shield_var"):
                self.shield_var.set(str(data.get("shield", "")))

            # --- ARMOR NOTES (tk.Text) ---
            if hasattr(self, "armor_notes_text"):
                self.armor_notes_text.delete("1.0", tk.END)
                self.armor_notes_text.insert("1.0", str(data.get("armor_notes", "")))

            # --- WOUNDS (tk.Text) ---
            if hasattr(self, "wounds_text"):
                self.wounds_text.delete("1.0", tk.END)
                self.wounds_text.insert("1.0", str(data.get("wounds", "")))

            # --- CONDITIONS (tk.Text) ---
            if hasattr(self, "conditions_text"):
                self.conditions_text.delete("1.0", tk.END)
                self.conditions_text.insert("1.0", str(data.get("conditions", "")))

            # 10. Weapons: Melee, Ranged, Ammo
            weapons_data = data.get("weapons", {})
            if hasattr(self, "weapons_vars"):

                # --- MELEE WEAPONS ---
                for item in list(self.weapons_vars.get("melee", [])):
                    if "frame" in item:
                        item["frame"].destroy()
                self.weapons_vars["melee"].clear()

                for m in weapons_data.get("melee", []):
                    if hasattr(self, "add_melee_row"):
                        self.add_melee_row()
                        last = self.weapons_vars["melee"][-1]

                        last["name"].delete(0, tk.END)
                        last["name"].insert(0, m.get("name", ""))

                        last["dmg"].set(m.get("dmg", "1d4"))
                        last["mat_bonus"].set(m.get("mat_bonus", "+0"))
                        last["h"].set(m.get("h", "1H"))

                        last["reach"].delete(0, tk.END)
                        last["reach"].insert(0, str(m.get("reach", "")))

                        last["enc"].delete(0, tk.END)
                        last["enc"].insert(0, str(m.get("enc", "")))

                        # Qualities
                        qualities = m.get("qualities", {})
                        if isinstance(qualities, dict):
                            last["qualities"]["crushing"].set(qualities.get("crushing", False))
                            last["qualities"]["splitting"].set(qualities.get("splitting", False))
                            last["qualities"]["slashing"].set(qualities.get("slashing", False))

                            last["qualities"]["other"].delete(0, tk.END)
                            last["qualities"]["other"].insert(0, str(qualities.get("other", "")))

                # --- RANGED WEAPONS ---
                for item in list(self.weapons_vars.get("ranged", [])):
                    if "frame" in item:
                        item["frame"].destroy()
                self.weapons_vars["ranged"].clear()

                for r in weapons_data.get("ranged", []):
                    if hasattr(self, "add_ranged_row"):
                        self.add_ranged_row()
                        last = self.weapons_vars["ranged"][-1]

                        last["type"].delete(0, tk.END)
                        last["type"].insert(0, r.get("type", ""))

                        last["dmg"].set(r.get("dmg", "1d4"))
                        last["h"].set(r.get("h", "2H"))

                        last["range_short"].delete(0, tk.END)
                        last["range_short"].insert(0, str(r.get("range_short", "")))

                        last["range_med"].delete(0, tk.END)
                        last["range_med"].insert(0, str(r.get("range_med", "")))

                        last["range_long"].delete(0, tk.END)
                        last["range_long"].insert(0, str(r.get("range_long", "")))

                        last["qualities"].delete(0, tk.END)
                        last["qualities"].insert(0, str(r.get("qualities", "")))

                        last["enc"].delete(0, tk.END)
                        last["enc"].insert(0, str(r.get("enc", "")))

                # --- AMMO ---
                for item in list(self.weapons_vars.get("ammo", [])):
                    if "frame" in item:
                        item["frame"].destroy()
                self.weapons_vars["ammo"].clear()

                for a in weapons_data.get("ammo", []):
                    if hasattr(self, "add_ammo_row"):
                        self.add_ammo_row()
                        last = self.weapons_vars["ammo"][-1]

                        last["qty"].delete(0, tk.END)
                        last["qty"].insert(0, str(a.get("qty", "")))

                        last["name"].delete(0, tk.END)
                        last["name"].insert(0, a.get("name", ""))

                        last["dam_mod"].delete(0, tk.END)
                        last["dam_mod"].insert(0, str(a.get("dam_mod", "")))

                        last["qualities"].delete(0, tk.END)
                        last["qualities"].insert(0, str(a.get("qualities", "")))

                        last["enc"].delete(0, tk.END)
                        last["enc"].insert(0, str(a.get("enc", "")))
            # Items & Equipment
            if hasattr(self, "equipment_rows"):
                # Czyszczenie dotychczasowych pól na stronie 4
                for row in self.equipment_rows:
                    row["qty"].delete(0, tk.END)
                    row["item"].delete(0, tk.END)
                    row["enc_var"].set("")

                equipment_list = data.get("equipment", [])
                for idx, item_data in enumerate(equipment_list):
                    if idx < len(self.equipment_rows):
                        self.equipment_rows[idx]["qty"].insert(0, str(item_data.get("qty", "")))
                        self.equipment_rows[idx]["item"].insert(0, str(item_data.get("item", "")))
                        self.equipment_rows[idx]["enc_var"].set(str(item_data.get("enc", "")))

            # Drakes
            if hasattr(self, "drakes_var"):
                self.drakes_var.set(str(data.get("drakes", "0")))

            if hasattr(self, "calculate_total_enc"):
                self.calculate_total_enc()
            # Talents, Traits, Powers
            if hasattr(self, "ttp_data"):
                saved_ttp = data.get("ttp_data", {})

                for category_key in ["talents", "traits", "powers"]:
                    if category_key in self.ttp_data:
                        for row in list(self.ttp_data[category_key]):
                            self._remove_ttp_row(category_key, row)

                        items = saved_ttp.get(category_key, [])
                        for item in items:
                            if hasattr(self, "_add_ttp_row_with_data"):
                                self._add_ttp_row_with_data(category_key, item.get("name", ""),
                                                            item.get("effect", ""))
            #  Magic
            magic_data = data.get("magic", {})

            # Spellcasting Skills
            saved_spells_skills = magic_data.get("spellcasting_skills", {})
            if hasattr(self, "spellcasting_vars"):
                for school_key, widgets in self.spellcasting_vars.items():
                    if school_key in saved_spells_skills:
                        s_info = saved_spells_skills[school_key]
                        widgets["level_cb"].set(s_info.get("level", "Untrained"))
                        self.update_magic_skill_values(school_key)

            # Custom Magic Skills
            if hasattr(self, "custom_magic_skills"):
                for row in list(self.custom_magic_skills):
                    row["frame"].destroy()
                self.custom_magic_skills.clear()

                saved_custom = magic_data.get("custom_skills", [])
                for c_item in saved_custom:
                    if hasattr(self, "add_custom_skill_row"):
                        self.add_custom_skill_row()
                        last_row = self.custom_magic_skills[-1]
                        last_row["name"].insert(0, c_item.get("name", ""))
                        last_row["attr_cb"].set(c_item.get("attr", "Wp"))
                        last_row["level_cb"].set(c_item.get("level", "Untrained"))
                        last_row["level_cb"].event_generate("<<ComboboxSelected>>")

            # Specializations
            if hasattr(self, "specializations_vars"):
                for row in list(self.specializations_vars):
                    row["frame"].destroy()
                self.specializations_vars.clear()

                saved_specs = magic_data.get("specializations", [])
                for spec_text in saved_specs:
                    if hasattr(self, "add_spec_row"):
                        self.add_spec_row()
                        last_row = self.specializations_vars[-1]
                        last_row["entry"].insert(0, str(spec_text))

            # Rituals
            if hasattr(self, "rituals_vars"):
                for row in list(self.rituals_vars):
                    row["frame"].destroy()
                self.rituals_vars.clear()

                saved_rituals = magic_data.get("rituals", [])
                for r_item in saved_rituals:
                    if hasattr(self, "add_ritual_row"):
                        self.add_ritual_row()
                        last_row = self.rituals_vars[-1]
                        last_row["name"].insert(0, r_item.get("name", ""))
                        last_row["notes"].insert(0, r_item.get("notes", ""))

            # Spells (Karty Zaklęć w wierszach po 3)
            if hasattr(self, "spells_vars"):
                for row in list(self.spells_vars):
                    row["row_frame"].destroy()
                self.spells_vars.clear()

                saved_spells = magic_data.get("spells", [])
                if saved_spells and hasattr(self, "add_spell_trio_row"):
                    needed_rows = (len(saved_spells) + 2) // 3
                    for _ in range(needed_rows):
                        self.add_spell_trio_row()

                    spell_idx = 0
                    for row in self.spells_vars:
                        for card in row["cards"]:
                            if spell_idx < len(saved_spells):
                                s_data = saved_spells[spell_idx]
                                card["name"].insert(0, s_data.get("name", ""))
                                card["attr"].insert(0, s_data.get("attr", ""))

                                grid_data = s_data.get("grid", {})
                                levels = grid_data.get("level", [])
                                costs = grid_data.get("cost", [])
                                spell_strs = grid_data.get("spell_str", [])

                                for idx, val in enumerate(levels):
                                    if idx < 7:
                                        card["grid"]["Level"][idx].insert(0, val)

                                for idx, val in enumerate(costs):
                                    if idx < 7:
                                        card["grid"]["Cost"][idx].insert(0, val)

                                for idx, val in enumerate(spell_strs):
                                    if idx < 7:
                                        card["grid"]["Spell Str."][idx].insert(0, val)

                                card["description"].delete("1.0", tk.END)
                                card["description"].insert("1.0", s_data.get("description", ""))

                                spell_idx += 1
                            else:
                                card["card_frame"].pack_forget()

            messagebox.showinfo("Success", "The character sheet has been successfully loaded")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the file:\n{e}")

    def calculate_bonus(self, attr, bonus_name):
        if not hasattr(self, "attr_vars") or attr not in self.attr_vars:
            return

        try:
            val_str = self.attr_vars[attr].get()
            val = int(val_str) if val_str.isdigit() else 0
            bonus_val = val // 10
        except (ValueError, TypeError):
            bonus_val = 0

        if hasattr(self, "bonus_vars") and bonus_name in self.bonus_vars:
            self.bonus_vars[bonus_name].set(str(bonus_val))

    def recalculate_magic_tn(self, *args):
        if hasattr(self, "magic_skills") and isinstance(self.magic_skills, dict):
            for skill_name, widgets in self.magic_skills.items():
                if not isinstance(widgets, dict):
                    continue

                attr_key = "Int" if "Int" in str(skill_name) else "Wp"
                base_attr = self.get_attribute_value(attr_key) if hasattr(self, "get_attribute_value") else 0

                rank_e = widgets.get("rank") or widgets.get("rank_entry")
                bonus_e = widgets.get("bonus") or widgets.get("bonus_entry")
                tn_e = widgets.get("tn") or widgets.get("tn_entry")

                try:
                    rank = float(rank_e.get().replace(',', '.')) if (rank_e and hasattr(rank_e, "get")) else 0.0
                except ValueError:
                    rank = 0.0

                try:
                    bonus = float(bonus_e.get().replace(',', '.')) if (bonus_e and hasattr(bonus_e, "get")) else 0.0
                except ValueError:
                    bonus = 0.0

                if tn_e and hasattr(tn_e, "config"):
                    tn = int(base_attr + rank + bonus)
                    tn_e.config(state="normal")
                    tn_e.delete(0, tk.END)
                    tn_e.insert(0, str(tn))
                    tn_e.config(state="readonly")

        if hasattr(self, "custom_magic_skills") and isinstance(self.custom_magic_skills, list):
            for row in self.custom_magic_skills:
                if not isinstance(row, dict):
                    continue

                attr_cb = row.get("attr") or row.get("attr_cb")
                attr_key = attr_cb.get() if (attr_cb and hasattr(attr_cb, "get")) else "Wp"
                base_attr = self.get_attribute_value(attr_key) if hasattr(self, "get_attribute_value") else 0

                rank_e = row.get("rank") or row.get("rank_entry")
                bonus_e = row.get("bonus") or row.get("bonus_entry")
                tn_e = row.get("tn") or row.get("tn_entry")

                try:
                    rank = float(rank_e.get().replace(',', '.')) if (rank_e and hasattr(rank_e, "get")) else 0.0
                except ValueError:
                    rank = 0.0

                try:
                    bonus = float(bonus_e.get().replace(',', '.')) if (bonus_e and hasattr(bonus_e, "get")) else 0.0
                except ValueError:
                    bonus = 0.0

                if tn_e and hasattr(tn_e, "config"):
                    tn = int(base_attr + rank + bonus)
                    tn_e.config(state="normal")
                    tn_e.delete(0, tk.END)
                    tn_e.insert(0, str(tn))
                    tn_e.config(state="readonly")
if __name__ == "__main__":
    app = UESRPGCharacterSheet()
    app.mainloop()