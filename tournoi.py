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
                i, j, x, y = meilleur_coup(game, heuristique, profondeur,False)
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
                i, j, x, y = meilleur_coup(game, heuristique, profondeur,True)
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

class Resultat:
    def ajouter_défaite(self):#[0]
        self.défaites += 1
        self.parties += 1
    def ajouter_victoire(self):#[1]
        self.victoires += 1
        self.parties += 1
    def ajouter_égalité(self):#[2]
        self.égalités += + 1
        self.parties += 1
    def __init__(self):
        self.défaites = 0
        self.victoires = 0
        self.égalités = 0
        self.parties = 0


def jouer_parties_heuristique_vs_heuristique_tournoi(n, heuristique1, heuristique2):
    profondeur = 2
    resultat = Resultat()  # h1, h2, égalité
    for i in range(n // 2):
        game = GigaMorpion()
        while game.check_giga_victoire() == "e":
            if game.joueur_actuel == "X":
                i, j, x, y = meilleur_coup_elagage(game, heuristique1, profondeur, True)
                game.play(i, j, x, y)
            else:
                i, j, x, y = meilleur_coup_elagage(game, heuristique2, profondeur, False)
                game.play(i, j, x, y)
        win = game.check_giga_victoire()
        if win == "X":
            resultat.ajouter_victoire()
        elif win == "O":
            resultat.ajouter_défaite()
        else:
            resultat.ajouter_égalité()
    for i in range(n // 2):
        game = GigaMorpion()
        while game.check_giga_victoire() == "e":
            if game.joueur_actuel == "X":
                i, j, x, y = meilleur_coup_elagage(game, heuristique2, profondeur, True)
                game.play(i, j, x, y)
            else:
                i, j, x, y = meilleur_coup_elagage(game, heuristique1, profondeur, False)
                game.play(i, j, x, y)
        win = game.check_giga_victoire()
        if win == "X":
            resultat.ajouter_défaite()
        elif win == "O":
            resultat.ajouter_victoire()
        else:
            resultat.ajouter_égalité()
    return resultat



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

def qualite_poids_tournoi(p1, p2) -> Resultat:
    n_parties = 4  # DOIT ETRE PAIR POUR FAIRE AUTANT DE PARTIE OU CHACUN COMMENCE
    t_random = 0

    def heuristique_evolutive_tournois(p):
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
        return heuristique_evolutive

    resultat = jouer_parties_heuristique_vs_heuristique_tournoi(n_parties,heuristique_evolutive_tournois(p1),heuristique_evolutive_tournois(p2))
    return resultat

def mutation(p):
    poids, giga_poids = p
    proba_mutation = 0.1
    for x in range(3):
        for y in range(3):
            if random.random() < 0.15:
                giga_poids[x][y] += random.uniform(-0.1, 0.1)
            for i in range(3):
                for j in range(3):
                    poids[x][y][i][j] += random.uniform(-0.1,0.1)
    return poids, giga_poids


def evolution_contre_random(iteration=10):
    temps_mutation = 0
    temps_qualite = 0

    taux_de_victoire = []
    evolution_meilleur_score = []
    generation = []
    p = initialisation_poids()
    meilleur_p = p
    meilleur_score = 0
    for i in range(iteration):
        pt = time.process_time()
        generation.append(i+1)
        t=time.time()
        nouveau_p = mutation(p)
        temps_mutation += time.time()-t
        t=time.time()
        score = qualite_poids_random(p)
        temps_qualite += time.time()-t
        if score > meilleur_score:
            meilleur_p = nouveau_p
            meilleur_score = score
        taux_de_victoire.append(score)
        evolution_meilleur_score.append(meilleur_score)
        elapsed_time = time.process_time() - pt
        print(f"Génération: {i}, Meilleur Score: {meilleur_score}, Score: {score}, in {elapsed_time}")
        print("Temps mutation",temps_mutation)
    print("Temps qualite",temps_qualite)
    return taux_de_victoire, generation, meilleur_p, evolution_meilleur_score


taille_population = 2

def valeur_enfant(v1, v2):
    curseur = random.random()
    return v1 * curseur + v2 * (1-curseur)

def enfant(p1, p2):
    poids = [[[[valeur_enfant(p1[0][i][j][k][l], p2[0][i][j][k][l]) for i in range(3)] for j in range(3)] for k in range(3)] for l in range(3)]
    giga_poids = [[valeur_enfant(p1[1][i][j], p2[1][i][j]) for i in range(3)] for j in range(3)]
    return poids, giga_poids

def reproduction_population(population):
    enfants = []
    for p1 in population:
        for p2 in population:
            enfants.append(enfant(p1, p2))
    population.extend(enfants)
    return population


def mutation_population(population): # mutation de 1 individu
    to_mute = population[random.randint(0, len(population)-1)]
    population.append(mutation(to_mute))
    return population

class ResultatJoueurs:
    def __init__(self, resultat:Resultat, j1:int, j2:int):
        self.resultat = resultat
        self.j1 = j1
        self.j2 = j2

def evolution_tournoi(iteration=100):
    temps_mutation = 0
    temps_qualite = 0

    evolution_meilleur_score = []
    generation = []
    population = [initialisation_poids() for _ in range(taille_population)]
    for i in range(iteration):
        pt = time.process_time()
        generation.append(i+1)
        t=time.time()
        population = mutation_population(population)
        population = reproduction_population(population)
        temps_mutation += time.time()-t
        t=time.time()
        scores:list[tuple[float, int, int]] = []
        resultat_joueurs_list:list[ResultatJoueurs] = []
        for j1 in range(0, len(population)):
            print(f"j1={j1}")
            p1 = population[j1]
            for j2 in range(j1+1, len(population)):
                print(f"j2={j2}")
                p2 = population[j2]
                resultat = qualite_poids_tournoi(p1, p2)
                resultat_joueurs_list.append(ResultatJoueurs(resultat, j1, j2))
        # n_victoires = resultats[1]
        # n_defaites = resultats[0]
        # n_égalités = resultats[2]
        # return (n_victoires + 0.5 * n_égalités) / n_parties
        scores:list[int] = [0] * len(population)
        for resultat_joueurs in resultat_joueurs_list:
            resultat = resultat_joueurs.resultat
            scores[resultat_joueurs.j1] += (resultat.victoires + 0.5 * resultat.égalités) / resultat.parties / len(resultat_joueurs_list)
            scores[resultat_joueurs.j2] += (resultat.défaites + 0.5 * resultat.égalités) / resultat.parties / len(resultat_joueurs_list)
        scores_avec_joueurs = [(scores[idx], idx) for idx in range(0, len(scores))]
        temps_qualite += time.time()-t
        sorted_scores_avec_joueurs = sorted(scores_avec_joueurs, key=lambda s12: s12[0], reverse=True)
        meilleur_score = sorted_scores_avec_joueurs[0][0]
        conserves_scores_avec_joueurs = sorted_scores_avec_joueurs[:taille_population]
        new_population = [population[scores_avec_joueurs[1]] for scores_avec_joueurs in conserves_scores_avec_joueurs]
        population = new_population
        evolution_meilleur_score.append(meilleur_score)
        elapsed_time = time.process_time() - pt
        print(f"Génération: {i}, Meilleur Score: {meilleur_score}, in {elapsed_time}")
        print("Temps mutation",temps_mutation)
    print("Temps qualite",temps_qualite)
    return generation, evolution_meilleur_score


g, ms = evolution_tournoi()
plt.plot(g, ms)
plt.show()
