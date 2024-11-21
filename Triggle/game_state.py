
# players positions in format (T1, T2, T3) e.g. (A1, A2, B2)
x_player_fields = set()
o_player_fields = set()

# each rubber in format (letter, number, direction) e.g (A, 1, BR)
# direction can be one of the following: R - Right, BR - Bottom Right, BL - Bottom Left
rubber_positions = set()

# triangle sides in format (start_point, end_point) e.g. ((A,1), (B,2))
# second point is always Right or Bottom Right or Bottom Left compared to the first point
completed_sides = set()

# length of table side, e.g. 4 pillars
table_size = 4


