Logs Folder -> Contains output files and log files.
src Foldr -> Contains all source code.

Ensure Python 3 is installed:

	

If not, download latest version via Anaconda:
	

https://www.anaconda.com/distribution/#download-section



Once Python 3 installed, install the libraries using the given commands. (Some of these may already be installed through Anaconda):


	Treys:
	pip install treys

	

	Pandas:(To run ExperimentSuite.py)

	
	pip install pandas

	

	Matplotlib:(To run ExperimentSuite.py)
	

	pip install matplotlib

	
	
	Pytest:(To run test_suite.py)

	
	pip install pytest



——————	Casino ————————————————————————————————————————————————



To run Casino file:

	

DEFAULT SET UP -> 2 Game Simulation , Callbot vs Callbot
	
	

From Command Line/Prompt:
	
	

Change directory to $Path_To_Casino source code:

	
	
e.g cd ~\Downloads\14570733\supporting\src

	

python HeadsUpLimitHoldemCasino.py

	

(Pretty Card Printout is disabled in command line. Run in Spyder for more details)

—OR—

	

Open Anaconda Navigator -> Open Spyder -> 
	
Open HeadsUpLimitHoldemCasino.py -> Click Run -> Output printed to console.


	
	——————	OPTIONAL ————————————————————————————————————————————————

	

Open up file, bot type can be changed in main() function: 

	

For statistical bot, ResetFoldPercent() should be called before playing game.

	
	
e.g StatisticalBot creation —> bot_1 = StatisticalBot()
				       
bot_1.ResetFoldPercent(0.25) #To Set 25% fold rate


	
BotX used in creation of Call/Fold/Random Bot:

	
	
e.g BotX -> bot_1 = Bot()
		    
bot_1.X = ‘c’ #CallBot		
		    
bot_1.X = ‘f’ #FoldBot
		   
bot_1.X = ‘cr’ #Random choice between raise and call

	

To print game_summary to file, uncomment both lines with ‘self.Game_Summary’
	
Name of file can be changed at the top.



——————	Experiment Suite ————————————————————————————————————————————————



To run ExperimentSuite file:


	
Open file in text editor.
	

Change FOLDER_PATH to Logs directory and include ‘/’ after:

	
e.g FOLDER_PATH = ‘/User/Username/Downloads/14570733/supporting/Logs/’
	
	

(Plots can only be seen from Notebook or Spyder Console, not from command line)

From Command Line/Prompt:
	

	
Change directory to $Path_To_ExperimentSuite source code:

	
	
e.g cd ~\Downloads\14570733\supporting\src

	

python ExperimentSuite.py


	
—OR—

	

Open Anaconda Navigator -> Open Spyder -> 
	
Open ExperimentSuite.py -> Click Run -> Output printed to console.


	
—OR—

	

Open Anaconda Prompt -> run jupyter notebook command (i.e jupyter notebook)

	

This opens new notebook in internet browser.

	
Find ExperimentSuite.ipynb and open it.
	
	
SHIFT + ENTER runs cell

	

	——————	OPTIONAL ————————————————————————————————————————————————

	

	To run tests class, follow instruction under main.




——————	test_suite.py  ————————————————————————————————————————————————



To run test_suite.py file:
	
	

From Command Line/Prompt:
	
	

Change directory to $Path_To_testsuite.py source code folder:
	
	

e.g cd ~\Downloads\14570733\supporting\src

	

pytest -v test_suite.py

	
	
	

