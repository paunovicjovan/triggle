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
        self.window_height = 600
        self.side_length_var = tk.IntVar(value=4) # Broj stubica po stranici table
        self.human_or_computer = None
        self.x_or_o = None
        self.game_started = False
        self.pillars = dict() # ovde ce da budu sacuvane oznake
                              # i koordinate centra stubica npr. (A,1): (x,y)
                              # ili mozda obrnuto

        self.letters = [] # slova koja odredjuju red stubica
        self.numbers = [] # brojevi koji odredjuju "kolonu" stubica
        self.pillar_radius = 10 # poluprecnik stubica

        self.triangle_sides = {
            4: 100,
            5: 85,
            6: 75,
            7: 70,
            8: 65
        }

        self.hexagon_diagonal_length = 6 * self.triangle_sides[4] # dijagonala sestougla koji formiraju stubici, ne pozadine
        self.hexagon_padding = 30 # razmak od stubica do temena hexagona
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
        title2.place(x=30, y=180)
        self.human_or_computer = tk.StringVar(value="abc") # mora nesto da se stavi da ne bi bili cekirani
        human_radio = tk.Radiobutton(
            self.options_frame,
            text="Covek",
            variable=self.human_or_computer,
            value="human",
            font=("Emotion Engine Italic", 18)
        )
        computer_radio = tk.Radiobutton(
            self.options_frame,
            text="Racunar",
            variable=self.human_or_computer,
            value="computer",
            font=("Emotion Engine Italic", 18)
        )
        human_radio.place(x=30, y=230)
        computer_radio.place(x=150, y=230)

        #Deo za izbor koji simbol je prvi X ili O
        title3 = tk.Label(self.options_frame, text="Pocetni simbol:", font=("Emotion Engine Italic", 22))
        title3.place(x=30, y=300)
        self.x_or_o = tk.StringVar(value="abc") # mora nesto da se stavi da nebi bili cekirani
        x_radio = tk.Radiobutton(
            self.options_frame,
            text="X",
            variable=self.x_or_o,
            value="X",
            font=("Emotion Engine Italic", 18)
        )
        o_radio = tk.Radiobutton(
            self.options_frame,
            text="O",
            variable=self.x_or_o,
            value="O",
            font=("Emotion Engine Italic", 18)
        )
        x_radio.place(x=30, y=350)
        o_radio.place(x=100, y=350)

        #Dugme za pocetak igre
        start_button = tk.Button(self.options_frame, text="Zapocni igru", command=self.start_game, font=("Emotion Engine Italic", 18), bg="#32cd32")
        start_button.place(x=30, y=420)

        # Dugme za zavrsetak igre
        if self.game_started:
            self.end_button = tk.Button(self.options_frame, text="Zavrsi igru", command=self.end_game, font=("Emotion Engine Italic", 18), bg="#ff2c2c")
            self.end_button.place(x=30, y=500)

        self.root.mainloop()

    def generate_table(self):
        self.hexagon_diagonal_length = ((self.side_length_var.get() - 1) * 2 *
                                        self.triangle_sides[self.side_length_var.get()])
        # mora malo veci canvas jer je table_diagonal_length za stubice a za pozadinu treba jos malo prostor
        # i plus jos 50 okolo da ne bude zalepljena tabla uz ivice
        self.table_region_width = self.hexagon_diagonal_length + 2 * self.hexagon_padding + 50

        if self.canvas:
            self.canvas.destroy()

        self.canvas = tk.Canvas(self.root, width=self.table_region_width, height=self.table_region_width)
        self.canvas.place(x=self.options_region_width, y=0)

        self.root.geometry(f"{self.options_region_width + self.table_region_width}x{self.table_region_width}")

        self.letters = [chr(x+65) for x in range(0, 2 * self.side_length_var.get()-1)]
        self.numbers = [x + 1 for x in range(0, 2*self.side_length_var.get() - 1)]

        self.draw_hexagon()
        self.draw_pillars()

    def draw_hexagon(self):
        center_x = self.table_region_width / 2  # X koordinata centra
        center_y = self.table_region_width / 2  # Y koordinata centra
        radius = self.hexagon_diagonal_length / 2 + self.hexagon_padding  # Poluprečnik

        # Računanje koordinata temena sestougla
        points = []
        for i in range(6):
            angle = math.radians(i * 60)  # Ugao u radijanima
            x = center_x + radius * math.cos(angle)  # X koordinata tačke
            y = center_y + radius * math.sin(angle)  # Y koordinata tačke
            points.append(x)
            points.append(y)

        # Crtanje pravilnog šestougla
        self.canvas.create_polygon(points, outline="black", fill="#333", width=2)

    def draw_pillars(self):
        center_x = self.table_region_width / 2  # X koordinata centra
        center_y = self.table_region_width / 2  # Y koordinata centra
        radius = self.hexagon_diagonal_length / 2  # Poluprečnik
        triangle_side = self.triangle_sides[self.side_length_var.get()] # Duzina stranice trouglica
        triangle_height = triangle_side * math.sqrt(3) / 2
        first_x = center_x + radius * math.cos(-2 * math.pi / 3)
        first_y = center_y + radius * math.sin(-2 * math.pi / 3)

        pillars_in_row_count = self.side_length_var.get()

        for i, letter in enumerate(self.letters):
            x=first_x
            y=first_y
            for j in range(pillars_in_row_count):
                self.pillars[(letter, j+1)] = (x, y)
                circle_id = self.canvas.create_oval(x - self.pillar_radius,
                                        y - self.pillar_radius,
                                        x + self.pillar_radius,
                                        y + self.pillar_radius,
                                        fill="white")

                # Dodeljivanje jedinstvenog taga svakom stubicu
                tag = f"circle_{letter}_{j+1}"
                self.canvas.itemconfig(circle_id, tags=(tag,))

                # Vezivanje dogadjaja za klik na stubic
                self.canvas.tag_bind(tag, "<Button-1>", self.on_pillar_click)

                x+=triangle_side

            first_y += triangle_height

            if i < len(self.letters) // 2:
                first_x -= triangle_side / 2
                pillars_in_row_count += 1
            else:
                first_x += triangle_side / 2
                pillars_in_row_count -= 1

    def on_pillar_click(self, event):
        clicked_item = self.canvas.find_withtag("current")[0]
        tags = self.canvas.gettags(clicked_item)

        # Pronađi red i kolonu iz taga
        for tag in tags:
            if tag.startswith("circle_"):
                letter, number = tag.split("_")[1:]
                print(f"Kliknuto na stubic {letter}{number}")

    def start_game(self):
        if self.human_or_computer.get() == "abc" or self.x_or_o.get() == "abc":
            print("Niste odabrali ko igra prvi i sa kojim simbolom pocinje")
            return

        first_player = "Covek" if self.human_or_computer.get() == "human" else "Racunar"
        starting_symbol = self.x_or_o.get()

        print(f"{first_player} igra prvi koristeci simbol '{starting_symbol}'.")

        self.game_started = True

        self.end_button = tk.Button(self.options_frame, text="Zavrsi igru", command=self.end_game, font=("Emotion Engine Italic", 18), bg="#ff2c2c")
        self.end_button.place(x=30, y=500)

    def end_game(self):
        print("Igra je zavrsena")
        self.end_button.place_forget() # sakrije dugme za zavrsetak
        self.human_or_computer.set("abc") # ocisti radio button
        self.x_or_o.set("abc")
        self.side_length_var.set(4) # resetuje dropdown
        self.game_started = False
