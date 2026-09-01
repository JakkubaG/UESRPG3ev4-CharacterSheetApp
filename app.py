import tkinter as tk
from tkinter import ttk, messagebox

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

        # Kontroler zakładek (Notebook)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Tworzenie zakładek dla stron karty
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

# ---------------PAGE1------------------
    def setup_tab1(self, parent):
        # Nagłówek - Dane podstawowe
        header_frame = ttk.LabelFrame(parent, text="Character Sheet")
        header_frame.pack(fill="x", padx=10, pady=5)

        # Wiersz 1: Name, Race, Birthsign, Elite Advances
        row1_fields = [
            ("Name:", 35),
            ("Race:", 35),
            ("Birthsign:", 35),
            ("Elite Advances:", 35)
        ]

        for i, (field_label, width_val) in enumerate(row1_fields):
            ttk.Label(header_frame, text=field_label).grid(row=0, column=i * 2, padx=5, pady=5, sticky="e")
            ttk.Entry(header_frame, width=width_val).grid(row=0, column=i * 2 + 1, padx=5, pady=5, sticky="w")

        # Wiersz 2: Size, XP, Total XP
        row2_fields = [
            ("Size:", 20),
            ("XP:", 20),
            ("Total XP:", 20)
        ]

        for i, (field_label, width_val) in enumerate(row2_fields):
            ttk.Label(header_frame, text=field_label).grid(row=1, column=i * 2, padx=5, pady=5, sticky="e")
            ttk.Entry(header_frame, width=width_val).grid(row=1, column=i * 2 + 1, padx=5, pady=5, sticky="w")

        # Characteristics
        attr_frame = ttk.LabelFrame(parent, text="Characteristics")
        attr_frame.pack(fill="x", padx=10, pady=5)

        attributes = ["Str", "End", "Ag", "Int", "Wp", "Prc", "Prs", "Lck"]
        bonus_names = ["SB", "EB", "AB", "IB", "WB", "PcB", "PsB", "LB"]

        self.attr_vars = {}
        self.bonus_vars = {}
        self.favored_vars = {}

        # Etykieta "Favored" po lewej stronie wiersza
        ttk.Label(attr_frame, text="Favored", font=('Helvetica', 9, 'bold')).grid(row=2, column=0, padx=(10, 5), pady=2,
                                                                                  sticky="e")

        for i, (attr, bonus_name) in enumerate(zip(attributes, bonus_names), start=1):
            # 1. Etykieta atrybutu (Góra: Str, End, ...)
            ttk.Label(attr_frame, text=attr, font=('Helvetica', 9, 'bold')).grid(row=0, column=i, padx=12, pady=2)

            # 2. Wartość atrybutu (Wpisywana liczba)
            var = tk.StringVar(value="0")
            self.attr_vars[attr] = var
            entry = ttk.Entry(attr_frame, textvariable=var, width=5, justify="center")
            entry.grid(row=1, column=i, padx=5, pady=2)

            # 3. Checkbutton (Favored) - z wyjątkiem 'Lck'
            if attr != "Lck":
                cb_var = tk.BooleanVar(value=False)
                self.favored_vars[attr] = cb_var

                cb = ttk.Checkbutton(
                    attr_frame,
                    variable=cb_var,
                    command=lambda a=attr: self.on_favored_toggle(a)
                )
                cb.grid(row=2, column=i, padx=5, pady=2)
            else:
                # Działka bez checkboxa dla Lck
                ttk.Label(attr_frame, text="-").grid(row=2, column=i, padx=5, pady=2)

            # 4. Wyliczony bonus (Wyświetlany pod spodem)
            b_var = tk.StringVar(value="0")
            self.bonus_vars[bonus_name] = b_var
            bonus_entry = ttk.Entry(attr_frame, textvariable=b_var, width=5, justify="center", state="readonly")
            bonus_entry.grid(row=3, column=i, padx=5, pady=2)

            # 5. Etykieta bonusu (Dół: SB, EB, ...)
            ttk.Label(attr_frame, text=bonus_name, foreground="gray").grid(row=4, column=i, padx=12, pady=2)

            # Automatyczne liczenie bonusu
            var.trace_add("write", lambda *args, a=attr, b=bonus_name: self.calculate_bonus(a, b))

        lucky_frame = ttk.Frame(attr_frame)
        lucky_frame.grid(row=5, column=0, columnspan=9, pady=(10, 5), sticky="w", padx=10)

        for i, field in enumerate(["Lucky Numbers:", "Unlucky Numbers:"]):
            ttk.Label(lucky_frame, text=field, font=('Helvetica', 9, 'bold')).grid(row=0, column=i * 2, padx=(10, 5),
                                                                                   pady=5, sticky="e")
            ttk.Entry(lucky_frame, width=25).grid(row=0, column=i * 2 + 1, padx=(0, 15), pady=5, sticky="w")

        # Sekcja Attributes (dwa słupki według wzoru ze zdjęcia)
        attributes_frame = ttk.LabelFrame(parent, text="Attributes")
        attributes_frame.pack(fill="x", padx=10, pady=5)

        # Lewa kolumna: HP, WT, Speed, IR, Linguistics
        # HP (Current / Max)
        ttk.Label(attributes_frame, text="HP", font=('Helvetica', 9, 'bold')).grid(row=0, column=0, padx=5, pady=2,
                                                                                   sticky="e")
        hp_frame = ttk.Frame(attributes_frame)
        hp_frame.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        ttk.Entry(hp_frame, width=5, justify="center").pack(side="left")
        ttk.Label(hp_frame, text="/").pack(side="left", padx=2)
        ttk.Entry(hp_frame, width=5, justify="center").pack(side="left")

        # WT
        ttk.Label(attributes_frame, text="WT", font=('Helvetica', 9, 'bold')).grid(row=1, column=0, padx=5, pady=2,
                                                                                   sticky="e")
        ttk.Entry(attributes_frame, width=13, justify="center").grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Speed (Base / Armor Mod)
        ttk.Label(attributes_frame, text="Speed", font=('Helvetica', 9, 'bold')).grid(row=2, column=0, padx=5, pady=2,
                                                                                   sticky="e")
        ttk.Entry(attributes_frame, width=13, justify="center").grid(row=2, column=1, padx=5, pady=2, sticky="w")

        # IR
        ttk.Label(attributes_frame, text="IR", font=('Helvetica', 9, 'bold')).grid(row=3, column=0, padx=5, pady=2,
                                                                                   sticky="e")
        ttk.Entry(attributes_frame, width=13, justify="center").grid(row=3, column=1, padx=5, pady=2, sticky="w")

        # Linguistics
        ttk.Label(attributes_frame, text="Linguistics", font=('Helvetica', 9, 'bold')).grid(row=4, column=0, padx=5,
                                                                                            pady=2, sticky="e")
        ttk.Entry(attributes_frame, width=25).grid(row=4, column=1, padx=5, pady=2, sticky="w")

        # Prawa kolumna: MP, SP, LP, AP, ENC / CR
        # MP (Current / Max)
        ttk.Label(attributes_frame, text="MP", font=('Helvetica', 9, 'bold')).grid(row=0, column=2, padx=(20, 5),
                                                                                   pady=2, sticky="e")
        mp_frame = ttk.Frame(attributes_frame)
        mp_frame.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        ttk.Entry(mp_frame, width=5, justify="center").pack(side="left")
        ttk.Label(mp_frame, text="/").pack(side="left", padx=2)
        ttk.Entry(mp_frame, width=5, justify="center").pack(side="left")

        # SP (Current / Max)
        ttk.Label(attributes_frame, text="SP", font=('Helvetica', 9, 'bold')).grid(row=1, column=2, padx=(20, 5),
                                                                                   pady=2, sticky="e")
        sp_frame = ttk.Frame(attributes_frame)
        sp_frame.grid(row=1, column=3, padx=5, pady=2, sticky="w")
        ttk.Entry(sp_frame, width=5, justify="center").pack(side="left")
        ttk.Label(sp_frame, text="/").pack(side="left", padx=2)
        ttk.Entry(sp_frame, width=5, justify="center").pack(side="left")

        # LP (Current / Max)
        ttk.Label(attributes_frame, text="LP", font=('Helvetica', 9, 'bold')).grid(row=2, column=2, padx=(20, 5),
                                                                                   pady=2, sticky="e")
        lp_frame = ttk.Frame(attributes_frame)
        lp_frame.grid(row=2, column=3, padx=5, pady=2, sticky="w")
        ttk.Entry(lp_frame, width=5, justify="center").pack(side="left")
        ttk.Label(lp_frame, text="/").pack(side="left", padx=2)
        ttk.Entry(lp_frame, width=5, justify="center").pack(side="left")

        # AP (Current / Max)
        ttk.Label(attributes_frame, text="AP", font=('Helvetica', 9, 'bold')).grid(row=3, column=2, padx=(20, 5),
                                                                                   pady=2, sticky="e")
        ap_frame = ttk.Frame(attributes_frame)
        ap_frame.grid(row=3, column=3, padx=5, pady=2, sticky="w")
        ttk.Entry(ap_frame, width=5, justify="center").pack(side="left")
        ttk.Label(ap_frame, text="/").pack(side="left", padx=2)
        ttk.Entry(ap_frame, width=5, justify="center").pack(side="left")

        # ENC / CR
        ttk.Label(attributes_frame, text="ENC / CR", font=('Helvetica', 9, 'bold')).grid(row=4, column=2,
                                                                                         padx=(20, 5), pady=2,
                                                                                         sticky="e")
        enc_frame = ttk.Frame(attributes_frame)
        enc_frame.grid(row=4, column=3, padx=5, pady=2, sticky="w")
        ttk.Entry(enc_frame, width=5, justify="center").pack(side="left")
        ttk.Label(enc_frame, text="/").pack(side="left", padx=2)
        ttk.Entry(enc_frame, width=5, justify="center").pack(side="left")

        # Dół: Languages (roziągnięte pod obiema kolumnami)
        ttk.Label(attributes_frame, text="Languages", font=('Helvetica', 9, 'bold')).grid(row=5, column=0, padx=5,
                                                                                          pady=(5, 10), sticky="e")
        ttk.Entry(attributes_frame, width=65).grid(row=5, column=1, columnspan=3, padx=5, pady=(5, 10), sticky="w")

        # --- SEKCJA BONDS ---
        bonds_frame = ttk.LabelFrame(parent, text="Bonds")
        bonds_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Pole tekstowe do wpisywania więzi z paskiem przewijania
        self.bonds_text = tk.Text(bonds_frame, height=5, wrap="word")
        bonds_scrollbar = ttk.Scrollbar(bonds_frame, orient="vertical", command=self.bonds_text.yview)
        self.bonds_text.configure(yscrollcommand=bonds_scrollbar.set)

        self.bonds_text.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        bonds_scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=5)

    def calculate_bonus(self, attr_name, bonus_name):
        raw_val = self.attr_vars[attr_name].get()
        try:
            val = int(raw_val)
            bonus = val // 10
        except ValueError:
            bonus = 0

        self.bonus_vars[bonus_name].set(str(bonus))
