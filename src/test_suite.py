# -*- coding: utf-8 -*-

import pytest
import treys as poker
import ExperimentSuite
import HeadsUpLimitHoldemCasino
import StatisticalBot
import BotX

''' TESTS FOR BOTX, STATISTICALBOT, EXPERIMENTSUITE, CASINO 27/03/2019 All Pass '''
class TestClass_BotX(object): 
    #Tests for basic bot, pokercnn frame work and statistical bot
    def test_card_assignment(self):
        sample_hand = [poker.Card.new('Ah'),poker.Card.new('Ad')]
        bot = BotX.Bot()
        bot.add_cards(sample_hand)
        assert bot.hand == sample_hand
    def test_board_assignment(self):
        sample_flop_board = [poker.Card.new('Ah'),poker.Card.new('Ad'),poker.Card.new('Ac')]
        sample_turn_board = [poker.Card.new('Ah'),poker.Card.new('Ad'),poker.Card.new('Ac'),poker.Card.new('Jd')]
        sample_river_board = [poker.Card.new('Ah'),poker.Card.new('Ad'),poker.Card.new('Ac'),poker.Card.new('Jd'),poker.Card.new('Td')]
        bot = BotX.Bot()
        bot.add_board(sample_flop_board)
        assert bot.board == sample_flop_board
        bot.add_board(sample_turn_board)
        assert bot.board == sample_turn_board
        bot.add_board(sample_river_board)
        assert bot.board == sample_river_board
        bot.add_board(sample_flop_board)
        assert bot.hand != sample_river_board
    def test_decision_switch(self):
        #Tests Switching between Callbot,Foldbot,Raisebot
        bot = BotX.Bot()
        bot.X = 'c'
        assert bot.MakeDecision(0,0,0) == 'c'
        bot.X = 'f'
        assert bot.MakeDecision(0,0,0) == 'f'
        bot.X = 'r'
        assert bot.MakeDecision(0,0,0) == 'r'

class TestClass_Casino(object):
    def test_table_successful_buy_in(self):
        bot_1 = BotX.Bot()
        bot_2 = BotX.Bot()
        bot_3 = BotX.Bot()
        table = HeadsUpLimitHoldemCasino.Table()
        table.BuyIn([bot_1,bot_2],100)
        assert len(table.members) == 2
        assert table.members[0].player.stack == 100
        assert table.members[1].player.stack == 100
        assert table.members[0].name == 'Player 1'
        assert table.members[1].name == 'Player 2'
        table.BuyIn([bot_3],100)
        assert table.is_full == True
        assert len(table.members) == 2
        assert table.members[0].player.stack == 100
        assert table.members[1].player.stack == 100
        assert table.members[0].name == 'Player 1'
        assert table.members[1].name == 'Player 2'
    def test_call_bot_game(self):
        bot_1 = bot_1 = BotX.Bot()
        bot_2 = bot_2 = BotX.Bot()
        bot_1.X = 'c'
        bot_2.X = 'c'
        game = HeadsUpLimitHoldemCasino.Game()
        game.current_table.BuyIn([bot_1,bot_2],300)
        winners = game.PlayGame(no_of_games = 1)
        assert type(winners) == list and len(winners) == 1
        assert (game.current_table.members[0].player.stack + game.current_table.members[1].player.stack) / 2 == 300.0
        assert game.current_table.members[1].player.stack != 300.0 and game.current_table.members[0].player.stack != 300.0
        assert game.current_table.pot == 0
        for player in game.current_table.members:
            assert player.has_raised == False
            assert player.actions == ''
            assert player.player.hand == []
            assert player.player.board == []
            assert player.CALL == 0.0
        assert game.board == []
    def test_raise_bot_game(self):
        bot_1 = bot_1 = BotX.Bot()
        bot_2 = bot_2 = BotX.Bot()
        bot_1.X = 'r'
        bot_2.X = 'r'
        game = HeadsUpLimitHoldemCasino.Game()
        game.current_table.BuyIn([bot_1,bot_2],300)
        winners = game.PlayGame(no_of_games = 1)
        assert type(winners) == list and len(winners) == 1
        assert (game.current_table.members[0].player.stack + game.current_table.members[1].player.stack) / 2 == 300.0
        assert game.current_table.members[1].player.stack != 300.0 and game.current_table.members[0].player.stack != 300.0
        assert game.current_table.pot == 0
        for player in game.current_table.members:
            assert player.has_raised == False
            assert player.actions == ''
            assert player.player.hand == []
            assert player.player.board == []
            assert player.CALL == 0.0
        assert game.board == []
    def test_fold_bot_game(self):
        bot_1 = bot_1 = BotX.Bot()
        bot_2 = bot_2 = BotX.Bot()
        bot_1.X = 'f'
        bot_2.X = 'r'
        game = HeadsUpLimitHoldemCasino.Game()
        game.current_table.BuyIn([bot_1,bot_2],300)
        winners = game.PlayGame(no_of_games = 1)
        assert type(winners) == list and len(winners) == 1
        assert (game.current_table.members[0].player.stack + game.current_table.members[1].player.stack) / 2 == 300.0
        assert game.current_table.members[0].player.stack !=300.0 
        assert game.current_table.members[1].player.stack !=300.0
        assert game.current_table.pot == 0
        for player in game.current_table.members:
            assert player.has_raised == False
            assert player.actions == ''
            assert player.player.hand == []
            assert player.player.board == []
            assert player.CALL == 0.0
        assert game.board == []

class TestClass_StatisticalBot(object):
    def test_fold_percent_adjustments(self):
        bot_1 = bot_1 = StatisticalBot.StatisticalBot()
        bot_2 = bot_2 = BotX.Bot()
        bot_2.X = 'c'
        bot_1.ResetFoldPercent(0.25)
        game = HeadsUpLimitHoldemCasino.Game()
        game.current_table.BuyIn([bot_1,bot_2],300)
        game.PlayGame(no_of_games = 1)
        assert bot_1.villain_fold_percent == 0
        bot_2.X = 'f'
        bot_1.ResetFoldPercent(0.25)
        game.PlayGame(no_of_games = 1)
        assert bot_1.villain_fold_percent == 1
    def test_fold_percent_slight_adjustments(self):
        bot_1 = bot_1 = StatisticalBot.StatisticalBot()
        bot_1.ResetFoldPercent(0.25)
        bot_1.UpdateFoldPercent(-1,5)
        assert bot_1.villain_fold_percent < 0.25 and bot_1.villain_fold_percent>0
        bot_1.ResetFoldPercent(0.25)
        bot_1.UpdateFoldPercent(1,5)
        assert bot_1.villain_fold_percent > 0.25 and bot_1.villain_fold_percent < 1
        
class TestClass_ExperimentSuite(object):
    def test_successful(self):
        ExperimentSuite.analyse_cepheus_vs_callbot()
        ExperimentSuite.analyse_cepheus_vs_Foldbot()
        ExperimentSuite.analyse_cepheus_vs_statsbot()
        ExperimentSuite.analyse_Callbot_vs_statsbot()
        ExperimentSuite.analyse_Foldbot_vs_statsbot()
        pass
        
        