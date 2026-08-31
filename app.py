import tkinter as tk
from tkinter import ttk
def __init__(self):
    super().__init__()
    self.title("CHARACTER SHEET - 3ev4")
    self.geometry("800x600")
    # Kontroler zakładek (Notebook)
    notebook = ttk.Notebook(self)
    notebook.pack(fill="both", expand=True)

    # Tworzenie zakładek dla stron karty
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)
    tab4 = ttk.Frame(notebook)

    notebook.add(tab1, text="Page 1: Character and skills")
    notebook.add(tab2, text="Page 2: Armor and Weapons  ")
    notebook.add(tab3, text="Page 3: Talents, Traits, & Powers")
    notebook.add(tab4, text="Page 4: Items & Equipment")

    self.setup_tab1(tab1)
    self.setup_tab2(tab2)
    self.setup_tab3(tab3)
    self.setup_tab4(tab4)