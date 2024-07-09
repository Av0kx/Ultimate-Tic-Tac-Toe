import copy
import random as ran
import math


def autre_player(player):
    if player == "X":
        return "O"
    return "X"


class Case:
    def __init__(self):
        self.valeur = "e"

    def est_vide(self):
        return self.valeur == "e"

    def placer_X(self):
        if self.est_vide():
            self.valeur = "X"
            return True
        return False

    def placer_O(self):
        if self.est_vide():
            self.valeur = "O"
            return True
        return False


class Morpion:
    def __init__(self):
        self.plateau = [[Case() for _ in range(3)] for _ in range(3)]
        self.status = "e"

    def check_victoire(self):  # Returns e on ongoing, X or O on win, stalemate on stalemate
        for i in range(3):
            if self.plateau[i][0].valeur == self.plateau[i][1].valeur == self.plateau[i][2].valeur != 'e':
                self.status = self.plateau[i][0].valeur
                return self.status
        for i in range(3):
            if self.plateau[0][i].valeur == self.plateau[1][i].valeur == self.plateau[2][i].valeur != 'e':
                self.status = self.plateau[0][i].valeur
                return self.status
        if self.plateau[0][0].valeur == self.plateau[1][1].valeur == self.plateau[2][2].valeur != 'e':
            self.status = self.plateau[0][0].valeur
            return self.status
        if self.plateau[0][2].valeur == self.plateau[1][1].valeur == self.plateau[2][0].valeur != 'e':
            self.status = self.plateau[0][2].valeur
            return self.status
        if all(case.valeur != "e" for row in self.plateau for case in row):  # all(): and sur tout
            self.status = "stalemate"
            return self.status
        self.status = "e"
        return self.status

    def legal_moves(self):
        L = []
        for i in range(3):
            for j in range(3):
                if self.plateau[i][j].valeur == "e":
                    L.append([i, j])
        return L


class GigaMorpion:
    def __init__(self):
        self.plateau = [[Morpion() for _ in range(3)] for _ in range(3)]
        self.joueur_actuel = "X"
        self.legal_moves = [[i, j] for i in range(3) for j in range(3)]

    def change_joueur(self):
        if self.joueur_actuel == "X":
            self.joueur_actuel = "O"
        else:
            self.joueur_actuel = "X"

    def play(self, i, j, x, y):
        if self.plateau[i][j].status == "e" and [i, j] in self.legal_moves:
            if [x, y] in self.plateau[i][j].legal_moves():
                if self.joueur_actuel == "X":
                    self.plateau[i][j].plateau[x][y].placer_X()
                else:
                    self.plateau[i][j].plateau[x][y].placer_O()

                self.plateau[i][j].check_victoire()
                if self.plateau[x][y].status in ["X", "O", "stalemate"]:
                    self.legal_moves = [[k, l] for k in range(3) for l in range(3)
                                        if self.plateau[k][l].status == "e"
                                        and self.plateau[k][l].legal_moves()]
                else:
                    self.legal_moves = [[x, y]] if self.plateau[x][y].legal_moves() else []

                self.change_joueur()
                return True

        return False

    def clone(self):
        return copy.deepcopy(self)

    def unplay(self, i, j, x, y):
        self.plateau[i][j].plateau[x][y].valeur = "e"
        self.plateau[i][j].status = "e"

    def random_play(self):
        random_plateau = ran.choice(self.legal_moves)
        random_morpion = ran.choice(self.plateau[random_plateau[0]][random_plateau[1]].legal_moves())
        return self.play(random_plateau[0], random_plateau[1], random_morpion[0],
                         random_morpion[1])  # de la forme [i,j,x,y] où i,j est le morpion et x,y la case

    def check_giga_victoire(self):
        for i in range(3):
            if self.plateau[i][0].status == self.plateau[i][1].status == self.plateau[i][2].status != "e":
                return self.plateau[i][0].status

            if self.plateau[0][i].status == self.plateau[1][i].status == self.plateau[2][i].status != "e":
                return self.plateau[0][i].status

        if self.plateau[0][0].status == self.plateau[1][1].status == self.plateau[2][2].status != "e":
            return self.plateau[0][0].status

        if self.plateau[0][2].status == self.plateau[1][1].status == self.plateau[2][0].status != "e":
            return self.plateau[0][2].status

        if all(morpion.status != "e" for row in self.plateau for morpion in row):
            return "stalemate"

        return "e"

    def get_legal_moves_mcts(self):
        morpions = self.legal_moves
        actions = []
        for coords in morpions:
            x, y = coords[0], coords[1]
            moves = self.plateau[x][y].legal_moves()
            for move in moves:
                i, j = move[0], move[1]
                actions.append((x, y, i, j))
        return actions


