# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 22:09:19 2019

@author: squas
"""
from treys import Card
from treys import Evaluator
from treys import Deck
from time import sleep as wait_for_decision
from pdb import set_trace as breakp

class MyBot:
    def call(self,filepath):
        return "Call"
    
    def raise_(self,filepath):
        return "Raise"
    
    def fold(self,filepath):
        return "Fold"
            
    def start_game(self,bot,game_stage):
        self.play(bot,game_stage)
        
    def play(self,bot,stage,hand=[],board=[],showdown=False):
        if stage==0:
            bot.set_hand(hand)
            # Make Decision
            self.call()
            '''Neural Network Calculation'''
            '''Decision r,c,f'''       
        if stage==1:
            bot.update_board(board)
            # Make Decision
            self.call()
            '''Neural Network Calculation'''
            '''Decision r,c,f'''
            
        if stage==2:
            bot.update_board(board)
            # Make Decision
            self.call()
            '''Neural Network Calculation'''
            '''Decision r,c,f'''
            
        if stage==3:
            bot.update_board(board)
            # Make Decision
            self.call()
            '''Neural Network Calculation'''
            '''Decision r,c,f'''
        if stage==4:
            '''Neural Network Calculation'''
            '''Decision r,c,f'''
