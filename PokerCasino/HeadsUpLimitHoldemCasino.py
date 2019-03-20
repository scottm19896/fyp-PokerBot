# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 23:15:28 2018

@author: squas
"""

from treys import Card
from treys import Evaluator
from treys import Deck
from time import sleep as wait_for_decision
from pdb import set_trace as breakp
from BotX import Bot as Bot_1
from BotY import Bot as Bot_2

PRIVATE_FILE_NAMES=["Player_1_To_Casino.txt.txt","Player_2_To_Casino.txt.txt"]


'''Class to Represent a seat at the poker table --> Keep track of player details'''
class SeatAtTable: 
    def __init__(self,player,buy_in,seat_no,name):
        self.player=player
        self.stack=buy_in
        self.cards=[]
        self.seat_no=seat_no
        self.name= name
        self.has_raised=False
        self.round_betting=0
        self.CALL=2
    def __str__(self):
        return str(self.name)
    
'''Class to Represent the poker table --> Keep track of all active players'''
class Table:
    def __init__(self):
        self.members=[]
        self.pot=0
        self.is_full=False
        self.dealer_position=0
        self.big_blind=2.00
        self.small_blind=1.00
        
    def __str__(self):
        return "Members:"+str([str(member) for member in self.members])+"\nPot:"+str(self.pot)+"\nBB:"+str(self.big_blind) 
    
    def BuyIn(self,players,buy_in_amount):
        if len(players)>2: #Can Be Changed to add more players to table
            self.is_full=True
        if not self.is_full:
            name_of_player=1
            for i in players:
                self.members.append(SeatAtTable(i,buy_in_amount,len(self.members),("Player "+str(name_of_player))))
                name_of_player+=1
            
'''Class to Represent a poker game --> Keep track of game progress'''
class Game:
    def __init__(self):
        self.current_table=Table()
        self.evaluator=Evaluator()
        self.board=[]
    
    def Call(self,seat,opp):
            seat.CALL = opp.round_betting-seat.round_betting
            if seat.CALL <= 0 : seat.CALL= 2
            self.current_table.pot+=seat.CALL
            seat.stack-=seat.CALL
            seat.round_betting+=seat.CALL
            print(str(seat)+": Calls For "+str(seat.CALL))

    def Raise(self,seat):
            if seat.has_raised:
                return False
            else:
                self.current_table.pot+=seat.CALL*2
                seat.stack-=seat.CALL*2
                seat.has_raised=True
                seat.round_betting+=seat.CALL*2
                print(str(seat)+": Raises For "+str(seat.CALL*2))
                return True
    
    def Decisions(self,playing_order):
        player_1=playing_order[0]
        player_2=playing_order[1]
        player_decision=player_1.player.MakeDecision()
        if player_decision =='f':
            return True
        if player_decision =='c':
            self.Call(player_1,player_2)
        elif player_decision =='r':
            successful=self.Raise(player_1)
            if successful:
                player_2.CALL=player_2.CALL * 2
        return self.PlayBetting(player_1,player_2)
        
    def PlayBetting(self,player_1,player_2):
        while player_1.round_betting != player_2.round_betting:
            player= player_2 if player_1.round_betting > player_2.round_betting else player_1
            opponent= player_1 if player_1.round_betting > player_2.round_betting else player_2
            player_decision = player.player.MakeDecision()
            if player_decision =='f':
                return True
            if player_decision =='c':
                self.Call(player,opponent)
            elif player_decision =='r':
                successful=self.Raise(player)
                player.CALL=player.CALL * 2
                if not successful:
                    self.Call(player,opponent)
            player.CALL=2
            opponent.CALL=2
        return -1

    def Showdown(self,player_folded=(False,0)):
        if player_folded[0]==False:
            players_hands=[]
            for player in self.current_table.members:
                players_hands.append(player.cards)
            self.evaluator.hand_summary(self.board,players_hands)
            print("PLAYER_1:\t"+Card.print_pretty_cards(players_hands[0]))
            print("PLAYER_2:\t"+Card.print_pretty_cards(players_hands[1]))
            print("Board:\t"+Card.print_pretty_cards(self.board))
            if self.evaluator.evaluate(players_hands[0],self.board)>self.evaluator.evaluate(players_hands[1],self.board):
                self.current_table.members[1].stack+=self.current_table.pot
                print("Player 1 Stack:\t"+str(self.current_table.members[0].stack))
                print("Player 2 Stack:\t"+str(self.current_table.members[1].stack))
                return "2"
            elif self.evaluator.evaluate(players_hands[0],self.board)<self.evaluator.evaluate(players_hands[1],self.board):
                self.current_table.members[0].stack+=self.current_table.pot
                print("Player 1 Stack:\t"+str(self.current_table.members[0].stack))
                print("Player 2 Stack:\t"+str(self.current_table.members[1].stack))
                return "1"
            else:
                self.current_table.members[0].stack+=self.current_table.pot/2
                self.current_table.members[1].stack+=self.current_table.pot/2
                print("Player 1 Stack:\t"+str(self.current_table.members[0].stack))
                print("Player 2 Stack:\t"+str(self.current_table.members[1].stack))
                return "Draw"
        else:
            players_hands=[]
            for player in self.current_table.members:
                players_hands.append(player.cards)
            print("PLAYER_1:\t"+Card.print_pretty_cards(players_hands[0]))
            print("PLAYER_2:\t"+Card.print_pretty_cards(players_hands[1]))
            print("Board:\t"+Card.print_pretty_cards(self.board))
            if player_folded[1] == 1: 
                print("Player 1 Folds -> Player 2 is the winner")
                self.current_table.members[1].stack+=self.current_table.pot
                print("Player 1 Stack:\t"+str(self.current_table.members[0].stack))
                print("Player 2 Stack:\t"+str(self.current_table.members[1].stack))
                return 2
            else:
                print("Player 2 Folds -> Player 1 is the winner")
                self.current_table.members[0].stack+=self.current_table.pot
                print("Player 1 Stack:\t"+str(self.current_table.members[0].stack))
                print("Player 2 Stack:\t"+str(self.current_table.members[1].stack))
                return 1
        
    def PlayGame(self,no_of_games=1):
        def Preflop(dealer):
            first_to_act =  self.current_table.members[1] if dealer == 0 else self.current_table.members[0]
            second_to_act = self.current_table.members[dealer]
            player_folded=self.Decisions([first_to_act,second_to_act])
            return player_folded
        def Flop(dealer):
            drawn_cards=[]
            drawn_cards=deck.draw(3)
            print("Flop:"+Card.print_pretty_cards(drawn_cards))
            for i in drawn_cards:
                  self.board.append(i)
            first_to_act =  self.current_table.members[1] if dealer == 0 else self.current_table.members[0]
            second_to_act = self.current_table.members[dealer]
            player_folded=self.Decisions([first_to_act,second_to_act])
            return player_folded
        def Turn(dealer):
            drawn_cards=[deck.draw(1)]
            print("Turn:"+Card.print_pretty_cards(drawn_cards))
            for i in drawn_cards:
                  self.board.append(i)
            first_to_act =  self.current_table.members[1] if dealer == 0 else self.current_table.members[0]
            second_to_act = self.current_table.members[dealer]
            player_folded=self.Decisions([first_to_act,second_to_act])
            return player_folded
        def River(dealer):
            drawn_cards=[deck.draw(1)]
            print("River:"+Card.print_pretty_cards(drawn_cards))
            for i in drawn_cards:
                self.board.append(i)
            first_to_act =  self.current_table.members[1] if dealer == 0 else self.current_table.members[0]
            second_to_act = self.current_table.members[dealer]
            player_folded=self.Decisions([first_to_act,second_to_act])
            return player_folded
        def GoToShowdown(dealer):
            first_to_act =  self.current_table.members[1] if dealer == 0 else self.current_table.members[0]
            second_to_act = self.current_table.members[dealer]
            player_folded=self.Decisions([first_to_act,second_to_act])
            if player_folded==-1:   
                self.Showdown()
            else:
                self.Showdown(player_folded=(True,player_folded))
            self.board=[]
            self.current_table.pot=0
            self.current_table.dealer_position = 0 if self.current_table.dealer_position == 1 else 1
                
        current_game=0
        while current_game<no_of_games:
            round_no=0    #0,1,2,3,4,5 -> Preflop,Flop,Turn,River,Showdown
            deck=Deck()
            player_folded=False
            for member in self.current_table.members:
                member.cards=deck.draw(2)
            dealer=self.current_table.dealer_position
            while round_no<5:
                print(str(round_no)+" Pot:" +str(self.current_table.pot)+"\n")
                if round_no==0:
                    Preflop(dealer)
                if round_no==1:
                    Flop(dealer)
                if round_no==2:
                    Turn(dealer)
                if round_no==3:
                    River(dealer)
                if round_no==4:
                    GoToShowdown(dealer)
                    round_no+=1
                if player_folded == True:
                    round_no=5
                else:
                    round_no+=1 
                for player in self.current_table.members:
                    player.has_raised=False
            no_of_games-=1
    
if __name__ == '__main__':    
    player_1=Bot_1()
    player_2=Bot_2()       
    new_game=Game()
    new_game.current_table.BuyIn([player_1,player_2],300)
    hands=new_game.PlayGame(no_of_games=5)