# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 23:13:16 2018

@author: squas
"""

from treys import Card
from pdb import set_trace as breakp
from holdem_calc_2 import calculate


class StatisticalBot:
    def __init__(self):
        self.hand=[]
        self.board=[]
        self.seat=0
        self.win_prob=0.00
        self.investment=0
        self.exp_val=0.00
        #Opponents Fold Percentage
        self.villain_fold_percent=0.1 #0.0 #0.25
        self.villain_fold_decisions=0
        self.stage=0
        self.stack=0.0
        self.hand_number=0
        #For use by holdem calc ---> don't need to be changed for the functionality of holdem_calc used
        self.dealer=False
        self.VERBOSE = False
        self.INPUT_FILE = None
        self.EXACT = True
        self.NUM_SIMULATIONS = 1
    def add_cards(self,cards):
        self.hand=cards
    def add_board(self, cards):
        self.board=cards
    def set_position(self,char_index):
        self.position=char_index
    def update_stage(self,stage):
        self.stage=stage
    def update_hand_number(self,number):
        self.hand_number=number
    def set_seat(self,seat):
        self.seat=seat
    # '?' represents hidden hole cards --> simulations run for all possible cards to come to the table 
    def CalculateWinProb(self,hand,board):
        hand_string= [Card.int_to_str(card) for card in hand]
        hand_string.append("?")
        hand_string.append("?")
        equity=calculate([Card.int_to_str(card) for card in board], self.EXACT, self.NUM_SIMULATIONS, self.INPUT_FILE, hand_string, self.VERBOSE)[1] 
        return equity
    def AllinExpectedValue(self,AllIn_Loses, AllIn_Winnings, Fold_Winnings, Fold_Percent,Equity,stage,pot):
        cards_left={0:5,1:2,2:1,3:0}
        
        #Fold Expected Value
        FoldEV = (Fold_Percent * Fold_Winnings)
        #AllIn 
        AllinEV = (1 - Fold_Percent) * ((AllIn_Winnings * Equity) + (AllIn_Loses * (1 - Equity)))
        #Final Expected Value
        AllinExpectedValue = FoldEV + AllinEV 
        
        if AllinExpectedValue > 0:
            return 'r', AllinExpectedValue
        else:
            if (FoldEV + AllinEV) * -(1/(cards_left[0]-cards_left[stage])) > 1.5*pot: #tolerance level for raises --> Aggressive Play to adjust for chance of good cards to be drawn
                AllinExpectedValue = (FoldEV + AllinEV) * -(1/(cards_left[0]-cards_left[stage]))
                return 'r', AllinExpectedValue
            elif (FoldEV + AllinEV) * -(1/(cards_left[0]-cards_left[stage])) > 0.5 * pot:
                AllinExpectedValue = (FoldEV + AllinEV) * -(1/(cards_left[0]-cards_left[stage]))
                return 'c', AllinExpectedValue
            return 'f', AllinExpectedValue
    def AllInLoses(self,pot):
        return -self.stack
    def AllInWinnings(self,pot,bet_size):
        return (self.stack - bet_size) + pot
    def FoldWinnings(self,pot):
        return pot
    def FoldPercent(self,fold_decision,games_left=100):
        return self.villain_fold_percent
    
    #Takes in a fold_decision -> -1 if opponent calls, 1 if opponent fails, and the number of games left
    def UpdateFoldPercent(self,fold_decision,games_left=100):
        #Prevents Divide by Zero arithmetic error
        if games_left == 0 : games_left = 1
        #Depending on the number of games left, the villains fold percent is increased or decreased if fold_decision == -1
        #By dividing in games_left, large adjustments are made for a small number of games, with more slight adjustments taking place over a large simulation
        self.villain_fold_percent = (fold_decision/games_left) + self.villain_fold_percent 
        #Keeps fold percent within bounds of 0 and 1
        if self.villain_fold_percent>1.0:self.villain_fold_percent = 1.0
        if self.villain_fold_percent<0.0:self.villain_fold_percent = 0.0

    def ResetFoldPercent(self,fold_percent):
        self.villain_fold_percent = fold_percent
    def MakeDecision(self,pot,stage,bet_size):
        if stage==0:
            self.investment+=bet_size
            return "c"
        if len(self.board) == 0:
            return 'c'
        all_in_loses=self.AllInLoses(pot)
        all_in_wins=self.AllInWinnings(pot,bet_size)
        fold_winnings=self.FoldWinnings(pot)
        fold_percent=self.FoldPercent(0,games_left=1)
        equity=self.CalculateWinProb(self.hand,self.board)
        decision,exp_val=self.AllinExpectedValue(all_in_loses,all_in_wins,fold_winnings,fold_percent,equity,stage,pot)
        return decision
    def Game_Over(self,i_won,player_fold,games_left):
        if player_fold:
            if i_won:
                self.UpdateFoldPercent(1,games_left)
            else:
                self.UpdateFoldPercent(-1,games_left)
        else:
            self.UpdateFoldPercent(-1,games_left)
        return






