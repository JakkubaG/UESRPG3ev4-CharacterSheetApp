import tkinter as tk
from tkinter import ttk, messagebox


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
        # self.setup_tab4(tab4)
        # self.setup_tab5(tab5)
        # self.setup_tab6(tab6)

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
        # Główny kontener dzielący ekran na lewy (Skills) i prawy (Professions, Combat Style, Specializations)
        main_container = ttk.Frame(parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        skills_frame = ttk.LabelFrame(main_container, text="Skills")
        skills_frame.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)

        right_container = ttk.Frame(main_container)
        right_container.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=5)

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
            ttk.Label(skills_frame, text=h, font=('Helvetica', 9, 'bold')).grid(row=0, column=i, padx=5, pady=5, sticky=sticky_val)

        self.skill_vars = {}

        for row_idx, (skill_name, stats) in enumerate(skills_data, start=1):
            stats_str = f" ({', '.join(stats)})"
            ttk.Label(skills_frame, text=f"{skill_name}{stats_str}").grid(row=row_idx, column=0, padx=5, pady=2, sticky="w")

            level_cb = ttk.Combobox(skills_frame, values=list(self.skill_ranks_info.keys()), state="readonly", width=10)
            level_cb.set("Untrained")
            level_cb.grid(row=row_idx, column=1, padx=2, pady=2)

            rank_var = tk.StringVar(value="-1")
            bonus_var = tk.StringVar(value="-20")

            ttk.Entry(skills_frame, textvariable=rank_var, width=4, justify="center", state="readonly").grid(row=row_idx, column=2, padx=2, pady=2)
            ttk.Entry(skills_frame, textvariable=bonus_var, width=5, justify="center", state="readonly").grid(row=row_idx, column=3, padx=2, pady=2)

            tn_container = ttk.Frame(skills_frame)
            tn_container.grid(row=row_idx, column=4, padx=2, pady=2, sticky="w")

            tn_vars = []
            for stat_idx, stat in enumerate(stats):
                if stat_idx > 0:
                    ttk.Label(tn_container, text=",").pack(side="left", padx=1)

                tn_v = tk.StringVar(value="0")
                tn_vars.append((stat, tn_v))
                ttk.Entry(tn_container, textvariable=tn_v, width=4, justify="center", state="readonly").pack(side="left")

            self.skill_vars[skill_name] = {
                "level_cb": level_cb,
                "rank_var": rank_var,
                "bonus_var": bonus_var,
                "tn_vars": tn_vars,
                "stats": stats
            }

            level_cb.bind("<<ComboboxSelected>>", lambda event, s=skill_name: self.update_skill_values(s))
            self.update_skill_values(skill_name)

        # --- PRAWA STRONA: PROFESSIONS ---
        prof_frame = ttk.LabelFrame(right_container, text="Professions / Custom Skills")
        prof_frame.pack(fill="x", padx=0, pady=(0, 5))

        prof_headers = ["Custom Skill / Profession", "Level", "Attributes", "Rank", "Bonus", "TN"]
        for i, h in enumerate(prof_headers):
            ttk.Label(prof_frame, text=h, font=('Helvetica', 9, 'bold')).grid(row=0, column=i, padx=5, pady=5)

        attr_options = ["None", "Str", "End", "Ag", "Int", "Wp", "Prc", "Prs", "Lck"]
        self.prof_vars = {}

        for i in range(1, 6):
            name_entry = ttk.Entry(prof_frame, width=18)
            name_entry.grid(row=i, column=0, padx=4, pady=4)

            level_cb = ttk.Combobox(prof_frame, values=list(self.skill_ranks_info.keys()), state="readonly", width=10)
            level_cb.set("Untrained")
            level_cb.grid(row=i, column=1, padx=4, pady=4)

            attr_cb_frame = ttk.Frame(prof_frame)
            attr_cb_frame.grid(row=i, column=2, padx=4, pady=4)

            attr_cbs = []
            for c in range(3):
                cb = ttk.Combobox(attr_cb_frame, values=attr_options, state="readonly", width=5)
                cb.set("None")
                cb.pack(side="left", padx=1)
                attr_cbs.append(cb)

            rank_var = tk.StringVar(value="-1")
            bonus_var = tk.StringVar(value="-20")

            ttk.Entry(prof_frame, textvariable=rank_var, width=4, justify="center", state="readonly").grid(row=i, column=3, padx=4, pady=4)
            ttk.Entry(prof_frame, textvariable=bonus_var, width=5, justify="center", state="readonly").grid(row=i, column=4, padx=4, pady=4)

            tn_container = ttk.Frame(prof_frame)
            tn_container.grid(row=i, column=5, padx=4, pady=4, sticky="w")

            prof_id = f"prof_{i}"
            self.prof_vars[prof_id] = {
                "name_entry": name_entry,
                "level_cb": level_cb,
                "attr_cbs": attr_cbs,
                "rank_var": rank_var,
                "bonus_var": bonus_var,
                "tn_container": tn_container,
                "tn_entries": []
            }

            level_cb.bind("<<ComboboxSelected>>", lambda event, pid=prof_id: self.update_prof_values(pid))
            for cb in attr_cbs:
                cb.bind("<<ComboboxSelected>>", lambda event, pid=prof_id: self.update_prof_values(pid))

            self.update_prof_values(prof_id)

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
        ttk.Entry(cs_top, textvariable=self.cs_rank_var, width=4, justify="center", state="readonly").pack(side="left", padx=(0, 10))

        ttk.Label(cs_top, text="Bonus:").pack(side="left", padx=(0, 2))
        self.cs_bonus_var = tk.StringVar(value="-20")
        ttk.Entry(cs_top, textvariable=self.cs_bonus_var, width=5, justify="center", state="readonly").pack(side="left", padx=(0, 10))

        ttk.Label(cs_top, text="TN:").pack(side="left", padx=(0, 2))
        self.cs_tn_str_var = tk.StringVar(value="0")
        self.cs_tn_ag_var = tk.StringVar(value="0")
        ttk.Entry(cs_top, textvariable=self.cs_tn_str_var, width=4, justify="center", state="readonly").pack(side="left")
        ttk.Label(cs_top, text=",").pack(side="left", padx=1)
        ttk.Entry(cs_top, textvariable=self.cs_tn_ag_var, width=4, justify="center", state="readonly").pack(side="left")

        cs_text_frame = ttk.Frame(cs_frame)
        cs_text_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        self.cs_text = tk.Text(cs_text_frame, height=3, wrap="word")
        cs_scroll = ttk.Scrollbar(cs_text_frame, orient="vertical", command=self.cs_text.yview)
        self.cs_text.configure(yscrollcommand=cs_scroll.set)

        self.cs_text.pack(side="left", fill="both", expand=True)
        cs_scroll.pack(side="right", fill="y")

        self.cs_level_cb.bind("<<ComboboxSelected>>", lambda event: self.update_cs_values())
        self.update_cs_values()

        # --- PRAWA STRONA: SPECIALIZATIONS ---
        spec_frame = ttk.LabelFrame(right_container, text="Specializations")
        spec_frame.pack(fill="both", expand=True, padx=0, pady=(5, 0))

        self.spec_text = tk.Text(spec_frame, height=4, wrap="word")
        spec_scroll = ttk.Scrollbar(spec_frame, orient="vertical", command=self.spec_text.yview)
        self.spec_text.configure(yscrollcommand=spec_scroll.set)

        self.spec_text.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        spec_scroll.pack(side="right", fill="y", padx=(0, 5), pady=5)

    def update_skill_values(self, skill_name):
        """Aktualizuje pola Rank, Bonus oraz TN dla standardowych umiejętności."""
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

    def update_prof_values(self, prof_id):
        """Aktualizuje pola Rank, Bonus oraz dynamiczne pola TN dla Custom Skills/Professions."""
        data = self.prof_vars[prof_id]
        selected_level = data["level_cb"].get()

        rank, bonus = self.skill_ranks_info.get(selected_level, (-1, -20))

        data["rank_var"].set(str(rank))
        data["bonus_var"].set(f"+{bonus}" if bonus >= 0 else str(bonus))

        for widget in data["tn_container"].winfo_children():
            widget.destroy()

        data["tn_entries"] = []
        selected_attrs = [cb.get() for cb in data["attr_cbs"] if cb.get() != "None"]

        for idx, stat in enumerate(selected_attrs):
            if idx > 0:
                ttk.Label(data["tn_container"], text=",").pack(side="left", padx=1)

            stat_val_str = getattr(self, "attr_vars", {}).get(stat, tk.StringVar(value="0")).get()
            try:
                stat_val = int(stat_val_str)
            except ValueError:
                stat_val = 0

            tn_val = stat_val + bonus
            tn_var = tk.StringVar(value=str(tn_val))
            tn_entry = ttk.Entry(data["tn_container"], textvariable=tn_var, width=4, justify="center", state="readonly")
            tn_entry.pack(side="left")

            data["tn_entries"].append((stat, tn_var))

    def update_cs_values(self):
        """Aktualizuje wartości Rank, Bonus oraz TN (dla Str i Ag) w Combat Style."""
        selected_level = self.cs_level_cb.get()
        rank, bonus = self.skill_ranks_info.get(selected_level, (-1, -20))

        self.cs_rank_var.set(str(rank))
        self.cs_bonus_var.set(f"+{bonus}" if bonus >= 0 else str(bonus))

        str_val = int(getattr(self, "attr_vars", {}).get("Str", tk.StringVar(value="0")).get() or 0)
        ag_val = int(getattr(self, "attr_vars", {}).get("Ag", tk.StringVar(value="0")).get() or 0)

        self.cs_tn_str_var.set(str(str_val + bonus))
        self.cs_tn_ag_var.set(str(ag_val + bonus))

    def recalculate_all_tns(self):
        """Wywoływane przy zmianie statystyk w Tab 1 - odświeża TN dla wszystkich sekcji w Tab 2."""
        if hasattr(self, 'skill_vars'):
            for skill_name in self.skill_vars:
                self.update_skill_values(skill_name)

        if hasattr(self, 'prof_vars'):
            for prof_id in self.prof_vars:
                data = self.prof_vars[prof_id]
                _, bonus = self.skill_ranks_info.get(data["level_cb"].get(), (-1, -20))
                for stat, tn_var in data["tn_entries"]:
                    stat_val_str = getattr(self, "attr_vars", {}).get(stat, tk.StringVar(value="0")).get()
                    try:
                        stat_val = int(stat_val_str)
                    except ValueError:
                        stat_val = 0
                    tn_var.set(str(stat_val + bonus))

        if hasattr(self, 'cs_level_cb'):
            self.update_cs_values()
