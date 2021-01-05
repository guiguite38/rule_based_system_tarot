import player as p
import tricks as t
from tarot_lib import *

class Game():
    """DOC"""

    def __init__(self, *args, **kwargs):
        """DOC"""
        hand0,hand1,hand2,hand3,dog=self.deal()
        self.hands = [hand0,hand1,hand2,hand3]
        for hand in self.hands:
            sort_cards(hand)
        self.dog = dog
        self.ecart=6*[0]
        self.players = [p.Player(hand) for hand in self.hands]
        
        self.contract=None
        self.dealer = 0
        self.first_player = 1
        self.tricks=t.Tricks()
        self.taker_id=-1

    # GAME FUNCTION
    def deal(self):
        '''Returns 4 hands of 18 cards + a dog of 6 cards'''
        deck = PLAYING_CARDS.copy()
        random.shuffle(deck)
        return [deck[0:18],deck[18:36],deck[36:54],deck[54:72],deck[72:78]]

    # GAME FUNCTION
    def bid(self):
        '''
        Computes win_factor for each player
        Returns taker_id, announces
        '''
        current_bid=BID_VALUES[0]
        player_bids = [0,0,0,0]
        for i in range(4):
            win_factor = self.estimate_win_factor(self.players[i].hand)
            if win_factor<.9:
                pass
            else:
                # TAKE
                if win_factor < QUANTILES[3] and current_bid<BID_VALUES[1]:
                    player_bids[i]=BID_VALUES[1]
                    current_bid=BID_VALUES[1]
                    self.contract='TAKE'
                    self.taker_id=i
                # PUSH
                elif win_factor < QUANTILES[5] and current_bid<BID_VALUES[2]:
                    player_bids[i]=BID_VALUES[2]
                    current_bid=BID_VALUES[2]
                    self.contract='PUSH'
                    self.taker_id=i
                # GUARD
                elif win_factor < QUANTILES[7] and current_bid<BID_VALUES[3]:
                    player_bids[i]=BID_VALUES[3]
                    current_bid=BID_VALUES[3]
                    self.contract='GUARD'
                    self.taker_id=i
                # GUARD WITHOUT
                elif win_factor < QUANTILES[8] and current_bid<BID_VALUES[4]:
                    player_bids[i]=BID_VALUES[4]
                    current_bid=BID_VALUES[4]
                    self.contract='GUARD WITHOUT'
                    self.taker_id=i
                # GUARD AGAINST
                elif current_bid<BID_VALUES[5]:
                    player_bids[i]=BID_VALUES[5]
                    current_bid=BID_VALUES[5]
                    self.contract='GUARD AGAINST'
                    self.taker_id=i
                    
        if max(player_bids) is 0: 
            print("[Game.bid] No one took : you may re-run the code until one player takes !")
        else:
            for i in range(4):
                self.players[(player_bids.index(max(player_bids))-i)%4].role=ROLES[i%4]
        
        return player_bids.index(max(player_bids)),[BIDS[BID_VALUES.index(bid)] for bid in player_bids]

    # HAND + SCORING FUNCTION
    def estimate_win_factor(self, hand):
        '''
        2 essential params : number of trump cards + actual score
        each has .5 potential influence -> the closest to 1, the higher the chances of victory
        '''
        # compare actual points vs needed
        # TODO : check if hands valued under 1 are worth taking
        score_param = .5 + .02*(compute_score(hand) + 10 - get_contract(hand))
        
        # ratio of actual trump count VS mean    
        # trump_mean = 0 if get_trump_count(hand)==0 else sum([10 if card is 0 else card for card in hand if is_trump(card)]) / get_trump_count(hand)

        # TODO : biggest trumps have more value
        trump_param = .5 + 0.05*(get_trump_count(hand)-22/4)
        
        return score_param + trump_param

    def incorporate_dog(self,player):
        '''
        Add 6 dog cards to TAKER hand.
        Then removes 6 cards from TAKER hand.
        '''
        #TODO incorporate DEPENDS on CONTRACT

        if self.contract is 'GUARD AGAINST':
            self.ecart=[]
            return 0
        elif self.contract is 'GUARD WITHOUT':
            self.ecart=self.dog
            return 0    

        for card in self.dog:
            player.hand.append(card)

        ecartables=[self.is_ecartable(get_color_cards(player.hand,color)) for color in COLOR_VALUES]

        print(f"[Game.incorporate_dog] Color {COLOR_VALUES[ecartables.index(max(ecartables))]} chosen for ecart of type [CUT or KING CINGLETTE]: {get_color_cards(player.hand,COLOR_VALUES[ecartables.index(max(ecartables))])}")
        # TODO what else can be done ?
        ecart_count=0
        chosen_color=COLOR_VALUES[ecartables.index(max(ecartables))]

        # ecart first color
        for card in get_color_cards(player.hand,COLOR_VALUES[ecartables.index(max(ecartables))]):
            if not get_card_role(card)=='K':
                self.ecart[ecart_count]=card
                player.hand.remove(card)
                ecart_count=ecart_count+1
        
        new_ecartables=[self.is_ecartable(get_color_cards(player.hand,color)) for color in COLOR_VALUES]

        # ecart second color
        ecart_2 = False
        if ecart_count < 6:
            for color in COLOR_VALUES:
                if color is not chosen_color:
                    if new_ecartables[COLOR_VALUES.index(color)]>.6 and len(get_color_cards(player.hand,color))<=6-ecart_count:
                        print(f"[Game.incorporate_dog] Second color {color} was chosen for ecart [CUT or KING CINGLETTE] : {get_color_cards(player.hand,color)}")
                        ecart_2 = True
                        for card in get_color_cards(player.hand,color):
                            if not get_card_role(card)=='K':
                                self.ecart[ecart_count]=card
                                player.hand.remove(card)
                                ecart_count=ecart_count+1
        
        # create cinglette
        if ecart_2 == False and ecart_count<6:
            for color in COLOR_VALUES:
                if color is not chosen_color:
                    if new_ecartables[COLOR_VALUES.index(color)]>.6 and len(get_color_cards(player.hand,color))<=7-ecart_count:
                        print(f"[Game.incorporate_dog] Second color {color} was chosen for ecart [CINGLETTE] : {get_color_cards(player.hand,color)}")
                        cards=get_color_cards(player.hand,color)
                        cards.sort(key=get_index,reverse=True)
                        for card in cards:
                            if not get_card_role(card)=='K' and is_figure(card):
                                self.ecart[ecart_count]=card
                                player.hand.remove(card)
                                ecart_count=ecart_count+1
                        cards.sort(key=get_index,reverse=False)
                        for card in cards:
                            if ecart_count<6:
                                self.ecart[ecart_count]=card
                                player.hand.remove(card)
                                ecart_count=ecart_count+1

        # TODO do a better ecart by removing orphan figures (such as knight or jack)
        while ecart_count<6:
            card=random.choice(player.hand)
            # pick random cards except kings and trumps
            if not is_trump(card) and not get_card_role(card)=='K':
                self.ecart[ecart_count]=card
                print(f"[Game.incorporate_dog] card {card} was picked RANDOMLY to complete the ecart")
                player.hand.remove(card)
                ecart_count=ecart_count+1

    def is_ecartable(self, cards):
        '''
        Computes if a color can be fully put in ecart.
        Empirical threshold is 0.6 : 1 means color is ecartable.
        '''
        # ecart if count_factor close to 1
        count_factor=(14-len(cards))/14 if len(cards) < 7 else -.5
        # ecart if score_factor close to 1
        score_factor=((4.5+3.5+2.5+2.5)-compute_score([card for card in cards if is_figure(card)]))/(4.5+3.5+2.5+2.5)
        # score has more value than nb of cards
        return (count_factor+2*score_factor)/3

    # GAME FUNCTION
    def play_trick(self):
        '''
        Each player plays one card.
        First player is opener, the rest simply answer.
        The strongest determines the trick's winner.
        '''
        current_trick=[]
        roles=[0,0,0,0]
        if len(self.players[0].hand) == 18:
            self.first_player = (self.dealer+1)%4
        else:
            for player in self.players:
                if player.role is self.tricks.winner_role[18-(len(player.hand)+1)]:
                    self.first_player = self.players.index(player)
                    print(f'[Game.play_trick] Next first player should be {self.players[self.first_player].role}')

        print("\n[Game.play_trick] === NEW TRICK ===")
        for i in range(4):
            # players should play in the right order
            player_id=(self.first_player+i)%4
            player=self.players[player_id]
            taker_turn=(self.taker_id+4-self.first_player)%4+1
            # print("[Game.play_trick] displaying roles")
            # print(f"[Game.play_trick] player_id is {player_id}")
            # print(f"[Game.play_trick] current player is {player.role}")
            roles[i]=player.role
            # print(f"[Game.play_trick] taker will play as {taker_turn}")
            chosen_card=self.players[(self.first_player+i)%4].play_card(current_trick,taker_turn-1,self.tricks,is_first=((self.first_player+i)%4==self.first_player))
            # print(f"[Game.play_trick] chosen card : {chosen_card}")
            current_trick.append(chosen_card)
        # print(f"[Game.play_trick] called function [tricks.add_trick] over trick={current_trick} and roles {roles}")
        self.tricks.add_trick(current_trick,roles)
        # print(f"[Game.play_trick] winner_role list is now : {self.tricks.winner_role}")