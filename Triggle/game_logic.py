
def is_move_valid(start_pillar, direction, game_state):
    letter, number = start_pillar
    end_pillar_position = find_end_pillar(start_pillar, direction, game_state.table_size)

    # ako je krajnji stubic izvan table potez je nevalidan
    if end_pillar_position not in game_state.pillars:
        return False

    completed_sides = find_completed_sides(start_pillar, direction, game_state)
    # ako gumica ne formira nijednu novu stranicu, potez je nevalidan
    if set(completed_sides).issubset(game_state.completed_sides):
        return False

    return True

def find_completed_sides(start_pillar, direction, game_state):
    middle_pillar_1 = find_end_pillar(start_pillar, direction, game_state.table_size, rubber_length=1)
    middle_pillar_2 = find_end_pillar(middle_pillar_1, direction, game_state.table_size, rubber_length=1)
    end_pillar = find_end_pillar(middle_pillar_2, direction, game_state.table_size, rubber_length=1)
    return [(start_pillar, middle_pillar_1), (middle_pillar_1, middle_pillar_2), (middle_pillar_2, end_pillar)]

# start je stubic npr. ("A",1), smer je "DD" | "GL" | "DL" | "GD" | "D" | "L"
def find_end_pillar(start, direction, table_size, rubber_length=3):
    # ova metoda samo nalazi zavrsni stubic ali ne garantuje da je unutar table
    letter = start[0]
    number = start[1]
    middle_letter = chr(ord("A") + table_size - 1) # ord uzima ASCII kod, chr vraca iz ASCII koda u karakter

    if direction == "D":
        # ako se ide udesno, slovo je uvek isto a broj se poveca za duzinu gumice
        return letter, number + rubber_length

    if direction == "L":
        # suprotno od D
        return letter, number - rubber_length

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

    if direction == "GL":
        # suprotno od DD
        for _ in range(rubber_length):
            if letter <= middle_letter:
                letter = chr(ord(letter) - 1)
                number -= 1
            else:
                letter = chr(ord(letter) - 1)

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

    if direction == "GD":
        # suprotno od DL
        for _ in range(rubber_length):
            if letter <= middle_letter:
                letter = chr(ord(letter) - 1)
            else:
                letter = chr(ord(letter) - 1)
                number += 1

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

def find_triangles_to_occupy(start_pillar, direction, game_state):

    current_pillar = start_pillar
    next_pillar = find_end_pillar(current_pillar, direction, game_state.table_size, rubber_length=1)
    # smerovi "normalni" na smer poteza
    normal_directions = {
        "D": ["GD", "DD"],
        "DD": ["D", "DL"],
        "DL": ["DD", "L"]
    }
    result = []
    for _ in range(3):
        for normal_direction in normal_directions[direction]:
            third_pillar = find_end_pillar(current_pillar, normal_direction, game_state.table_size, rubber_length=1)

            # ako je treci stubic van table, predji na sledecu iteraciju
            if third_pillar not in game_state.pillars:
                continue

            # imamo current, next i third pillar pa proveravamo da li je tu formiran trougao
            # ako postoje gumice od current do third i od third do next onda je formiran trougao
            if (sort_two_pillars(current_pillar, third_pillar) in game_state.completed_sides and
               sort_two_pillars(third_pillar, next_pillar) in game_state.completed_sides):
                triangle = sort_three_pillars_clockwise(current_pillar, third_pillar, next_pillar)
                # ako je trouglic vec zauzet, ne dodajemo ga u rezultat
                if triangle not in game_state.x_player_fields and triangle not in game_state.o_player_fields:
                    result.append(triangle)

        current_pillar = next_pillar
        next_pillar = find_end_pillar(current_pillar, direction, game_state.table_size, rubber_length=1)

    return result

# ova funkcija vraca tuple od prosledjena dva susedna stubica, ali s tim da je drugi u tupple-u
# ili desno ili dole desno ili dole levo u odnosu na prvi, jer su u tom formatu zapamceni u set-u
def sort_two_pillars(p1, p2):
    letter1, number1 = p1
    letter2, number2 = p2

    if letter1 < letter2:
        return p1,p2
    elif letter1 > letter2:
        return p2,p1
    else:
        if number1 < number2:
            return p1,p2
        else:
            return p2,p1

