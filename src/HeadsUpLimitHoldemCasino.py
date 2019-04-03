# -*- coding: utf-8 -*-

from treys import Card
from treys import Evaluator
from treys import Deck
import time
import datetime
from BotX import Bot as Bot_1
import StatisticalBot

NUM_GAMES = 1000
#SUMMARY WRITING COMMENTED OUT LINE 269
GAME_SUMMARY_FILE_LOG = "Game_Summaries_" + datetime.datetime.today().strftime('%Y%m%d') + f"_{NUM_GAMES}_STATISTICALVSFOLD2_BOTS.csv"
BIG_BLIND = 10
SMALL_BLIND = 5

'''Class to Represent a seat at the poker table --> Keep track of player details'''
class SeatAtTable: 
    def __init__(self,player,buy_in,seat_no,name):
        self.player=player
        self.player.stack=buy_in
        self.cards=[]
        self.seat_no=seat_no
        self.name= name
        self.has_raised=False
        self.round_betting=0
        self.bet_count = 0
        self.CALL = 0 
        self.actions = ""
        self.time_taken = 0.0
    def __str__(self):
        return str(self.name)
    
'''Class to Represent the poker table --> Keep track of all active players'''
class Table:
    def __init__(self):
        self.members=[]
        self.pot=0
        self.is_full=False
        self.dealer_position=0
        self.big_blind = BIG_BLIND
        self.small_blind = SMALL_BLIND
        
    def __str__(self):
        return "Members:"+str([str(member) for member in self.members])+"\nPot:"+str(self.pot)+"\nBB:"+str(self.big_blind) 
    
    def BuyIn(self,players,buy_in_amount):
        if len(self.members)>=2: #Can Be Changed to add more players to table
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
    
    #Used in creating game logs --. Analysed by Experiment Suite
    def Game_Summary(self,winner="",pot="",actions="",attP1="",attP2="",handno="",new_file=False,):
        csv_headers="Winner,Pot,Actions,ATTP1,ATTP2,HandNo"
        if new_file:
            with open(GAME_SUMMARY_FILE_LOG,'w') as log:
                log.write(csv_headers)
        else:
            winner=winner
            with open(GAME_SUMMARY_FILE_LOG,'a') as log:
                log.write(f'\n{winner},{pot},{actions},{attP1},{attP2},{handno}')
            
    def PlayGame(self,no_of_games=1):
        #Set Dealer and initial 2 card deal to each player
        def SetUpGame():
            non_dealer = 0
            for member in table.members:
                    member.cards=deck.draw(2)
                    member.player.add_cards(member.cards)
            if current_game == 1:
                table.dealer_position = 0 
                non_dealer = 1
            else:
                if table.dealer_position == 1:
                    table.dealer_position = 0
                    non_dealer = 1
                else:
                    table.dealer_position = 1    #Swap Dealer Button
                    non_dealer = 0
            return table.dealer_position, non_dealer
        #add blinds from each player stack
        def PostBlinds(dealer,non_dealer):
            table.pot += table.small_blind
            table.pot += table.big_blind
            table.members[dealer].player.stack -= table.small_blind
            table.members[non_dealer].player.stack -= table.big_blind
            table.members[dealer].round_betting += table.small_blind
            table.members[non_dealer].round_betting += table.big_blind
            table.members[dealer].bet_count += 1
            table.members[non_dealer].bet_count += 1
        #Preflop Betting    
        def Preflop(dealer,non_dealer):
            first_to_act =  table.members[dealer]
            second_to_act = table.members[non_dealer]
            player_folded = Decisions([first_to_act,second_to_act],0)
            return player_folded
        #Flop Draw and Betting
        def Flop(dealer,non_dealer):
            drawn_cards=deck.draw(3)
            print("Flop:"+Card.print_pretty_cards(drawn_cards))
            
            for i in drawn_cards:
                  self.board.append(i)
            for member in table.members:
                member.player.add_board(self.board)#
                
            first_to_act =  table.members[non_dealer]
            second_to_act = table.members[dealer]
            player_folded = Decisions([first_to_act,second_to_act],1)
            return player_folded
        #Turn Draw and Betting
        def Turn(dealer,non_dealer):
            table.big_blind = table.big_blind * 2
            drawn_cards=[deck.draw(1)]
            print("Turn:"+Card.print_pretty_cards(drawn_cards))
            
            for i in drawn_cards:
                  self.board.append(i)
            for member in table.members:
                member.player.add_board(self.board)
                
            first_to_act =  table.members[non_dealer] 
            second_to_act = table.members[dealer]
            player_folded = Decisions([first_to_act,second_to_act],2)
            return player_folded
        #River Draw and Betting
        def River(dealer,non_dealer):
            drawn_cards=[deck.draw(1)]
            print("River:"+Card.print_pretty_cards(drawn_cards))
            
            for i in drawn_cards:
                self.board.append(i)
            for member in table.members:
                member.player.add_board(self.board)
                
            first_to_act =  table.members[non_dealer] 
            second_to_act = table.members[dealer]
            player_folded = Decisions([first_to_act,second_to_act],3)
            return player_folded
        #Initial Decision by first to act
        def Decisions(playing_order,round_no):
            player_1 = playing_order[0]
            player_2 = playing_order[1]
            player_1.CALL = table.big_blind
            player_2.CALL = table.big_blind
            start_timer = time.time()
            player_decision = player_1.player.MakeDecision(table.pot, round_no, player_1.CALL)
            end_timer = time.time()
            player_1.time_taken += end_timer - start_timer
            
            if player_decision =='f':
                player_1.actions += 'f'
                player_folded = True,player_1.name
                print(f'{player_1.name} : Folded!')
                return player_folded
            if player_decision =='r':
                if player_1.has_raised :
                        player_decision = 'c'
                else:
                    Raise(player_1)
                    player_2.CALL = player_2.CALL * 2    
                        
            if player_decision =='c':
                Call(player_1,player_2)
            print(f'\n{player_1.name} : {player_decision}')
            
            
            player_folded = BettingRound(player_1,player_2,round_no)
            player_1.has_raised = False
            player_2.has_raised = False
            return player_folded
        #Run for rest of betting round until bets are equal
        def BettingRound(player_1,player_2,round_no):
            #Keep Track of Player Folded
            player_folded = False,""
            #Runs until each player has equalled each others bet size and have made an equal number of bets !
            while player_1.round_betting != player_2.round_betting or player_1.bet_count != player_2.bet_count :
                #Checks who's turn it is to make a decision
                player = player_2 if player_1.bet_count > player_2.bet_count else player_1
                opponent = player_1 if player_1.bet_count > player_2.bet_count else player_2
                #timer calculates time taken to make a decision if needed 
                start_timer = time.time()
                player_decision = player.player.MakeDecision(table.pot,round_no,player.CALL)
                end_timer = time.time()
                player.time_taken += end_timer - start_timer
                #If player folds, break loop and return player folded = True and that players name
                if player_decision =='f':
                    player.actions += 'f'
                    player_folded = True,player.name
                    print(f'{player.name} : Folded!')
                    break
                #If player raises call Raise, If they have already raised once, change decision to call
                if player_decision =='r':
                    if player.has_raised :
                        player_decision = 'c'
                    else:
                        Raise(player)
                        opponent.CALL = opponent.CALL * 2
                #If player calls, run Call
                if player_decision =='c':
                    Call(player,opponent)
                if player_1.round_betting == player_2.round_betting :
                    player_1.bet_count = 0
                    player_2.bet_count = 0
                print(f'{player.name} : {player_decision}')
            return player_folded
        #Call Decision
        def Call(seat,opp):
            seat.CALL = opp.round_betting-seat.round_betting
            if seat.CALL < 0 : seat.CALL= table.big_blind
            if seat.player.stack <= 0 : 
                print(f'{seat.name} BUYS IN : {(0 - seat.player.stack) + 300}')
                seat.player.stack = (0 - seat.player.stack) + 300
            table.pot += seat.CALL
            seat.player.stack-=seat.CALL
            seat.round_betting+=seat.CALL
            seat.bet_count += 1
            seat.actions += "c"
        #Raise decision
        def Raise(seat):
            if seat.player.stack <= 0 : 
                print(f'{seat.name} BUYS IN : {(0 - seat.player.stack) + 300}')
                seat.player.stack = (0 - seat.player.stack) + 300
            table.pot+=seat.CALL * 2
            seat.player.stack-=seat.CALL * 2
            seat.has_raised=True
            seat.round_betting+=seat.CALL * 2
            seat.bet_count += 1
            seat.actions += 'r'
        #Called if player folds --> Output different from Showdown
        def PlayerFolded(game,total_games):
            players_hands=[]
            for player in table.members:
                players_hands.append(player.cards)
                
            print("PLAYER_1:\t"+Card.print_pretty_cards(players_hands[0]))
            print("PLAYER_2:\t"+Card.print_pretty_cards(players_hands[1]))
            print("Board:\t"+Card.print_pretty_cards(self.board))
            if player_folded[1] == 'Player 1': 
                print("Player 1 Folds -> Player 2 is the winner")
                self.current_table.members[1].player.stack+=table.pot
                print("Player 1 Stack:\t"+str(table.members[0].player.stack))
                print("Player 2 Stack:\t"+str(table.members[1].player.stack))
                winner = 2
                table.members[0].player.Game_Over(False,True,total_games-game)
                table.members[1].player.Game_Over(True,True,total_games-game)
            else:
                print("Player 2 Folds -> Player 1 is the winner")
                self.current_table.members[0].player.stack+=table.pot
                print("Player 1 Stack:\t"+str(table.members[0].player.stack))
                print("Player 2 Stack:\t"+str(table.members[1].player.stack))
                winner = 1
                table.members[1].player.Game_Over(False,True,total_games-game)
                table.members[0].player.Game_Over(True,True,total_games-game)
            print('--------------------------------------------------------------------------\n')
            num_actions = len(table.members[0].actions) if len(table.members[0].actions) > 0 else 1
            #Uncomment to Write to GAME LOGS
            #self.Game_Summary(winner,table.pot,table.members[0].actions+"/"+table.members[1].actions,table.members[0].time_taken/num_actions,table.members[1].time_taken/num_actions,game)
            table.members[0].time_taken = 0
            table.members[1].time_taken = 0
            return winner
        #Summarise Game
        def Showdown(game,total_games):
            winner=0
            players_hands=[]
            for player in table.members:
                players_hands.append(player.cards)
            self.evaluator.hand_summary(self.board,players_hands)
            player_1_rank = self.evaluator.evaluate(players_hands[0],self.board)
            player_2_rank = self.evaluator.evaluate(players_hands[1],self.board)
            print("PLAYER_1:\t"+Card.print_pretty_cards(players_hands[0]))
            print("PLAYER_2:\t"+Card.print_pretty_cards(players_hands[1]))
            print("Board:\t"+Card.print_pretty_cards(self.board))
            if player_1_rank > player_2_rank:
                self.current_table.members[1].player.stack+=table.pot
                print("Player 1 Stack:\t"+str(table.members[0].player.stack))
                print("Player 2 Stack:\t"+str(table.members[1].player.stack))
                table.members[0].player.Game_Over(False,False,total_games-game)
                table.members[1].player.Game_Over(True,False,total_games-game)
                winner = 2
            elif player_1_rank < player_2_rank:
                self.current_table.members[0].player.stack+=table.pot
                print("Player 1 Stack:\t"+str(table.members[0].player.stack))
                print("Player 2 Stack:\t"+str(table.members[1].player.stack))
                table.members[0].player.Game_Over(True,False,total_games-game)
                table.members[1].player.Game_Over(False,False,total_games-game)
                winner = 1
            else:
                self.current_table.members[0].player.stack+=table.pot/2
                self.current_table.members[1].player.stack+=table.pot/2
                print("Player 1 Stack:\t"+str(table.members[0].player.stack))
                print("Player 2 Stack:\t"+str(table.members[1].player.stack))
                table.members[0].player.Game_Over(False,False,total_games-game)
                table.members[1].player.Game_Over(False,False,total_games-game)
                winner = 0
            #UNCOMMENT TO ADD TO GAME FILE    
            #self.Game_Summary(winner,table.pot,table.members[0].actions+"/"+table.members[1].actions,table.members[0].time_taken/len(table.members[0].actions),table.members[1].time_taken/len(table.members[1].actions),game)
            table.members[0].time_taken = 0
            table.members[1].time_taken = 0
            return winner
        #Resets after each game back to defaults
        def Reset():
            table.big_blind = 10.0
            for player in table.members:
                    player.has_raised=False
                    player.actions = ""
                    player.player.hand = []
                    player.player.board = []
                    player.CALL = 0.0
            self.board=[]
            table.pot=0

        current_game = 1
        winners=[]
        while current_game <= no_of_games:
            round_no=0    #0,1,2,3,4,5 -> Preflop,Flop,Turn,River,Showdown,Reset
            deck=Deck()   #New Deck
            player_folded=False,"" #Reset Player Folded
            table = self.current_table
            dealer, non_dealer = SetUpGame()
            PostBlinds(dealer,non_dealer) 
            print(dealer)
            winner = 0
            while round_no<=5:
                if round_no==0:
                    player_folded = Preflop(dealer,non_dealer)
                    print("Preflop Pot:" +str(table.pot)+"\n")
                    #breakp()
                if round_no==1:
                    player_folded = Flop(dealer,non_dealer)
                    print("Flop Pot:" +str(table.pot)+"\n")
                if round_no==2:
                    player_folded = Turn(dealer,non_dealer)
                    print("Turn Pot:" +str(table.pot)+"\n")
                if round_no==3:
                    player_folded = River(dealer,non_dealer)
                    print("River Pot:" +str(table.pot)+"\n")
                if round_no==4:
                    print("Showdown Pot:" +str(table.pot)+"\n")
                    winner = Showdown(current_game,no_of_games)
                    round_no+=1
                if round_no == 5:
                    Reset()
                if player_folded[0] == True:
                    winner = PlayerFolded(current_game,no_of_games)
                    Reset()
                    break
                round_no+=1
            Reset()
            current_game+=1
            winners.append(winner)
        return winners

def main():
    #To use Statistical bot, create new instance, set fold percent to start percentage : RECOMMENDED 0.25s
    player_1=Bot_1()
    player_1.X = 'c'
    player_2=StatisticalBot.StatisticalBot()  
    player_2.ResetFoldPercent(0.25)
    new_game=Game()
    #new_game.Game_Summary(new_file=True)
    new_game.current_table.BuyIn([player_1,player_2],300)
    winners=new_game.PlayGame(no_of_games=2)
    print(f'Winners : {winners}')
if __name__ == '__main__': 
    main()