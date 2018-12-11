# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 10:58:24 2018

@author: squas
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 01:18:11 2018

@author: squas
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 23:13:16 2018

@author: squas
"""
from treys import Card
from treys import Evaluator
from treys import Deck
'''ExpectedValue=TotalValuexProbability'''
#Sample Hand Value

class Bot:
    def __init__(self):
        self.hand=[]
        self.board=[]
        #self.position=0
        #self.hand_number=0
        #self.dealer=False
        self.seat=0
        self.win_prob=0.00
        self.investment=0
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

#Given More Information, better calc for EV
#def AllinExpectedValue(AllIn_Loses, AllIn_Winnings, Fold_Winnings, Fold_Percent, Equity):
 #   FoldEV = (Fold_Percent * Fold_Winnings)
  #  AllinEV = (1 - Fold_Percent) * ((AllIn_Winnings * Equity) + (AllIn_Loses * (1 - Equity)))
   # AllinExpectedValue = FoldEV + AllinEV
    #if AllinExpectedValue > 0:
     #   return 'Raise!', AllinExpectedValue
    #else:
    #    return 'Fold!', AllinExpectedValue

def CalculateWinProb(hand,board):
    hand_rank=evaluator.evaluate(board,hand)
    return ((7462-hand_rank)/7462)

def MakeDecision(bot,prob):
    pot_raise=0
    if prob<=0.6 and prob>0.3:
        print("Bot-"+bot.seat+"-Raise")
        print(bot.seat+"-WinProb:"+str(prob))
        pot_raise+=pot-bot.investment
        bot.investment+=pot-bot.investment
    elif prob<=0.3:
        print("Bot-"+bot.seat+"-Raise")
        print(bot.seat+"-WinProb:"+str(prob))
        pot_raise+=(pot-bot.investment)+100
        bot.investment+=(pot-bot.investment)+100
    else:
        print("Bot-"+bot.seat+"-Fold")
        print(bot.seat+"-WinProb:"+str(prob))
        pot_raise+=0
    return pot_raise

def GoToShowdown(player_1,player_2):
    if evaluator.evaluate(player_1.board,player_1.hand) == evaluator.evaluate(player_2.board,player_2.hand):
        print("Draw")
    elif evaluator.evaluate(player_1.board,player_1.hand) < evaluator.evaluate(player_2.board,player_2.hand):
        print("Player 1 Wins")
    else:
        print("Player 2 Wins")
    print(Card.print_pretty_cards(player_1.board+player_1.hand))
    print("Player 1 hand rank = %d (%s)\n" % (evaluator.evaluate(player_1.board,player_1.hand), evaluator.class_to_string(evaluator.get_rank_class(evaluator.evaluate(player_1.board,player_1.hand)))))
    print(Card.print_pretty_cards(player_2.board+player_2.hand))
    print("Player 2 hand rank = %d (%s)\n" % (evaluator.evaluate(player_2.board,player_2.hand), evaluator.class_to_string(evaluator.get_rank_class(evaluator.evaluate(player_2.board,player_2.hand)))))

def play_game(bot1,bot2,pot):
    stage=0
    while stage<5:
        if stage==0: #Call on Preflop--Change when preflop statistics is found
            print("Preflop")
            print("---------------")
            print()
            bot1.seat="1"
            bot2.seat="2"
            bot1.hand=deck.draw(2)
            bot2.hand=deck.draw(2)
            print("Bot 1-Call")
            print("Bot 2-Call")
            pot=200
            print("Pot:" +str(pot))
            print()
            stage+=1
        if stage==1:
            #Simulate Casino Flop
            print("Flop")
            print("---------------")
            print()
            flop=deck.draw(3)
            for i in flop:
                bot1.add_board(i)
                bot2.add_board(i)
            bot1_prob=CalculateWinProb(bot1.hand,bot1.board)
            bot2_prob=CalculateWinProb(bot2.hand,bot2.board)
            pot+=MakeDecision(bot1,bot1_prob)
            pot+=MakeDecision(bot2,bot2_prob)
            print("Pot:" +str(pot))
            print()
            stage+=1
        if stage==2:
            #Simulate Casino Turn
            print("Turn")
            print("---------------")
            print()
            turn=deck.draw(1)
            bot1.add_board(turn)
            bot2.add_board(turn)
            bot1_prob=CalculateWinProb(bot1.hand,bot1.board)
            bot2_prob=CalculateWinProb(bot2.hand,bot2.board)
            pot+=MakeDecision(bot1,bot1_prob)
            pot+=MakeDecision(bot2,bot2_prob)
            print("Pot:" +str(pot))
            print()
            stage+=1
        if stage==3:
            #Simulate Casino River
            print("River")
            print("---------------")
            river=deck.draw(1)
            bot1.add_board(river)
            bot2.add_board(river)
            bot1_prob=CalculateWinProb(bot1.hand,bot1.board)
            bot2_prob=CalculateWinProb(bot2.hand,bot2.board)
            pot+=MakeDecision(bot1,bot1_prob)
            pot+=MakeDecision(bot2,bot2_prob)
            print("Pot:" +str(pot))
            print()
            stage+=1
        if stage==4:
            #Call Or Raise Expected Value-Don't fold
            print("Post")
            print("---------------")
            print()
            bot1_prob=CalculateWinProb(bot1.hand,bot1.board)
            bot2_prob=CalculateWinProb(bot2.hand,bot2.board)
            pot+=MakeDecision(bot1,bot1_prob)
            pot+=MakeDecision(bot2,bot2_prob)
            print("Pot:" +str(pot))
            print()
            print("Showdown")
            print("---------------")
            print()
            GoToShowdown(bot1,bot2)
            stage+=1
        
big_blind=100
pot=0
player_1=Bot()
player_2=Bot()
evaluator=Evaluator()
deck=Deck()
play_game(player_1,player_2,pot)
print(CalculateWinProb(player_1.hand,player_1.board))