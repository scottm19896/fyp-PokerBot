# -*- coding: utf-8 -*-



from HeadsUpLimitHoldemCasino import Game
from StatisticalBot import StatisticalBot
from BotX import Bot
import pandas as pd
import matplotlib.pyplot as plt


FOLDER_PATH = "C:/Users/squas/Desktop/14570733/supporting/Logs/"
REPORT_FILE=f"{FOLDER_PATH}10_StatsVSCallBot_Simulation5.csv"
CEPHEUS_VS_CALL_LOG = f"{FOLDER_PATH}Cepheus_VS_Callbot_Simulations_1000_Games.csv"
CEPHEUS_VS_FOLD_LOG = f"{FOLDER_PATH}Cepheus_VS_Foldbot_Simulations_1000_games.csv"
CEPHEUS_VS_STAT_LOG = f"{FOLDER_PATH}Cepheus_VS_StatisticalBot_1000_Simulations.csv"
STAT_VS_CALL_LOG = f"{FOLDER_PATH}Game_Summaries_20190326_30_STATISTICALVSCALL2_BOTS.csv"
STAT_VS_FOLD_LOG = f'{FOLDER_PATH}Game_Summaries_20190326_1000_STATISTICALVSFOLD2_BOTS.csv'
ITERATIONS = 30

class Tests:
    #Runs Tests
    #Creates a dataframe for each test type
    #Depending on test type-> stores the relevant information
    def __init__(self):
        self.callbot_test_Statistic=pd.DataFrame(columns=['Iteration','Stats Win','Call Win','Draw','Test'])
        self.foldbot_test_Statistic=pd.DataFrame(columns=['Iteration','Stats Win','Call Win','Draw','Test'])
    def RunSimulation(self,player_1,player_2,test_type):
        df = pd.DataFrame()
        if test_type == "StatVCall": df = self.callbot_test_Statistic
        if test_type == 'StatVFold': df = self.foldbot_test_Statistic
        for iteration in range(ITERATIONS):
            p1_wins=0
            p2_wins=0
            draws=0
            game=Game()
            game.current_table.BuyIn([player_1,player_2],300)
            #sys.stdout.write(f'{(iteration+1)*5} / {ITERATIONS*5} {(((iteration+1)*5)/(ITERATIONS*5))*100} %'); sys.stdout.flush();  # print a small progress bar
            winner = game.PlayGame(no_of_games=5)
            p2_wins += winner.count(2)
            p1_wins += winner.count(1)
            draws += winner.count(2)
            df = df.append({'Iteration':iteration,'Stats Win' : p1_wins, 'Call Win' : p2_wins , 'Draw' : draws, 'Test' : test_type} , ignore_index=True)
            
        self.SendToCsv(df,REPORT_FILE)
    def SendToCsv(self,df,file_path):
        df.to_csv(file_path)
        plt.plot(df['Stats Win'])
        print(df['Stats Win'].std())
        print(df['Call Win'].std())
        plt.ylabel('Wins Per 100')

def analyse_cepheus_vs_callbot(): 
    print('Cepheus Vs CallBot')
    print()
    df = pd.read_csv(CEPHEUS_VS_CALL_LOG)
    cepheus_wins = 0
    call_wins = 0
    winrate = pd.DataFrame(columns = ['Cepheus','Callbot'])
    for i in range(len(df)):
        winner = df.iloc[i]['Winner']
        if winner == 'c':
            cepheus_wins += 1
        elif winner == 's':
            call_wins += 1
        if i % 10 == 0 and i!=0:
            winrate = winrate.append({'Cepheus' : cepheus_wins,'Callbot' : call_wins},ignore_index = True)
            cepheus_wins = 0
            call_wins = 0
    plt.figure(1)
    plt.subplot(211)
    plt.plot(winrate['Cepheus'])
    plt.plot(winrate['Callbot'])
    plt.ylabel('Winrate (Wins Per 10)')
    plt.xlabel('No. Of Games (x10)')
    plt.legend()
    plt.title('Cepheus Vs CallBot')
    print("Cepheus Winrate : " + str((len(df[df['Winner'] == 'c'])/1000) *100) + '%')
    print("Callbot Winrate : " + str((len(df[df['Winner'] == 's'])/1000) *100) + '%')
    cepheus_earn = sum(df[df['Winner'] == 'c']['Pot'])/10
    call_earn = sum(df[df['Winner'] == 's']['Pot'])/10
    print("Cepheus Earnings Per 100 : " + str(cepheus_earn - call_earn))
    print("Callbot Earnings Per 100 : " + str(call_earn - cepheus_earn))
    print("Cepheus Percentage Increase on Takings : " + str(((cepheus_earn - call_earn )/cepheus_earn) * 100) + '%')
    print()
    
