import random
import pygame
from morpion import *
import sys
import time
import os
import io
from tqdm import tqdm
import matplotlib.pyplot as plt
from math import inf


def random_vs_heuristique(n, heuristique, profondeur):
    print("Nous sommes ici")
    start_time = time.time()
    results = [0, 0, 0]  # random, heuristique, égalité
    results1 = [0, 0, 0]
    results2 = [0, 0, 0]
    for i in tqdm(range(n // 2)):
        game = GigaMorpion()
        while game.check_giga_victoire() == "e":
            if game.joueur_actuel == "X":
                game.random_play()
            else:
                i, j, x, y = meilleur_coup(game, heuristique, profondeur)
                game.play(i, j, x, y)
        win = game.check_giga_victoire()
        if win == "X":
            results[1] += 1
        elif win == "O":
            results[0] += 1
        else:
            results[2] += 1
    results1 = results.copy()
    for i in tqdm(range(n // 2)):
        game = GigaMorpion()
        while game.check_giga_victoire() == "e":
            if game.joueur_actuel == "X":
                i, j, x, y = meilleur_coup(game, heuristique, profondeur)
                game.play(i, j, x, y)
            else:
                game.random_play()
        win = game.check_giga_victoire()
        if win == "X":
            results[0] += 1
        elif win == "O":
            results[1] += 1
        else:
            results[2] += 1
    results2 = [results[k] - results1[k] for k in range(3)]
    return results, results1, results2


def initialisation_poids():
    # le poids[x][y][i][j] correspond au poids de la petite case [x][y][i][j]
    poids = [[[[random.uniform(-1, 1) for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
    giga_poids = [[random.uniform(-1, 1) for i in range(3)] for i in range(3)]
    return (poids, giga_poids)


# selection1 et selection2 sont des fonctions qui renvoie selon une configuration, un joueur, un coup à jouer

def jouer_parties_random_vs_heuristique(n, heuristique):
    profondeur = 2
    results = [0, 0, 0]  # random, heuristique, égalité
    results1 = [0, 0, 0]
    results2 = [0, 0, 0]
    for i in range(n // 2):
        game = GigaMorpion()
        while game.check_giga_victoire() == "e":
            if game.joueur_actuel == "X":
                game.random_play()
            else:
                i, j, x, y = meilleur_coup_elagage(game, heuristique, profondeur, False)
                game.play(i, j, x, y)
        win = game.check_giga_victoire()
        if win == "X":
            results[1] += 1
        elif win == "O":
            results[0] += 1
        else:
            results[2] += 1
    results1 = results.copy()
    for i in range(n // 2):
        game = GigaMorpion()
        while game.check_giga_victoire() == "e":
            if game.joueur_actuel == "X":
                i, j, x, y = meilleur_coup_elagage(game, heuristique, profondeur, True)
                game.play(i, j, x, y)
            else:
                game.random_play()
        win = game.check_giga_victoire()
        if win == "X":
            results[0] += 1
        elif win == "O":
            results[1] += 1
        else:
            results[2] += 1
    results2 = [results[k] - results1[k] for k in range(3)]
    return results



def jouer_partie_heuristique1_vs_heuristique2(n, heuristique1, heuristique2):
    profondeur = 3
    results = [0, 0, 0]  # heuristique1, heuristique2, égalité
    results1 = [0, 0, 0]
    results2 = [0, 0, 0]
    for i in range(n // 2):
        game = GigaMorpion()
        while game.check_giga_victoire() == "e":
            if game.joueur_actuel == "X":
                i, j, x, y = meilleur_coup_elagage(game, heuristique2, profondeur, False)
                game.play(i, j, x, y)
            else:
                i, j, x, y = meilleur_coup_elagage(game, heuristique1, profondeur, False)
                game.play(i, j, x, y)
        win = game.check_giga_victoire()
        if win == "X":
            results[1] += 1
        elif win == "O":
            results[0] += 1
        else:
            results[2] += 1
    results1 = results.copy()
    for i in range(n // 2):
        game = GigaMorpion()
        while game.check_giga_victoire() == "e":
            if game.joueur_actuel == "X":
                i, j, x, y = meilleur_coup(game, heuristique1, profondeur, False)
                game.play(i, j, x, y)
            else:
                i, j, x, y = meilleur_coup(game, heuristique2, profondeur, False)
                game.play(i, j, x, y)
        win = game.check_giga_victoire()
        if win == "X":
            results[0] += 1
        elif win == "O":
            results[1] += 1
        else:
            results[2] += 1
    results2 = [results[k] - results1[k] for k in range(3)]
    return results


t_heuristique = 0


def qualite_poids_random(p):
    n_parties = 10  # DOIT ETRE PAIR POUR FAIRE AUTANT DE PARTIE OU CHACUN COMMENCE
    t_random = 0

    def heuristique_evolutive(game):
        poids, giga_poids = p
        score = 0
        if game.check_giga_victoire() == "X":
            return inf
        if game.check_giga_victoire() == "O":
            return -inf
        for x in range(3):
            for y in range(3):
                if game.plateau[x][y].status == "X":
                    score += giga_poids[x][y]
                elif game.plateau[x][y].status == "O":
                    score -= giga_poids[x][y]
                for i in range(3):
                    for j in range(3):
                        if game.plateau[x][y].plateau[i][j].valeur == "X":
                            score += poids[x][y][i][j]
                        elif game.plateau[x][y].plateau[i][j].valeur == "O":
                            score -= poids[x][y][i][j]

        return score

    resultats = jouer_parties_random_vs_heuristique(n_parties, heuristique_evolutive)
    n_victoires = resultats[1]
    n_defaites = resultats[0]
    n_égalités = resultats[2]
    return (n_victoires + 0.5 * n_égalités) / n_parties


def mutation(p):
    poids, giga_poids = p
    proba_mutation = 0.1
    for x in range(3):
        for y in range(3):
            if random.random() < 0.15:
                giga_poids[x][y] += 2 * random.uniform(-0.1, 0.1)
            for i in range(3):
                for j in range(3):
                    if random.random() < 0.15:
                        poids[x][y][i][j] += random.uniform(-0.1, 0.1)
    return poids, giga_poids


def evolution_contre_random(iteration=1000):
    temps_mutation = 0
    temps_qualite = 0

    taux_de_victoire = []
    evolution_meilleur_score = []
    generation = []
    p = initialisation_poids()
    meilleur_p = p
    meilleur_score = 0
    for i in range(iteration):
        generation.append(i + 1)
        t = time.time()
        nouveau_p = mutation(p)
        temps_mutation += time.time() - t
        t = time.time()
        score = qualite_poids_random(p)
        temps_qualite += time.time() - t
        if score > meilleur_score:
            meilleur_p = nouveau_p
            meilleur_score = score
        taux_de_victoire.append(score)
        evolution_meilleur_score.append(meilleur_score)
        print(f"Génération: {i}, Meilleur Score: {meilleur_score}, Score: {score}")
    print("Temps mutation", temps_mutation)
    print("Temps qualite", temps_qualite)
    return taux_de_victoire, generation, meilleur_p, evolution_meilleur_score


tv, g, mp, ms = evolution_contre_random()
plt.plot(g, tv, 'r')
plt.plot(g, ms)
plt.show()
print(mp)
print(g)
print(tv)
print(ms)
