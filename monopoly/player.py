"""
player.py
Author : TDLOG group A
Date : 24/01/2022
Comments : fully functional (18/01/2022)
"""

# Standard library
import pygame

pygame.init()

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


