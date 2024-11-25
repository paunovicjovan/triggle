import game_logic
from game_state import GameState
import math

# iskopiraj tcl folder iz foldera gde je python instaliran, u venv

# 1. otvori ovaj link: https://www.fontspace.com/category/gaming?p=10
# 2. skini Emotion Engine Font
# 3. kad ga raspakujes otvori ovo i instaliraj ga: EmotionEngineItalic-Mr0v.ttf
# 4. (moz da proveris u Font settings u windows dal ga ima za svaki slucaj, al mora da ga ima)

import tkinter as tk

class GameUI:
    def __init__(self):
        # Prozor
        self.root = tk.Tk()

        # stanje igre
        self.game_state = GameState(4)

        # UI atributi
        self.root.resizable(False, False)
        self.options_region_width = 300 # Sirina levog dela prozora sa opcijama za igru
        self.options_frame = None # Frame u kom se nalaze UI elementi za opcije
        self.table_region_width = 0 # Sirina desnog dela gde je tabla
        self.window_height = 600
        # ove promenljive koje se zavrsavaju sa var su za vezane ui elemente
        # game state svakako ima svoje odgovarajuce atribute
        self.table_size_var = tk.IntVar(value=self.game_state.table_size) # Broj stubica po stranici table
        self.human_or_computer_var = tk.StringVar(value="human") # po defaultu human
        self.x_or_o_var = tk.StringVar(value="X")  # po defaultu X
        self.pillars = dict() # ovde ce da budu sacuvane oznake
                              # i koordinate centra stubica npr. (A,1): (x,y)
                              # nije u game_state jer je vise stvar vezana za UI zbog pozicije x,y

        self.pillar_radius = 10 # poluprecnik stubica
        self.player_radius = 12 # poluprecnik oznake igraca
        self.clicked_pillar = None

        self.triangle_sides = { # duzina stranice trouglica u zavisnosti od broja stubica po stranici
            4: 100,
            5: 85,
            6: 75,
            7: 70,
            8: 65
        }

        self.hexagon_diagonal_length = 6 * self.triangle_sides[self.game_state.table_size] # dijagonala sestougla koji formiraju stubici, ne pozadine
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
        side_length_dropdown = tk.OptionMenu(self.options_frame, self.table_size_var, *side_length_options)
        side_length_dropdown.config(font=("Emotion Engine Italic", 18), padx=10, pady=7)
        side_length_dropdown.place(x=30, y=80)

        # Deo za izbor ko igra prvi covek ili racunar
        title2 = tk.Label(self.options_frame, text="Ko igra prvi:", font=("Emotion Engine Italic", 22))
        title2.place(x=30, y=180)

        human_radio = tk.Radiobutton(
            self.options_frame,
            text="Covek",
            variable=self.human_or_computer_var,
            value="human",
            font=("Emotion Engine Italic", 18)
        )
        computer_radio = tk.Radiobutton(
            self.options_frame,
            text="Racunar",
            variable=self.human_or_computer_var,
            value="computer",
            font=("Emotion Engine Italic", 18)
        )
        human_radio.place(x=30, y=230)
        computer_radio.place(x=150, y=230)

        #Deo za izbor koji simbol je prvi X ili O
        title3 = tk.Label(self.options_frame, text="Pocetni simbol:", font=("Emotion Engine Italic", 22))
        title3.place(x=30, y=300)
        x_radio = tk.Radiobutton(
            self.options_frame,
            text="X",
            variable=self.x_or_o_var,
            value="X",
            font=("Emotion Engine Italic", 18)
        )
        o_radio = tk.Radiobutton(
            self.options_frame,
            text="O",
            variable=self.x_or_o_var,
            value="O",
            font=("Emotion Engine Italic", 18)
        )
        x_radio.place(x=30, y=350)
        o_radio.place(x=100, y=350)

        #Dugme za pocetak igre
        start_button = tk.Button(self.options_frame, text="Zapocni igru", command=self.start_game, font=("Emotion Engine Italic", 18), bg="#32cd32")
        start_button.place(x=30, y=420)

        # Dugme za zavrsetak igre
        if self.game_state.game_started:
            self.end_button = tk.Button(self.options_frame, text="Zavrsi igru", command=self.end_game, font=("Emotion Engine Italic", 18), bg="#ff2c2c")
            self.end_button.place(x=30, y=500)

        self.root.mainloop()

    def generate_table(self):
        self.hexagon_diagonal_length = ((self.table_size_var.get() - 1) * 2 *
                                        self.triangle_sides[self.table_size_var.get()])
        # mora malo veci canvas jer je table_diagonal_length za stubice a za pozadinu treba jos malo prostor
        # i plus jos 50 okolo da ne bude zalepljena tabla uz ivice
        self.table_region_width = self.hexagon_diagonal_length + 2 * self.hexagon_padding + 50

        if self.canvas:
            self.canvas.destroy()

        self.canvas = tk.Canvas(self.root, width=self.table_region_width, height=self.table_region_width)
        self.canvas.place(x=self.options_region_width, y=0)

        self.root.geometry(f"{self.options_region_width + self.table_region_width}x{self.table_region_width}")

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
        triangle_side = self.triangle_sides[self.table_size_var.get()] # Duzina stranice trouglica
        triangle_height = triangle_side * math.sqrt(3) / 2
        first_x = center_x + radius * math.cos(-2 * math.pi / 3) # x koordinata stubica A1
        first_y = center_y + radius * math.sin(-2 * math.pi / 3) # y koordinata stubica A1

        pillars_in_row_count = self.table_size_var.get()

        for i, letter in enumerate(self.game_state.letters):
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

            if i < len(self.game_state.letters) // 2:
                first_x -= triangle_side / 2
                pillars_in_row_count += 1
            else:
                first_x += triangle_side / 2
                pillars_in_row_count -= 1

    def on_pillar_click(self, event):
        if self.clicked_pillar:
            self.canvas.itemconfig(self.clicked_pillar, fill="white")

        self.clicked_pillar = self.canvas.find_withtag("current")[0]
        tags = self.canvas.gettags(self.clicked_pillar)

        # Pronađi red i kolonu iz taga
        for tag in tags:
            if tag.startswith("circle_"):
                letter, number = tag.split("_")[1:]
                self.canvas.itemconfig(self.clicked_pillar, fill="yellow")
                print(f"Kliknuto na stubic {letter}{number}")
                self.find_possible_directions((letter, int(number)))


    def start_game(self):
        # nebitno, samo za test bilo
        first_player = "Covek" if self.human_or_computer_var.get() == "human" else "Racunar"
        starting_symbol = self.x_or_o_var.get()
        print(f"{first_player} igra prvi koristeci simbol '{starting_symbol}'.")
        ###

        self.game_state = GameState(self.table_size_var.get())
        self.game_state.human_or_computer = self.human_or_computer_var.get()
        self.game_state.x_or_o = self.x_or_o_var.get()
        self.game_state.game_started = True

        self.generate_table()

        # test
        self.occupy_triangle(("B",1), ("A", 1), ("B", 2), "o")
        self.occupy_triangle(("A",1), ("A", 2), ("B", 2), "x")
        self.draw_rubber(("A", 4),("D", 4))
        # test
        game_logic.is_game_over(self.game_state)

        self.end_button = tk.Button(self.options_frame, text="Zavrsi igru", command=self.end_game, font=("Emotion Engine Italic", 18), bg="#ff2c2c")
        self.end_button.place(x=30, y=500)

    def end_game(self):
        print("Igra je zavrsena")
        self.end_button.place_forget() # sakrije dugme za zavrsetak
        self.human_or_computer_var.set("human") # resetuje radio button
        self.x_or_o_var.set("X")
        self.table_size_var.set(4) # resetuje dropdown
        self.game_state.game_started = False

    # t je oblika (A,1)
    def occupy_triangle(self, t1, t2, t3, player):

        x1,y1 = self.pillars[t1]
        x2,y2 = self.pillars[t2]
        x3,y3 = self.pillars[t3]
        xc = (x1 + x2 + x3) / 3
        yc = (y1 + y2 + y3) / 3
        color = "blue" if player == "X" or player == "x" else "red"

        self.canvas.create_oval(xc - self.player_radius,
                                yc - self.player_radius,
                                xc + self.player_radius,
                                yc + self.player_radius,
                                fill=color)

        self.canvas.create_text(
            xc, yc,
            text=player.upper(),
            font=("Arial", 10),
            fill="white"
        )

        # promeni game_state

    def draw_rubber(self, start, end):
        if start not in self.pillars or end not in self.pillars:
            print("Nemoguce crtanje gumice, zadati nevalidni stubici")
            return

        x1, y1 = self.pillars[start]
        x2, y2 = self.pillars[end]
        r = self.pillar_radius

        dx = x2 - x1
        dy = y2 - y1

        theta = math.atan2(dy, dx)

        # Ugao za tangente
        theta1 = theta + math.pi / 2  # Prva tangenta
        theta2 = theta - math.pi / 2  # Druga tangenta

        # tacke dodira na prvom stubicu
        # jedna linija krece odavde
        t1x1 = x1 + r * math.cos(theta1)
        t1y1 = y1 + r * math.sin(theta1)

        # druga krece odavde
        t2x1 = x1 + r * math.cos(theta2)
        t2y1 = y1 + r * math.sin(theta2)

        # tacke dodira na drugom stubicu
        # prva linija se zavrsava ovde
        t1x2 = x2 + r * math.cos(theta1)
        t1y2 = y2 + r * math.sin(theta1)

        # druga linija se zavrsava ovde
        t2x2 = x2 + r * math.cos(theta2)
        t2y2 = y2 + r * math.sin(theta2)

        # crtanje gumice
        self.canvas.create_line(t1x1, t1y1, t1x2, t1y2, fill="white", width=2)
        self.canvas.create_line(t2x1, t2y1, t2x2, t2y2, fill="white", width=2)

        # promeni game_state

    def find_possible_directions(self, pillar_position):
        for direction in self.game_state.all_directions:
            end_pillar_position = game_logic.find_end_pillar(pillar_position, direction, self.game_state.table_size)
            if end_pillar_position in self.pillars:
                print("Moze " + direction)

        print()
