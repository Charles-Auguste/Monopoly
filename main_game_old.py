import pygame
import text_input as input
from text_input import text_format
from time import sleep
from pygame.locals import *
from Monopoly_graph_old import read_properties, Board, Game_graph
import random
import time
from color import *

#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================


# INITIALISATION OF PYGAME          /!\ IMPORTANT
pygame.init()


# Text Renderer



# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


class Game_graphical():
    def __init__(self):
        self.main_screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.width, self.height  = self.main_screen.get_size()

    # BEGINNING OF THE GAME : MAIN MENU AND PLAYER SELECTION
    def run_main_menu(self):
        """Main menu of the game
        -> return 0 if new game
        -> return -1 if quit
        """
        play: bool = True
        selected = "start"
        game_on = True
        title_screen = pygame.image.load('pictures/title_screen.jpg')
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
                        if(selected == "start"):
                            play = False
                        elif(selected == "quit"):
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
            self.main_screen.blit(title_screen, (self.width/2 - picture_width/2, self.height/2 - picture_height/2))
            self.main_screen.blit(text_start,(self.width/2 - (start_rect[2]/2), self.height/2))
            self.main_screen.blit(text_quit,(self.width/2 - (quit_rect[2]/2), self.height/2 + 100))
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
        play : bool = True
        selection_cursor = 0
        nb_players = -1
        title_screen = pygame.image.load('pictures/title_screen.jpg')
        title_screen = title_screen.convert()
        picture_width, picture_height = title_screen.get_size()
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection_cursor = ((selection_cursor-1) % 3)
                    if event.key == pygame.K_DOWN:
                        selection_cursor = ((selection_cursor+1) % 3)
                    if event.key == pygame.K_RETURN:
                        if(selection_cursor == 0):
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
                player2 = text_format("2 players",30,red)
                player3 = text_format("3 players", 30, black)
                player4 = text_format("4 players", 30, black)
            if selection_cursor == 1:
                player2 = text_format("2 players",30,black)
                player3 = text_format("3 players", 30, red)
                player4 = text_format("4 players", 30, black)
            if selection_cursor == 2:
                player2 = text_format("2 players",30,black)
                player3 = text_format("3 players", 30, black)
                player4 = text_format("4 players", 30, red)
            player2_rect = player2.get_rect()
            player3_rect = player3.get_rect()
            player4_rect = player4.get_rect()
            self.main_screen.fill(pygame.Color("white"))
            self.main_screen.blit(title_screen, (self.width/2 - picture_width/2, self.height/2 - picture_height/2))
            self.main_screen.blit(player2,(self.width/2 - (player2_rect[2]/2), self.height/2))
            self.main_screen.blit(player3,(self.width/2 - (player3_rect[2]/2), self.height/2 + 100))
            self.main_screen.blit(player4,(self.width/2 - (player4_rect[2]/2), self.height/2+ 200))
            pygame.display.update()
        self.main_screen.fill(pygame.Color("white"))
        pygame.display.update()
        return nb_players

    def enter_player_names (self, nb_player):
        """
        :param nb_player: the number of player
        :return: -1 if exit, 0 if everything is ok
        """
        title_screen = pygame.image.load('pictures/title_screen.jpg')
        title_screen = title_screen.convert()
        picture_width, picture_height = title_screen.get_size()
        name_1 = ""
        name_2 = ""
        name_3 = ""
        name_4 = ""
        play : bool = True
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
            self.main_screen.blit(title_screen, (self.width/2 - picture_width/2, self.height/2 - picture_height/2))
            text_continue = text_format("Write your names & press Enter to continue", 30, black)
            text_continue_rect = text_continue.get_rect()
            self.main_screen.blit(text_continue,(self.width/2 - (text_continue_rect[2]/2), self.height/2 + 300))

            text_player1 = input.Text_input_box(200,40,self.width/2,self.height/2,screen=self.main_screen)
            text_player2 = input.Text_input_box(200,40,self.width/2,self.height/2 + 70,screen=self.main_screen)
            text_player3 = input.Text_input_box(200,40,self.width/2,self.height/2 + 140,screen=self.main_screen)
            text_player4 = input.Text_input_box(200,40,self.width/2,self.height/2 + 210,screen=self.main_screen)

            pion1 = pygame.image.load('pictures/PION1.png')
            pion1_width, pion1_height = pion1.get_size()
            self.main_screen.blit(pion1,
                                  (self.width / 2 - 80 - pion1_width / 2, self.height / 2  + 20 - pion1_height / 2))

            pion2 = pygame.image.load('pictures/PION2.png')
            pion2_width, pion2_height = pion2.get_size()
            self.main_screen.blit(pion2,
                                  (self.width / 2 - 80 - pion2_width / 2, self.height / 2 + 90 - pion2_height / 2))

            if (nb_player >= 3):
                pion3 = pygame.image.load('pictures/PION3.png')
                pion3_width, pion3_height = pion3.get_size()
                self.main_screen.blit(pion3,
                                      (self.width / 2 - 80 - pion3_width / 2, self.height / 2 + 160 - pion3_height / 2))
            if (nb_player >= 4):
                pion4 = pygame.image.load('pictures/PION4.png')

                pion4_width, pion4_height = pion4.get_size()
                self.main_screen.blit(pion4,
                                      (self.width / 2 - 80 - pion4_width / 2, self.height / 2 + 230 - pion4_height / 2))
            if (nb_player >= 2 and name_1 ==""):
                name_1 = text_player1.show_box()
                name_2 = text_player2.show_box()
                if(nb_player == 2):
                    end_signal = True
            if (nb_player >= 3 and name_3 == ""):
                name_3 = text_player3.show_box()
                if(nb_player == 3):
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
        """Première partie du programme graphique. Menu principal + choix du nombre de joueurs
            => return le nombre de player (int)"""
        exit_condition = self.run_main_menu()
        if exit_condition != -1:
            nb_players = game.run_choose_your_character()
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

    def create_game(self,game_var):
        self.main_screen.fill(pygame.Color("white"))
        pygame.display.update()
        main_game = Game_graph(game_var)
        main_game.term = input.Terminal(self.width//2 - 250,10, self.main_screen)
        main_game.screen = self.main_screen
        first_player_index = random.randint(1, len(game_var) - 1)
        return [main_game, first_player_index]

    # MAIN LOOP OF THE GAME

    def player_tour(self):
        pass

    # END OF THE GAME
    def end_game(self, winning_player):
        end_screen = pygame.image.load('pictures/end_screen.jpg')
        end_screen = end_screen.convert()
        play = (winning_player != -1)
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        play = False
            
            self.main_screen.fill(pygame.Color("white"))
            self.main_screen.blit(end_screen, (0, 0))
            text_winner = text_format("Player "+str(winning_player)+" wins!", 50, black)
            text_winner_rect = text_winner.get_rect()
            text_continue = text_format("Press Enter to close", 50, black)
            text_continue_rect = text_continue.get_rect()
            self.main_screen.blit(text_winner,(self.width/2 - (text_winner_rect[2]/2), self.height/2 + 200))
            self.main_screen.blit(text_continue,(self.width/2 - (text_continue_rect[2]/2), self.height/2 + 300))
            pygame.display.update()
        self.end_pygame()

    def end_pygame(self):
        pygame.quit()

#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================


def report_begin_game(g_var):
    print("DEBUG REPORT BEGIN GAME ------- MONOPOLY")
    print("========================================")
    print("Paramètres d'initialisation de la partie")
    print("Nombre de joueurs : ", len(g_var) - 1)
    print("Nom des joueurs :")
    for i in range(1, len(g_var)):
        print("-  ", g_var[i])
    print("========================================")




#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================


# TEST
game = Game_graphical()
game_var = game.begin_game()
report_begin_game(game_var)
main_game_system, id_first_player = game.create_game(game_var)
main_game_system.player_tour(main_game_system.players[1])
time.sleep(3)
game.end_pygame()
