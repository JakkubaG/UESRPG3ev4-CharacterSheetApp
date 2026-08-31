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
        notebook.add(tab4, text="Page 4: Talents, Traits, & Powers")
        notebook.add(tab5, text="Page 5: Items & Equipment")
        notebook.add(tab6, text="Page 6: Spellcasting")

        self.setup_tab1(tab1)
        # self.setup_tab2(tab2)
        # self.setup_tab3(tab3)
        # self.setup_tab4(tab4)
        # self.setup_tab5(tab5)
        # self.setup_tab6(tab6)

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
#---------------------------------
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

if __name__ == "__main__":
    app = UESRPGCharacterSheet()
    app.mainloop()