def heuristique_simpliste1(game):
    score_x = 0
    score_o = 0
    for i in range(3):
        for j in range(3):
            if game.plateau[i][j].status == "X":
                score_x += 1
            elif game.plateau[i][j].status == "O":
                score_o += 1
    return score_x - score_o


def heuristique_efficace1(game):
    x_score = 0
    o_score = 0
    for i in range(3):
        for j in range(3):
            if game.plateau[i][j].status == "X":
                x_score += 1
            elif game.plateau[i][j].status == "O":
                o_score += 1
    if game.check_giga_victoire() == "X":
        return 1000
    elif game.check_giga_victoire() == "O":
        return -1000
    return x_score - o_score


def heuristique_lukas(game):
    coeff_grosse_case = 80
    x_score = 0
    o_score = 0
    for i in range(3):
        for j in range(3):
            if (i, j) == (1, 1):
                if game.plateau[i][j].status == "X":
                    x_score += 4 * coeff_grosse_case
                elif game.plateau[i][j].status == "O":
                    o_score += 4 * coeff_grosse_case
                coeff = 4

            if (i, j) == (0, 0) or (i, j) == (0, 2) or (i, j) == (2, 0) or (i, j) == (2, 2):
                if game.plateau[i][j].status == "X":
                    x_score += 3 * coeff_grosse_case
                elif game.plateau[i][j].status == "O":
                    o_score += 3 * coeff_grosse_case
                coeff = 3
            if (i, j) == (0, 1) or (i, j) == (1, 0) or (i, j) == (1, 2) or (i, j) == (2, 1):
                if game.plateau[i][j].status == "X":
                    x_score += 2 * coeff_grosse_case
                elif game.plateau[i][j].status == "O":
                    o_score += 2 * coeff_grosse_case
                coeff = 2
            if game.plateau[i][j].status == "e":
                for x in range(3):
                    for y in range(3):
                        if (x, y) == (1, 1):
                            if game.plateau[i][j].plateau[x][y].valeur == "X":
                                x_score += 4 * coeff
                            elif game.plateau[i][j].plateau[x][y].valeur == "O":
                                o_score += 4 * coeff
                        if (x, y) == (0, 0) or (x, y) == (0, 2) or (x, y) == (2, 0) or (x, y) == (2, 2):
                            if game.plateau[i][j].plateau[x][y].valeur == "X":
                                x_score += 3 * coeff
                            elif game.plateau[i][j].plateau[x][y].valeur == "O":
                                o_score += 3 * coeff
                        if (x, y) == (0, 1) or (x, y) == (1, 0) or (x, y) == (1, 2) or (x, y) == (2, 1):
                            if game.plateau[i][j].plateau[x][y].valeur == "X":
                                x_score += 2 * coeff
                            elif game.plateau[i][j].plateau[x][y].valeur == "O":
                                o_score += 2 * coeff
    if game.check_giga_victoire() == "X":
        return math.inf
    elif game.check_giga_victoire() == "O":
        return -math.inf
    return x_score - o_score


