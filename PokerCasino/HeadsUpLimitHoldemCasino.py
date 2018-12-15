# -*- coding: utf-8 -*-
from treys import Card
from treys import Evaluator
from treys import Deck
from time import sleep as wait_for_decision
from pdb import set_trace as breakp

PUBLIC_FILE_NAME="Casino_To_Players.txt.txt"
PRIVATE_FILE_NAMES=["Player_1_To_Casino.txt.txt","Player_2_To_Casino.txt.txt"]
CALL=1
RAISE=2

class SeatAtTable:
    def __init__(self,buy_in,seat_no):
        self.stack=buy_in
        self.cards=[]
        self.seat_no=seat_no
    def __str__(self):
        return "Stack Size:"+str(self.stack)

class Table:
    def __init__(self):
        self.members=[]
        self.pot=0
        self.is_full=False
        self.dealer_position=0
        self.big_blind=100.00
        self.small_blind=self.big_blind/2
        
    def __str__(self):
        return "Members:"+str([str(member) for member in self.members])+"\nPot:"+str(self.pot)+"\nBB:"+str(self.big_blind) 
    
    def BuyIn(self,buy_in_amount):
        if len(self.members)==2:
            self.is_full=True
        if not self.is_full:
            self.members.append(SeatAtTable(buy_in_amount,len(self.members)))
            
class Game:
    def __init__(self):
        self.current_table=Table()
        self.current_table.BuyIn(100)
        self.current_table.BuyIn(100)
        self.evaluator=Evaluator()
        self.board=[]
        self.game_string=""
    
    def IncreasePot(self,decision,prev_decision='c',seat_no=0):
        if decision=='c':
            self.current_table.pot+=CALL
            self.current_table.members[seat_no].stack-=CALL
        elif decision=='r':
            self.current_table.pot+=RAISE
            self.current_table.members[seat_no].stack-=RAISE
    def GetDecisions(self):
        decisions=""
        current_player=1
        for file in PRIVATE_FILE_NAMES:
            with open(file,'r') as f:
                player_decision=f.readline()
                decisions+=player_decision
                if player_decision=='f':
                    #breakp()
                    return decisions,current_player
                self.IncreasePot(player_decision)
            current_player+=1
        return decisions,-1
    
    def UpdateGame(self):
        with open(PUBLIC_FILE_NAME,'w') as file:
            file.write(self.game_string)
            
    def GetCardInt(self,card):
        card_suit=Card.get_suit_int(card)-1
        if card_suit==7: #Treys Clubs suit == 8-> From line above, if clubs, card_suit == 7 (Club_Suit-1 --> 8 - 1 == 7)
            card_suit=2  #Correct the fact clubs suit should == 3, from first line (clubs_int - 1 == 2)
        return str((13*card_suit)+Card.get_rank_int(card))
   
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
        #if self.current_table.is_full:
        current_game=0
        while current_game<no_of_games:
            self.game_string=f'{str(current_game+1)}D{str(self.current_table.dealer_position)}P'
            game_round=0    #0,1,2,3,4,5 -> Preflop,Flop,Turn,River,Postflop,Showdown
            deck=Deck()
            for member in self.current_table.members:
                member.cards=deck.draw(2)
                #Write Cards to Bot File 
            while game_round<6:
                if game_round==0:
                    print("Pot:" +str(self.current_table.pot)+"\n")
                    #time.sleep(5)
                    decisions,player_folded=self.GetDecisions()
                    self.game_string+=f'{decisions}'
                    self.UpdateGame()
                    if player_folded == -1:
                         game_round+=1
                        
                    else:
                        game_round=5
                if game_round==1:
                    print("Pot:" +str(self.current_table.pot)+"\n")
                    drawn_cards=[]
                    drawn_cards=deck.draw(3)
                    print("Flop:"+Card.print_pretty_cards(drawn_cards))
                    for i in drawn_cards:
                        self.board.append(i)
                        self.game_string+=f'F{self.GetCardInt(i)}'
                    decisions,player_folded=self.GetDecisions()
                    self.game_string+=f'F{decisions}'
                    self.UpdateGame()
                    if player_folded == True:
                        game_round=5
                    else:
                        game_round+=1
                if game_round==2:
                    print("Pot:" +str(self.current_table.pot)+"\n")
                    drawn_cards=[deck.draw(1)]
                    print("Turn:"+Card.print_pretty_cards(drawn_cards))
                    for i in drawn_cards:
                        self.board.append(i)
                        self.game_string+=f'T{self.GetCardInt(i)}'
                    decisions,player_folded=self.GetDecisions()
                    self.game_string+=f'T{decisions}'
                    self.UpdateGame()
                    if player_folded == True:
                        game_round=5
                    else:
                        game_round+=1
                if game_round==3:
                    print("Pot:" +str(self.current_table.pot)+"\n")
                    drawn_cards=[deck.draw(1)]
                    print("River:"+Card.print_pretty_cards(drawn_cards))
                    for i in drawn_cards:
                        self.board.append(i)
                        self.game_string+=f'R{self.GetCardInt(i)}'
                    decisions,player_folded=self.GetDecisions()
                    self.game_string+=f'R{decisions}'
                    self.UpdateGame()
                    if player_folded == True:
                        game_round=5
                    else:
                        game_round+=1
                if game_round==4:
                    print("Pot:" +str(self.current_table.pot)+"\n")
                    game_round+=1
                if game_round==5:
                    if player_folded==-1:
                        for member in self.current_table.members:
                            self.game_string+=f'S{member.seat_no}A{self.GetCardInt(member.cards[0])}B{self.GetCardInt(member.cards[1])}'
                        winner=self.Showdown()
                        self.game_string+=f'W{winner}E'
                        self.UpdateGame()
                    else:
                        winner=self.Showdown(player_folded=(True,player_folded))
                        self.game_string+=f'W{winner}E'
                        self.UpdateGame()
                    game_round+=1
                    self.board=[]
                    self.current_table.pot=0
            no_of_games-=1
    
                
if __name__ == '__main__':                
    new_game=Game()
    hands=new_game.PlayGame(no_of_games=5)
