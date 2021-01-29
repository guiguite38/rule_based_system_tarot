from tarot_lib import *

class Tricks():
    '''
    Class used to easily access data about past tricks, and resulting information 
    about the game (ex: strongest card in color).
    '''
    def __init__(self):
        self.tricks=[[]]*18
        self.winner_role=18*[0]        
        self.tricks_color=18*['']
        self.current_trick=0
        
        # ex tricks_color : { 'H' : 0, 'C' : 3, 'D' : 1, 'S' : 0}
        self.color_turns = { color:0 for color in COLOR_VALUES }

        # ex cut_colors : 'TAKER' : { 'H' : False, 'C' : False, 'D' : True, 'S' : False}
        self.cut_colors = { role: { color:False for color in COLOR_VALUES } for role in ROLES }
    
    def add_trick(self,trick,roles):
        '''
        Adds a new trick to the object -> all fields are updated with trick data
        '''
        turn=self.current_trick
        print(f"[Tricks.add_trick] turn is {turn}")
        self.tricks[turn]=trick
        self.winner_role[turn]=roles[trick.index(holder(trick))]
        print(f"[Tricks.add_trick] holder is {roles[trick.index(holder(trick))]} - taker's index is {roles.index('TAKER')}")        
        print(f"[Tricks.add_trick] trick is {trick}")        
        self.tricks_color[turn]=get_color(trick[0]) if trick[0]!=0 else get_color(trick[1])
        
        if self.tricks_color[turn] is not None:
            self.color_turns[self.tricks_color[turn]]=self.color_turns[self.tricks_color[turn]]+1

        # update cuts
        if self.tricks_color[turn] is not None:
            for i in range(4):
                if is_trump(trick[i]):
                    self.cut_colors[roles[i]][self.tricks_color[turn]]=True
                    #self.cut_colors[roles[i]][self.tricks_color[turn]]+1
        self.current_trick=turn+1
    
    def to_string(self):
        '''
        Displays the content of each field in Tricks
        '''
        print(f"\nturn : {self.current_trick}")
        print(f"tricks : {self.tricks}")
        print(f"winner : {self.winner_role}")
        print(f"color : {self.tricks_color}")
        # print(f"color turns : {self.color_turns}")
        print(f"cuts : {self.cut_colors}")
    
    def master(self, color):
        '''
        Returns the strongest card remaining in color        
        '''
        # TODO take the dog into account
        card_color_in_tricks = [card for trick in self.tricks for card in trick if get_color(card) is color]
        color_cards = [card for card in COLOR_CARDS if get_color(card) is color]

        color_cards.sort(key=get_index,reverse=True)
        for card in color_cards:
            if card not in card_color_in_tricks:
                return card
    
    def trump_master(self):
        '''
        Returns the trump master card
        '''
        trumps_in_tricks = [card for trick in self.tricks for card in trick if is_trump(card)]
        trumps=TRUMPS.copy()
        trumps.sort(reverse=True)
        
        for trump in trumps:
            if trump not in trumps_in_tricks:
                return trump
    
    def determine_trump_mastery(self,hand):
        '''
        Returns the number of trumps in hand that are master
        ex: having 21-20-19-17 at game start returns 3 (21-20-19 are untakable, 18 takes 17)
        '''
        trumps_in_tricks = [card for trick in self.tricks for card in trick if is_trump(card)]
        trumps=TRUMPS.copy()
        trumps.sort(reverse=True)
        
        masters=[]
        for trump in trumps:
            if trump not in trumps_in_tricks:
                if trump in hand:
                    masters.append(trump)
                else: 
                    return masters
    
    def compute_final_score(self, ecart):
        '''
        returns the sum of taker tricks + his dog if not empty
        '''
        # TODO Trump Fool must go back to his owner !!!
        taker_cards=[]
        if ecart is not []:
            for card in ecart:
                taker_cards.append(card)
        # print(f"[Tricks.compute_final_score] reference list is {self.winner_role}")
        for i in range(0,18):
            if self.winner_role[i] == 'TAKER':
                for card in self.tricks[i]:
                    taker_cards.append(card)
        print(f"[Tricks.compute_final_score] Taker got {self.winner_role.count('TAKER')} tricks\necart={taker_cards[:6]}\ntricks={taker_cards[6:]}")
        return compute_score(taker_cards), get_contract(taker_cards)

    def compute_cut_risk(self,color,role):
        '''
        Coputes the risk for a color to get cut
        Risk 0 is safe -> risk 100 is unsafe
        '''
        risk=0
        # TODO take hand cards and dog into account
        if role is 'TAKER':
            # TAKER won't play color's figures if getting cut
            for player in self.cut_colors:
                if self.cut_colors[player][color]:
                    risk=100
            # the more turns played the higher the risk
            if risk==0:
                risk=33*self.color_turns[color]
        else:
            # defense needs to open colors and then can moderately take risks
            if self.color_turns[color]==0:
                risk=70-25*sum(value == True for value in self.cut_colors['TAKER'].values())
            else:
                # color has been played or opened
                if self.cut_colors['TAKER'][color]:
                    risk = 100
                # less risk if allies cut
                # TODO : is that ok ?? ^^
                else:
                    allies_cutting=sum([1 for role in ROLES if self.cut_colors[role][color]] ) 
                    risk = 25*self.color_turns[color] - 25*(allies_cutting) -25*sum(value == True for value in self.cut_colors['TAKER'].values())
        return risk