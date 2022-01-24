"""
propriete.py
Author : TDLOG group A
Date : 24/01/2022
Comments : fully functional (18/01/2022)
"""

# Standard library
import random

# Local source
from player import Player

class Case:
    _type: str
    _id: int

    def __init__(self,type="#",id=0):
        self._type = type
        self._id = id

    # === Accesseurs ===
    
    def id(self):
        return self._id

    def type(self):
        return self._type

    # Afficheur



class Property(Case):
    _name: str
    _id: int #Possiblement osef
    # Prix achat
    _value: int
    _owner: int
    _nb_houses: int
    _price_houses: int
    #Prix à payer si pas proprio
    _rent: list

    def __init__(self,name="#",id=0, monopole_id=0, value=0,owner=0,nb_houses=0,price_houses=0,rent=[0]*6, color = (50,50,50)):
        super().__init__("Property",id)
        self._name = name.replace("_"," ")
        self._monopole_id = monopole_id
        self._value = value
        self._owner = owner
        self._nb_houses = nb_houses
        self._price_houses = price_houses
        self._rent = rent
        self.color = color
        
    # ===   Accesseurs   ===
    def name(self):
        return self._name
    
    def monopole_id(self):
        return self._monopole_id

    def value(self):
        return self._value

    def owner(self):
        return self._owner

    def nb_houses(self):
        return self._nb_houses

    def price_houses(self):
        return self._price_houses

    def rent(self):
        return self._rent[self._nb_houses]

    def rent_graph(self,i):
        return self._rent[i]

    def set_owner(self,id):
        self._owner=id

    def set_nb_houses(self,n):
        self._nb_houses=n


class Luck(Case):
    def __init__(self,id):
        super().__init__("Luck",id)

    def action(self, player, print_instruction):
        n = random.randint(1,8)
        if (n==1):
            print_instruction(" Allez en prison. Allez tout droit à la prison. Ne passez pas par la case départ, ne reçevez pas 200€.", None, None, None, None)
            player.set_free(False)
            player.set_position(10)
        if (n==2):
            print_instruction(" Rendez-vous Rue de La Paix. Si vous passez par la case départ, recevez 200€.", None, None, None, None)
            if (player.position()>39):
                player.set_money(player.money()+200)
            player.set_position(39)
        if (n==3):
            print_instruction(" Rendez-vous Avenue Henri Martin. Si vous passez par la case départ, recevez 200€.", None, None, None, None)
            if(player.position()>24):
                player.set_money(player.money()+200)
            player.set_position(24)
        if (n==4):
            print_instruction(" Rendez-vous case Départ. Recevez 400€.", None, None, None, None)
            player.set_position(0)
            player.set_money(player.money()+400)
        if (n == 5):
            print_instruction(" La banque vous verse un dividende de 50€.", None, None, None, None)
            player.set_money(player.money()+50)
        if (n == 6):
            print_instruction(" Vous êtes libéré de prison. Cette carte peut être conservée jusqu'à ce qu'elle soit utilisée ou vendue.", None, None, None, None)
            player.set_escape_card(player.escape_card()+1)
        if (n == 7):
            print_instruction(" Amende pour excès de vitesse. Payez 50€.", None, None, None, None)
            player.set_money(player.money()-50)
        if (n == 8):
            print_instruction(" Amende pour ivresse. Payez 50€.", None, None, None, None)
            player.set_money(player.money()-50)


class GoToPrison(Case):
    def __init__(self):
        super().__init__("Go to Prison",30)

    def imprison(self,player : Player):
        player.set_position(10)
        player.set_free(False)


class Prison(Case):
    def __init__(self):
        super().__init__("Prison",10)

    def exit_prison(self, player):
        player.set_free(True)
        player.set_money(player.money()-50)
        player.set_round_in_prison(0)
        return True

    def rounds_passed(self, player, print_instruction):
        if (player.round_in_prison()==3):
            print_instruction(" You can exit the prison !", None, None, None, None)
            return self.exit_prison(player)
        else :
            print_instruction(" You can't exit the prison...", None, None, None, None)
            player.set_round_in_prison(player.round_in_prison()+1)
            return False

    def trying_to_escape_prison(self, dice_1, dice_2, player, print_instruction):
        if (dice_1==dice_2):
            print_instruction(" You can exit the prison ! But you have to pay 50€.", None, None, None, None)
            return self.exit_prison(player)
        else:
            return self.rounds_passed(player, print_instruction)


class Taxes(Case):
    def __init__(self, id=0, value=0):
        super().__init__("Taxes", id)
        self._value_tax = value

    def value(self):
        return self._value_tax

    def pay(self, player: Player):
        player.set_money(player.money()-self._value_tax)


class Company(Case):
    def __init__(self, id, name="#", owner=0):
        super().__init__("Company", id)
        self._value=100
        self._name=name
        self._owner=owner

    def value(self):
        return self._value

    def name(self):
        return self._name

    def owner(self):
        return self._owner

    def set_owner(self, id):
        self._owner = id


class TrainStation(Case):
    def __init__(self, name="#", id=0, owner = 0):
        super().__init__("Train Station", id)
        self._name = name
        self._value = 200
        self._owner = owner
        # On n'appellera jamais la case 0 de rent, on appellera la case en fonction du nombre de gares possédées par le joueur
        self._rent = [0,25,50,100,200]

    def name(self):
        return self._name

    def value(self):
        return self._value

    def owner(self):
        return self._owner

    def rent(self,i):
        return self._rent[i]

    def set_owner(self,id):
        self._owner=id