def sort_three_pillars_clockwise(p1,p2,p3):
    letter1, number1 = p1
    letter2, number2 = p2
    letter3, number3 = p3

    single_pillar = None
    double_pillars = []

    # prvo nadjemo koje slovo se javlja u dva temena, a koje u samo jednom
    if letter1 == letter2:
        # ako su l1 i l2 isti, onda je l3 sam
        double_letter = letter1
        single_letter = letter3
        single_pillar = p3
        double_pillars.append(p1)
        double_pillars.append(p2)
    elif letter1 == letter3:
        # ako nije ispunjen prvi uslov, a l1 i l3 su isti, onda je l2 sam
        double_letter = letter1
        single_letter = letter2
        single_pillar = p2
        double_pillars.append(p1)
        double_pillars.append(p3)
    else:
        # ako nijedan od prva dva uslova nije ispunjen, onda je l1 sam
        double_letter = letter2
        single_letter = letter1
        single_pillar = p1
        double_pillars.append(p2)
        double_pillars.append(p3)

    if single_letter < double_letter:
        # radi se o trouglu okrenutom nagore
        # vracamo gornje teme iza koga slede donja dva sdesna nalevo
        left, right = sort_two_pillars(double_pillars[0], double_pillars[1])
        return single_pillar, right, left
    else:
        # radi se o trouglu okrenutom nadole
        # vracamo gornja dva temena uredjena sleva nadesno, iza kojih sledi donje teme
        left, right = sort_two_pillars(double_pillars[0], double_pillars[1])
        return left, right, single_pillar

def change_game_state(start_pillar, direction, game_state):
    # dodajemo stranice trouglica koje je postavljena gumica formirala
    completed_sides = find_completed_sides(start_pillar, direction, game_state)
    for completed_side in completed_sides:
        game_state.completed_sides.add(completed_side)


    # dodajemo trouglice koji su formirani
    triangles_to_occupy = find_triangles_to_occupy(start_pillar, direction, game_state)
    for triangle in triangles_to_occupy:
        if game_state.x_or_o == "X":
            game_state.x_player_fields.add(triangle)
        else:
            game_state.o_player_fields.add(triangle)

    old_player = game_state.x_or_o
    # menjamo ko je na potezu
    game_state.x_or_o = "X" if old_player == "O" else "O"

    # vratimo trouglice koje ui treba da oboji
    return old_player, triangles_to_occupy, completed_sides

def find_all_possible_moves(game_state):
    all_possible_moves = []
    for pillar in game_state.pillars:
        letter, number = pillar
        for direction in game_state.all_directions:
            if is_move_valid(pillar, direction, game_state):
                all_possible_moves.append((letter, number, direction))

    return all_possible_moves


def find_all_game_states(game_state):
    result = []

    for move in find_all_possible_moves(game_state):
        letter, number, direction = move
        new_state = game_state.clone()
        change_game_state((letter, number), direction, new_state)
        result.append(new_state)

    return result

def evaluate_state(game_state):
    return len(game_state.x_player_fields) - len(game_state.o_player_fields)

def max_value(state, depth, alpha, beta, possible_moves, move=None):
    if is_game_over(state):
        return move, evaluate_state(state)

    if depth == 0 or possible_moves is None or len(possible_moves) == 0:
        return move, evaluate_state(state)
    else:
        for s in possible_moves:
            letter, number, direction = s
            new_possible_moves = possible_moves.copy()
            new_possible_moves.remove(s)
            new_state = state.clone()
            change_game_state((letter, number), direction, new_state)
            alpha = max(
                alpha,
                min_value(new_state, depth - 1, alpha, beta, new_possible_moves, s if move is None else move),
                key=lambda x: x[1]
            )
            if alpha[1] >= beta[1]:
                return beta
        return alpha

def min_value(state, depth, alpha, beta, possible_moves, move=None):
    if is_game_over(state):
        return move, evaluate_state(state)

    if depth == 0 or possible_moves is None or len(possible_moves) == 0:
        return move, evaluate_state(state)
    else:
        for s in possible_moves:
            letter, number, direction = s
            new_possible_moves = possible_moves.copy()
            new_possible_moves.remove(s)
            new_state = state.clone()
            change_game_state((letter, number), direction, new_state)
            beta = min(
                beta,
                max_value(new_state, depth - 1, alpha, beta, new_possible_moves, s if move is None else move),
                key=lambda x: x[1]
            )
            if beta[1] <= alpha[1]:
                return alpha
        return beta


def minimax(state, depth, is_my_move, alpha=(None, -1000), beta=(None, 1000)):
    if is_my_move:
        return max_value(state, depth, alpha, beta, state.all_possible_moves)
    else:
        return min_value(state, depth, alpha, beta, state.all_possible_moves)