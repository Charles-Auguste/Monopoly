from player import *
from propriete import *
import random
import pygame
import text_input as input
from text_input import text_format
from time import sleep
from pygame.locals import *
from PIL import Image

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
bleu_ciel = (186, 228, 250)
bleu_fonce = (2, 104, 179)
orange = (245, 146, 3)
marron = (148, 72, 40)
vert = (31, 165, 76)
violet = (217, 46, 134)
jaune = (253, 237, 3)
pink = (255,192,203)

def print_basic_text(screen,text,x_init,y_init,font_size = 10,color = black):
    text_to_write = text_format(text, font_size, color)
    rect_text = text_to_write.get_rect()
    screen.blit(text_to_write, (x_init - (rect_text[2] / 2), y_init))

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

def mini_bijection(i: int,marge : int, size : int):
    if (i == 0):
        return [marge + 21 * size//22, marge + 21 * size//22]
    if (i == 1):
        return [marge + 19 * size//22, marge + 21 * size//22]
    if (i == 2):
        return [marge + 17 * size//22, marge + 21 * size//22]
    if (i == 3):
        return [marge + 15 * size//22, marge + 21 * size//22]
    if (i == 4):
        return [marge + 13 * size//22, marge + 21 * size//22]
    if (i == 5):
        return [marge + 11 * size//22, marge + 21 * size//22]
    if (i == 6):
        return [marge + 9 * size//22, marge + 21 * size//22]
    if (i == 7):
        return [marge + 7 * size//22, marge + 21 * size//22]
    if (i == 8):
        return [marge + 5 * size//22, marge + 21 * size//22]
    if (i == 9):
        return [marge + 3 * size//22, marge + 21 * size//22]
    if (i == 10):
        return [marge + size//22, marge + 21 * size//22]
    if (i == 11):
        return [marge + size//22, marge + 19 * size//22]
    if (i == 12):
        return [marge + size//22, marge + 17 * size//22]
    if (i == 13):
        return [marge + size//22, marge + 15 * size//22]
    if (i == 14):
        return [marge + size//22, marge + 13 * size//22]
    if (i == 15):
        return [marge + size//22, marge + 11 * size//22]
    if (i == 16):
        return [marge + size//22, marge + 9 * size//22]
    if (i == 17):
        return [marge + size//22, marge + 7 * size//22]
    if (i == 18):
        return [marge + size//22, marge + 5 * size//22]
    if (i == 19):
        return [marge + size//22, marge + 3 * size//22]
    if (i == 20):
        return [marge + size//22, marge +  size//22]
    if (i == 21):
        return [marge + 3 * size//22, marge + size//22]
    if (i == 22):
        return [marge + 5 * size//22, marge + size//22]
    if (i == 23):
        return [marge + 7 * size//22, marge + size//22]
    if (i == 24):
        return [marge + 9 * size // 22, marge + size // 22]
    if (i == 25):
        return [marge + 11 * size // 22, marge + size // 22]
    if (i == 26):
        return [marge + 13* size // 22, marge + size // 22]
    if (i == 27):
        return [marge + 15 * size // 22, marge + size // 22]
    if (i == 28):
        return [marge + 17 * size // 22, marge + size // 22]
    if (i == 29):
        return [marge + 19 * size // 22, marge + size // 22]
    if (i == 30):
        return [marge + 21 * size // 22, marge + size // 22]
    if (i == 31):
        return [marge + 21 * size // 22, marge + 3 * size // 22]
    if (i == 32):
        return [marge + 21 * size // 22, marge + 5 * size // 22]
    if (i == 33):
        return [marge + 21 * size // 22, marge + 7 * size // 22]
    if (i == 34):
        return [marge + 21 * size // 22, marge + 9 * size // 22]
    if (i == 35):
        return [marge + 21 * size // 22, marge + 11 * size // 22]
    if (i == 36):
        return [marge + 21 * size // 22, marge + 13 * size // 22]
    if (i == 37):
        return [marge + 21 * size // 22, marge + 15 * size // 22]
    if (i == 38):
        return [marge + 21 * size // 22, marge + 17 * size // 22]
    if (i == 39):
        return [marge + 21 * size // 22, marge + 19 * size // 22]

    else :
        return [0,0]

def grande_bijection(i: int,x_init : int, y_init : int, size : int):
    pass



class Board:
    def __init__(self):
            # Plus complexe parce qu'il faut différencier toutes les cases
            # Mettre le bon nom de fichier puis ne plus y toucher
        properties = read_properties("properties.txt")
        self._cases = [Case("Start", 0)]
        c = 0
        for i in range(1, 40):
            if (i == 2 or i == 7 or i == 17 or i == 22 or i == 33 or i == 36):
                self._cases.append(Luck(i))
            elif (i == 4):
                self._cases.append(Taxes(i, 100))
            elif (i == 38):
                self._cases.append(Taxes(i, 200))
            elif (i == 10):
                self._cases.append(Prison())
            elif (i == 20):
                self._cases.append(Case("Free Park", i))
            elif (i == 30):
                self._cases.append(GoToPrison())
            elif (i == 12):
                self._cases.append(Company(i, "Compagnie des eaux"))
            elif (i == 28):
                self._cases.append(Company(i, "Compagnie d'électricité"))
            elif (i == 5):
                self._cases.append(TrainStation("Gare Montparnasse", i))
            elif (i == 15):
                self._cases.append(TrainStation("Gare de Lyon", i))
            elif (i == 25):
                self._cases.append(TrainStation("Gare du Nord", i))
            elif (i == 35):
                self._cases.append(TrainStation("Gare Saint Lazare", i))
            else:
                self._cases.append(properties[c])
                c += 1
            self._nb_spaces = 40

    ## Accesseurs ##
    def cases(self):
        return self._cases

    def nb_spaces(self):
        return self._nb_spaces

    ## Méthodes ##
    def buy_property(self, player):
        """Un joueur veut acheter une propriété. Aucun return mais fait des print et màj des données des propriétés et du joueur"""
        value = self.cases()[player.position()].value()
        player.set_money(player.money() - value)
        self.cases()[player.position()].set_owner(player.id())

    def is_owned(self, id_space):
        """Renvoie l'ID du joueur si la propriété située sur id_space a été achetée et None sinon"""
        potential_owner = self.cases()[id_space].owner()
        if (potential_owner == 0):
            return None
        else:
            return potential_owner

    def ids_same_monopole(self, id_mono):
        ids = []
        for i in range(len(self.cases())):
            if (self.cases()[i].type() == "Property" and self.cases()[i].monopole_id() == id_mono):
                ids.append(self.cases()[i].id())
        return ids

    def list_property(self, player):
        """retourne la liste des propriétes que possède un joueur"""
        player_properties = []
        for i in range(1, len(self.cases())):
            if (self.cases()[i].type() in ["Property", "Company", "Train Station"]):
                if (self.is_owned(i) == player.id()):
                    player_properties.append(self.cases()[i])
        return player_properties

    def transaction(self, giver, receiver, amount_of_money):
        """ne retourne rien, effectue une transaction entre les joueurs giver et receiver"""
        giver.set_money(giver.money() - amount_of_money)
        receiver.set_money(receiver.money() + amount_of_money)

    def houses_on_monopole(self, id_property):
        ids_monopole = self.ids_same_monopole(self.cases()[id_property].monopole_id())
        nb_house = 0
        for id in ids_monopole:
            if (self.cases()[id].nb_houses() > 0):
                nb_house += 1
        return nb_house

    def sell_property(self, player, id_property):
        """vend la propriete d'id id_property du joueur player"""
        if (self.cases()[id_property].type == "Property"):
            if (self.houses_on_monopole(id_property) > 0):
                print(" \n \n You have to sell all the houses of the monopole before selling this property \n \n")
            else:
                self.cases()[id_property].set_owner(0)
                value = self.cases()[id_property].value()
                player.set_money(player.money() + value)
                print(" \n \n You earned ", value, "€ \n \n")
        else:
            self.cases()[id_property].set_owner(0)
            value = self.cases()[id_property].value()
            player.set_money(player.money() + value)
            print(" \n \n You earned ", value, "€ \n \n")


class miniBoard(Board):
    def __init__(self):
            # Plus complexe parce qu'il faut différencier toutes les cases
            # Mettre le bon nom de fichier puis ne plus y toucher
        properties = read_properties("properties.txt")
        print(properties)
        self._cases = [Case("Start", 0)]
        c = 0
        for i in range(1, 40):

            if (i == 2 or i==7 or i==17 or i==22 or i==33 or i==36):
                self._cases.append(Luck(i))
            elif (i == 4 or i== 38):
                self._cases.append(Taxes(i, 100))

            elif (i == 10):
                self._cases.append(Prison())
            elif (i == 20):
                self._cases.append(Case("Free Park", i))
            elif (i == 30):
                self._cases.append(GoToPrison())

            elif (i == 5):
                self._cases.append(TrainStation("Montparnasse", i))
            elif (i == 15):
                self._cases.append(TrainStation("Lyon", i))
            elif (i == 25):
                self._cases.append(TrainStation("Est", i))
            elif (i == 35):
                self._cases.append(TrainStation("St Lazare", i))

            elif (i == 12):
                self._cases.append(TrainStation("Electricté", i))
            elif (i == 28):
                self._cases.append(TrainStation("Eau", i))

            else:
                self._cases.append(properties[c])
                c += 1
            #print (i)
            self._nb_spaces = 40

    def show_board(self, screen, list_players : list, id_main_player : int) -> int:
        width, height = screen.get_size()
        marge = 10
        height_marge = height - 2*marge
        taille_case = height_marge//11

        pygame.draw.rect(screen, red,pygame.Rect(marge + taille_case, marge + 2 * taille_case // 3, taille_case, taille_case // 3))
        pygame.draw.rect(screen, red, pygame.Rect(marge + 3 * taille_case, marge + 2 * taille_case // 3, taille_case,taille_case // 3))
        pygame.draw.rect(screen, red, pygame.Rect(marge + 4 * taille_case, marge + 2 * taille_case // 3, taille_case,taille_case // 3))

        pygame.draw.rect(screen, yellow,pygame.Rect(marge + 6*taille_case, marge + 2 * taille_case // 3, taille_case, taille_case // 3))
        pygame.draw.rect(screen, yellow, pygame.Rect(marge + 7* taille_case, marge + 2 * taille_case // 3, taille_case,taille_case // 3))
        pygame.draw.rect(screen, yellow, pygame.Rect(marge + 9* taille_case, marge + 2 * taille_case // 3, taille_case,taille_case // 3))

        pygame.draw.rect(screen, bleu_ciel,pygame.Rect(marge + taille_case, marge + 10 * taille_case, taille_case, taille_case // 3))
        pygame.draw.rect(screen, bleu_ciel, pygame.Rect(marge + 2 * taille_case, marge + 10 * taille_case, taille_case,taille_case // 3))
        pygame.draw.rect(screen, bleu_ciel, pygame.Rect(marge + 4 * taille_case, marge + 10 * taille_case, taille_case,taille_case // 3))

        pygame.draw.rect(screen, marron, pygame.Rect(marge + 7 * taille_case, marge + 10 * taille_case, taille_case,taille_case // 3))
        pygame.draw.rect(screen, marron, pygame.Rect(marge + 9 * taille_case, marge + 10 * taille_case, taille_case,taille_case // 3))

        pygame.draw.rect(screen, orange,pygame.Rect(marge + 2 * taille_case // 3, marge + taille_case, taille_case//3, taille_case))
        pygame.draw.rect(screen, orange,pygame.Rect(marge + 2 * taille_case // 3, marge + 2*taille_case, taille_case // 3, taille_case))
        pygame.draw.rect(screen, orange,pygame.Rect(marge + 2 * taille_case // 3, marge + 4*taille_case, taille_case // 3, taille_case))

        pygame.draw.rect(screen, pink ,pygame.Rect(marge + 2 * taille_case // 3, marge + 6*taille_case, taille_case // 3, taille_case))
        pygame.draw.rect(screen, pink,pygame.Rect(marge + 2 * taille_case // 3, marge + 7 * taille_case, taille_case // 3,taille_case))
        pygame.draw.rect(screen, pink,pygame.Rect(marge + 2 * taille_case // 3, marge + 9 * taille_case, taille_case // 3,taille_case))

        pygame.draw.rect(screen, green,pygame.Rect(marge + 10 * taille_case , marge + taille_case, taille_case // 3, taille_case))
        pygame.draw.rect(screen, green,pygame.Rect(marge + 10 * taille_case, marge + 2*taille_case, taille_case // 3, taille_case))
        pygame.draw.rect(screen, green,pygame.Rect(marge + 10 * taille_case, marge + 4*taille_case, taille_case // 3, taille_case))

        pygame.draw.rect(screen, bleu_fonce,pygame.Rect(marge + 10 * taille_case, marge + 7*taille_case, taille_case // 3, taille_case))
        pygame.draw.rect(screen, bleu_fonce,pygame.Rect(marge + 10 * taille_case, marge + 9*taille_case, taille_case // 3, taille_case))

        pygame.draw.line(screen, black, (marge,marge), (marge,height-marge))
        pygame.draw.line(screen, black, (marge, marge), (height - marge, marge))
        pygame.draw.line(screen, black, (marge,height-marge), (height - marge, height-marge))
        pygame.draw.line(screen, black, (height - marge, marge), (height-marge, height - marge))

        pygame.draw.line(screen, black, (marge + taille_case,  marge + taille_case), (marge +10*taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge + taille_case, marge + taille_case),(marge + taille_case, marge +10*taille_case))
        pygame.draw.line(screen, black, (marge +10*taille_case, marge + taille_case),(marge +10*taille_case, marge +10*taille_case))
        pygame.draw.line(screen, black, (marge + taille_case, marge +10*taille_case),(marge +10*taille_case, marge +10*taille_case))

        pygame.draw.line(screen, black, (marge + taille_case, marge),(marge + taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge + 2 * taille_case, marge), (marge + 2 * taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge + 3 * taille_case, marge),(marge + 3 * taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge + 4 * taille_case, marge),(marge + 4 * taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge + 5 * taille_case, marge),(marge + 5 * taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge + 6 * taille_case, marge),(marge + 6 * taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge + 7 * taille_case, marge),(marge + 7 * taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge + 8 * taille_case, marge),(marge + 8 * taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge + 9 * taille_case, marge),(marge + 9 * taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge + 10 * taille_case, marge),(marge + 10 * taille_case, marge + taille_case))

        pygame.draw.line(screen, black, (marge + taille_case, marge+10*taille_case), (marge + taille_case, height-marge))
        pygame.draw.line(screen, black, (marge + 2 * taille_case, marge+ 10 * taille_case),(marge + 2 * taille_case, height-marge))
        pygame.draw.line(screen, black, (marge + 3 * taille_case, marge+ 10 * taille_case),(marge + 3 * taille_case, height-marge))
        pygame.draw.line(screen, black, (marge + 4 * taille_case, marge+ 10 * taille_case),(marge + 4 * taille_case, height-marge))
        pygame.draw.line(screen, black, (marge + 5 * taille_case, marge+ 10 * taille_case),(marge + 5 * taille_case, height-marge))
        pygame.draw.line(screen, black, (marge + 6 * taille_case, marge+ 10 * taille_case),(marge + 6 * taille_case, height-marge))
        pygame.draw.line(screen, black, (marge + 7 * taille_case, marge+ 10 * taille_case),(marge + 7 * taille_case, height-marge))
        pygame.draw.line(screen, black, (marge + 8 * taille_case, marge+ 10 * taille_case),(marge + 8 * taille_case, height-marge))
        pygame.draw.line(screen, black, (marge + 9 * taille_case, marge+ 10 * taille_case),(marge + 9 * taille_case, height-marge))
        pygame.draw.line(screen, black, (marge + 10 * taille_case, marge+ 10 * taille_case),(marge + 10 * taille_case, height-marge))

        pygame.draw.line(screen, black, (marge, marge + taille_case),(marge + taille_case, marge + taille_case))
        pygame.draw.line(screen, black, (marge, marge + 2*taille_case), (marge + taille_case, marge + 2*taille_case))
        pygame.draw.line(screen, black, (marge, marge + 3 * taille_case),(marge + taille_case, marge + 3 * taille_case))
        pygame.draw.line(screen, black, (marge, marge + 4 * taille_case),(marge + taille_case, marge + 4 * taille_case))
        pygame.draw.line(screen, black, (marge, marge + 5 * taille_case), (marge + taille_case, marge + 5 * taille_case))
        pygame.draw.line(screen, black, (marge, marge + 6 * taille_case),(marge + taille_case, marge + 6 * taille_case))
        pygame.draw.line(screen, black, (marge, marge + 7 * taille_case),(marge + taille_case, marge + 7 * taille_case))
        pygame.draw.line(screen, black, (marge, marge + 8 * taille_case),(marge + taille_case, marge + 8 * taille_case))
        pygame.draw.line(screen, black, (marge, marge + 9 * taille_case),(marge + taille_case, marge + 9 * taille_case))
        pygame.draw.line(screen, black, (marge, marge + 10 * taille_case),(marge + taille_case, marge + 10 * taille_case))

        pygame.draw.line(screen, black, (marge+ 10 * taille_case, marge + taille_case), (height-marge, marge + taille_case))
        pygame.draw.line(screen, black, (marge+ 10 * taille_case, marge + 2 * taille_case),(height-marge, marge + 2 * taille_case))
        pygame.draw.line(screen, black, (marge+ 10 * taille_case, marge + 3 * taille_case),(height-marge, marge + 3 * taille_case))
        pygame.draw.line(screen, black, (marge+ 10 * taille_case, marge + 4 * taille_case),(height-marge, marge + 4 * taille_case))
        pygame.draw.line(screen, black, (marge+ 10 * taille_case, marge + 5 * taille_case),(height-marge, marge + 5 * taille_case))
        pygame.draw.line(screen, black, (marge+ 10 * taille_case, marge + 6 * taille_case),(height-marge, marge + 6 * taille_case))
        pygame.draw.line(screen, black, (marge+ 10 * taille_case, marge + 7 * taille_case),(height-marge, marge + 7 * taille_case))
        pygame.draw.line(screen, black, (marge+ 10 * taille_case, marge + 8 * taille_case),(height-marge, marge + 8 * taille_case))
        pygame.draw.line(screen, black, (marge+ 10 * taille_case, marge + 9 * taille_case),(height-marge, marge + 9 * taille_case))
        pygame.draw.line(screen, black, (marge+ 10 * taille_case, marge + 10 * taille_case),(height-marge, marge + 10 * taille_case))

        print_basic_text(screen,self.cases()[5].name(),marge + 11*taille_case//2, 32*taille_case//3)
        print_basic_text(screen, self.cases()[15].name(), marge + taille_case//2, marge + 11*taille_case//2)
        print_basic_text(screen, self.cases()[25].name(), marge + 11*taille_case//2, taille_case//3)
        print_basic_text(screen, self.cases()[35].name(), marge +21*taille_case//2, marge + 11*taille_case//2)

        print_basic_text(screen, "Start", marge +21*taille_case//2, marge +21*taille_case//2)
        print_basic_text(screen, "Jail", marge + taille_case//2, marge +21*taille_case//2)
        print_basic_text(screen, "Free Park", marge + taille_case//2, marge + taille_case//2)
        print_basic_text(screen, "Go to Jail", marge +21*taille_case//2, marge + taille_case//2)

        luck = pygame.image.load('pictures/MINI_CHANCE.png')
        luck_width, luck_height = luck.get_size()
        screen.blit(luck,(marge + 5*taille_case//2- luck_width // 2, marge + taille_case//2 - luck_height // 2))
        screen.blit(luck,(marge + 7*taille_case//2- luck_width // 2, marge  +21*taille_case//2 - luck_height // 2))
        screen.blit(luck, (marge + 17*taille_case//2- luck_width // 2, marge  +21*taille_case//2 - luck_height // 2))
        screen.blit(luck, (marge + taille_case//2- luck_width // 2, marge + 7*taille_case//2- luck_height // 2))
        screen.blit(luck, (marge + 21*taille_case//2 - luck_width // 2, marge + 7*taille_case//2- luck_height // 2))
        screen.blit(luck, (marge + 21*taille_case//2 - luck_width // 2, marge + 13*taille_case//2- luck_height // 2))

        taxes = pygame.image.load('pictures/MINI_TAXE.png')
        taxes_width, taxes_height = taxes.get_size()
        screen.blit(taxes,(marge + 13*taille_case//2- taxes_width // 2, marge  +21*taille_case//2 - taxes_height // 2))
        screen.blit(taxes,(marge + 21*taille_case//2 - taxes_width // 2, marge + 17*taille_case//2- taxes_height // 2))

        for i in range(len(self.cases())):
            x_position, y_position = mini_bijection(i,marge,taille_case)
            #if (i!= 0 and i!=3 and i!=6 and i!=9 and i!=12 and i!=15 and i!=18 and i!= 21 and i!=8 and i!=2 and i!=20 and i!=13):
            #print(i)
            #print_basic_text(screen,self.cases()[i].name(),x_position,y_position)

        for player in list_players:
            if player.id() == id_main_player:
                self.cases()[player.position()].show_case(height_marge//2 - 150, height_marge//2 - 170, screen)

        '''
        for player in list_players:
            x_position, y_position = mini_bijection(player.position(),marge, taille_case)
            print(x_position,y_position)
            if player.id() == 2:
                pion2 = pygame.image.load('pictures/MINI_PION2.png')
                pion2_width, pion2_height = pion2.get_size()
                screen.blit(pion2,
                            (x_position , y_position ))
        
            if player.id() == 1:
                pion1 = pygame.image.load('pictures/MINI_PION1.png')
                pion1_width, pion1_height = pion1.get_size()
                screen.blit(pion1,
                            (x_position - 2*taille_case//70 - pion1_width//2, y_position - 3*taille_case//70 - pion1_height//2))
            if player.id() == 3:
                pion3 = pygame.image.load('pictures/MINI_PION3.png')
                pion3_width, pion3_height = pion3.get_size()
                screen.blit(pion3,
                            (x_position - 2*taille_case//70 - pion3_width//2, y_position + 3*taille_case//70 - pion3_height//2))
            if player.id() == 4:
                pion4 = pygame.image.load('pictures/MINI_PION4.png')
                pion4_width, pion4_height = pion4.get_size()
                screen.blit(pion4,
                            (x_position + 2*taille_case//70 - pion4_width//2, y_position + 3*taille_case//70 - pion4_height//2))
            
            
            #==================================================================================================
            # Mini board Specificities (recommended size : 700 px, less than 10 char in teh name of properties)
            # =================================================================================================
    
            # Name of classic cases
    
            # show luck and tax cases
    
            #display main_player's case
    
            #display players position
    
    
            #display property names
    
    
    
    
    
            '''
        # Update the display
        pygame.display.update()


if __name__ == "__main__":
    main_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = main_screen.get_size()
    pygame.draw.rect(main_screen,white,Rect(0,0,screen_width,screen_height))
    pygame.display.update()
    test_board = miniBoard()
    Go = True
    test_board.show_board(main_screen,
                              [Player(1, "A", position=16),
                               Player(2, "B", position=16),
                               Player(3, "C", position=16),
                               Player(4, "D", position=8)], 1)
    sleep(4)
    pygame.quit()