def analyse_cepheus_vs_Foldbot(): 
    print('Cepheus Vs FoldBot')
    print()
    df = pd.read_csv(CEPHEUS_VS_FOLD_LOG)
    cepheus_wins = 0
    Fold_wins = 0
    winrate = pd.DataFrame(columns = ['Cepheus','Foldbot'])
    for i in range(len(df)):
        winner = df.iloc[i]['Winner']
        if winner == 'c':
            cepheus_wins += 1
        elif winner == 's':
            Fold_wins += 1
        if i % 10 == 0 and i!=0:
            winrate = winrate.append({'Cepheus' : cepheus_wins,'Foldbot' : Fold_wins},ignore_index = True)
            cepheus_wins = 0
            Fold_wins = 0
    plt.figure(2)
    plt.subplot(211)
    plt.plot(winrate['Cepheus'])
    plt.plot(winrate['Foldbot'])
    plt.ylabel('Winrate (Wins Per 10)')
    plt.xlabel('No. Of Games (x10)')
    plt.legend()
    plt.title('Cepheus Vs FoldBot')
    print("Cepheus Winrate : " + str((len(df[df['Winner'] == 'c'])/1000) *100) + ' %')
    print("Foldbot Winrate : " + str((len(df[df['Winner'] == 's'])/1000) *100) + ' %')
    cepheus_earn = sum(df[df['Winner'] == 'c']['Pot'])/10
    Fold_earn = sum(df[df['Winner'] == 's']['Pot'])/10
    print("Cepheus Earnings Per 100 : " + str(cepheus_earn - Fold_earn))
    print("Foldbot Earnings Per 100 : " + str(Fold_earn - cepheus_earn))
    print("Cepheus Percentage Increase on Takings : " + str(((cepheus_earn - Fold_earn )/cepheus_earn) * 100) + ' %')
    print()
    
def analyse_cepheus_vs_statsbot(): 
    print('Cepheus Vs Statistical Bot')
    print()
    df = pd.read_csv(CEPHEUS_VS_STAT_LOG)
    cepheus_wins = 0
    Statistical_wins = 0
    winrate = pd.DataFrame(columns = ['Cepheus','Statisticalbot'])
    for i in range(len(df)):
        winner = df.iloc[i]['Winner']
        if winner == 'c':
            cepheus_wins += 1
        elif winner == 's':
            Statistical_wins += 1
        if i % 10 == 0 and i!=0:
            winrate = winrate.append({'Cepheus' : cepheus_wins,'Statisticalbot' : Statistical_wins},ignore_index = True)
            cepheus_wins = 0
            Statistical_wins = 0
    plt.figure(3)
    plt.subplot(211)
    plt.plot(winrate['Cepheus'])
    plt.plot(winrate['Statisticalbot'])
    plt.ylabel('Winrate (Wins Per 10)')
    plt.xlabel('No. Of Games (x10)')
    plt.legend()
    plt.title('Cepheus Vs Statistical Bot')
    print("Cepheus Winrate : " + str((len(df[df['Winner'] == 'c'])/1000) *100) + ' %')
    print("Statisticalbot Winrate : " + str((len(df[df['Winner'] == 's'])/1000) *100) + ' %')
    cepheus_earn = sum(df[df['Winner'] == 'c']['Pot'])/10
    Statistical_earn = sum(df[df['Winner'] == 's']['Pot'])/10
    print("Cepheus Avg. Earnings Per 100 : " + str(cepheus_earn - Statistical_earn))
    print("Statisticalbot Avg. Earnings Per 100 : " + str(Statistical_earn - cepheus_earn))
    print("Cepheus Percentage Increase on Takings : " + str(((cepheus_earn - Statistical_earn )/cepheus_earn) * 100) + ' %')
    print("Statistical Bot Percentage Increase on Takings : " + str(((Statistical_earn - cepheus_earn )/Statistical_earn) * 100) + ' %')
    print()
    
