
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

