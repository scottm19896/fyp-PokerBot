class Bot:
    def __init__(self):
        self.hand=[]
        self.board=[]
        self.position=0;
        self.stage=0
        self.hand_number=0
        self.dealer=False
        self.seat=0
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

def call(filepath):
    with open(filepath) as f:
        f.write('c')

def raise_(filepath):
    with open(filepath) as f:
        f.write('r')

def fold(filepath):
    with open(filepath) as f:
        f.write('f')
        
def read_game(bot,filepath):
    with open(filepath) as f:
        game=f.readline()[bot.position:]
    parse_string(bot,game)
    
def parse_string(bot,game):
    stage=bot.stage
    if stage==0:
        hand_divide=game.split('D')
        bot.update_hand_number(hand_divide[0])
        action_divide=hand_divide[1].split('P')
        if action_divide[0]==bot.seat:
            bot.dealer=True
        actions=action_divide[1]
        if len(actions)==0 or all(p == 'c ' for p in actions):
            call()
        '''Neural Network Calculation'''
        '''Decision r,c,f'''
        call()        
    if stage==1:
        flop_divide=game.split('F')
        for card in range(0,3):
            bot.add_board(flop_divide[card])
        flop_actions=flop_divide[3]
        if len(flop_actions)==0 or all(p == 'c ' for p in flop_actions):
            call()
        '''Neural Network Calculation'''
        '''Decision r,c,f'''
        
    if stage==2:
        turn_divide=game.split('T')
        bot.add_board(turn_divide[0])
        turn_actions=turn_divide[1]
        if len(turn_actions)==0 or all(p == 'c ' for p in turn_actions):
            call()
        '''Neural Network Calculation'''
        '''Decision r,c,f'''
        
    if stage==3:
        river_divide=game.split('T')
        bot.add_board(river_divide[0])
        river_actions=river_divide[1]
        if len(river_actions)==0 or all(p == 'c ' for p in river_actions):
            call()
        '''Neural Network Calculation'''
        '''Decision r,c,f'''
        
    if stage==4:
        
        '''Neural Network Calculation'''
        '''Decision r,c,f'''
        
