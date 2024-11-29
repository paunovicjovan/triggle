

class GameState:
    def __init__(self, table_size):

        if table_size < 4 or table_size > 8:
            raise "Neispravna velicina table"
        # pozicije igraca u formatu (T1, T2, T3) npr. ((A,1), (A,2), (B,2))
        # tri temena koja odredjuju poziciju igraca su uvek uredjena kao kad
        # se obilaze u smeru kazaljke na satu pocev od gornjeg/gornjeg levog temena
        self.x_player_fields = set()
        self.o_player_fields = set()

        # svaka razvucena gumica u formatu (slovo, broj, smer) npr. (A, 1, "DD")
        # smerovi mogu da budu: "D" - Desno, "DD" - Dole Desno, "DL" - Dole Levo
        self.rubber_positions = set()

        # popunjene stranice trouglica u formatu (T1, T2) npr. ((A,1), (B,2))
        # druga tacka je uvek desno ili dole desno ili dole levo u odnosu na prvu
        self.completed_sides = set()

        # broj stubica po stranici table
        self.table_size = table_size

        self.human_or_computer = "human" # "human" | "computer"
        self.x_or_o = "X" # "X" | "O"
        self.game_started = False

        self.letters = [chr(x+65) for x in range(0, 2 * self.table_size - 1)]
        self.numbers = [x + 1 for x in range(0, 2 * self.table_size - 1)]
        self.all_directions = ["D", "DD", "DL"]
