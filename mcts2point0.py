import math

import numpy as np
from morpion import *


class Node():
    def __init__(self, state, player_to_max, parent=None, parent_move=None):
        self.state = state
        self.parent = parent
        self.parent_move = parent_move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self.state.get_legal_moves_mcts()
        self.player_to_max = player_to_max

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_leaf(self):
        return len(self.children) == 0

    def is_leaf_final(self):
        return self.state.check_giga_victoire() != "e"

    def game_result(self, result):
        if result == self.player_to_max:
            return 1
        elif result == "stalemate":
            return 0.5
        else:
            return 0

    def ucb1(self):
        if self.visits == 0:
            return math.inf
        return (self.wins / self.visits) + 0.1 * np.sqrt(np.log(self.parent.visits) / self.visits)

    def selection(self):
        if self.is_leaf() or not (self.is_fully_expanded()):
            return self
        else:
            choices_weights = [child.ucb1() for child in self.children]
            return self.children[np.argmax(choices_weights)]

    def expansion(self):
        (x, y, i, j) = self.untried_moves.pop()
        new_state = self.state.clone()
        new_state.play(x, y, i, j)
        child = Node(state=new_state, parent=self, parent_move=(x, y, i, j), player_to_max=self.player_to_max, k=self.k,
                     c=self.c)
        self.children.append(child)
        return child

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def simulation(self):
        simulated_state = self.state.clone()
        while simulated_state.check_giga_victoire() == "e":
            possible_moves = simulated_state.get_legal_moves_mcts()
            (x, y, i, j) = self.rollout_policy(possible_moves)
            simulated_state.play(x, y, i, j)
        return self.game_result(simulated_state.check_giga_victoire())

    def backpropagation(self, result):
        self.visits += 1  # Incrémenter les visites pour le nœud actuel
        self.wins += result
        if self.parent:
            self.parent.backpropagation(result)


def mcts_play(game, n, player_to_max):
    root = Node(state=game, player_to_max=player_to_max)
    root.expansion()
    for i in range(n):
        leaf = root.selection()
        # print("Selection done")
        if not leaf.is_leaf_final():
            if len(leaf.untried_moves) != 0:
                leaf = leaf.expansion()
                # print("Expansion done")a
        result = leaf.simulation()
        # print("Simulation done")
        leaf.backpropagation(result)
        # print("backpropagation done")

    visits = [child.visits for child in root.children]
    best_child = root.children[np.argmax(visits)]
    return best_child.parent_move


def simuler_partie():
    game = GigaMorpion()
    result = game.check_giga_victoire()
    while result == "e":
        if game.joueur_actuel == "X":
            i, j, x, y = mcts_play(game=game, n=100, player_to_max="X")
            game.play(i, j, x, y)
        elif game.joueur_actuel == "O":
            i, j, x, y = mcts_play(game=game, n=100, player_to_max="O")
            game.play(i, j, x, y)
        result = game.check_giga_victoire()
    print(result)
    return result


def simuler_n_parties(n):
    c = [0, 0, 0]
    for i in range(n):
        print(f"Partie numéro {i}")
        res = simuler_partie()
        if res == 'X':
            c[0] += 1
        elif res == 'O':
            c[1] += 1
        else:
            c[2] += 1
    print(f"X a gagné {c[0]} fois, O a gagné {c[1]} fois et il y a eu {c[2]} égalités pour {n} parties jouées")
