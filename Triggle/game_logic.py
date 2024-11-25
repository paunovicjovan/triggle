from xmlrpc.client import boolean


# start je stubic npr. (A,1), smer je "DD" | "DL" | "D"
def find_end_pillar(start, direction, table_size):
    # ova metoda samo nalazi zavrsni stubic ali ne garantuje da je unutar table
    rubber_length = 3
    letter = start[0]
    number = start[1]
    middle_letter = chr(ord("A") + table_size - 1) # ord uzima ASCII kod, chr vraca iz ASCII koda u karakter

    if direction == "D":
        # ako se ide udesno, slovo je uvek isto a broj se poveca za duzinu gumice
        return letter, number + rubber_length

    if direction == "DD":
        for _ in range(rubber_length):
            # ako smo iznad polovine table i idemo dole desno, povecavaju se i slovo i broj
            if letter < middle_letter:
                letter = chr(ord(letter) + 1)
                number += 1
            # ako smo ispod polovine table i idemo dole desno, povecava se samo slovo
            else:
                letter = chr(ord(letter) + 1)

        return letter, number

    if direction == "DL":
        for _ in range(rubber_length):
            # ako smo iznad polovine table i idemo dole levo, povecava se samo slovo
            if letter < middle_letter:
                letter = chr(ord(letter) + 1)
            # ako smo ispod polovine table i idemo dole levo, povecava se slovo a broj se smanjuje
            else:
                letter = chr(ord(letter) + 1)
                number -= 1

        return letter, number

def is_game_over(game_state):
    # racunanje koliko tabla ima ukupno mogucih polja koja mogu da se osvoje
    # sestougao se sastoji od 6 jednakostranicna trougla, a u svakom je (table_size - 1) ** 2 trouglica
    total_triangles_count = 6 * (game_state.table_size - 1) ** 2
    half_triangles_count = total_triangles_count // 2

    # prvi kriterijum - neki od igraca je zauzeo vise od polovine mogucih polja
    if (len(game_state.x_player_fields) > half_triangles_count or
        len(game_state.o_player_fields) > half_triangles_count):
        return True

    # i koliko ima stranica trouglica bez ponavljanja
    # izbroje se prvo vodoravne stranice pa se na kraju pomnozi sa 3 da se dobije za celu tablu
    # suma brojeva od 3 do 6 za tablu velicine 4
    half = sum(range(game_state.table_size - 1, 2 * game_state.table_size - 1))
    # sabiramo za gornju i donju polovinu i oduzimamo broj stranica na dijagonali jer je dva puta uracunat
    horizontal_triangle_sides_count = 2 * half - 2 * (game_state.table_size - 1)
    total_triangle_sides_count = 3 * horizontal_triangle_sides_count

    if len(game_state.completed_sides) == total_triangle_sides_count:
        return True

    return False