#---------------PAGE2------------------
    def setup_tab2(self, parent):
        # Definicja rang i odpowiadających im wartości (Rank, Bonus)
        self.skill_ranks_info = {
            "Untrained": (-1, -20),
            "Novice": (0, 0),
            "Apprentice": (1, 10),
            "Journeyman": (2, 20),
            "Adept": (3, 30),
            "Expert": (4, 40),
            "Master": (5, 50)
        }

        # 1. FUNKCJE POMOCNICZE (Lokalne, zapobiegają błędom AttributeError)
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

        # Przypisanie funkcji przeliczania do klasy, aby Tab1 mógł ją wywoływać
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

        # 2. KONTENER ZE SCROLLBAREM (Canvas + Scrollbar)
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

        # 3. PODZIAŁ EKRANU (Skills | Professions, CS, Spec)
        skills_frame = ttk.LabelFrame(main_container, text="Skills")
        skills_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=5)

        right_container = ttk.Frame(main_container)
        right_container.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=5)

        # --- LEWA STRONA: STANDARD SKILLS ---
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

            level_cb = ttk.Combobox(skills_frame, values=list(self.skill_ranks_info.keys()), state="readonly", width=10)
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

        # --- PRAWA STRONA: PROFESSIONS ---
        prof_frame = ttk.LabelFrame(right_container, text="Professions / Custom Skills")
        prof_frame.pack(fill="x", padx=0, pady=(0, 5))

        prof_headers_frame = ttk.Frame(prof_frame)
        prof_headers_frame.pack(fill="x", padx=2, pady=(5, 2))

        ttk.Label(prof_headers_frame, text="Custom Skill / Profession", font=('Helvetica', 9, 'bold'), width=22).pack(
            side="left", padx=2)
        ttk.Label(prof_headers_frame, text="Level", font=('Helvetica', 9, 'bold'), width=12).pack(side="left", padx=2)
        ttk.Label(prof_headers_frame, text="Attributes", font=('Helvetica', 9, 'bold'), width=18).pack(side="left",
                                                                                                       padx=2)
        ttk.Label(prof_headers_frame, text="Rank", font=('Helvetica', 9, 'bold'), width=5).pack(side="left", padx=2)
        ttk.Label(prof_headers_frame, text="Bonus", font=('Helvetica', 9, 'bold'), width=6).pack(side="left", padx=2)
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
            ttk.Entry(r_frame, textvariable=bonus_var, width=5, justify="center", state="readonly").pack(side="left",
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

        for _ in range(3):
            add_prof_row()

        add_prof_btn = ttk.Button(prof_frame, text="+ Add Profession", command=add_prof_row)
        add_prof_btn.pack(anchor="w", padx=5, pady=5)

        # --- PRAWA STRONA: COMBAT STYLE (Str, Ag) ---
        cs_frame = ttk.LabelFrame(right_container, text="Combat Style (Str, Ag)")
        cs_frame.pack(fill="x", padx=0, pady=5)

        cs_top = ttk.Frame(cs_frame)
        cs_top.pack(fill="x", padx=5, pady=5)

        ttk.Label(cs_top, text="Style Name:").pack(side="left", padx=(0, 5))
        self.cs_name_entry = ttk.Entry(cs_top, width=18)
        self.cs_name_entry.pack(side="left", padx=(0, 10))

        ttk.Label(cs_top, text="Level:").pack(side="left", padx=(0, 5))
        self.cs_level_cb = ttk.Combobox(cs_top, values=list(self.skill_ranks_info.keys()), state="readonly", width=10)
        self.cs_level_cb.set("Untrained")
        self.cs_level_cb.pack(side="left", padx=(0, 10))

        ttk.Label(cs_top, text="Rank:").pack(side="left", padx=(0, 2))
        self.cs_rank_var = tk.StringVar(value="-1")
        ttk.Entry(cs_top, textvariable=self.cs_rank_var, width=4, justify="center", state="readonly").pack(side="left",
                                                                                                           padx=(0, 10))

        ttk.Label(cs_top, text="Bonus:").pack(side="left", padx=(0, 2))
        self.cs_bonus_var = tk.StringVar(value="-20")
        ttk.Entry(cs_top, textvariable=self.cs_bonus_var, width=5, justify="center", state="readonly").pack(side="left",
                                                                                                            padx=(0,
                                                                                                                  10))

        ttk.Label(cs_top, text="TN:").pack(side="left", padx=(0, 2))
        self.cs_tn_str_var = tk.StringVar(value="0")
        self.cs_tn_ag_var = tk.StringVar(value="0")
        ttk.Entry(cs_top, textvariable=self.cs_tn_str_var, width=4, justify="center", state="readonly").pack(
            side="left")
        ttk.Label(cs_top, text=",").pack(side="left", padx=1)
        ttk.Entry(cs_top, textvariable=self.cs_tn_ag_var, width=4, justify="center", state="readonly").pack(side="left")

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

        for _ in range(5):
            add_cs_line_row()

        add_cs_line_btn = ttk.Button(cs_frame, text="+ Add Weapon / Armor", command=add_cs_line_row)
        add_cs_line_btn.pack(anchor="w", padx=5, pady=(0, 5))

        self.cs_level_cb.bind("<<ComboboxSelected>>", lambda event: update_cs_values())
        update_cs_values()

        # --- PRAWA STRONA: SPECIALIZATIONS ---
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

        for _ in range(2):
            add_spec_line_row()

        add_spec_btn = ttk.Button(spec_frame, text="+ Add Specialization", command=add_spec_line_row)
        add_spec_btn.pack(anchor="w", padx=5, pady=(0, 5))
#---------------PAGE3------------------
    def setup_tab3(self, parent):
        # 1. KONTENER ZE SCROLLBAREM (Canvas + Scrollbar)
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

        # Podział ekranu na stronę lewą i prawą
        left_side = ttk.Frame(main_container)
        left_side.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=5)

        right_side = ttk.Frame(main_container)
        right_side.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=5)

        # ==========================================
        # LEWA STRONA: ARMOR, SHIELD, NOTES
        # ==========================================
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

        # 1. Lewa strefa pancerza
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

        # 2. Środek (Placeholder graficzny)
        center_arm_container = ttk.Frame(armor_frame)
        center_arm_container.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        body_canvas = tk.Canvas(center_arm_container, width=120, height=240, bg="#f0f0f0", highlightthickness=1,
                                highlightbackground="#ccc")
        body_canvas.pack(expand=True)
        body_canvas.create_text(60, 120, text="[ Character ]", fill="#888888", justify="center")

        # 3. Prawa strefa pancerza
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

        # Sekcje tekstowe
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

        # ==========================================
        # PRAWA STRONA: WEAPONS & AMMUNITION
        # ==========================================
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
                # Pusta etykieta do wyrównania nagłówka z przyciskiem usuwania
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

                def remove_row(item_data):
                    item_data["frame"].destroy()
                    if item_data in self.weapons_vars["ammo"]:
                        self.weapons_vars["ammo"].remove(item_data)

                for _ in range(3):
                    add_ammo_row()

                btn = ttk.Button(frame, text="+ Add Ammunition", command=add_ammo_row)
                btn.pack(anchor="w", padx=5, pady=5)

        # Wywołanie budujące wszystkie 3 dynamiczne sekcje
        build_dynamic_weapon_table(right_side, "Melee Weapons", "melee")
        build_dynamic_weapon_table(right_side, "Ranged Weapons", "ranged")
        build_dynamic_weapon_table(right_side, "Ammunition", "ammo")

