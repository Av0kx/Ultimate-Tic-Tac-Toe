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
from mcts2point0 import *

def ajuster_clarte(image, facteur_clarte):
    largeur, hauteur = image.get_size()
    image_ajustee = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)

    for x in range(largeur):
        for y in range(hauteur):
            pixel = image.get_at((x, y))
            r = min(int(pixel.r * facteur_clarte), 255)
            g = min(int(pixel.g * facteur_clarte), 255)
            b = min(int(pixel.b * facteur_clarte), 255)
            a = pixel.a
            image_ajustee.set_at((x, y), (r, g, b, a))

    return image_ajustee


def afficher_heuristique(screen, screen_size, game, heuristique):
    heuristique_X, heuristique_O = heuristique(game)
    total = heuristique_X + heuristique_O
    if total != 0:
        heuristique_X = heuristique_X / total
        heuristique_O = heuristique_O / total
    else:
        heuristique_X = 0.5
        heuristique_O = 0.5
    rect_rouge_hauteur = (heuristique_O * (screen_size - 20))
    pygame.draw.rect(screen, (255, 0, 0),
                     pygame.Rect(10, screen_size - 10 - rect_rouge_hauteur, 10, rect_rouge_hauteur))
    rect_bleu_hauteur = (heuristique_X * (screen_size - 20))
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(10, 10, 10, rect_bleu_hauteur))


# bleu clair presque blanc:
bleu_clair = (202, 202, 251, 255)
rouge_clair = (251, 202, 202, 255)

def main(screen_size):
    nom_px = "petite_croix_bleue.png"
    nom_gx = "grande_croix_bleue.png"
    nom_po = "petite_cercle_rouge.png"
    nom_go = "grande_cercle_rouge.png"
    chemin_pc = os.path.join("images", nom_px)
    chemin_gc = os.path.join("images", nom_gx)
    chemin_po = os.path.join("images", nom_po)
    chemin_go = os.path.join("images", nom_go)
    px = pygame.image.load(chemin_pc)
    gx = pygame.image.load(chemin_gc)
    po = pygame.image.load(chemin_po)
    go = pygame.image.load(chemin_go)
    buffer = io.BytesIO()
    px = ajuster_clarte(px, 3)
    go = ajuster_clarte(go, 0.8)
    player_turn = "X"
    pygame.init()
    screen = pygame.display.set_mode((screen_size, screen_size))
    clock = pygame.time.Clock()

    game = GigaMorpion()

    cell_size = screen_size // 9
    giga_cell_size = screen_size // 3
    lighten_color = (255, 255, 255)
    done = False
    screen.fill(lighten_color)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                x = click_pos[0] // cell_size
                y = click_pos[1] // cell_size
                subgrid_x, subgrid_pos_x = divmod(x, 3)
                subgrid_y, subgrid_pos_y = divmod(y, 3)

                if player_turn == "O":
                    if game.play(subgrid_x, subgrid_y, subgrid_pos_x, subgrid_pos_y):
                        player_turn = "X"
                        afficher_morpion(game)

                if game.check_giga_victoire() != "e":
                    print(f"{game.check_giga_victoire()} WIN")
                    done = True
                    break
                if player_turn == "X":
                    i, j, x, y = meilleur_coup_elagage(game,heuristique_gabriel, 5 a, True)
                    if game.play(i, j, x, y):
                        player_turn = "O"


                if game.check_giga_victoire() != "e":
                    print(f"{game.check_giga_victoire()} WIN")
                    done = True
                    break

                for i in range(9):
                    for j in range(9):
                        subgrid_x, subgrid_pos_x = divmod(i, 3)
                        subgrid_y, subgrid_pos_y = divmod(j, 3)

                        cell_status = game.plateau[subgrid_x][subgrid_y].plateau[subgrid_pos_x][subgrid_pos_y].valeur
                        x = i * cell_size
                        y = j * cell_size

                        cell_color = lighten_color
                        if game.joueur_actuel == "X":
                            if [subgrid_x, subgrid_y] in game.legal_moves and [subgrid_pos_x, subgrid_pos_y] in \
                                    game.plateau[subgrid_x][subgrid_y].legal_moves():
                                cell_color = bleu_clair
                        else:
                            if [subgrid_x, subgrid_y] in game.legal_moves and [subgrid_pos_x, subgrid_pos_y] in \
                                    game.plateau[subgrid_x][subgrid_y].legal_moves():
                                cell_color = rouge_clair

                        pygame.draw.rect(screen, cell_color, pygame.Rect(x, y, cell_size, cell_size))
                        xx, yx = x + 3, y + 3
                        xo, yo = x + 3, y + 3
                        if cell_status == "X":
                            # afficher une image des dossiers
                            screen.blit(px, (xx, yx))

                        if cell_status == "O":
                            screen.blit(po, (xo, yo))

            for i in range(0, screen_size, cell_size):
                line_width = 3 if i % (cell_size * 3) == 0 else 1
                pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, screen_size), line_width)
                pygame.draw.line(screen, (0, 0, 0), (0, i), (screen_size, i), line_width)
            for i in range(9):
                # on parcours les morpions et on vérifie si ils sont gagnés
                if game.plateau[i // 3][i % 3].check_victoire() != "e":
                    xx, yx = i // 3 * giga_cell_size + 8, i % 3 * giga_cell_size + 3
                    xo, yo = i // 3 * giga_cell_size + 6, i % 3 * giga_cell_size + 6
                    # on affiche une grande croix ou un grand cercle sur le morpion gagné
                    if game.plateau[i // 3][i % 3].check_victoire() == "X":
                        screen.blit(gx, (xx, yx))
                    if game.plateau[i // 3][i % 3].check_victoire() == "O":
                        screen.blit(go, (xo, yo))

        pygame.display.flip()
        clock.tick(60)


random_vs_random = [41149, 36787, 22064]

if __name__ == "__main__":
    main(720)  # Multiple de 9 pour que ce soit plus joli
    pygame.image.save(pygame.display.get_surface(), "capture_ecran.png")
    pygame.quit()
    pass
