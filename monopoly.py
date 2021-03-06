"""
monopoly.py
Author : TDLOG group A
Date : 24/01/2022
Comments :
"""

# Standard library
import random
import pygame
from pygame.locals import *
from time import sleep
import importlib.resources



# local source
from board_game.player import Player
from board_game.propriete import Property, Prison, GoToPrison, Taxes, TrainStation, Company, Case, Luck
from board_game.board import Board
from board_game import text_input as input
from board_game.text_input import text_format
from board_game.color import *
from board_game.utility_functions import obt_path

pygame.init()

class Game():
    def __init__(self):
        self.main_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.main_screen.get_size()
        self.game_var = self.begin_game()
        self.create_game(self.game_var)
        if self.height >= 900:
            self.size_board = 1056
        else :
            self.size_board = 660


    # BEGINNING OF THE GAME : MAIN MENU AND PLAYER SELECTION
    def run_main_menu(self):
        """Main menu of the game
        -> return 0 if new game
        -> return -1 if quit
        """
        play: bool = True
        selected = "start"
        game_on = True
        title_screen = pygame.image.load(obt_path('board_game.pictures','title_screen.jpg'))
        title_screen = title_screen.convert()
        picture_width, picture_height = title_screen.get_size()
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    game_on = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = "start"
                    if event.key == pygame.K_DOWN:
                        selected = "quit"
                    if event.key == pygame.K_RETURN:
                        if (selected == "start"):
                            play = False
                        elif (selected == "quit"):
                            play = False
                            game_on = False
                    if event.key == pygame.K_ESCAPE:
                        play = False
                        game_on = False
            if selected == "start":
                text_start = text_format("New Game", 30, red)
                text_quit = text_format("Quit", 30, black)
            if selected == "quit":
                text_start = text_format("New Game", 30, black)
                text_quit = text_format("Quit", 30, red)
            start_rect = text_start.get_rect()
            quit_rect = text_quit.get_rect()
            self.main_screen.fill(pygame.Color("white"))
            self.main_screen.blit(title_screen,
                                  (self.width / 2 - picture_width / 2, self.height / 2 - picture_height / 2))
            self.main_screen.blit(text_start, (self.width / 2 - (start_rect[2] / 2), self.height / 2))
            self.main_screen.blit(text_quit, (self.width / 2 - (quit_rect[2] / 2), self.height / 2 + 100))
            pygame.display.update()
        self.main_screen.fill(pygame.Color("white"))
        pygame.display.update()
        if not game_on:
            return -1
        return 0

    def run_choose_your_character(self):
        """ choose the number of players
        -> return 2, 3, or 4 for the number of player
        -> return -1 if echap
        -> return 0 if quit
        """
        play: bool = True
        selection_cursor = 0
        nb_players = -1
        title_screen = pygame.image.load(obt_path('board_game.pictures','title_screen.jpg'))
        title_screen = title_screen.convert()
        picture_width, picture_height = title_screen.get_size()
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection_cursor = ((selection_cursor - 1) % 3)
                    if event.key == pygame.K_DOWN:
                        selection_cursor = ((selection_cursor + 1) % 3)
                    if event.key == pygame.K_RETURN:
                        if (selection_cursor == 0):
                            play = False
                            nb_players = 2
                        elif (selection_cursor == 1):
                            play = False
                            nb_players = 3
                        elif (selection_cursor == 2):
                            play = False
                            nb_players = 4
                    if event.key == pygame.K_ESCAPE:
                        play = False
                        nb_players = -1
            if selection_cursor == 0:
                player2 = text_format("2 players", 30, red)
                player3 = text_format("3 players", 30, black)
                player4 = text_format("4 players", 30, black)
            if selection_cursor == 1:
                player2 = text_format("2 players", 30, black)
                player3 = text_format("3 players", 30, red)
                player4 = text_format("4 players", 30, black)
            if selection_cursor == 2:
                player2 = text_format("2 players", 30, black)
                player3 = text_format("3 players", 30, black)
                player4 = text_format("4 players", 30, red)
            player2_rect = player2.get_rect()
            player3_rect = player3.get_rect()
            player4_rect = player4.get_rect()
            self.main_screen.fill(pygame.Color("white"))
            self.main_screen.blit(title_screen,
                                  (self.width / 2 - picture_width / 2, self.height / 2 - picture_height / 2))
            self.main_screen.blit(player2, (self.width / 2 - (player2_rect[2] / 2), self.height / 2))
            self.main_screen.blit(player3, (self.width / 2 - (player3_rect[2] / 2), self.height / 2 + 100))
            self.main_screen.blit(player4, (self.width / 2 - (player4_rect[2] / 2), self.height / 2 + 200))
            pygame.display.update()
        self.main_screen.fill(pygame.Color("white"))
        pygame.display.update()
        return nb_players

    def enter_player_names(self, nb_player):
        """
        :param nb_player: the number of player
        :return: -1 if exit, 0 if everything is ok
        """
        title_screen = pygame.image.load(obt_path('board_game.pictures','title_screen.jpg'))
        title_screen = title_screen.convert()
        picture_width, picture_height = title_screen.get_size()
        name_1 = ""
        name_2 = ""
        name_3 = ""
        name_4 = ""
        play: bool = True
        exit = -1
        while play:
            end_signal = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        play = False
                        exit = -2
            self.main_screen.fill(pygame.Color("white"))
            self.main_screen.blit(title_screen,
                                  (self.width / 2 - picture_width / 2, self.height / 2 - picture_height / 2))
            text_continue = text_format("Write your names & press Enter to continue", 30, black)
            text_continue_rect = text_continue.get_rect()
            self.main_screen.blit(text_continue, (self.width / 2 - (text_continue_rect[2] / 2), self.height / 2 + 300))

            text_player1 = input.Text_input_box(200, 40, self.width / 2, self.height / 2, screen=self.main_screen)
            text_player2 = input.Text_input_box(200, 40, self.width / 2, self.height / 2 + 70, screen=self.main_screen)
            text_player3 = input.Text_input_box(200, 40, self.width / 2, self.height / 2 + 140, screen=self.main_screen)
            text_player4 = input.Text_input_box(200, 40, self.width / 2, self.height / 2 + 210, screen=self.main_screen)

            pion1 = pygame.image.load(obt_path('board_game.pictures', 'PION1.png'))
            pion1_width, pion1_height = pion1.get_size()
            self.main_screen.blit(pion1,
                                  (self.width / 2 - 80 - pion1_width / 2, self.height / 2  - pion1_height / 2))

            pion2 = pygame.image.load(obt_path('board_game.pictures', 'PION2.png'))
            pion2_width, pion2_height = pion2.get_size()
            self.main_screen.blit(pion2,
                                  (self.width / 2 - 80 - pion2_width / 2, self.height / 2 + 70 - pion2_height / 2))

            if (nb_player >= 3):
                pion3 = pygame.image.load(obt_path('board_game.pictures', 'PION3.png'))
                pion3_width, pion3_height = pion3.get_size()
                self.main_screen.blit(pion3,
                                      (self.width / 2 - 80 - pion3_width / 2, self.height / 2 + 140 - pion3_height / 2))
            if (nb_player >= 4):
                pion4 = pygame.image.load(obt_path('board_game.pictures', 'PION4.png'))

                pion4_width, pion4_height = pion4.get_size()
                self.main_screen.blit(pion4,
                                      (self.width / 2 - 80 - pion4_width / 2, self.height / 2 + 210 - pion4_height / 2))
            if (nb_player >= 2 and name_1 == ""):
                name_1 = text_player1.show_box()
                name_2 = text_player2.show_box()
                if (nb_player == 2):
                    end_signal = True
            if (nb_player >= 3 and name_3 == ""):
                name_3 = text_player3.show_box()
                if (nb_player == 3):
                    end_signal = True

            if (nb_player >= 4 and name_4 == ""):
                name_4 = text_player4.show_box()
                end_signal = True

            if (end_signal):
                text_wait = text_format("Amazing, the game will start in 5 seconds...", 20, black)
                text_wait_rect = text_wait.get_rect()
                self.main_screen.blit(text_wait,
                                      (self.width / 2 - (text_wait_rect[2] / 2), self.height / 2 + 350))
                pygame.display.update()
                sleep(5)
                play = False
                exit = 0
            pygame.display.update()
        self.main_screen.fill(pygame.Color("white"))
        pygame.display.update()
        exit_var = [exit, name_1, name_2]
        if nb_player >= 3:
            exit_var.append(name_3)
        if nb_player >= 4:
            exit_var.append(name_4)
        return exit_var

    def begin_game(self):
        """Premi??re partie du programme graphique. Menu principal + choix du nombre de joueurs
            => return le nombre de player (int)"""
        exit_condition = self.run_main_menu()
        if exit_condition != -1:
            nb_players = self.run_choose_your_character()
            if nb_players != -1:
                exit_var = self.enter_player_names(nb_players)
                if exit_var[0] == -2:
                    return self.begin_game()
                return exit_var
            elif nb_players == 0:
                self.end_pygame()
                return ([-1])
            else:
                return self.begin_game()
        else:
            self.end_pygame()
            return ([-1])

    def create_game(self, game_var):
        self.main_screen.fill(pygame.Color("white"))
        pygame.display.update()
        self.nb_player = len(game_var) - 1
        self.game_board = Board()
        self.players = [0]
        for i in range(1, self.nb_player + 1):
            self.players.append(Player(i, game_var[i]))
        self.playing_status = game_var[0] + 1

    def run(self):
        if self.playing_status:
            self.id_current_player = random.randint(1, self.nb_player)
            nb_player_init = self.nb_player
            while (self.nb_player > 1):
                if (self.id_current_player > self.nb_player):
                    self.id_current_player = 1
                if (self.players[self.id_current_player].money() >= 0):
                    self.player_tour(self.players[self.id_current_player])
                    if (self.players[self.id_current_player].money() < 0):
                        self.nb_player -= 1
                self.id_current_player += 1
        for i in range(nb_player_init):
            if(self.players[i+1].money() >= 0):
                winner = self.players[i+1].name()
        self.end_game(winner)

    def find_player(self, player_name):
        """renvoie l'id du player de nom player_name, 0 s'il n'existe pas"""
        id_player = 0
        for i in range(1, len(self.players)):
            if self.players[i].name() == player_name:
                id_player = self.players[i].id()
        return id_player

    def exchange_properties(self, id_buyer, id_seller, value_exchange, id_property_buyer, id_property_seller):
        """??change les propri??t??s de deux joueurs, avec en plus une transaction value_exchange"""
        self.game_board.cases()[id_property_buyer].set_owner(id_seller)
        self.game_board.cases()[id_property_seller].set_owner(id_buyer)
        self.game_board.transaction(self.players[id_buyer], self.players[id_seller], value_exchange)

    def show_quit_panel(self, x_init, y_init):
        choosing = True
        selection_cursor = 0
        response = 0
        while choosing:
            pygame.draw.rect(self.main_screen, white, pygame.Rect(x_init, y_init, 500, 300))
            pygame.draw.rect(self.main_screen, black, pygame.Rect(x_init - 3, y_init -3, 506, 306), 3)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selection_cursor = ((selection_cursor - 1) % 2)
                    if event.key == pygame.K_RIGHT:
                        selection_cursor = ((selection_cursor + 1) % 2)
                    if event.key == pygame.K_RETURN:
                        if (selection_cursor == 0):
                            choosing = False
                            response = "continue"
                        elif (selection_cursor == 1):
                            choosing = False
                            response = "quit"
                        if event.key == pygame.K_ESCAPE:
                            choosing = False
                            response = "continue"
            if selection_cursor == 0:
                choice0 = text_format("Continue", 25, red)
                choice1 = text_format("Quit", 25, black)
            if selection_cursor == 1:
                choice0 = text_format("Continue", 25, black)
                choice1 = text_format("Quit", 25, red)
            rect_choice0 = choice0.get_rect()
            rect_choice1 = choice1.get_rect()
            rect_width = max(rect_choice0[2], rect_choice1[2])
            rect_height = max(rect_choice0[3], rect_choice1[3])
            quit_message = text_format("Do you want to quit ?", 30, red)
            rect_quit = quit_message.get_rect()
            self.main_screen.blit(quit_message, (x_init + 250 - rect_quit[2] // 2, y_init + 100))
            self.main_screen.blit(choice0, (x_init +150 - rect_width//2, y_init +200))
            self.main_screen.blit(choice1, (x_init +350 - rect_width//2, y_init + 200))
            pygame.display.update()
        if response == "quit":
            self.end_pygame()
        if response == "continue":
            return 0

    def print_player_info(self, player, main_player):
        if main_player:
            if(player.id() == 1):
                pion1 = pygame.image.load(obt_path('board_game.pictures', 'PION1.png'))
                picture_width, picture_height = pion1.get_size()
                self.main_screen.blit(pion1,
                                      (self.width  - 2 *picture_width , 5 * self.height // 100 - picture_height / 2))
            if (player.id() == 2):
                pion2 = pygame.image.load(obt_path('board_game.pictures', 'PION2.png'))
                picture_width, picture_height = pion2.get_size()
                self.main_screen.blit(pion2,
                                      (self.width - 2 * picture_width, 5 * self.height // 100 - picture_height / 2))
            if (player.id() == 3):
                pion3 = pygame.image.load(obt_path('board_game.pictures', 'PION3.png'))
                picture_width, picture_height = pion3.get_size()
                self.main_screen.blit(pion3,
                                      (self.width - 2 * picture_width, 5 * self.height // 100 - picture_height / 2))
            if (player.id() == 4):
                pion4 = pygame.image.load(obt_path('board_game.pictures', 'PION4.png'))
                picture_width, picture_height = pion4.get_size()
                self.main_screen.blit(pion4,
                                      (self.width - 2 * picture_width, 5 * self.height // 100 - picture_height / 2))
            self.main_screen.blit(text_format("It's " + player.name() + "'s turn!", 30, red),
                                  (self.size_board + 60, 5 * self.height // 100))
            self.main_screen.blit(
                text_format(player.name() + "'s bank account : " + str(player.money()) + " k???", 18, black),
                (self.size_board + 60, 10 * self.height // 100))

        property_player = self.game_board.list_property(player)
        if len(property_player) > 0:
            self.main_screen.blit(text_format(player.name() + "'s properties :", 18, black),
                                  (self.size_board + 60, 10 * self.height // 100 + 20))

        for i in range(1, len(property_player) + 1):
            if (property_player[i - 1].type() == "Property"):
                nb_houses = property_player[i - 1].nb_houses()
                if (nb_houses < 5):
                    self.main_screen.blit(text_format(
                        " " + str(i) + " - " + property_player[i - 1].name() + " - Number of houses : " + str(
                            nb_houses), 13, black), (self.size_board + 60,
                                                     10 * self.height // 100 + 15 + (i + 1) * 15))
                else:
                    self.main_screen.blit(
                        text_format(" " + str(i) + " - " + property_player[i - 1].name() + " - Number of hotels : 1",
                                    13, black),
                        (self.size_board + 60, 10 * self.height // 100 + 15+ (i + 1) * 15))
            else:
                self.main_screen.blit(text_format(" " + str(i) + " - " + property_player[i - 1].name(), 13, black), (
                self.size_board + 60, 10 * self.height // 100 + 15 + (i + 1) * 15))

        pygame.display.update()

    def clear_bottom_panel(self):
        clear_rectangle = pygame.Rect(self.size_board + 60, 75 * self.height // 100, self.width,
                                      25 * self.height // 100)
        pygame.draw.rect(self.main_screen, pygame.Color("white"), clear_rectangle)

    def clear_right_panel(self):
        clear_rectangle = pygame.Rect(self.size_board + 60, 0, self.width, 70 * self.height // 100)
        pygame.draw.rect(self.main_screen, pygame.Color("white"), clear_rectangle)

    def print_instruction(self,player,instruction_1, instruction_2,instruction_3,instruction_4, yes_no_choice):
        """affiche des instructions pour le joueur, ??ventuellement un choix, en bas de l'??cran ?? droite, on rend ensuite la r??ponse du joueur, 0 si pas de choix, -1 si quitte"""
        self.clear_bottom_panel()
        text_instruction_1 = text_format(instruction_1, 16, black)
        self.main_screen.blit(text_instruction_1, (self.size_board + 60, 75 * self.height // 100))

        if instruction_2 != None:
            text_instruction_2 = text_format(instruction_2, 16, black)
            self.main_screen.blit(text_instruction_2, (self.size_board + 60, 77 * self.height // 100))
        pygame.display.update()

        if instruction_3 != None:
            text_instruction_3 = text_format(instruction_3, 16, black)
            self.main_screen.blit(text_instruction_3, (self.size_board + 60, 79 * self.height // 100))
        pygame.display.update()

        if instruction_4 != None:
            text_instruction_4 = text_format(instruction_4, 16, black)
            self.main_screen.blit(text_instruction_4, (self.size_board + 60, 81 * self.height // 100))
        pygame.display.update()

        coef_yes_no = 77
        if (instruction_2 != None):
            coef_yes_no = 79
        if (instruction_3 != None):
            coef_yes_no = 81
        if (instruction_4 != None):
            coef_yes_no = 83

        choosing = (yes_no_choice != None)
        selection_cursor = 0
        response = 0
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selection_cursor = ((selection_cursor - 1) % 2)
                    if event.key == pygame.K_RIGHT:
                        selection_cursor = ((selection_cursor + 1) % 2)
                    if event.key == pygame.K_RETURN:
                        if (selection_cursor == 0):
                            choosing = False
                            response = yes_no_choice[0]
                        elif (selection_cursor == 1):
                            choosing = False
                            response = yes_no_choice[1]
                        if event.key == pygame.K_ESCAPE:
                            choosing = False
                            response = -1
            if selection_cursor == 0:
                choice0 = text_format(yes_no_choice[0], 25, red)
                choice1 = text_format(yes_no_choice[1], 25, black)
            if selection_cursor == 1:
                choice0 = text_format(yes_no_choice[0], 25, black)
                choice1 = text_format(yes_no_choice[1], 25, red)
            rect_choice0 = choice0.get_rect()
            rect_choice1 = choice1.get_rect()
            rect_width = max(rect_choice0[2],rect_choice1[2])
            rect_height = max(rect_choice0[3], rect_choice1[3])
            pygame.draw.rect(self.main_screen, white, pygame.Rect(self.size_board + 100 - rect_width//2
                                                                                  ,coef_yes_no * self.height // 100,self.width,rect_height))
            self.main_screen.blit(choice0, (self.size_board + 100, coef_yes_no * self.height // 100))
            self.main_screen.blit(choice1, (self.size_board + 100 + 200, coef_yes_no * self.height // 100))
            pygame.display.update()

        if yes_no_choice == None:
            self.wait_for_player(player)
        return response

    def refresh_page(self,player):
        self.main_screen.fill(white)
        self.game_board.show_board(self.main_screen, 10, self.height // 2 - self.size_board // 2, self.size_board,
                                   self.players, player.id())
        pygame.draw.rect(self.main_screen, black, pygame.Rect(self.size_board + 40, 20, 5, self.height - 40))
        pygame.draw.rect(self.main_screen, black,
                         pygame.Rect(self.size_board + 40, 70 * self.height // 100, self.width, 5))
        self.refresh_player_info(player)

    def refresh_player_info(self,player):
        self.clear_right_panel()
        pygame.draw.rect(self.main_screen, black, pygame.Rect(self.size_board + 40, 20, 5, self.height - 40))
        pygame.draw.rect(self.main_screen, black,
                         pygame.Rect(self.size_board + 40, 70 * self.height // 100, self.width, 5))
        self.print_player_info(player, True)

    def wait_for_player(self,player):
        """m??thode qui attend que le joueur appuie sur entrer pour continuer, rend False s'il quitte le jeu, True sinon"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing_status = False
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
                    if event.key == pygame.K_ESCAPE:
                        self.show_quit_panel(self.width // 2 - 250, self.height//2 - 150)
                        self.refresh_page(player)
                        return False

    def enter_response(self, text, condition = None):
        if text != None:
            self.clear_bottom_panel()
            instruction_text = text_format(text, 13, black)
            self.main_screen.blit(instruction_text, (self.size_board + 60, 75 * self.height / 100))
        if condition != None:
            response_text = input.Text_input_box(x_init= self.size_board + 100, y_init=89 * self.height / 100,
                                             screen=self.main_screen, validate=condition )
        else :
            response_text = input.Text_input_box(x_init=self.size_board + 100, y_init=89 * self.height / 100,
                                                 screen=self.main_screen)
        response = ""
        while response == "":
            pygame.draw.rect(self.main_screen, black, pygame.Rect(self.size_board + 100,89 * self.height / 100,40,20),1)
            response = response_text.show_box()
        return response

    def player_choice_menu(self):
        self.clear_bottom_panel()

        choice_text = text_format("Select the action you want to make :", 13, orange)
        self.main_screen.blit(choice_text, (self.size_board + 60, 75 * self.height // 100))
        choice_text = text_format(
            "1 - Display information about one of your properties", 13,
            black)
        self.main_screen.blit(choice_text, (self.size_board + 60, 77 * self.height // 100))
        choice_text = text_format("2 - Build a house", 13, black)
        self.main_screen.blit(choice_text, (self.size_board + 60, 79 * self.height // 100))
        choice_text = text_format("3 - Sell a house", 13, black)
        self.main_screen.blit(choice_text, (self.size_board + 60, 81 * self.height // 100))
        choice_text = text_format("4 - Display information about the properties of another player", 13, black)
        self.main_screen.blit(choice_text, (self.size_board + 60, 83 * self.height // 100))
        choice_text = text_format("5 - Make an offer to another player", 13, black)
        self.main_screen.blit(choice_text, (self.size_board + 60, 85 * self.height // 100))
        choice_text = text_format("6 - End your turn", 13, black)
        self.main_screen.blit(choice_text, (self.size_board + 60, 87 * self.height // 100))

        pygame.display.update()
        answer = self.enter_response(None)
        return answer

    def player_tour(self,player):
        self.main_screen.fill(white)
        self.game_board.show_board(self.main_screen,10,self.height//2 - self.size_board//2,self.size_board,self.players,player.id())
        pygame.draw.rect(self.main_screen, black,pygame.Rect(self.size_board + 40, 20 , 5, self.height - 40))
        pygame.draw.rect(self.main_screen, black, pygame.Rect(self.size_board + 40, 70 * self.height // 100, self.width, 5))


        self.refresh_player_info(player)
        self.print_instruction(player,"Time for " + player.name() + " to play !", None,None,None,None)

        # Chargement des propri??t??s que poss??de le joueur qui joue son tour
        property_player = self.game_board.list_property(player)

        # b est un bool??en pour d??terminer si le joueur peut lancer les d??s pour avancer
        b = True
        ## Cas Prison ##

        if (player.free() == False):
            if (player.escape_card() > 0):
                self.print_instruction(player,"You have an escape card","You can leave the prison for free !",None, None, None)
                player.set_free(True)
                player.set_escape_card(player.escape_card() - 1)
            else:
                answer = self.print_instruction(player,
                    "You are imprisoned !","Do you want to roll the dices to try to exit the prison this round ?", None, None,
                    ["yes", "no"])
                if answer == "no":
                    b = self.game_board.cases()[player.position()].rounds_passed(player)
                elif answer == "yes":
                    self.print_instruction(player,"Press Enter to roll the dices", None, None,None, None)
                    dice_1 = random.randint(1, 6)
                    dice_2 = random.randint(1, 6)
                    self.print_instruction(player," You've got " + str(dice_1) + " and " + str(dice_2), None, None,None, None)

                    b = self.game_board.cases()[player.position()].trying_to_escape_prison(dice_1, dice_2, player, self.print_instruction)

        ## Cas possibilit?? d'avancer ##
        if b:
            self.print_instruction(player,"Press Enter to roll the dices", None, None,None, None)
            dice_1 = random.randint(1, 6)
            dice_2 = random.randint(1, 6)
            dice_result = dice_1 + dice_2
            self.print_instruction(player,"You've got " + str(dice_1) + "+" + str(dice_2), None, None,None, None)
            if (player.position() + dice_result > self.game_board.nb_spaces()):
                player.set_money(player.money() + 200)
                self.print_instruction(player,"You passed the Start ! You receive 200??? !", None, None,None, None)
            if (player.position() + dice_result == self.game_board.nb_spaces()):
                player.set_money(player.money() + 400)
                self.print_instruction(player,"You're exactly at the Start ! You receive 400??? !", None, None,None, None)
            player.set_position((player.position() + dice_result) % self.game_board.nb_spaces())

            self.game_board.show_board(self.main_screen,10,self.height//2 - self.size_board//2,self.size_board,self.players,player.id())

            ## Cas d??part ##
            if (self.game_board.cases()[player.position()].type() == "Start"):
                self.print_instruction(player,"You are at the start !!", None, None,None, None)

            ## Cas Parc Gratuit ##
            elif (self.game_board.cases()[player.position()].type() == "Free Park"):
                self.print_instruction(player,"You are at the free park !!", None, None,None, None)

            ## Cas Simple visite en Prison ##
            elif (self.game_board.cases()[player.position()].type() == "Prison"):
                self.print_instruction(player,"You are just visiting the prison", None, None,None, None)

            ## Cas Allez En Prison ##
            elif (self.game_board.cases()[player.position()].type() == "Go to Prison"):
                self.print_instruction(player,"How unlucky... You're imprisonned...", None, None,None, None)
                self.game_board.cases()[player.position()].imprison(player)

            ## Cas Chance ##
            elif (self.game_board.cases()[player.position()].type() == "Luck"):
                self.print_instruction(player,"You're now on a Chance square !", None, None,None, None)
                self.game_board.cases()[player.position()].action(player, self.print_instruction)

            ## Cas Taxes ##
            elif (self.game_board.cases()[player.position()].type() == "Taxes"):
                self.print_instruction(player,"Oh no ! You fell on a taxes square !",
                                       "You have to pay taxes... It costs " + str(
                                           self.game_board.cases()[player.position()].value()) + "???", None,None,None)
                self.game_board.cases()[player.position()].pay(player)

            ## Cas Compagnies, Gares et Propri??t??s ##
            if (self.game_board.cases()[player.position()].type() in ["Company", "Train Station", "Property"]):
                welcome_text = "You're now on " + self.game_board.cases()[player.position()].name() + "."
                if (self.game_board.is_owned(player.position()) == player.id()):
                    welcome_text += "Welcome Home !!!"
                elif self.game_board.is_owned(player.position()) is not None:
                    id_of_owner = self.game_board.is_owned(player.position())
                    welcome_text += " You must pay a tax to player " + self.players[id_of_owner].name() + "!"

                    ## Cas Compagnie ##
                    if (self.game_board.cases()[player.position()].type() == "Company"):
                        if (self.game_board.is_owned(12) == self.game_board.is_owned(28)):
                            self.print_instruction(player,welcome_text,
                                                   "The rent is 10 times the sum of the value on the dices.", None,None,None)
                            self.game_board.transaction(player, self.players[id_of_owner], 10 * dice_result)
                        else:
                            self.print_instruction(player,welcome_text,
                                                   "The rent is 4 times the sum of the value on the dices.", None,None, None)
                            self.game_board.transaction(player, self.players[id_of_owner], 4 * dice_result)

                    ## Cas Gare ##
                    elif (self.game_board.cases()[player.position()].type() == "Train Station"):
                        nb_train_stations_owned = 0
                        for i in range(5, 36, 10):
                            if (self.game_board.is_owned(i) == id_of_owner):
                                nb_train_stations_owned += 1
                        self.print_instruction(player,welcome_text, "It costs " + str(
                            self.game_board.cases()[player.position()].rent(nb_train_stations_owned)) + "k???", None, None, None)
                        self.game_board.transaction(player, self.players[id_of_owner],
                                                    self.game_board.cases()[player.position()].rent(
                                                        nb_train_stations_owned))

                    ## Cas Propri??t?? ##
                    else:
                        self.print_instruction(player,welcome_text, "It costs " + str(
                            self.game_board.cases()[player.position()].rent()) + "k???", None, None, None)
                        self.game_board.transaction(player, self.players[id_of_owner],
                                                    self.game_board.cases()[player.position()].rent())
                else:
                    if (self.game_board.cases()[player.position()].value() > player.money()):
                        self.print_instruction(player,welcome_text,"Free Space ! It costs " + str(
                        self.game_board.cases()[player.position()].value()) + "k???", "You don't have enough money to buy the property.", None,None)
                    else:
                        answer = self.print_instruction(player,welcome_text,"Free Space ! It costs " + str(
                        self.game_board.cases()[player.position()].value()) + "k???","Do you want to buy it ?", None, ["yes", "no"])
                        if answer == "yes":
                            self.game_board.buy_property(player)
                            property_player=self.game_board.list_property(player)
                        else:
                            pass

                while (player.money() < 0 and len(property_player) > 0):
                    answer = self.print_instruction(player,
                        "You don't have enough money.","Would you like to sell a house or a property?", None,None,
                        ["house", "property"])
                    if (answer == "house"):
                        id_property = int(self.enter_response(
                            "On which house would you like to sell a house? Enter it's number in the recap"))
                        if (id_property < 1 or id_property > len(property_player) or property_player[
                            id_property - 1].type() != "Property"):
                            self.print_instruction(player,"The number you entered is invalid", None, None, None, None)
                        else:
                            if (self.game_board.cases()[property_player[id_property - 1].id()].nb_houses() == 0):
                                self.print_instruction(player,"You do not have a house in this property",None,None, None, None)
                            else:
                                price_house = self.game_board.cases()[
                                    property_player[id_property - 1].id()].price_houses()
                                former_nb_houses = self.game_board.cases()[
                                    property_player[id_property - 1].id()].nb_houses()
                                self.game_board.cases()[property_player[id_property - 1].id()].set_nb_houses(
                                    former_nb_houses - 1)
                                player.set_money(player.money() + price_house)
                                self.print_instruction(player,"You earned " + str(price_house) + "???", None, None, None, None)
                    elif (answer == "property"):
                        id_property = int(self.enter_response("Which property ? Enter the id displayed above :"))
                        if (id_property < 1 or id_property > len(property_player)):
                            self.print_instruction(player,"The number you entered is invalid", None, None, None, None)
                        else:
                            self.game_board.sell_property(player, property_player[id_property - 1].id(), self.print_instruction)

                if (player.money() < 0):
                    self.print_instruction(player,"You just lost the game!", None, None, None, None)

                self.refresh_player_info(player)

                if (len(property_player) > 0):
                    ## Actions joueur ##
                    try :
                        answer = int(self.player_choice_menu())
                    except :
                        answer = 6
                    while answer != 6:
                        ## Affichage informations ##
                        if (answer == 1):
                            id_property = int(
                                self.enter_response("On which property would you like to have information ?"))
                            if (id_property < 1 or id_property > len(property_player) or (property_player[
                                id_property - 1].type() != "Property" or property_player[
                                id_property - 1].type() != "Company" or property_player[
                                id_property - 1].type() != "TrainStation")):
                                self.print_instruction(player,"The number you have entered is invalid",None, None, None, None)
                            else:
                                property_player[id_property - 1].show_case(10 + self.size_board // 2 - 150, self.height / 2 - 170,
                                                                           self.main_screen)

                        ## Construction maison ##
                        elif answer == 2:
                            id_property = int(self.enter_response(
                                "On which property do you want to build a house ? Enter the id diplayed in the recap above :"))
                            if (id_property < 1 or id_property > len(property_player) or property_player[
                                id_property - 1].type() != "Property"):
                                self.print_instruction(player,"The number you have entered is invalid",None, None, None, None)
                            else:
                                ids_monopole = self.game_board.ids_same_monopole(
                                    property_player[id_property - 1].monopole_id())
                                size_monopole = len(ids_monopole)
                                if (size_monopole == 2):
                                    if (self.game_board.is_owned(ids_monopole[0]) == self.game_board.is_owned(
                                            ids_monopole[1])):
                                        price_house = self.game_board.cases()[
                                            property_player[id_property - 1].id()].price_houses()
                                        if (player.money() < price_house):
                                            self.print_instruction(player,"You don't have enough money to build a house",None,None, None,
                                                                   None)
                                        else:
                                            former_nb_houses = self.game_board.cases()[
                                                property_player[id_property - 1].id()].nb_houses()
                                            self.game_board.cases()[
                                                property_player[id_property - 1].id()].set_nb_houses(
                                                former_nb_houses + 1)
                                            player.set_money(player.money() - price_house)
                                            self.print_instruction(player,
                                                "You have built a house on " + self.game_board.cases()[
                                                    property_player[id_property - 1].id()].name(), None, None, None, None)

                                    else:
                                        self.print_instruction(player,"You have to own the whole monopole to build a house",
                                                               None,
                                                               None, None, None)
                                else:
                                    if self.game_board.is_owned(ids_monopole[0]) == self.game_board.is_owned(
                                            ids_monopole[1]) and self.game_board.is_owned(
                                        ids_monopole[1]) == self.game_board.is_owned(ids_monopole[2]):
                                        price_house = self.game_board.cases()[
                                            property_player[id_property - 1].id()].price_houses()
                                        if player.money() < price_house:
                                            self.print_instruction(player,"You don't have enough money to build a house", None,
                                                                   None, None, None)
                                        else:
                                            former_nb_houses = self.game_board.cases()[
                                                property_player[id_property - 1].id()].nb_houses()
                                            self.game_board.cases()[
                                                property_player[id_property - 1].id()].set_nb_houses(
                                                former_nb_houses + 1)
                                            player.set_money(player.money() - price_house)
                                            self.print_instruction(player,
                                                "You have built a house on " + self.game_board.cases()[
                                                    property_player[id_property - 1].id()].name(), None, None,None,None)
                                    else:
                                        self.print_instruction(player,"You have to own the whole monopole to build a house",
                                                               None,
                                                               None, None, None)

                        ## Vente maison ##
                        elif answer == 3:
                            id_property = int(self.enter_response(
                                "On which property do you want to sell a house ? Enter the id diplayed in the recap :"))
                            if (id_property < 1 or id_property > len(property_player) or property_player[
                                id_property - 1].type() != "Property"):
                                self.print_instruction(player,"The number you have entered is invalid", None, None, None, None)
                            else:
                                if (self.game_board.cases()[property_player[id_property - 1].id()].nb_houses() == 0):
                                    self.print_instruction(player,"You don't have any houses on this property", None, None, None, None)
                                else:
                                    price_house = self.game_board.cases()[
                                        property_player[id_property - 1].id()].price_houses()
                                    former_nb_houses = self.game_board.cases()[
                                        property_player[id_property - 1].id()].nb_houses()
                                    self.game_board.cases()[property_player[id_property - 1].id()].set_nb_houses(
                                        former_nb_houses - 1)
                                    player.set_money(player.money() + price_house)
                                    self.print_instruction(player,"You  have earned " + str(price_house) + "???", None, None, None, None)

                        ## Affichage informations propri??t??s autre joueur ##
                        elif answer == 4:
                            player_name = self.enter_response(
                                "Write the name of the player whose property you want to see:")
                            id_player = self.find_player(player_name)
                            if (id_player == 0):
                                self.print_instruction(player,"The player you entered does not exist", None, None, None, None)
                            else:
                                seller_properties = self.game_board.list_property(self.players[id_player])
                                if (len(seller_properties) == 0):
                                    self.print_instruction(player,"The player you chose does not have any property", None,
                                                           None, None, None)
                                else:
                                    self.clear_right_panel()
                                    self.print_player_info(self.players[id_player], False)
                                    answer2 = ""
                                    while (answer2 != "no"):
                                        answer2 = self.print_instruction(player,
                                            "Do you want to display information about one of those properties?","(Does not work for train stations or companies)",
                                            None,None, ["yes", "no"])
                                        if answer2 == "yes":
                                            id_property = int(
                                                self.enter_response("Which property ? Enter the id diplayed before :"))
                                            if (id_property < 1 or id_property > len(seller_properties) or
                                                    seller_properties[
                                                        id_property - 1].type() != "Property"):
                                                self.print_instruction(player,"The number you entered is invalid", None, None, None, None)
                                            else:
                                                seller_properties[id_property - 1].show_case(self.height / 2 - 150,
                                                                                             self.height / 2 - 170,
                                                                                             self.main_screen)

                        elif answer == 5:
                            player_name = self.enter_response(
                                "Write the name of the player to whom you want to make an offer :")
                            id_seller = self.find_player(player_name)
                            if id_seller == 0:
                                self.print_instruction(player,"The player you entered does not exist", None, None, None, None)
                            else:
                                seller_properties = self.game_board.list_property(self.players[id_seller])
                                if len(seller_properties) == 0:
                                    self.print_instruction(player,"This player you chose does not have any property", None,
                                                           None, None, None)
                                else:
                                    self.clear_right_panel()
                                    self.print_player_info(self.players[id_seller], False)
                                    id_seller_property = int(self.enter_response(
                                        "Which property belonging to the other player do you want ? Enter the id diplayed in their recap above :"))
                                    if id_seller_property < 1 or id_seller_property > len(seller_properties):
                                        self.print_instruction(player,"The number you entered is invalid", None, None, None, None)
                                    elif seller_properties[id_seller_property -1].type() == "Property" and self.game_board.houses_on_monopole(
                                            seller_properties[id_seller_property - 1].id()) > 0:
                                        self.print_instruction(player,
                                            "You can't buy a house in a monopole where some houses are built", None,
                                            None, None, None)
                                    else:
                                        self.clear_right_panel()
                                        self.print_player_info(player, True)
                                        id_buyer_property = int(self.enter_response(
                                            "Which property do you offer ? Enter the id diplayed in your recap above :"))
                                        if id_buyer_property < 1 or id_buyer_property > len(property_player):
                                            self.print_instruction(player,"The number you entered is invalid", None, None, None, None)
                                        elif (property_player[id_buyer_property -1].type()=="Property" and self.game_board.houses_on_monopole(
                                                property_player[id_buyer_property - 1].id()) > 0):
                                            self.print_instruction(player,
                                                "You can't sell a house in a monopole where some houses are built",
                                                None, None, None, None)
                                        else:
                                            price_offer = int(
                                                self.enter_response("How much do you offer for the exchange ?"))
                                            if (player.money() < price_offer):
                                                self.print_instruction(player,
                                                    "You don't have enough money to make such an offer",
                                                    None, None, None, None)
                                            elif (self.players[id_seller].money() < -price_offer):
                                                self.print_instruction(player,
                                                    str(self.players[id_seller].name()) + " doesn't have enough money", "to accept such an offer",
                                                    None, None, None)
                                            else:
                                                answer2 = self.print_instruction(player,
                                                    self.players[id_seller].name() + ", do you accept to exchange ",
                                                    seller_properties[id_seller_property - 1].name() + " with " +
                                                    property_player[id_buyer_property - 1].name(),  " for " + str(
                                                        price_offer) + "????", None, ["yes", "no"])
                                                if answer2 == "yes":
                                                    self.exchange_properties(player.id(), id_seller, price_offer,
                                                                             property_player[
                                                                                 id_buyer_property - 1].id(),
                                                                             seller_properties[
                                                                                 id_seller_property - 1].id())
                                                    property_player = self.game_board.list_property(player)
                                                    self.print_instruction(player,"The exchange took place!", None, None,None,None)
                                                elif answer2 == "no":
                                                    self.print_instruction(player,"The offer was refused", None, None, None, None)
                                                else:
                                                    self.print_instruction(player,"You entered an incorrect answer", None,
                                                                           None,None,None)
                        else:
                            self.print_instruction(player,"You entered an incorrect answer", None, None, None, None)
                        if answer != 6:
                            self.refresh_player_info(player)
                            self.game_board.cases()[player.position()].show_case(10 + self.size_board // 2 - 150, self.height / 2 - 170, self.main_screen)
                            try :
                                answer = int(self.player_choice_menu())
                            except:
                                answer = 6

        self.refresh_player_info(player)
        self.print_instruction(player,"This is the end of your turn", "Here is a brief recap of your situation", " ", "Press enter to continue", None)

    def end_game(self, winning_player):
        end_screen = pygame.image.load(obt_path('board_game.pictures', 'end_screen.jpg'))
        end_screen = end_screen.convert()
        picture_rect = end_screen.get_rect()
        play = (winning_player != -1)
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        play = False

            self.main_screen.fill(pygame.Color("white"))
            self.main_screen.blit(end_screen,
                                  (self.width / 2 - picture_rect[2] / 2, self.height / 2 - picture_rect[3] / 2))
            text_winner = text_format("Player " + str(winning_player) + " wins!", 50, black)
            text_winner_rect = text_winner.get_rect()
            text_continue = text_format("Press Enter to close", 50, black)
            text_continue_rect = text_continue.get_rect()
            self.main_screen.blit(text_winner, (self.width / 2 - (text_winner_rect[2] / 2), self.height / 2 + 200))
            self.main_screen.blit(text_continue, (self.width / 2 - (text_continue_rect[2] / 2), self.height / 2 + 300))
            pygame.display.update()
        self.end_pygame()

    def end_pygame(self):
        self.main_screen = 0
        self.width, self.height = 0,0
        self.game_var = 0
        pygame.quit()
        exit()

if __name__ == '__main__':
    new_game = Game()
    new_game.run()
