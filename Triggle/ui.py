import game_state
import math

# iskopiraj tcl folder iz foldera gde je python instaliran, u venv

# 1. otvori ovaj link: https://www.fontspace.com/category/gaming?p=10
# 2. skini Emotion Engine Font
# 3. kad ga raspakujes otvori ovo i instaliraj ga: EmotionEngineItalic-Mr0v.ttf
# 4. (moz da proveris u Font settings u windows dal ga ima za svaki slucaj, al mora da ga ima)

import tkinter as tk

class GameUI:
    def __init__(self):
        self.root = tk.Tk() # Prozor
        self.root.resizable(False, False)
        self.options_region_width = 300 # Sirina levog dela prozora sa opcijama za igru
        self.options_frame = None # Frame u kom se nalaze UI elementi za opcije
        self.table_region_width = 0 # Sirina desnog dela gde je tabla
        self.window_height = 500
        self.side_length_var = tk.IntVar(value=4) # Broj stubica po stranici table
        self.human_or_computer = None # 1 za coveka, 2 za racunara
        self.x_or_o = None # 1 za X, 2 za O
        self.game_started = False

        # self.start_triangle_side = 40 # Pocetna duzina stranice trouglica
        # self.triangle_side_factor = 5 # Faktor za skaliranje pri promeni velicine table, mora da se sredi to i formula ispod
        # self.triangle_side = self.start_triangle_side - self.triangle_side_factor * self.side_length_var.get()

        # hardkodirane duzine stranica trouglica jer nijedna formula iznad ne uspeva lepo da rasporedi
        self.triangle_sides = {
            4: 100,
            5: 85,
            6: 75,
            7: 70,
            8: 65
        }
        self.table_diagonal_length = 6 * self.triangle_sides[4]

        self.canvas = None

    def draw_ui(self):
        self.root.geometry(f'{self.options_region_width}x{self.window_height}')
        self.root.title("Triggle")

        # Leva strana - opcije igre
        self.options_frame = tk.Frame(self.root, width=self.options_region_width, height=self.window_height)
        self.options_frame.place(x=0, y=0)
        self.options_frame.pack_propagate(False)

        title = tk.Label(self.options_frame, text="Tabla:", font=("Emotion Engine Italic", 22))
        title.place(x=30, y=30)

        # Dropdown meni za izbor dužine stranice
        side_length_options = [4, 5, 6, 7, 8]
        side_length_dropdown = tk.OptionMenu(self.options_frame, self.side_length_var, *side_length_options)
        side_length_dropdown.config(font=("Emotion Engine Italic", 18), padx=10, pady=7)
        side_length_dropdown.place(x=30, y=80)

        # Dugme za generisanje table
        generate_button = tk.Button(self.options_frame, text="Generisi", command=self.generate_table, font=("Emotion Engine Italic", 18))
        generate_button.place(x=120, y=80)

        # Deo za izbor ko igra prvi covek ili racunar
        title2 = tk.Label(self.options_frame, text="Ko igra prvi:", font=("Emotion Engine Italic", 22))
        title2.place(x=30, y=150)
        human_button = tk.Button(self.options_frame, text="Covek", command=self.select_human, font=("Emotion Engine Italic", 18))
        computer_button = tk.Button(self.options_frame, text="Racunar", command=self.select_computer, font=("Emotion Engine Italic", 18))
        human_button.place(x=30, y=200)
        computer_button.place(x=120, y=200)

        #Deo za izbor koji simbol je prvi X ili O
        title3 = tk.Label(self.options_frame, text="X ili O:", font=("Emotion Engine Italic", 22))
        title3.place(x=30, y=280)
        x_button = tk.Button(self.options_frame, text="X", command=self.select_x, font=("Emotion Engine Italic", 18), padx=10)
        x_button.place(x=30, y=330)
        o_button = tk.Button(self.options_frame, text="O", command=self.select_o, font=("Emotion Engine Italic", 18), padx=10)
        o_button.place(x=100, y=330)

        #Dugme za pocetak igre
        start_button = tk.Button(self.options_frame, text="Zapocni igru", command=self.start_game, font=("Emotion Engine Italic", 18), bg="#32cd32")
        start_button.place(x=30, y=420)

        self.root.mainloop()

    def generate_table(self):
        # self.triangle_side = self.start_triangle_side + int(math.log2(self.side_length_var.get()) * self.triangle_side_factor)
        self.table_diagonal_length = (self.side_length_var.get() - 1) * 2 * self.triangle_sides[self.side_length_var.get()]
        # mora malo veci canvas jer je table_diagonal_length za stubice a za pozadinu treba jos malo prostor
        # i plus jos 20 okolo da ne bude zalepljena tabla uz ivice
        self.table_region_width = self.table_diagonal_length + 40 + 20

        if self.canvas:
            self.canvas.destroy()

        self.canvas = tk.Canvas(self.root, width=self.table_region_width, height=self.table_region_width)
        self.canvas.place(x=self.options_region_width, y=0)

        self.root.geometry(f"{self.options_region_width + self.table_region_width}x{self.table_region_width}")

        center_x = self.table_region_width / 2  # X koordinata centra
        center_y = self.table_region_width / 2 # Y koordinata centra
        radius = self.table_diagonal_length / 2 + 20  # Poluprečnik

        # Računanje koordinata tačaka
        points = []
        for i in range(6):
            angle = math.radians(i * 60)  # Ugao u radijanima
            x = center_x + radius * math.cos(angle)  # X koordinata tačke
            y = center_y + radius * math.sin(angle)  # Y koordinata tačke
            points.append(x)
            points.append(y)

        # Crtanje pravilnog šestougla
        self.canvas.create_polygon(points, outline="black", fill="#333", width=2)

    def select_human(self):
        self.human_or_computer = 1
        print("Covek igra prvi") # samo da testiram jel radi

    def select_computer(self):
        self.human_or_computer = 2
        print("Racunar igra prvi")

    def select_x(self):
        self.x_or_o = 1
        print("Prvi igra X")

    def select_o(self):
        self.x_or_o = 2
        print("Prvi igra O")

    def start_game(self):
        game_started = True
        print("Igra je zapoceta")