def heuristique_gabriel(game):
    x_score = 0
    o_score = 0
    alpha = 12
    beta = 5
    for i in range(3):
        for j in range(3):
            if game.plateau[i][j].status != "e":
                if (i, j) == (0, 0) or (i, j) == (0, 2) or (i, j) == (2, 0) or (i, j) == (2, 2):  # Coins
                    if game.plateau[i][j].status == "X":
                        x_score += 3 * alpha
                    elif game.plateau[i][j].status == "O":
                        o_score += 3 * alpha
                elif (i, j) == (1, 1):  # Centre
                    if game.plateau[i][j].status == "X":
                        x_score += 4 * alpha
                    elif game.plateau[i][j].status == "O":
                        o_score += 4 * alpha
                else:  # Bords
                    if game.plateau[i][j].status == "X":
                        x_score += 2 * alpha
                    elif game.plateau[i][j].status == "O":
                        o_score += 2 * alpha
            else:  # Si la grande case n'est pas finie
                plat = game.plateau[i][j].plateau
                for x in range(2):
                    if plat[x][0].valeur == "X" and plat[x][1].valeur == "X" and plat[x][2].valeur == "e":
                        x_score += beta
                    if plat[x][0].valeur == "X" and plat[x][2].valeur == "X" and plat[x][1].valeur == "e":
                        x_score += beta
                    if plat[x][1].valeur == "X" and plat[x][2].valeur == "X" and plat[x][0].valeur == "e":
                        x_score += beta
                    if plat[0][x].valeur == "X" and plat[1][x].valeur == "X" and plat[2][x].valeur == "e":
                        x_score += beta
                    if plat[0][x].valeur == "X" and plat[2][x].valeur == "X" and plat[1][x].valeur == "e":
                        x_score += beta
                    if plat[1][x].valeur == "X" and plat[2][x].valeur == "X" and plat[0][x].valeur == "e":
                        x_score += beta
                if plat[0][0].valeur == "X" and plat[1][1].valeur == "X" and plat[2][2].valeur == "e":
                    x_score += beta
                if plat[0][0].valeur == "X" and plat[2][2].valeur == "X" and plat[1][1].valeur == "e":
                    x_score += beta
                if plat[1][1].valeur == "X" and plat[2][2].valeur == "X" and plat[0][0].valeur == "e":
                    x_score += beta
                if plat[0][2].valeur == "X" and plat[1][1].valeur == "X" and plat[2][0].valeur == "e":
                    x_score += beta
                if plat[0][2].valeur == "X" and plat[2][0].valeur == "X" and plat[1][1].valeur == "e":
                    x_score += beta
                if plat[1][1].valeur == "X" and plat[2][0].valeur == "X" and plat[0][2].valeur == "e":
                    x_score += beta
                for x in range(2):
                    if plat[x][0].valeur == "O" and plat[x][1].valeur == "O" and plat[x][2].valeur == "e":
                        o_score += beta
                    if plat[x][0].valeur == "O" and plat[x][2].valeur == "O" and plat[x][1].valeur == "e":
                        o_score += beta
                    if plat[x][1].valeur == "O" and plat[x][2].valeur == "O" and plat[x][0].valeur == "e":
                        o_score += beta
                    if plat[0][x].valeur == "O" and plat[1][x].valeur == "O" and plat[2][x].valeur == "e":
                        o_score += beta
                    if plat[0][x].valeur == "O" and plat[2][x].valeur == "O" and plat[1][x].valeur == "e":
                        o_score += beta
                    if plat[1][x].valeur == "O" and plat[2][x].valeur == "O" and plat[0][x].valeur == "e":
                        o_score += beta
                if plat[0][0].valeur == "O" and plat[1][1].valeur == "O" and plat[2][2].valeur == "e":
                    o_score += beta
                if plat[0][0].valeur == "O" and plat[2][2].valeur == "O" and plat[1][1].valeur == "e":
                    o_score += beta
                if plat[1][1].valeur == "O" and plat[2][2].valeur == "O" and plat[0][0].valeur == "e":
                    o_score += beta
                if plat[0][2].valeur == "O" and plat[1][1].valeur == "O" and plat[2][0].valeur == "e":
                    o_score += beta
                if plat[0][2].valeur == "O" and plat[2][0].valeur == "O" and plat[1][1].valeur == "e":
                    o_score += beta
                if plat[1][1].valeur == "O" and plat[2][0].valeur == "O" and plat[0][2].valeur == "e":
                    o_score += beta

    if game.check_giga_victoire() == "X":
        return 1000
    elif game.check_giga_victoire() == "O":
        return -1000
    return x_score - o_score


def min_random(L):  # renvoie l'indice d'un des plus petit élément qu'on aura choisi au hasard
    min = [0]
    for i in range(1, len(L)):
        if L[i] < L[min[0]]:
            min = [i]
        elif L[i] == L[min[0]]:
            min.append(i)
    return ran.choice(min)


def max_random(L):  # renvoie l'indice d'un des plus grands éléments qu'on aura choisi au hasard
    max = [0]
    for i in range(1, len(L)):
        if L[i] > L[max[0]]:
            max = [i]
        elif L[i] == L[max[0]]:
            max.append(i)
    return ran.choice(max)