#---------------PAGE3------------------
    def setup_tab3(self, parent):
        # Główny kontener dzielący ekran na lewy i prawy
        main_container = ttk.Frame(parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        left_side = ttk.Frame(main_container)
        left_side.pack(side="left", fill="both", expand=True, padx=(0, 5))

        right_side = ttk.Frame(main_container)
        right_side.pack(side="right", fill="both", expand=True, padx=(5, 0))

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
        # PRAWA STRONA: WEAPONS (MELEE & RANGED)
        # ==========================================
        dmg_options = ["1d4", "1d6", "1d8", "1d10", "1d12", "2d8", "2d10", "2d12"]
        bonus_mat_options = [f"+{i}" for i in range(0, 11)]

        self.weapons_vars = {"melee": [], "ranged": []}

        # Funkcja pomocnicza do budowania tabeli broni
        def build_weapon_table(parent_frame, title, category_key):
            frame = ttk.LabelFrame(parent_frame, text=title)
            frame.pack(fill="x", pady=(0, 5))

            headers = ["Name", "Dmg", "Mat. Bonus", "H", "Reach", "ENC"]
            for col_idx, h in enumerate(headers):
                ttk.Label(frame, text=h, font=('Helvetica', 8, 'bold')).grid(row=0, column=col_idx, padx=2, pady=2)

            for row_idx in range(1, 6):  # 3 wiersze na kategorię
                name_entry = ttk.Entry(frame, width=50)
                name_entry.grid(row=row_idx, column=0, padx=2, pady=2)

                dmg_cb = ttk.Combobox(frame, values=dmg_options, state="readonly", width=6)
                dmg_cb.set("1d4")
                dmg_cb.grid(row=row_idx, column=1, padx=2, pady=2)

                mat_cb = ttk.Combobox(frame, values=bonus_mat_options, state="readonly", width=5)
                mat_cb.set("0")
                mat_cb.grid(row=row_idx, column=2, padx=2, pady=2)

                h_entry = ttk.Entry(frame, width=4, justify="center")
                h_entry.grid(row=row_idx, column=3, padx=2, pady=2)

                reach_entry = ttk.Entry(frame, width=6, justify="center")
                reach_entry.grid(row=row_idx, column=4, padx=2, pady=2)

                enc_entry = ttk.Entry(frame, width=5, justify="center")
                enc_entry.grid(row=row_idx, column=5, padx=2, pady=2)

                self.weapons_vars[category_key].append({
                    "name": name_entry,
                    "dmg": dmg_cb,
                    "mat_bonus": mat_cb,
                    "h": h_entry,
                    "reach": reach_entry,
                    "enc": enc_entry
                })

        build_weapon_table(right_side, "Melee Weapons", "melee")
        build_weapon_table(right_side, "Ranged Weapons", "ranged")
if __name__ == "__main__":
    app = UESRPGCharacterSheet()
    app.mainloop()