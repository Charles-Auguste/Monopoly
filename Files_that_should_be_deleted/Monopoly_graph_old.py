from monopoly.player import *
from monopoly.propriete import *
from monopoly.board import Board, miniBoard, mini_bijection, read_properties
import random
import pygame
from monopoly import text_input as input
from monopoly.text_input import text_format
from time import sleep
from pygame.locals import *
from PIL import Image

pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

class Game:
    def __init__(self, debug):
        """Initialise le board et les joueurs"""
        self.debug = debug
        
        self.main_screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.width, self.height  = self.main_screen.get_size()
        self.resize_factor = (1,1)
        self.playing_status = (self.run_main_menu() != -1) #booleen qui vaut True si on est en train de jouer le jeu, False sinon (il faut alors tout fermer, etc...)
        
        if self.playing_status:
            self.nb_player = self.run_choose_your_character()
            self.playing_status = self.nb_player > 0

        if self.playing_status:
            self.nb_player_in_game = self.nb_player
            self.id_current_player = 0
        
            game_var = self.enter_player_names(self.nb_player)
            self.players = [0]
            for i in range(1, self.nb_player + 1):
                self.players.append(Player(i, game_var[i]))
                self.game_board = Board()

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
        play = True
        selection_cursor = 0
        self.nb_player = -1
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
                player2 = text_format("2 players", 30,red)
                player3 = text_format("3 players", 30, black)
                player4 = text_format("4 players", 30, black)
            if selection_cursor == 1:
                player2 = text_format("2 players", 30,black)
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
    
    def enter_player_names(self, nb_player):
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
        play = True
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
                                  (self.width / 2 - 80 - pion1_width / 2, self.height / 2   - pion1_height / 2))

            pion2 = pygame.image.load('pictures/PION2.png')
            pion2_width, pion2_height = pion2.get_size()
            self.main_screen.blit(pion2,
                                  (self.width / 2 - 80 - pion2_width / 2, self.height / 2 + 70 - pion2_height / 2))

            if (nb_player >= 3):
                pion3 = pygame.image.load('pictures/PION3.png')
                pion3_width, pion3_height = pion3.get_size()
                self.main_screen.blit(pion3,
                                      (self.width / 2 - 80 - pion3_width / 2, self.height / 2 + 140 - pion3_height / 2))
            if (nb_player >= 4):
                pion4 = pygame.image.load('pictures/PION4.png')

                pion4_width, pion4_height = pion4.get_size()
                self.main_screen.blit(pion4,
                                      (self.width / 2 - 80 - pion4_width / 2, self.height / 2 + 210 - pion4_height / 2))
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
                #sleep(5)
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
    
    def run(self):
        if self.playing_status:
            self.id_current_player = random.randint(1, self.nb_player)
            while(self.nb_player_in_game > 1):
                if (self.id_current_player > self.nb_player):
                    self.id_current_player = 1
                if(self.players[self.id_current_player].money() > 0):
                    self.player_tour(self.players[self.id_current_player])
                    if(self.players[self.id_current_player].money() < 0):
                        self.nb_player_in_game -= 1
                self.id_current_player += 1

        self.end_game(self.debug)

    def find_player(self, player_name):
        """renvoie l'id du player de nom player_name, 0 s'il n'existe pas"""
        id_player = 0
        for i in range(1, len(self.players)):
            if self.players[i].name() == player_name:
                id_player = self.players[i].id()
        return id_player

    def exchange_properties(self, id_buyer, id_seller, value_exchange, id_property_buyer, id_property_seller):
        """échange les propriétés de deux joueurs, avec en plus une transaction value_exchange"""
        self.game_board.cases()[id_property_buyer].set_owner(id_seller)
        self.game_board.cases()[id_property_seller].set_owner(id_buyer)
        self.game_board.transaction(self.players[id_buyer], self.players[id_seller], value_exchange)

    def display_properties(self,property_player):
        for i in range(1,len(property_player)+1):
            if (property_player[i-1].type()=="Property"):
                nb_houses = property_player[i - 1].nb_houses()
                if (nb_houses < 5):
                    print(" ", i, " - ", property_player[i - 1].name(), " - Number of houses : ",
                          nb_houses, "\n")
                else:
                    print(" ", i, " - ", property_player[i - 1].name(), " - Number of hotel : ",
                          1, "\n")
            else:
                print(" ", i, " - ", property_player[i - 1].name(), "\n")

    def print_player_info(self, player, main_player):
        if main_player:
            self.main_screen.blit(text_format("It's " + player.name() + "'s turn!", 20, black), (self.height + 10, self.height//20))
            self.main_screen.blit(text_format(player.name() + "'s bank account : " + str(player.money()) + " €", 13, black),(self.height + 10, self.height//10))
        
        property_player = self.game_board.list_property(player)        
        if len(property_player) > 0:
            self.main_screen.blit(text_format(player.name() + "'s properties :", 13, black), (self.height + 10, self.height//10 + 12))
        
        for i in range(1,len(property_player)+1):
            if (property_player[i-1].type()=="Property"):
                nb_houses = property_player[i - 1].nb_houses()
                if (nb_houses < 5):
                    self.main_screen.blit(text_format(" " + str(i) + " - " + property_player[i - 1].name() + " - Number of houses : " + str(nb_houses), 13, black), (self.height + 10, self.height//10 + (i+1)*12))
                else:
                    self.main_screen.blit(text_format(" " + str(i) + " - " + property_player[i - 1].name() + " - Number of hotels : 1", 13, black), (self.height + 10, self.height//10 + (i+1)*12))
            else:
                self.main_screen.blit(text_format(" " + str(i) + " - " + property_player[i - 1].name(), 13, black),  (self.height + 10, self.height//10 + (i+1)*12))

        pygame.display.update()

    def clear_bottom_panel(self):
        clear_rectangle = pygame.Rect(self.height + 10, 75*self.height//100, self.width - (self.height + 10), 25*self.height//100)
        pygame.draw.rect(self.main_screen, pygame.Color("white"), clear_rectangle)
    
    def clear_right_panel(self):
        clear_rectangle = pygame.Rect(self.height + 10, 0, self.width - (self.height + 10), 70*self.height//100)
        pygame.draw.rect(self.main_screen, pygame.Color("white"), clear_rectangle)

    def print_instruction(self, instruction_1, instruction_2, yes_no_choice):
        """affiche des instructions pour le joueur, éventuellement un choix, en bas de l'écran à droite, on rend ensuite la réponse du joueur, 0 si pas de choix, -1 si quitte"""
        self.clear_bottom_panel()
        text_instruction_1 = text_format(instruction_1, 13, black)
        self.main_screen.blit(text_instruction_1, (self.height + 10, 75*self.height//100))

        if instruction_2 != None:
            text_instruction_2 = text_format(instruction_2, 13, black)
            self.main_screen.blit(text_instruction_2, (self.height + 10, 77*self.height//100))
        pygame.display.update()

        chosing = (yes_no_choice != None)
        selection_cursor = 0
        response = 0
        while chosing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selection_cursor = ((selection_cursor-1) % 2)
                    if event.key == pygame.K_RIGHT:
                        selection_cursor = ((selection_cursor+1) % 2)
                    if event.key == pygame.K_RETURN:
                        if(selection_cursor == 0):
                            chosing = False
                            response = yes_no_choice[0]
                        elif (selection_cursor == 1):
                            chosing = False
                            response = yes_no_choice[1]
                        if event.key == pygame.K_ESCAPE:
                            chosing = False 
                            response = -1
            if selection_cursor == 0:
                choice0 = text_format(yes_no_choice[0], 13, red)
                choice1 = text_format(yes_no_choice[1], 13, black)
            if selection_cursor == 1:
                choice0 = text_format(yes_no_choice[0], 13, black)
                choice1 = text_format(yes_no_choice[1], 13, red)

            self.main_screen.blit(choice0, (self.height + 10, 77*self.height//100))
            self.main_screen.blit(choice1, (27*self.width//40, 77*self.height//100))
            pygame.display.update()

        if yes_no_choice == None:
            self.wait_for_player()
        return response

    def wait_for_player(self):
        """méthode qui attend que le joueur appuie sur entrer pour continuer, rend False s'il quitte le jeu, True sinon"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing_status = False
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
                    if event.key == pygame.K_ESCAPE:
                        self.playing_status = False
                        return False

    def enter_response(self, text):
        if text != None:
            self.clear_bottom_panel()
            instruction_text = text_format(text, 13, black)
            self.main_screen.blit(instruction_text, (self.height + 10, 75*self.height/100))
        response_text = input.Text_input_box(200,40,self.height + 10, 89*self.height/100, screen=self.main_screen)
        response = ""
        while response == "":
            response = response_text.show_box()
        return response

    def player_choice_menu(self):
        self.clear_bottom_panel()

        choice_text = text_format("Select the action you want to make :", 13, black)
        self.main_screen.blit(choice_text, (self.height + 10, 75*self.height//100))
        choice_text = text_format("1 - Display information about one of your properties (Does not work for train stations or companies)", 13, black)
        self.main_screen.blit(choice_text, (self.height + 10, 77*self.height//100))
        choice_text = text_format("2 - Build a house", 13, black)
        self.main_screen.blit(choice_text, (self.height + 10, 79*self.height//100))
        choice_text = text_format("3 - Sell a house", 13, black)
        self.main_screen.blit(choice_text, (self.height + 10, 81*self.height//100))
        choice_text = text_format("4 - Display information about the properties of another player", 13, black)
        self.main_screen.blit(choice_text, (self.height + 10, 83*self.height//100))
        choice_text = text_format("5 - Make an offer to another player", 13, black)
        self.main_screen.blit(choice_text, (self.height + 10, 85*self.height//100))
        choice_text = text_format("6 - End your turn", 13, black)
        self.main_screen.blit(choice_text, (self.height + 10, 87*self.height//100))
        
        pygame.display.update()
        answer = self.enter_response(None)
        return answer

    def player_tour(self, player):
        """Un tour de jeu pour un joueur player"""
        
        board_background_image = Image.open('pictures/board.png')
    
        if (self.width, self.height) != board_background_image.size:
            board_background_image = board_background_image.resize((self.width, self.height))
            board_background_image.save('pictures/board_resized.png')
            board_background = pygame.image.load('pictures/board_resized.png')
            self.resize_factor = (self.width/board_background_image.size[0], self.height/board_background_image.size[1])
        else:   
            board_background = pygame.image.load('pictures/board.png')

        self.main_screen.fill(pygame.Color("white"))
        self.main_screen.blit(board_background,(0,0))
        self.game_board.cases()[player.position()].show_case(self.height/2 - 150, self.height/2 - 170, self.main_screen)
        for i in range(1, self.nb_player + 1):
            self.players[i].show_player(self.main_screen, self.height, self.resize_factor)
        pygame.display.update()

        self.print_player_info(player, True)
        self.print_instruction("Time for " + player.name() + " to play !", None, None)


        # Chargement des propriétés que possède le joueur qui joue son tour
        property_player = self.game_board.list_property(player)

        ## b est un booléen pour déterminer si le joueur peut lancer les dés pour avancer
        b = True
        ## Cas Prison ##

        if (player.free() == False):
            if (player.escape_card() > 0):
                self.print_instruction("You have an escape card, you can leave the prison for free.", None, None)
                player.set_free(True)
                player.set_escape_card(player.escape_card() - 1)
            else:
                answer = self.print_instruction("You are imprisonned. Do you want to roll the dices to try to exit the prison this round ?", None, ["yes","no"])
                if answer == "no":
                    b = self.game_board.cases()[player.position()].rounds_passed(player, self.print_instruction)
                elif answer == "yes":
                    self.print_instruction("Press Enter to roll the dices", None, None)
                    dice_1 = random.randint(1, 6)
                    dice_2 = random.randint(1, 6)
                    self.print_instruction(" You've got " + str(dice_1) + " and " + str(dice_2), None, None)

                    b = self.game_board.cases()[player.position()].trying_to_escape_prison(dice_1, dice_2, player, self.print_instruction)

        ## Cas possibilité d'avancer ##
        if b:
            self.print_instruction("Press Enter to roll the dices", None, None)
            if (self.debug):
                dice_result = 1
            else:
                dice_1 = random.randint(1, 6)
                dice_2 = random.randint(1, 6)
                dice_result = dice_1 + dice_2
                self.print_instruction("You've got " + str(dice_1) + "+" + str(dice_2), None, None)
            if (player.position() + dice_result > self.game_board.nb_spaces()):
                player.set_money(player.money() + 200)
                self.print_instruction("You passed the Start ! You receive 200€ !", None, None)
            if (player.position() + dice_result == self.game_board.nb_spaces()):
                player.set_money(player.money() + 400)
                self.print_instruction("You're exactly at the Start ! You receive 400€ !", None, None)
            player.set_position((player.position() + dice_result) % self.game_board.nb_spaces())

            self.main_screen.fill(pygame.Color("white"))
            self.main_screen.blit(board_background,(0,0))
            self.game_board.cases()[player.position()].show_case(self.height/2 - 150, self.height/2 - 170, self.main_screen)
            self.print_player_info(player, True)
            for i in range(1, self.nb_player +1):
                self.players[i].show_player(self.main_screen, self.height, self.resize_factor)
            pygame.display.update()

            ## Cas départ ##
            if (self.game_board.cases()[player.position()].type() == "Start"):
                self.print_instruction("You are at the start !!", None, None)

            ## Cas Parc Gratuit ##
            elif (self.game_board.cases()[player.position()].type() == "Free Park"):
                self.print_instruction("You are at the free park !!", None, None)

            ## Cas Simple visite en Prison ##
            elif (self.game_board.cases()[player.position()].type() == "Prison"):
                self.print_instruction("You are just visiting the prison", None, None)

            ## Cas Allez En Prison ##
            elif (self.game_board.cases()[player.position()].type() == "Go to Prison"):
                self.print_instruction("How unlucky... You're imprisonned...", None, None)
                self.game_board.cases()[player.position()].imprison(player)

            ## Cas Chance ##
            elif (self.game_board.cases()[player.position()].type() == "Luck"):
                self.print_instruction("You're now on a Chance square !", None, None)
                self.game_board.cases()[player.position()].action(player, self.print_instruction)

            ## Cas Taxes ##
            elif (self.game_board.cases()[player.position()].type() == "Taxes"):
                self.print_instruction("Oh no ! You fell on a taxes square !", "You have to pay taxes... It costs " + str(self.game_board.cases()[player.position()].value()) + "€", None)
                self.game_board.cases()[player.position()].pay(player)

            ## Cas Compagnies, Gares et Propriétés ##
            if (self.game_board.cases()[player.position()].type() in ["Company", "Train Station", "Property"]):
                welcome_text = "You're now on " + self.game_board.cases()[player.position()].name() + "."
                if (self.game_board.is_owned(player.position()) == player.id()):
                    welcome_text += "Welcome Home !!!"
                elif self.game_board.is_owned(player.position()) is not None:
                    id_of_owner = self.game_board.is_owned(player.position())
                    welcome_text += " You must pay a tax to player " + str(id_of_owner) + "!"

                    ## Cas Compagnie ##
                    if (self.game_board.cases()[player.position()].type() == "Company"):
                        if (self.game_board.is_owned(12) == self.game_board.is_owned(28)):
                            self.print_instruction(welcome_text, "The rent is 10 times the sum of the value on the dices.", None)
                            self.game_board.transaction(player, self.players[id_of_owner], 10 * dice_result)
                        else:
                            self.print_instruction(welcome_text, "The rent is 4 times the sum of the value on the dices.", None)
                            self.game_board.transaction(player, self.players[id_of_owner], 4 * dice_result)

                    ## Cas Gare ##
                    elif (self.game_board.cases()[player.position()].type() == "Train Station"):
                        nb_train_stations_owned = 0
                        for i in range(5, 36, 10):
                            if (self.game_board.is_owned(i) == id_of_owner):
                                nb_train_stations_owned += 1
                        self.print_instruction(welcome_text, "It costs " + str(self.game_board.cases()[player.position()].rent(nb_train_stations_owned)) + "€", None)
                        self.game_board.transaction(player, self.players[id_of_owner], self.game_board.cases()[player.position()].rent(nb_train_stations_owned))

                    ## Cas Propriété ##
                    else:
                        self.print_instruction(welcome_text, "It costs " + str(self.game_board.cases()[player.position()].rent()) + "€", None)
                        self.game_board.transaction(player, self.players[id_of_owner], self.game_board.cases()[player.position()].rent())
                else:
                    welcome_text += ". Free Space ! It costs " + str(self.game_board.cases()[player.position()].value()) + "€"
                    if (self.game_board.cases()[player.position()].value() > player.money()):
                        self.print_instruction(welcome_text, "You don't have enough money to buy the property.", None)
                    else:
                        welcome_text += ". Do you want to buy it ?"
                        answer = self.print_instruction(welcome_text, None, ["yes","no"])
                        if answer == "yes":
                            self.game_board.buy_property(player)
                        else:
                            pass


        while (player.money() < 0 and len(property_player) > 0):
            answer = self.print_instruction("You don't have enough money. Would you like to sell a house or a property?", None, ["house","property"])
            if (answer == "house"):
                id_property = int(self.enter_response("On which house would you like to sell a house? Enter it's number in the recap"))
                if (id_property < 1 or id_property > len(property_player) or property_player[id_property - 1].type() != "Property"):
                    self.print_instruction("The number you entered is invalid", None, None)
                else:
                    if (self.game_board.cases()[property_player[id_property - 1].id()].nb_houses() == 0):
                        self.print_instruction("You do not have a house in this property", None, None)
                    else:
                        price_house = self.game_board.cases()[property_player[id_property - 1].id()].price_houses()
                        former_nb_houses = self.game_board.cases()[property_player[id_property - 1].id()].nb_houses()
                        self.game_board.cases()[property_player[id_property - 1].id()].set_nb_houses(former_nb_houses - 1)
                        player.set_money(player.money() + price_house)
                        self.print_instruction("You earned " + str(price_house) + "€", None, None)
            elif (answer == "property"):
                id_property = int(self.enter_response("Which property ? Enter the id displayed above :"))
                if (id_property < 1 or id_property > len(property_player)):
                    self.print_instruction("The number you entered is invalid", None, None)
                else:
                    self.game_board.sell_property(player, property_player[id_property - 1].id())

        if(player.money() < 0):
            self.print_instruction("You just lost the game!", None, None)

        if(len(property_player) > 0):
            ## Actions joueur ##
            self.main_screen.fill(pygame.Color("white"))
            self.main_screen.blit(board_background,(0,0))
            self.game_board.cases()[player.position()].show_case(self.height/2 - 150, self.height/2 - 170, self.main_screen)
            for i in range(1, self.nb_player + 1):
                self.players[i].show_player(self.main_screen, self.height, self.resize_factor)
            pygame.display.update()

            self.print_player_info(player, True)
            answer = int(self.player_choice_menu())
            while answer != 6:
                ## Affichage informations ##
                if (answer == 1):
                    self.display_properties(property_player)
                    id_property = int(self.enter_response("On which property would you like to have information ?"))
                    if (id_property < 1 or id_property > len(property_player) or property_player[id_property - 1].type() != "Property"):
                        self.print_instruction("The number you have entered is invalid", None, None)
                    else:
                        property_player[id_property - 1].show_case(self.height/2 - 150, self.height/2 - 170, self.main_screen)

                ## Construction maison ##
                elif answer == 2:
                    id_property = int(self.enter_response("On which property do you want to build a house ? Enter the id diplayed in the recap above :"))
                    if (id_property < 1 or id_property > len(property_player) or property_player[id_property - 1].type() != "Property"):
                        self.print_instruction("The number you have entered is invalid", None, None)
                    else:
                        ids_monopole = self.game_board.ids_same_monopole(property_player[id_property - 1].monopole_id())
                        size_monopole = len(ids_monopole)
                        if (size_monopole == 2):
                            if (self.game_board.is_owned(ids_monopole[0]) == self.game_board.is_owned(ids_monopole[1])):
                                price_house = self.game_board.cases()[property_player[id_property - 1].id()].price_houses()
                                if (player.money() < price_house):
                                    self.print_instruction("You don't have enough money to build a house", None, None)
                                else:
                                    former_nb_houses = self.game_board.cases()[property_player[id_property - 1].id()].nb_houses()
                                    self.game_board.cases()[property_player[id_property - 1].id()].set_nb_houses(former_nb_houses + 1)
                                    player.set_money(player.money() - price_house)
                                    self.print_instruction("You have built a house on " + self.game_board.cases()[property_player[id_property - 1].id()].name(), None, None)

                            else:
                                self.print_instruction("You have to own the whole monopole to build a house", None, None)
                        else:
                            if self.game_board.is_owned(ids_monopole[0]) == self.game_board.is_owned(ids_monopole[1]) and self.game_board.is_owned(ids_monopole[1]) == self.game_board.is_owned(ids_monopole[2]):
                                price_house = self.game_board.cases()[property_player[id_property - 1].id()].price_houses()
                                if player.money() < price_house:
                                    self.print_instruction("You don't have enough money to build a house", None, None)
                                else:
                                    former_nb_houses = self.game_board.cases()[property_player[id_property - 1].id()].nb_houses()
                                    self.game_board.cases()[property_player[id_property - 1].id()].set_nb_houses(former_nb_houses + 1)
                                    player.set_money(player.money() - price_house)
                                    self.print_instruction("You have built a house on " + self.game_board.cases()[property_player[id_property - 1].id()].name(), None, None)
                            else:
                                self.print_instruction("You have to own the whole monopole to build a house", None, None)

                ## Vente maison ##
                elif answer == 3:
                    id_property = int(self.enter_response("On which property do you want to sell a house ? Enter the id diplayed in the recap :"))
                    if (id_property < 1 or id_property > len(property_player) or property_player[id_property - 1].type() != "Property"):
                        self.print_instruction("The number you have entered is invalid", None, None)
                    else:
                        if (self.game_board.cases()[property_player[id_property - 1].id()].nb_houses() == 0):
                            self.print_instruction("You don't have any houses on this property", None, None)
                        else:
                            price_house = self.game_board.cases()[property_player[id_property - 1].id()].price_houses()
                            former_nb_houses = self.game_board.cases()[property_player[id_property - 1].id()].nb_houses()
                            self.game_board.cases()[property_player[id_property - 1].id()].set_nb_houses(former_nb_houses - 1)
                            player.set_money(player.money() + price_house)
                            self.print_instruction("You  have earned " + str(price_house) + "€", None, None)

                ## Affichage informations propriétés autre joueur ##
                elif answer == 4:
                    player_name = self.enter_response("Write the name of the player whose property you want to see:")
                    id_player = self.find_player(player_name)
                    if (id_player == 0):
                        self.print_instruction("The player you entered does not exist", None, None)
                    else:
                        seller_properties = self.game_board.list_property(self.players[id_player])
                        if (len(seller_properties) == 0):
                            self.print_instruction("The player you chose does not have any property", None, None)
                        else:
                            self.clear_right_panel()
                            self.print_player_info(self.players[id_player], False)
                            answer2 = ""
                            while (answer2 != "no"):
                                answer2 = self.print_instruction("Do you want to display information about one of those properties? (Does not work for train stations or companies)", None, ["yes","no"])
                                if answer2 == "yes":
                                    id_property = int(self.enter_response("Which property ? Enter the id diplayed before :"))
                                    if (id_property < 1 or id_property > len(seller_properties) or seller_properties[id_property - 1].type() != "Property"):
                                        self.print_instruction("The number you entered is invalid", None, None)
                                    else:
                                        seller_properties[id_property - 1].show_case(self.height/2 - 150, self.height/2 - 170, self.main_screen)
                elif answer == 5:
                    player_name = self.enter_response("Write the name of the player to whom you want to make an offer :")
                    id_seller = self.find_player(player_name)
                    if id_seller == 0:
                        self.print_instruction("The player you entered does not exist", None, None)
                    else:
                        seller_properties = self.game_board.list_property(self.players[id_seller])
                        if len(seller_properties) == 0:
                            self.print_instruction("This player you chose does not have any property", None, None)
                        else:
                            self.clear_right_panel()
                            self.print_player_info(self.players[id_seller], False)
                            id_seller_property = int(self.enter_response("Which property belonging to the other player do you want ? Enter the id diplayed in their recap above :"))
                            if id_seller_property < 1 or id_seller_property > len(seller_properties):
                                self.print_instruction("The number you entered is invalid", None, None)
                            elif self.game_board.cases()[seller_properties[id_seller_property - 1].id()].type() == "Property" and self.game_board.houses_on_monopole(seller_properties[id_seller_property - 1].id()) > 0:
                                self.print_instruction("You can't buy a house in a monopole where some houses are built", None, None)
                            else:
                                id_buyer_property = int(self.enter_response("Which property do you offer ? Enter the id diplayed in your recap above :"))
                                self.clear_right_panel()
                                self.print_player_info(player, True)
                                if id_buyer_property < 1 or id_buyer_property > len(property_player):
                                    self.print_instruction("The number you entered is invalid", None, None)
                                elif (self.game_board.houses_on_monopole(property_player[id_seller_property - 1].id()) > 0):
                                    self.print_instruction("You can't sell a house in a monopole where some houses are built", None, None)
                                else:
                                    price_offer = int(self.enter_response("How much do you offer for the exchange ?"))
                                    if (player.money() < price_offer):
                                        self.print_instruction("You don't have enough money to make such an offer", None, None)
                                    else:
                                        answer2 = self.print_instruction(self.players[id_seller].name() + ", do you accept to exchange " + seller_properties[id_seller_property - 1].name() + " with " + property_player[id_buyer_property - 1].name() + " for " + str(price_offer) + "€?", None, ["yes","no"])
                                        if answer2 == "yes":
                                            self.exchange_properties(player.id(), id_seller, price_offer, property_player[id_buyer_property - 1].id(), seller_properties[id_seller_property - 1].id())
                                            property_player = self.game_board.list_property(player)
                                            self.print_instruction("The exchange took place!", None, None)
                                        elif answer2 == "no":
                                            self.print_instruction("The offer was refused", None, None)
                                        else:
                                            self.print_instruction("You entered an incorrect answer", None, None)
                else:
                    self.print_instruction("You entered an incorrect answer", None, None)
                if answer != 6:
                    answer = int(self.player_choice_menu())

        self.print_instruction("This is the end of your turn", None, None)

    def end_game(self, debug):
        """The last method of the Game. It shows the winner and ends the game"""
        if debug:
            aff.clear_console()
            print(aff.manette_char)
            print("\n \n \n #### END OF DEBUG SESSION #### \n \n \n")

if __name__ == '__main__':
    new_game = Game(False)
    new_game.run()