def analyse_Callbot_vs_statsbot(): 
    print('Statistical Bot Vs CallBot')
    print()
    df = pd.read_csv(STAT_VS_CALL_LOG)
    Callbot_wins = 0
    Statistical_wins = 0
    winrate = pd.DataFrame(columns = ['Callbot','Statisticalbot'])
    for i in range(len(df)):
        winner = df.iloc[i]['Winner']
        #print(winner)
        if winner == 1:
            Callbot_wins += 1
        elif winner == 2:
            Statistical_wins += 1
        if i % 10 == 0 and i!=0:
            winrate = winrate.append({'Callbot' : Callbot_wins,'Statisticalbot' : Statistical_wins},ignore_index = True)
            Callbot_wins = 0
            Statistical_wins = 0
    plt.figure(4)
    plt.subplot(211)
    plt.plot(winrate['Callbot'])
    plt.plot(winrate['Statisticalbot'])
    plt.ylabel('Winrate (Wins Per 10)')
    plt.xlabel('No. Of Games (x10)')
    plt.legend()
    plt.title('Statistical Bot Vs CallBot')
    print("Callbot Winrate : " + str((len(df[df['Winner'] == 1])/1000) *100) + ' %')
    print("Statisticalbot Winrate : " + str((len(df[df['Winner'] == 2])/1000) *100) + ' %')
    Callbot_earn = sum(df[df['Winner'] == 1]['Pot'])/10
    Statistical_earn = sum(df[df['Winner'] == 2]['Pot'])/10
    print("Callbot Avg. Earnings Per 100 : " + str(Callbot_earn - Statistical_earn))
    print("Statisticalbot Avg. Earnings Per 100 : " + str(Statistical_earn - Callbot_earn))
    print("Callbot Percentage Increase on Takings : " + str(((Callbot_earn - Statistical_earn )/Callbot_earn) * 100) + ' %')
    print("Statistical Bot Percentage Increase on Takings : " + str(((Statistical_earn - Callbot_earn )/Statistical_earn) * 100) + ' %')
    print()
    
def analyse_Foldbot_vs_statsbot():
    print('Statistical Bot Vs FoldBot')
    print()
    df = pd.read_csv(STAT_VS_FOLD_LOG)
    Foldbot_wins = 0
    Statistical_wins = 0
    winrate = pd.DataFrame(columns = ['Foldbot','Statisticalbot'])
    for i in range(len(df)):
        winner = df.iloc[i]['Winner']
        #print(winner)
        if winner == 1:
            Foldbot_wins += 1
        elif winner == 2:
            Statistical_wins += 1
        if i % 10 == 0 and i!=0:
            winrate = winrate.append({'Foldbot' : Foldbot_wins,'Statisticalbot' : Statistical_wins},ignore_index = True)
            Foldbot_wins = 0
            Statistical_wins = 0
    plt.figure(5)
    plt.subplot(211)
    plt.plot(winrate['Foldbot'])
    plt.plot(winrate['Statisticalbot'])
    plt.ylabel('Winrate (Wins Per 10)')
    plt.xlabel('No. Of Games (x10)')
    plt.legend()
    plt.title('Statistical Bot vs Foldbot')
    print("Foldbot Winrate : " + str((len(df[df['Winner'] == 1])/1000) *100) + ' %')
    print("Statisticalbot Winrate : " + str((len(df[df['Winner'] == 2])/1000) *100) + ' %')
    Foldbot_earn = sum(df[df['Winner'] == 1]['Pot'])/10
    Statistical_earn = sum(df[df['Winner'] == 2]['Pot'])/10
    print("Foldbot Avg. Earnings Per 100 : " + str(Foldbot_earn - Statistical_earn))
    print("Statisticalbot Avg. Earnings Per 100 : " + str(Statistical_earn - Foldbot_earn))
    print("Statistical Bot Percentage Increase on Takings : " + str(((Statistical_earn - Foldbot_earn )/Statistical_earn) * 100) + ' %')
    print()

if __name__== '__main__':
    tests=Tests()
    #Create Players
    player_2 = StatisticalBot()
    player_2.ResetFoldPercent(0.0)
    player_1 = Bot()
    #Choose Type of Bot X ---> 'c' CALL, 'f' FOLD, 'r' RAISE , Mixture-> Random Decision Making
    player_1.X = 'c'
    #Example Tests CALL -> Uncomment to run test output
    #tests.RunSimulation(player_1,player_2,"StatVCall") #Test Type == StatVCall or StatVFold --> Can Be Added To
    #analysis.Analyse([tests.callbot_test_PokerCNN,tests.callbot_test_Statistic,tests.foldbot_test_PokerCNN,tests.foldbot_test_Statistic])
    #tests.WinRate("10000_StatsVSCallBot_Simulation.csv")
    
    #Call Analysis Functions
    analyse_cepheus_vs_callbot()

    analyse_cepheus_vs_Foldbot()
    
    analyse_cepheus_vs_statsbot()
    
    analyse_Callbot_vs_statsbot()
    
    analyse_Foldbot_vs_statsbot()
