
class Node:
    def __init__(self, game_state):
        self.game_state = game_state
        self.children = []

    def add_child(self, game_state):
        self.children.append(Node(game_state))