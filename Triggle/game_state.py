import copy

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

        self.pillars = dict()  # ovde ce da budu sacuvane oznake
                               # i koordinate centra stubica npr. ("A",1): (x,y)

    def clone(self):
        new_instance = GameState(self.table_size)
        # duboko kopiranje za atribute koji se menjaju
        new_instance.x_player_fields = set(self.x_player_fields)
        new_instance.o_player_fields = set(self.o_player_fields)
        new_instance.completed_sides = set(self.completed_sides)
        new_instance.human_or_computer = self.human_or_computer
        new_instance.x_or_o = self.x_or_o
        new_instance.game_started = self.game_started

        # plitko kopiranje za atribute koji su u svakom game state-u isti
        new_instance.letters = self.letters
        new_instance.numbers = self.numbers
        new_instance.all_directions = self.all_directions
        new_instance.pillars = self.pillars

        return new_instance