# ---------------PAGE4------------------
    def setup_tab4(self, parent):
        # Główny kontener strony 4: Items & Equipment
        main_container = ttk.Frame(parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        eq_frame = ttk.LabelFrame(main_container, text="Items & Equipment")
        eq_frame.pack(fill="both", expand=True, padx=5, pady=5)

        eq_frame.columnconfigure(0, weight=1)
        eq_frame.columnconfigure(1, weight=1)

        self.equipment_vars = []

        # 1. LEWA STRONA: Items & Equipment (14 wierszy)
        left_eq_frame = ttk.Frame(eq_frame)
        left_eq_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        left_eq_frame.columnconfigure(1, weight=1)  # Nazwa przedmiotu rozciąga się w poziomie

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

            enc_var.trace_add("write", lambda *args: self.calculate_total_enc())
            self.equipment_vars.append(enc_var)

        # 2. PRAWA STRONA: Items & Equipment (Cont.) (12 wierszy + podsumowanie)
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

            enc_var.trace_add("write", self.calculate_total_enc)
            self.equipment_vars.append(enc_var)

        # 3. PODSUMOWANIE (Total ENC & Drakes)
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
        """Dynamicznie sumuje punkty obciążenia ze wszystkich pól ekwipunku."""
        total = 0.0
        for enc_var in self.equipment_vars:
            val_str = enc_var.get().strip().replace(',', '.')
            if val_str:
                try:
                    total += float(val_str)
                except ValueError:
                    pass

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
# ---------------PAGE6------------------
# ==========================================
    # STRONA 6: SPELLCASTING, RITUALS & SPELLS
    # ==========================================
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

        # ==========================================
        # 1. SPELLCASTING SKILLS
        # ==========================================
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

            level_cb = ttk.Combobox(spell_frame, values=list(self.skill_ranks_info.keys()), state="readonly", width=10)
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

        # Sekcja: Custom Magic Skills
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

            level_cb = ttk.Combobox(r_frame, values=list(self.skill_ranks_info.keys()), state="readonly", width=10)
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
                rank, bonus = self.skill_ranks_info.get(lvl, (-1, -20))
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
            self.custom_magic_skills.remove(row_data)

        for _ in range(1):
            add_custom_skill_row()

        add_skill_btn = ttk.Button(spell_frame, text="+ Add Custom Skill", command=add_custom_skill_row)
        add_skill_btn.grid(row=current_row + 1, column=0, columnspan=5, pady=5, padx=5, sticky="w")

        # ==========================================
        # 2. SPECIALIZATIONS
        # ==========================================
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
            self.specializations_vars.remove(row_data)

        for _ in range(1):
            add_spec_row()

        add_spec_btn = ttk.Button(spec_frame, text="+ Add Specialization", command=add_spec_row)
        add_spec_btn.pack(anchor="w", padx=5, pady=5)

        # ==========================================
        # 3. RITUALS
        # ==========================================
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
            self.rituals_vars.remove(row_data)

        for _ in range(1):
            add_ritual_row()

        add_ritual_btn = ttk.Button(rituals_frame, text="+ Add Ritual", command=add_ritual_row)
        add_ritual_btn.pack(anchor="w", padx=5, pady=5)

        # ==========================================
        # 4. SPELLS (PRAWA STRONA - 3 W WIERSZU)
        # ==========================================
        spells_main_frame = ttk.LabelFrame(right_side, text="Spells")
        spells_main_frame.pack(fill="both", expand=True, pady=(0, 10))

        spells_grid_container = ttk.Frame(spells_main_frame)
        spells_grid_container.pack(fill="both", expand=True, padx=5, pady=5)

        def create_single_spell_card(parent_frame, row_ref):
            card = ttk.LabelFrame(parent_frame, text="Spell Card")

            header_frame = ttk.Frame(card)
            header_frame.pack(fill="x", padx=2, pady=1)

            del_btn = ttk.Button(header_frame, text="✕", width=2)
            del_btn.pack(side="right")

            body_frame = ttk.Frame(card)
            body_frame.pack(fill="both", expand=True, padx=2, pady=2)

            # Wiersz 1: Spell Name
            ttk.Label(body_frame, text="Name:", font=('Helvetica', 8, 'bold')).grid(row=0, column=0, sticky="e", padx=1,
                                                                                    pady=1)
            name_entry = ttk.Entry(body_frame, width=34)
            name_entry.grid(row=0, column=1, columnspan=3, sticky="ew", padx=1, pady=1)

            # Wiersz 2: Cost & Skill
            ttk.Label(body_frame, text="Cost:", font=('Helvetica', 8, 'bold')).grid(row=1, column=0, sticky="e", padx=1,
                                                                                    pady=1)
            cost_entry = ttk.Entry(body_frame, width=5)
            cost_entry.grid(row=1, column=1, sticky="w", padx=1, pady=1)

            ttk.Label(body_frame, text="Skill:", font=('Helvetica', 8, 'bold')).grid(row=1, column=2, sticky="e",
                                                                                     padx=1, pady=1)
            skill_entry = ttk.Entry(body_frame, width=8)
            skill_entry.grid(row=1, column=3, sticky="ew", padx=1, pady=1)

            # Wiersz 3: Range & Target
            ttk.Label(body_frame, text="Range:", font=('Helvetica', 8, 'bold')).grid(row=2, column=0, sticky="e",
                                                                                     padx=1, pady=1)
            range_entry = ttk.Entry(body_frame, width=5)
            range_entry.grid(row=2, column=1, sticky="w", padx=1, pady=1)

            ttk.Label(body_frame, text="Target:", font=('Helvetica', 8, 'bold')).grid(row=2, column=2, sticky="e",
                                                                                      padx=1, pady=1)
            target_entry = ttk.Entry(body_frame, width=8)
            target_entry.grid(row=2, column=3, sticky="ew", padx=1, pady=1)

            # Wiersz 4: Duration & Resistance
            ttk.Label(body_frame, text="Duration:", font=('Helvetica', 8, 'bold')).grid(row=3, column=0, sticky="e",
                                                                                        padx=1, pady=1)
            duration_entry = ttk.Entry(body_frame, width=5)
            duration_entry.grid(row=3, column=1, sticky="w", padx=1, pady=1)

            ttk.Label(body_frame, text="Resist:", font=('Helvetica', 8, 'bold')).grid(row=3, column=2, sticky="e",
                                                                                      padx=1, pady=1)
            resist_entry = ttk.Entry(body_frame, width=8)
            resist_entry.grid(row=3, column=3, sticky="ew", padx=1, pady=1)

            # Wiersz 5: Effect / Notes
            ttk.Label(body_frame, text="Effect:", font=('Helvetica', 8, 'bold')).grid(row=4, column=0, sticky="ne",
                                                                                      padx=1, pady=2)
            effect_text = tk.Text(body_frame, height=3, width=16, wrap="word")
            effect_text.grid(row=4, column=1, columnspan=3, sticky="ew", padx=1, pady=2)

            card_data = {
                "card_frame": card,
                "del_btn": del_btn,
                "name": name_entry,
                "cost": cost_entry,
                "skill": skill_entry,
                "range": range_entry,
                "target": target_entry,
                "duration": duration_entry,
                "resist": resist_entry,
                "effect": effect_text
            }

            def remove_this_card():
                card.destroy()
                row_ref["active_cards"] -= 1
                # Jeśli w wierszu nie zostanie żadna karta, usuwamy cały kontener wiersza
                if row_ref["active_cards"] <= 0:
                    row_ref["row_frame"].destroy()
                    if row_ref in self.spells_vars:
                        self.spells_vars.remove(row_ref)

            del_btn.config(command=remove_this_card)
            return card_data

        def add_spell_trio_row():
            row_frame = ttk.Frame(spells_grid_container)
            row_frame.pack(fill="x", pady=2)

            row_data = {
                "row_frame": row_frame,
                "active_cards": 3,
                "cards": []
            }

            # Tworzymy 3 karty obok siebie
            for _ in range(3):
                card_data = create_single_spell_card(row_frame, row_data)
                card_data["card_frame"].pack(side="left", fill="both", expand=True, padx=2)
                row_data["cards"].append(card_data)

            self.spells_vars.append(row_data)

        # Domyślnie dodaj 2 wiersze po 3 zaklęcia (łącznie 6 kart)
        for _ in range(2):
            add_spell_trio_row()

        add_spell_btn = ttk.Button(spells_main_frame, text="+ Add 3 Spells Row", command=add_spell_trio_row)
        add_spell_btn.pack(anchor="w", padx=5, pady=5)

    def update_magic_skill_values(self, school_key):
        """Pomocnicza funkcja licząca Rank, Bonus i TN dla szkół magii."""
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
if __name__ == "__main__":
    app = UESRPGCharacterSheet()
    app.mainloop()