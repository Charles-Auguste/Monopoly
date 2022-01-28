"""
utility_functions.py
Author : TDLOG group A
Date : 24/01/2022
Comments : fully functional (18/01/2022)
"""

# Standard library
import pygame
import importlib.resources

# 3rd party packages
import pygame_textinput

#local source
from board_game.color import *
from board_game.propriete import Property

pygame.init()

def text_format(message, textSize, textColor):
    newFont = pygame.font.SysFont("Consolas", textSize)
    newText = newFont.render(message, True, textColor)
    return newText

def print_text(screen,nb_ligne, text, textSize, textColor):
    txt = text_format(text, textSize, textColor)
    y_init = nb_ligne*height//(nb_lignes+1)
    x_init = (width-height) + 100
    screen.blit(txt, (x_init, y_init))

def print_basic_text(screen,text,x_init,y_init,font_size = 9,color = black):
    text_to_write = text_format(text, font_size, color)
    rect_text = text_to_write.get_rect()
    screen.blit(text_to_write, (x_init - (rect_text[2] / 2), y_init - (rect_text[3] / 2)))

def read_properties(file):
    """Prend en entrée un fichier qui contient les informations des propriétés, renvoie une liste de Properties initialisées à l'aide du fichier"""
    list_properties = []
    with open(file, "r") as f:
        lines = f.readlines()
    split_lines = []
    for i in range(1, len(lines)):
        split_lines.append(lines[i].split(" "))  # On découpe les lignes du fichier (pour séparer les attributs) pour pouvoir définir les différentes propriétés
        for j in range(1, 7):
            split_lines[len(split_lines) - 1][j] = int(split_lines[len(split_lines) - 1][j])  # Conversion en entiers des champs qui doivent être entiers (prix de la propriété, ...)
        split_lines[len(split_lines) - 1][7] = [int(split_lines[len(split_lines) - 1][i]) for i in range(7, 13)]  # Création de la liste des différents loyers
        split_lines[len(split_lines) - 1][8] = tuple(map(int, split_lines[len(split_lines) - 1][13].split(","))) # Création d'un tuple qui correspond à la couleur de la propriété
    for i in range(len(split_lines)):
        list_properties.append(Property(*split_lines[i][:9]))  # Initialisation de chaque propriété avec les informations données dans le fichier
    return list_properties

