# -*- coding: utf-8 -*-

import random

class Bot:
    #Self.X stores bot type --> 'c' CALL, 'f' FOLD, 'r' RAISE , Mixture-> Random Decision Making
    def __init__(self):
        self.hand=[]
        self.board=[]
        self.position=0;
        self.stage=0
        self.hand_number=0
        self.dealer=False
        self.seat=0
        self.X = ''
    def add_cards(self,card):
        self.hand=card
    def add_board(self, card):
        self.board=card
    def set_position(self,char_index):
        self.position=char_index
    def update_stage(self,stage):
        self.stage=stage
    def update_hand_number(self,number):
        self.hand_number=number
    def set_seat(self,seat):
        self.seat=seat
    def MakeDecision(self,pot,stage,bet_size):
        #Works off given X type
        return random.choice(self.X)
    def Game_Over(self,i_won,player_fold,games_left):
        return