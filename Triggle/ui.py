import game_state
import math
# iskopiraj tcl folder iz foldera gde je python instaliran, u venv
import tkinter as tk

class GameUI:
    def __init__(self):
        self.root = tk.Tk() # Prozor
        self.options_region_width = 400 # Sirina levog dela prozora sa opcijama za igru
        self.options_frame = None # Frame u kom se nalaze UI elementi za opcije
        self.table_region_width = 0 # Sirina desnog dela gde je tabla
        self.window_height = 500
        self.side_length_var = tk.IntVar(value=4) # Broj stubica po stranici table
        self.start_triangle_side = 60 # Pocetna duzina stranice trouglica
        self.triangle_side_factor = 1 # Faktor za skaliranje pri promeni velicine table, mora da se sredi to i formula ispod
        self.triangle_side = self.start_triangle_side + int(math.log2(self.side_length_var.get()) * self.triangle_side_factor)
        self.table_diagonal_length = 6 * self.triangle_side

        self.canvas = None

    def draw_ui(self):
        self.root.geometry(f'{self.options_region_width}x{self.window_height}')
        self.root.title("Triggle")

        # Leva strana - opcije igre
        self.options_frame = tk.Frame(self.root, width=self.options_region_width, height=self.window_height)
        self.options_frame.place(x=0, y=0)

        title = tk.Label(self.options_frame, text="Triggle", font=("Helvetica", 24))
        title.pack(pady=20)

        # Dropdown meni za izbor dužine stranice
        side_length_options = [4, 5, 6, 7, 8]
        side_length_dropdown = tk.OptionMenu(self.options_frame, self.side_length_var, *side_length_options)
        side_length_dropdown.pack(pady=20)

        # Dugme za generisanje kvadrata
        generate_button = tk.Button(self.options_frame, text="Generisi", command=self.generate_table)
        generate_button.pack(pady=10)

        self.root.mainloop()

    def generate_table(self):
        self.triangle_side = self.start_triangle_side + int(math.log2(self.side_length_var.get()) * self.triangle_side_factor)
        self.table_diagonal_length = (self.side_length_var.get() - 1) * 2 * self.triangle_side
        self.table_region_width = self.table_diagonal_length

        if self.canvas:
            self.canvas.destroy()

        self.canvas = tk.Canvas(self.root, width=self.table_diagonal_length, height=self.table_diagonal_length)
        self.canvas.place(x=self.options_region_width, y=0)

        self.root.geometry(f"{self.options_region_width + self.table_region_width}x{self.table_region_width}")

        center_x = self.table_region_width / 2  # X koordinata centra
        center_y = self.table_region_width / 2  # Y koordinata centra
        radius = self.table_diagonal_length / 2  # Poluprečnik

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

