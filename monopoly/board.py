"""
Board.py
Author : TDLOG group A
Date : 24/01/2022
Comments : fully functional (18/01/2022)
"""

# standard library
import random
from time import sleep
import pygame
from pygame.locals import *
import os
import importlib.resources

# local source
import monopoly.text_input as input
from monopoly.text_input import text_format
from monopoly.color import *
from monopoly.player import *
from monopoly.propriete import *
from monopoly.utility_functions import print_basic_text,read_properties,mini_bijection,grande_bijection

pygame.init()

class Board:
    def __init__(self):
        full_path = os.getcwd()
        print(full_path)
        properties = read_properties(importlib.resources.path('monopoly.config','mini_properties.txt').args[0].path[:-11] +"properties.txt")
        with open(importlib.resources.path('monopoly.config','mini_properties.txt').args[0].path[:-11] +"short_properties_name.txt", "r") as tf:
            self._nom = tf.read().split('\n')
        print("nom=",self._nom)
        self._cases = [Case("Start", 0)]
        c = 0
        n = 0
        for i in range(1, 40):
            if (i == 2 or i == 7 or i == 17 or i == 22 or i == 33 or i == 36):
                self._cases.append(Luck(i))
            elif (i == 4 or i == 38):
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
                # print (i)
            #self._nom.append(nom[n])
            n += 1
            self._nb_spaces = 40

    ## Accesseurs ##
    def cases(self):
        return self._cases

    def nom(self):
        return self._nom

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

    def show_board(self, screen,x_init : int, y_init : int, size : int, list_players : list, id_main_player : int) -> int:

        # adjust the size for a perfect match
        marge = 10
        while (((size%22)!=0) or ((size%33)!=0)) :
            size +=1
        taille_case = size //11

        pygame.draw.rect(screen, white, pygame.Rect(x_init, y_init, size, size))

        # A small condition for the smallest board
        if size <= 900:
            mini = True
        else :
            mini = False

        # =========================================================
        # Board Specificities (recommended size : 700 px or 1000px
        # =========================================================

        pygame.draw.rect(screen, red,pygame.Rect(x_init + taille_case, y_init + 2 * taille_case // 3, taille_case, taille_case // 3))
        pygame.draw.rect(screen, red, pygame.Rect(x_init + 3 * taille_case, y_init + 2 * taille_case // 3, taille_case,taille_case // 3))
        pygame.draw.rect(screen, red, pygame.Rect(x_init + 4 * taille_case, y_init + 2 * taille_case // 3, taille_case,taille_case // 3))

        pygame.draw.rect(screen, jaune,pygame.Rect(x_init + 6*taille_case, y_init + 2 * taille_case // 3, taille_case, taille_case // 3))
        pygame.draw.rect(screen, jaune, pygame.Rect(x_init + 7* taille_case, y_init + 2 * taille_case // 3, taille_case,taille_case // 3))
        pygame.draw.rect(screen, jaune, pygame.Rect(x_init + 9* taille_case, y_init + 2 * taille_case // 3, taille_case,taille_case // 3))

        pygame.draw.rect(screen, bleu_ciel,pygame.Rect(x_init + taille_case, y_init + 10 * taille_case, taille_case, taille_case // 3))
        pygame.draw.rect(screen, bleu_ciel, pygame.Rect(x_init + 2 * taille_case, y_init + 10 * taille_case, taille_case,taille_case // 3))
        pygame.draw.rect(screen, bleu_ciel, pygame.Rect(x_init + 4 * taille_case, y_init + 10 * taille_case, taille_case,taille_case // 3))

        pygame.draw.rect(screen, marron, pygame.Rect(x_init + 7 * taille_case, y_init + 10 * taille_case, taille_case,taille_case // 3))
        pygame.draw.rect(screen, marron, pygame.Rect(x_init + 9 * taille_case, y_init + 10 * taille_case, taille_case,taille_case // 3))

        pygame.draw.rect(screen, orange,pygame.Rect(x_init + 2 * taille_case // 3, y_init + taille_case, taille_case//3, taille_case))
        pygame.draw.rect(screen, orange,pygame.Rect(x_init + 2 * taille_case // 3, y_init + 2*taille_case, taille_case // 3, taille_case))
        pygame.draw.rect(screen, orange,pygame.Rect(x_init + 2 * taille_case // 3, y_init + 4*taille_case, taille_case // 3, taille_case))

        pygame.draw.rect(screen, violet ,pygame.Rect(x_init + 2 * taille_case // 3, y_init + 6*taille_case, taille_case // 3, taille_case))
        pygame.draw.rect(screen, violet,pygame.Rect(x_init + 2 * taille_case // 3, y_init + 7 * taille_case, taille_case // 3,taille_case))
        pygame.draw.rect(screen, violet,pygame.Rect(x_init + 2 * taille_case // 3, y_init + 9 * taille_case, taille_case // 3,taille_case))

        pygame.draw.rect(screen, vert,pygame.Rect(x_init + 10 * taille_case , y_init + taille_case, taille_case // 3, taille_case))
        pygame.draw.rect(screen, vert,pygame.Rect(x_init + 10 * taille_case, y_init + 2*taille_case, taille_case // 3, taille_case))
        pygame.draw.rect(screen, vert,pygame.Rect(x_init + 10 * taille_case, y_init + 4*taille_case, taille_case // 3, taille_case))

        pygame.draw.rect(screen, bleu_fonce,pygame.Rect(x_init + 10 * taille_case, y_init + 7*taille_case, taille_case // 3, taille_case))
        pygame.draw.rect(screen, bleu_fonce,pygame.Rect(x_init + 10 * taille_case, y_init + 9*taille_case, taille_case // 3, taille_case))

        pygame.draw.line(screen, black, (x_init,y_init), (x_init,y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init, y_init), (x_init + 11*taille_case, y_init))
        pygame.draw.line(screen, black, (x_init,y_init + 11*taille_case), (x_init + 11*taille_case, y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init + 11*taille_case, y_init), (x_init + 11*taille_case, y_init + 11*taille_case))

        pygame.draw.line(screen, black, (x_init + taille_case,  y_init + taille_case), (x_init +10*taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init + taille_case, y_init + taille_case),(x_init + taille_case, y_init +10*taille_case))
        pygame.draw.line(screen, black, (x_init +10*taille_case, y_init + taille_case),(x_init +10*taille_case, y_init +10*taille_case))
        pygame.draw.line(screen, black, (x_init + taille_case, y_init +10*taille_case),(x_init +10*taille_case, y_init +10*taille_case))

        pygame.draw.line(screen, black, (x_init + taille_case, y_init),(x_init + taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init + 2 * taille_case, y_init), (x_init + 2 * taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init + 3 * taille_case, y_init),(x_init + 3 * taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init + 4 * taille_case, y_init),(x_init + 4 * taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init + 5 * taille_case, y_init),(x_init + 5 * taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init + 6 * taille_case, y_init),(x_init + 6 * taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init + 7 * taille_case, y_init),(x_init + 7 * taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init + 8 * taille_case, y_init),(x_init + 8 * taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init + 9 * taille_case, y_init),(x_init + 9 * taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init + 10 * taille_case, y_init),(x_init + 10 * taille_case, y_init + taille_case))

        pygame.draw.line(screen, black, (x_init + taille_case, y_init+10*taille_case), (x_init + taille_case, y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init + 2 * taille_case, y_init+ 10 * taille_case),(x_init + 2 * taille_case, y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init + 3 * taille_case, y_init+ 10 * taille_case),(x_init + 3 * taille_case, y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init + 4 * taille_case, y_init+ 10 * taille_case),(x_init + 4 * taille_case, y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init + 5 * taille_case, y_init+ 10 * taille_case),(x_init + 5 * taille_case, y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init + 6 * taille_case, y_init+ 10 * taille_case),(x_init + 6 * taille_case, y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init + 7 * taille_case, y_init+ 10 * taille_case),(x_init + 7 * taille_case, y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init + 8 * taille_case, y_init+ 10 * taille_case),(x_init + 8 * taille_case, y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init + 9 * taille_case, y_init+ 10 * taille_case),(x_init + 9 * taille_case, y_init + 11*taille_case))
        pygame.draw.line(screen, black, (x_init + 10 * taille_case, y_init+ 10 * taille_case),(x_init + 10 * taille_case, y_init + 11*taille_case))

        pygame.draw.line(screen, black, (x_init, y_init + taille_case),(x_init + taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init, y_init + 2*taille_case), (x_init + taille_case, y_init + 2*taille_case))
        pygame.draw.line(screen, black, (x_init, y_init + 3 * taille_case),(x_init + taille_case, y_init + 3 * taille_case))
        pygame.draw.line(screen, black, (x_init, y_init + 4 * taille_case),(x_init + taille_case, y_init + 4 * taille_case))
        pygame.draw.line(screen, black, (x_init, y_init + 5 * taille_case), (x_init + taille_case, y_init + 5 * taille_case))
        pygame.draw.line(screen, black, (x_init, y_init + 6 * taille_case),(x_init + taille_case, y_init + 6 * taille_case))
        pygame.draw.line(screen, black, (x_init, y_init + 7 * taille_case),(x_init + taille_case, y_init + 7 * taille_case))
        pygame.draw.line(screen, black, (x_init, y_init + 8 * taille_case),(x_init + taille_case, y_init + 8 * taille_case))
        pygame.draw.line(screen, black, (x_init, y_init + 9 * taille_case),(x_init + taille_case, y_init + 9 * taille_case))
        pygame.draw.line(screen, black, (x_init, y_init + 10 * taille_case),(x_init + taille_case, y_init + 10 * taille_case))

        pygame.draw.line(screen, black, (x_init+ 10 * taille_case, y_init + taille_case), (x_init + 11*taille_case, y_init + taille_case))
        pygame.draw.line(screen, black, (x_init+ 10 * taille_case, y_init + 2 * taille_case),(x_init + 11*taille_case, y_init + 2 * taille_case))
        pygame.draw.line(screen, black, (x_init+ 10 * taille_case, y_init + 3 * taille_case),(x_init + 11*taille_case, y_init + 3 * taille_case))
        pygame.draw.line(screen, black, (x_init+ 10 * taille_case, y_init + 4 * taille_case),(x_init + 11*taille_case, y_init + 4 * taille_case))
        pygame.draw.line(screen, black, (x_init+ 10 * taille_case, y_init + 5 * taille_case),(x_init + 11*taille_case, y_init + 5 * taille_case))
        pygame.draw.line(screen, black, (x_init+ 10 * taille_case, y_init + 6 * taille_case),(x_init + 11*taille_case, y_init + 6 * taille_case))
        pygame.draw.line(screen, black, (x_init+ 10 * taille_case, y_init + 7 * taille_case),(x_init + 11*taille_case, y_init + 7 * taille_case))
        pygame.draw.line(screen, black, (x_init+ 10 * taille_case, y_init + 8 * taille_case),(x_init + 11*taille_case, y_init + 8 * taille_case))
        pygame.draw.line(screen, black, (x_init+ 10 * taille_case, y_init + 9 * taille_case),(x_init + 11*taille_case, y_init + 9 * taille_case))
        pygame.draw.line(screen, black, (x_init+ 10 * taille_case, y_init + 10 * taille_case),(x_init + 11*taille_case, y_init + 10 * taille_case))


        # Luck and taxe icons
        luck = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11] +'MINI_MINI_CHANCE.png')
        luck_width, luck_height = luck.get_size()
        screen.blit(luck,(x_init + 5*taille_case//2- luck_width // 2, y_init + taille_case//2 - luck_height // 2))
        screen.blit(luck,(x_init + 7*taille_case//2- luck_width // 2, y_init  +21*taille_case//2 - luck_height // 2))
        screen.blit(luck, (x_init + 17*taille_case//2- luck_width // 2, y_init  +21*taille_case//2 - luck_height // 2))
        screen.blit(luck, (x_init + taille_case//2- luck_width // 2, y_init + 7*taille_case//2- luck_height // 2))
        screen.blit(luck, (x_init + 21*taille_case//2 - luck_width // 2, y_init + 7*taille_case//2- luck_height // 2))
        screen.blit(luck, (x_init + 21*taille_case//2 - luck_width // 2, y_init + 13*taille_case//2- luck_height // 2))

        taxes = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11] + 'MINI_MINI_TAXE.png')
        taxes_width, taxes_height = taxes.get_size()
        screen.blit(taxes,(x_init + 13*taille_case//2- taxes_width // 2, y_init  +21*taille_case//2 - taxes_height // 2))
        screen.blit(taxes,(x_init + 21*taille_case//2 - taxes_width // 2, y_init + 17*taille_case//2- taxes_height // 2))

        # Display property names
        for i in range(len(self.cases())):
            x_position, y_position = grande_bijection(i,x_init,y_init,size)
            print_basic_text(screen,self.nom()[i],x_position,y_position)

        # Display main player case
        for i in range(1, len(list_players)):
            if list_players[i].id() == id_main_player:
                self.cases()[list_players[i].position()].show_case(x_init + size // 2 - 150, y_init + size // 2 - 170,
                                                                   screen)

        for i in range(1, len(list_players)):
            x_position, y_position = grande_bijection(list_players[i].position(),x_init, y_init, size)
            print(x_position,y_position)

            if list_players[i].id() == 2:
                if not mini :
                    pion2 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11] + 'MINI_PION2.png')
                if mini :
                    pion2 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11] + 'MINI_MINI_PION2.png')
                pion2_width, pion2_height = pion2.get_size()
                screen.blit(pion2,(x_position - taille_case//4  - pion2_width//2, y_position - taille_case//4 - pion2_height//2))

            if list_players[i].id() == 1:
                if not mini :
                    pion1 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_PION1.png')
                if mini :
                    pion1 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_MINI_PION1.png')
                pion1_width, pion1_height = pion1.get_size()
                screen.blit(pion1,(x_position - taille_case//4  - pion1_width//2, y_position + taille_case//4 - pion1_height//2))

            if list_players[i].id() == 3:
                if not mini :
                    pion3 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_PION3.png')
                if mini :
                    pion3 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_MINI_PION3.png')
                pion3_width, pion3_height = pion3.get_size()
                screen.blit(pion3,(x_position + taille_case//4 - pion3_width//2, y_position- taille_case//4 - pion3_height//2))

            if list_players[i].id() == 4:
                if not mini :
                    pion4 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_PION4.png')
                if mini :
                    pion4 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_MINI_PION4.png')
                pion4_width, pion4_height = pion4.get_size()
                screen.blit(pion4,(x_position + taille_case//4  - pion4_width//2, y_position + taille_case//4 - pion4_height//2))

        # Update the display
        pygame.display.update()

class miniBoard(Board):
    def __init__(self):
        # Plus complexe parce qu'il faut différencier toutes les cases
        # Mettre le bon nom de fichier puis ne plus y toucher
        properties = read_properties(importlib.resources.path('monopoly.config','mini_properties.txt').args[0].path[:-11] + "mini_properties.txt")
        self._cases = [Case("Start", 0)]
        c = 0
        for i in range(1, 24):

            if (i == 8 or i==20):
                self._cases.append(Luck(i))
            elif (i == 2 or i== 13):
                self._cases.append(Taxes(i, 100))

            elif (i == 6):
                self._cases.append(Prison())
            elif (i == 12):
                self._cases.append(Case("Free Park", i))
            elif (i == 18):
                self._cases.append(GoToPrison())

            elif (i == 3):
                self._cases.append(TrainStation("Gare RER", i))
            elif (i == 9):
                self._cases.append(TrainStation("ENPC", i))
            elif (i == 15):
                self._cases.append(TrainStation("ESIEE", i))
            elif (i == 21):
                self._cases.append(TrainStation("Gare BUS", i))

            else:
                self._cases.append(properties[c])
                c += 1
            self._nb_spaces = 24

    def show_board(self, screen, x_init: int, y_init: int, size: int, list_players : list, id_main_player : int) -> int:
        while size%7 !=0 and size%70 != 0:
            size +=1
        pygame.draw.rect(screen, white, pygame.Rect(x_init, y_init, size, size))

        pygame.draw.rect(screen, black, pygame.Rect(x_init + size//7 , y_init + size//7, 5*size//7, 5*size//7), 1)
        pygame.draw.line(screen, black, (x_init + size//7, y_init), (x_init + size//7,y_init + size))
        pygame.draw.line(screen, black, (x_init + 6*size // 7 - 1, y_init), (x_init + 6*size // 7 - 1, y_init + size))
        pygame.draw.line(screen, black, (x_init, y_init + size//7), (x_init + size, y_init + size//7))
        pygame.draw.line(screen, black, (x_init, y_init + 6*size//7 - 1), (x_init + size, y_init + 6*size//7 - 1))

        pygame.draw.line(screen, black, (x_init + 7*size // 70, y_init), (x_init + 7*size // 70, y_init + size))
        pygame.draw.line(screen, black, (x_init + 63 * size // 70 - 1, y_init),(x_init + 63 * size // 70 - 1, y_init + size))
        pygame.draw.line(screen, black, (x_init, y_init + 7*size // 70), (x_init + size, y_init + 7*size // 70))
        pygame.draw.line(screen, black, (x_init, y_init + 63 * size // 70 - 1),(x_init + size, y_init + 63 * size // 70 - 1))

        pygame.draw.rect(screen, white,pygame.Rect(x_init, y_init ,size // 7 , size // 7 ))
        pygame.draw.rect(screen, white, pygame.Rect(x_init, y_init  + 6*size // 7 , size // 7, size // 7))
        pygame.draw.rect(screen, white, pygame.Rect(x_init + 6*size//7, y_init, size // 7, size // 7))
        pygame.draw.rect(screen, white, pygame.Rect(x_init + 6*size//7, y_init  + 6*size // 7, size // 7, size // 7))

        #==================================================================================================
        # Mini board Specificities (recommended size : 700 px, less than 10 char in teh name of properties)
        # =================================================================================================

        # Case's lines
        pygame.draw.line(screen, black, (x_init, y_init + 20*size // 70), (x_init + size, y_init + 20*size // 70))
        pygame.draw.line(screen, black, (x_init, y_init + 30 * size // 70), (x_init + size, y_init + 30 * size // 70))
        pygame.draw.line(screen, black, (x_init, y_init + 40*size // 70), (x_init + size, y_init + 40*size // 70))
        pygame.draw.line(screen, black, (x_init, y_init + 50* size // 70), (x_init + size, y_init + 50 * size // 70))

        pygame.draw.line(screen, black, (x_init+ 20 * size // 70, y_init), (x_init + 20 * size // 70, y_init + size))
        pygame.draw.line(screen, black, (x_init+ 30 * size // 70, y_init), (x_init + 30 * size // 70, y_init + size))
        pygame.draw.line(screen, black, (x_init+ 40 * size // 70, y_init), (x_init + 40 * size // 70, y_init + size))
        pygame.draw.line(screen, black, (x_init+ 50 * size // 70, y_init), (x_init + 50 * size // 70, y_init + size))

        pygame.draw.rect(screen, white,pygame.Rect(x_init + size // 7+1, y_init + size // 7+1, 5*size // 7-2, 5*size // 7-2))
        pygame.draw.rect(screen, black, pygame.Rect(x_init, y_init, size, size), 1)

        # White rect on train stations
        pygame.draw.rect(screen, white, pygame.Rect(x_init + 3*size//7 +1, y_init + 1, size//7 - 1, size//7 - 2))
        pygame.draw.rect(screen, white, pygame.Rect(x_init + 3*size//7 +1, y_init +6*size//7 + 1, size//7 - 1, size//7 - 2))
        pygame.draw.rect(screen, white, pygame.Rect(x_init +1, y_init + 3*size//7 + 1, size//7 - 1, size//7 - 1))
        pygame.draw.rect(screen, white, pygame.Rect(x_init +6*size//7, y_init + 3*size//7 + 1, size//7 - 1, size//7 - 1))

        # White rect on luck and tax cases
        pygame.draw.rect(screen, white,pygame.Rect(x_init + size // 7 + 1, y_init + 1, size // 7 - 1, size // 7 - 2))
        pygame.draw.rect(screen, white,pygame.Rect(x_init + 4 * size // 7 + 1, y_init + 6 * size // 7 + 1, size // 7 - 1,size // 7 - 2))
        pygame.draw.rect(screen, white,pygame.Rect(x_init + 1, y_init + 4 * size // 7 + 1, size // 7 - 1, size // 7 - 1))
        pygame.draw.rect(screen, white,pygame.Rect(x_init + 6 * size // 7, y_init + 2 * size // 7 + 1, size // 7 - 1, size // 7 - 1))

        # Color on the properties
        pygame.draw.rect(screen,self.cases()[1].color,pygame.Rect(x_init + 5*size // 7 + 1, y_init + 6*size // 7, size // 7 - 2,3 * size // 70 - 1))
        pygame.draw.rect(screen,self.cases()[1].color,pygame.Rect(x_init + 2*size // 7 + 1, y_init + 6*size // 7, size // 7 - 1,3 * size // 70 - 1))
        pygame.draw.rect(screen,self.cases()[1].color,pygame.Rect(x_init + size // 7 + 1, y_init + 6*size // 7, size // 7 - 1,3 * size // 70 - 1))
        pygame.draw.rect(screen,self.cases()[17].color,pygame.Rect(x_init + 5*size // 7 + 1, y_init + 7*size // 70 +1, size // 7 - 2,3 * size // 70 - 1))
        pygame.draw.rect(screen,self.cases()[17].color,pygame.Rect(x_init + 4*size // 7 + 1, y_init + 7*size // 70 +1, size // 7 - 1,3 * size // 70 - 1))
        pygame.draw.rect(screen,self.cases()[17].color,pygame.Rect(x_init + 2*size // 7 + 1, y_init + 7*size // 70 +1, size // 7 - 1,3 * size // 70 - 1))
        pygame.draw.rect(screen,self.cases()[7].color,pygame.Rect(x_init + 7*size // 70 +1, y_init + 5*size // 7 +1, 3 * size // 70 - 1,size//7 - 2))
        pygame.draw.rect(screen,self.cases()[7].color,pygame.Rect(x_init + 7*size // 70 +1, y_init + size // 7 +1, 3 * size // 70 - 1,size//7 - 1))
        pygame.draw.rect(screen,self.cases()[7].color,pygame.Rect(x_init + 7*size // 70 +1, y_init + 2*size // 7 +1, 3 * size // 70 - 1,size//7 - 1))
        pygame.draw.rect(screen,self.cases()[23].color,pygame.Rect(x_init + 60*size // 70 , y_init + size // 7 +1, 3 * size // 70 - 1,size//7 - 1))
        pygame.draw.rect(screen,self.cases()[23].color,pygame.Rect(x_init + 60*size // 70 , y_init + 4*size // 7 +1, 3 * size // 70 - 1,size//7 - 1))
        pygame.draw.rect(screen,self.cases()[23].color,pygame.Rect(x_init + 60*size // 70 , y_init + 5*size // 7 +1, 3 * size // 70 - 1,size//7 - 2))

        # Name of train stations
        print_basic_text(screen,self.cases()[3].name(),x_init + 35*size//70,y_init + 65*size//70 -7)
        print_basic_text(screen, self.cases()[15].name(), x_init + 35 * size // 70, y_init + 5 * size // 70 )
        print_basic_text(screen, self.cases()[9].name(), x_init + 5 * size // 70, y_init + 35 * size // 70 )
        print_basic_text(screen, self.cases()[21].name(), x_init + 65 * size // 70, y_init + 35 * size // 70 )

        # Name of classic cases
        print_basic_text(screen, "Start", x_init + 65 * size // 70, y_init + 65 * size // 70)
        print_basic_text(screen, "Jail", x_init + 5 * size // 70, y_init + 65 * size // 70 )
        print_basic_text(screen, "Free Park", x_init + 5 * size // 70, y_init + 5 * size // 70 )
        print_basic_text(screen, "Go to Jail", x_init + 65 * size // 70, y_init + 5 * size // 70 )

        # show luck and tax cases
        luck = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_CHANCE.png')
        luck_width, luck_height = luck.get_size()
        screen.blit(luck,
                    (x_init + 5 * size // 70 - luck_width // 2, y_init + 45 * size // 70 - luck_height // 2))
        screen.blit(luck,
                    (x_init + 65 * size // 70 - luck_width // 2, y_init + 25 * size // 70 - luck_height // 2))

        taxes = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_TAXE.png')
        taxes_width, taxes_height = taxes.get_size()
        screen.blit(taxes,
                    (x_init + 15 * size // 70 - taxes_width // 2, y_init + 5 * size // 70 - taxes_height // 2))
        screen.blit(taxes,
                    (x_init + 45 * size // 70 - taxes_width // 2, y_init + 65 * size // 70 - taxes_height // 2))

        #display main_player's case
        for i in range(1,len(list_players)):
            if list_players[i].id() == id_main_player:
                self.cases()[list_players[i].position()].show_case(x_init + size//2 - 150, y_init + size//2 - 170, screen)

        #display players position
        for i in range(1,len(list_players)):
            x_position, y_position = mini_bijection(list_players[i].position(),x_init,y_init, size)
            if list_players[i].id() == 2:
                pion2 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_PION2.png')
                pion2_width, pion2_height = pion2.get_size()
                screen.blit(pion2,
                            (x_position + 2*size//70 - pion2_width//2, y_position - 3*size//70 - pion2_height//2))
            if list_players[i].id() == 1:
                pion1 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_PION1.png')
                pion1_width, pion1_height = pion1.get_size()
                screen.blit(pion1,
                            (x_position - 2*size//70 - pion1_width//2, y_position - 3*size//70 - pion1_height//2))
            if list_players[i].id() == 3:
                pion3 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_PION3.png')
                pion3_width, pion3_height = pion3.get_size()
                screen.blit(pion3,
                            (x_position - 2*size//70 - pion3_width//2, y_position + 3*size//70 - pion3_height//2))
            if list_players[i].id() == 4:
                pion4 = pygame.image.load(importlib.resources.path('monopoly.pictures','board.png').args[0].path[:-11]+'MINI_PION4.png')
                pion4_width, pion4_height = pion4.get_size()
                screen.blit(pion4,
                            (x_position + 2*size//70 - pion4_width//2, y_position + 3*size//70 - pion4_height//2))


        #display property names
        for i in range(len(self.cases())):
            x_position, y_position = mini_bijection(i,x_init,y_init,size)
            if (i!= 0 and i!=3 and i!=6 and i!=9 and i!=12 and i!=15 and i!=18 and i!= 21 and i!=8 and i!=2 and i!=20 and i!=13):
                print_basic_text(screen,self.cases()[i].name(),x_position,y_position - size//70)

        # Update the display
        pygame.display.update()
        return 0

# A local test of the class Board
if __name__ == "__main__":

    main_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = main_screen.get_size()

    if screen_height >= 1100:
        size_board = 1000
    else:
        size_board = 700

    pygame.draw.rect(main_screen,white,Rect(0,0,screen_width,screen_height))

    list_player = [0,Player(1, "A", position=3),
                   Player(2, "B", position=3),
                   Player(3, "C", position=3),
                   Player(4, "D", position=3)]

    pygame.display.update()

    # Test 1
    test_board = miniBoard()
    test_board.show_board(main_screen, screen_width//2 - 350 , screen_height//2 - 350, 700,list_player, 1)
    sleep(3)

    # Test 2
    pygame.draw.rect(main_screen, white, Rect(0, 0, screen_width, screen_height))
    test_board2 = Board()
    test_board2.show_board(main_screen,10,10,size_board,list_player,1)
    sleep(3)

    # Test 3
    pygame.draw.rect(main_screen, white, Rect(0, 0, screen_width, screen_height))
    test_board3 = Board()
    test_board2.show_board(main_screen, 10, 10, 700, list_player, 1)
    sleep(3)


    pygame.quit()