def mini_bijection(i: int,x_init : int, y_init : int, size : int):
    if (i == 0):
        return [x_init + 65 * size//70, y_init + 65 * size//70]
    if (i == 1):
        return [x_init + 55 * size // 70, y_init +  65 * size // 70]
    if (i == 2):
        return [x_init + 45 * size // 70, y_init +  65 * size // 70]
    if (i == 3):
        return [x_init + 35 * size // 70, y_init +  65 * size // 70]
    if (i == 4):
        return [x_init + 25 * size // 70, y_init +  65 * size // 70]
    if (i == 5):
        return [x_init + 15 * size // 70, y_init +  65 * size // 70]
    if (i == 6):
        return [x_init + 5 * size // 70, y_init +  65 * size // 70]

    if (i == 7):
        return [x_init + 5 * size // 70, y_init +  55 * size // 70]
    if (i == 8):
        return [x_init + 5 * size // 70, y_init +  45 * size // 70]
    if (i == 9):
        return [x_init + 5 * size // 70, y_init +  35 * size // 70]
    if (i == 10):
        return [x_init + 5 * size // 70, y_init +  25 * size // 70]
    if (i == 11):
        return [x_init + 5 * size // 70, y_init +  15 * size // 70]

    if (i == 12):
        return [x_init + 5 * size // 70, y_init +  5 * size // 70]
    if (i == 13):
        return [x_init + 15 * size // 70, y_init +  5 * size // 70]
    if (i == 14):
        return [x_init + 25 * size // 70, y_init +  5 * size // 70]
    if (i == 15):
        return [x_init + 35 * size // 70, y_init +  5 * size // 70]
    if (i == 16):
        return [x_init + 45 * size // 70, y_init +  5 * size // 70]
    if (i == 17):
        return [x_init + 55 * size // 70, y_init +  5 * size // 70]
    if (i == 18):
        return [x_init + 65 * size // 70, y_init +  5 * size // 70]

    if (i == 19):
        return [x_init + 65 * size // 70, y_init +  15 * size // 70]
    if (i == 20):
        return [x_init + 65 * size // 70, y_init +  25 * size // 70]
    if (i == 21):
        return [x_init + 65 * size // 70, y_init +  35 * size // 70]
    if (i == 22):
        return [x_init + 65 * size // 70, y_init +  45 * size // 70]
    if (i == 23):
        return [x_init + 65 * size // 70, y_init +  55 * size // 70]
    else :
        return [0,0]

def grande_bijection(i: int, x_init : int, y_init : int, size : int):
    if (i == 0):
        return [x_init + 21 * size // 22, y_init + 21 * size // 22]
    if (i == 1):
        return [x_init + 19 * size // 22, y_init + 21 * size // 22]
    if (i == 2):
        return [x_init + 17 * size // 22, y_init + 21 * size // 22]
    if (i == 3):
        return [x_init + 15 * size // 22, y_init + 21 * size // 22]
    if (i == 4):
        return [x_init + 13 * size // 22, y_init + 21 * size // 22]
    if (i == 5):
        return [x_init + 11 * size // 22, y_init + 21 * size // 22]
    if (i == 6):
        return [x_init + 9 * size // 22, y_init + 21 * size // 22]
    if (i == 7):
        return [x_init + 7 * size // 22, y_init + 21 * size // 22]
    if (i == 8):
        return [x_init + 5 * size // 22, y_init + 21 * size // 22]
    if (i == 9):
        return [x_init + 3 * size // 22, y_init + 21 * size // 22]
    if (i == 10):
        return [x_init + size // 22, y_init + 21 * size // 22]
    if (i == 11):
        return [x_init + size // 22, y_init + 19 * size // 22]
    if (i == 12):
        return [x_init + size // 22, y_init + 17 * size // 22]
    if (i == 13):
        return [x_init + size // 22, y_init + 15 * size // 22]
    if (i == 14):
        return [x_init + size // 22, y_init + 13 * size // 22]
    if (i == 15):
        return [x_init + size // 22, y_init + 11 * size // 22]
    if (i == 16):
        return [x_init + size // 22, y_init + 9 * size // 22]
    if (i == 17):
        return [x_init + size // 22, y_init + 7 * size // 22]
    if (i == 18):
        return [x_init + size // 22, y_init + 5 * size // 22]
    if (i == 19):
        return [x_init + size // 22, y_init + 3 * size // 22]
    if (i == 20):
        return [x_init + size // 22, y_init + size // 22]
    if (i == 21):
        return [x_init + 3 * size // 22, y_init + size // 22]
    if (i == 22):
        return [x_init + 5 * size // 22, y_init + size // 22]
    if (i == 23):
        return [x_init + 7 * size // 22, y_init + size // 22]
    if (i == 24):
        return [x_init + 9 * size // 22, y_init + size // 22]
    if (i == 25):
        return [x_init + 11 * size // 22, y_init + size // 22]
    if (i == 26):
        return [x_init + 13 * size // 22, y_init + size // 22]
    if (i == 27):
        return [x_init + 15 * size // 22, y_init + size // 22]
    if (i == 28):
        return [x_init + 17 * size // 22, y_init + size // 22]
    if (i == 29):
        return [x_init + 19 * size // 22, y_init + size // 22]
    if (i == 30):
        return [x_init + 21 * size // 22, y_init + size // 22]
    if (i == 31):
        return [x_init + 21 * size // 22, y_init + 3 * size // 22]
    if (i == 32):
        return [x_init + 21 * size // 22, y_init + 5 * size // 22]
    if (i == 33):
        return [x_init + 21 * size // 22, y_init + 7 * size // 22]
    if (i == 34):
        return [x_init + 21 * size // 22, y_init + 9 * size // 22]
    if (i == 35):
        return [x_init + 21 * size // 22, y_init + 11 * size // 22]
    if (i == 36):
        return [x_init + 21 * size // 22, y_init + 13 * size // 22]
    if (i == 37):
        return [x_init + 21 * size // 22, y_init + 15 * size // 22]
    if (i == 38):
        return [x_init + 21 * size // 22, y_init + 17 * size // 22]
    if (i == 39):
        return [x_init + 21 * size // 22, y_init + 19 * size // 22]

    else:
        return [0, 0]


def obt_path(module,template):
    with importlib.resources.path(module,template) as p:
        path = p
    return path