# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 22:33:26 2019

@author: squas
"""
import random

class Bot:
    def __init__(self):
        self.hand=[]
        self.board=[]
        self.position=0;
        self.stage=0
        self.hand_number=0
        self.dealer=False
        self.seat=0
    def add_card(self,card):
        self.hand.append(card)
    def add_board(self, card):
        self.board.append(card)
    def set_position(self,char_index):
        self.position=char_index
    def update_stage(self,stage):
        self.stage=stage
    def update_hand_number(self,number):
        self.hand_number=number
    def set_seat(self,seat):
        self.seat=seat
    def MakeDecision(self):
        return random.choice('cr')