# Def heuristique(plateau)-> un nombre de point positif si X à l'avantage et négatif si O à l'avantage
# le but de X est donc de maximiser son coup en sachant que O va minimiser l'euristique
# le but de O est de minimiser son heuristique en sachant que X va maximiser le sien
nombre_chemin = 0
nombre_appel = 0


def minmax(game, heuristique, profondeur, joueur_is_X):  # joueur_is_X est un booléen
    global nombre_chemin, nombre_appel
    nombre_appel += 1
    if profondeur == 0 or game.check_giga_victoire() != "e":
        nombre_chemin += 1
        return heuristique(game)
    if joueur_is_X:
        liste_morpions = game.legal_moves
        L = []

        for (i, j) in liste_morpions:
            liste_coups = game.plateau[i][j].legal_moves()
            for (x, y) in liste_coups:
                clonegame = game.clone()
                clonegame.play(i, j, x, y)
                L.append(minmax(clonegame, heuristique, profondeur - 1, False))
        return L[max_random(L)]

    else:
        liste_morpions = game.legal_moves
        L = []
        for (i, j) in liste_morpions:
            liste_coups = game.plateau[i][j].legal_moves()
            for (x, y) in liste_coups:
                clonegame = game.clone()
                clonegame.play(i, j, x, y)
                L.append(minmax(clonegame, heuristique, profondeur - 1, True))
        return L[min_random(L)]


def meilleur_coup(game, heuristique, profondeur, joueur_is_X):
    global nombre_chemin, nombre_appel
    liste_morpions = game.legal_moves
    L = []
    for (i, j) in liste_morpions:
        liste_coups = game.plateau[i][j].legal_moves()
        for (x, y) in liste_coups:
            clonegame = game.clone()
            clonegame.play(i, j, x, y)
            L.append((minmax(clonegame, heuristique, profondeur - 1, not joueur_is_X), (i, j, x, y)))
    print("Il y a eu", nombre_chemin, "chemins et", nombre_appel, "appels à la profondeur", profondeur)
    if "X" == game.joueur_actuel:
        return L[max_random([elt[0] for elt in L])][1]
    else:
        return L[min_random([elt[0] for elt in L])][1]


def alpha_beta(game, heuristique, profondeur, joueur_is_X):
    global nombre_appel

    def elagage(game, heuristique, profondeur, joueur_is_X, alpha, beta):
        # code :
        global nombre_appel
        nombre_appel += 1
        if profondeur == 0 or game.check_giga_victoire() != "e":
            return heuristique(game)
        if not joueur_is_X:
            v = math.inf
            liste_morpions = game.legal_moves
            for (i, j) in liste_morpions:
                liste_coups = game.plateau[i][j].legal_moves()
                for (x, y) in liste_coups:
                    clonegame = game.clone()
                    clonegame.play(i, j, x, y)
                    v = min(v, elagage(clonegame, heuristique, profondeur - 1, True, alpha, beta))
                    if alpha >= v:
                        return v
                    beta = min(beta, v)
            return v

        else:
            liste_morpions = game.legal_moves
            v = -math.inf
            for (i, j) in liste_morpions:
                liste_coups = game.plateau[i][j].legal_moves()
                for (x, y) in liste_coups:
                    clonegame = game.clone()
                    clonegame.play(i, j, x, y)
                    v = max(v, elagage(clonegame, heuristique, profondeur - 1, False, alpha, beta))
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v

    return elagage(game, heuristique, profondeur, joueur_is_X, -math.inf, math.inf)


def meilleur_coup_elagage(game, heuristique, profondeur, joueur_is_X):
    global nombre_chemin, nombre_appel
    liste_morpions = game.legal_moves
    L = []
    for (i, j) in liste_morpions:
        liste_coups = game.plateau[i][j].legal_moves()
        for (x, y) in liste_coups:
            clonegame = game.clone()
            clonegame.play(i, j, x, y)
            L.append((alpha_beta(clonegame, heuristique, profondeur - 1, not joueur_is_X), (i, j, x, y)))
    print("Il y a eu", nombre_appel, "appels à la profondeur", profondeur)
    if "X" == game.joueur_actuel:
        return L[max_random([elt[0] for elt in L])][1]
    else:
        return L[min_random([elt[0] for elt in L])][1]
