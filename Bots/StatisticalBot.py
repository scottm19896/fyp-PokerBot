# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 21:58:03 2019

@author: squas
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 23:13:16 2018

@author: squas
"""

from treys import Evaluator
from pdb import set_trace as breakp
'''ExpectedValue=TotalValuexProbability'''
#Sample Hand Value

class StatisticalBot:
    def __init__(self):
        self.hand=[]
        self.board=[]
        self.seat=0
        self.win_prob=0.00
        self.investment=0
        self.exp_val=0.00
        self.position=0;
        self.stage=0
        self.hand_number=0
        self.dealer=False
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
    def CalculateWinProb(self,hand,board):
        hand_rank=Evaluator().evaluate(board,hand)
        return ((7462-hand_rank)/7462)
    def MakeDecision(self,pot,stage):
        if stage==0:
            return "c"
        exp_val=pot*self.CalculateWinProb(self.hand,self.board)
        if exp_val>=1.5*self.investment:
            self.investment+=(pot-self.investment)+100
            return "r"
        elif exp_val>=self.investment:
            self.investment+=pot-self.investment
            return "c"
        else:
            if stage<4:
                return "f"
            else:
                return "c"



#Given More Information, better calc for EV
#def AllinExpectedValue(AllIn_Loses, AllIn_Winnings, Fold_Winnings, Fold_Percent, Equity):
 #   FoldEV = (Fold_Percent * Fold_Winnings)
  #  AllinEV = (1 - Fold_Percent) * ((AllIn_Winnings * Equity) + (AllIn_Loses * (1 - Equity)))
   # AllinExpectedValue = FoldEV + AllinEV
    #if AllinExpectedValue > 0:
     #   return 'Raise!', AllinExpectedValue
    #else:
    #    return 'Fold!', AllinExpectedValue

#Hand is on scale 1->7462, 1=Royal Flush,
#7462 is number if distinctly ranked hands in poker


#Updated EV Example
#Hand1_AllIn_Loses = -20.95
#Hand1_AllIn_Winnings = 23
#Hand1_Fold_Winnings = 3.7
#Hand1_Fold_Percent = .25
#Hand1_Equity = .538
#Hand1_Decision, Hand1_EV = AllinExpectedValue(Hand1_AllIn_Loses, Hand1_AllIn_Winnings, Hand1_Fold_Winnings, Hand1_Fold_Percent, Hand1_Equity)
#print(Hand1_Decision)
#print(Hand1_EV)