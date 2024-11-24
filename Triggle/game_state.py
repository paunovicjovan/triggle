

class GameState:
    def __init__(self):
        # pozicije igraca u formatu (T1, T2, T3) npr. ((A,1), (A,2), (B,2))
        self.x_player_fields = set()
        self.o_player_fields = set()

        # svaka razvucena gumica u formatu (slovo, broj, smer) e.g (A, 1, "DD")
        # smerovi mogu da budu: "D" - Desno, "DD" - Dole Desno, "DL" - Dole Levo
        self.rubber_positions = set()

        # popunjene stranice trouglica u formatu (T1, T2) npr. ((A,1), (B,2))
        # druga tacka je uvek desno ili dole desno ili dole levo u odnosu na prvu
        self.completed_sides = set()

        # broj stubica po stranici table
        self.table_size = 4

        self.human_or_computer = "human" # "human" | "computer"
        self.x_or_o = "X" # "X" | "O"

        self.letters = []
        self.numbers = []