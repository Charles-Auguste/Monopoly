import pygame

pygame.init()

position_possible = [(21, 21),(19, 21),(17, 21),(15, 21),(13, 21),(11, 21),(9, 21),(7, 21),(5, 21),(3, 21),(1, 21),(1, 19),(1, 17),(1, 15),(1, 13),(1, 11),(1, 9),(1, 7),(1, 5),(1, 3),(1, 1),(3, 1),(5, 1),(7,1),(9,1),(11,1),(13,1),(15,1),(17,1),(19,1),(21,1),(21, 3),(21, 5),(21, 7),(21, 9),(21, 11),(21, 13),(21, 15),(21, 17),(21, 19)]
pion1 = pygame.image.load('pictures/PION1.png')
pion1_width, pion1_height = pion1.get_size()
pion2 = pygame.image.load('pictures/PION2.png')
pion2_width, pion2_height = pion2.get_size()
pion3 = pygame.image.load('pictures/PION3.png')
pion3_width, pion3_height = pion3.get_size()
pion4 = pygame.image.load('pictures/PION4.png')
pion4_width, pion4_height = pion4.get_size()


class Player:
    _id : int
    _money : int
    _position : int
    _free : bool
    _escape_card : int
    _round_in_prison : int
    _player_name : str
    
    def __init__(self, id_num=0, player_name="#", money=1500, position=0,free=True,escape=0,round_in_prison=0):
        self._id = id_num
        self._player_name=player_name
        self._money = money
        self._position = position
        self._free=free
        self._escape_card=escape
        self._round_in_prison=round_in_prison
        
    def position(self):
        return self._position

    def id(self):
        return self._id

    def name(self):
        return self._player_name

    def money(self):
        return self._money

    def free(self):
        return self._free

    def escape_card(self):
        return self._escape_card

    def round_in_prison(self):
        return self._round_in_prison

    def set_money(self, money):
        self._money = money

    def set_position(self, pos):
        self._position = pos

    def set_free(self,free):
        self._free = free

    def set_escape_card(self,card):
        self._escape_card = card

    def set_round_in_prison(self,round_prison):
        self._round_in_prison = round_prison

    def show_player(self, screen, height):
        if self.id() == 1:
            screen.blit(pion1, (position_possible[self.position()][0]*height//22 - pion1_width//2, position_possible[self.position()][1]*height//22 - pion1_height//2))
        elif self.id() == 2:
            screen.blit(pion2, (position_possible[self.position()][0]*height//22 - pion2_width//2, position_possible[self.position()][1]*height//22 - pion2_height//2))
        elif self.id() == 3:
            screen.blit(pion3, (position_possible[self.position()][0]*height//22 - pion3_width//2, position_possible[self.position()][1]*height//22 - pion3_height//2))
        elif self.id() == 4:
            screen.blit(pion4, (position_possible[self.position()][0]*height//22 - pion4_width//2, position_possible[self.position()][1]*height//22 - pion4_height//2))
