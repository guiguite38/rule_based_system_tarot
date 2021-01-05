from tarot_lib import *

class Player():
    def __init__(self, hand, *args, **kwargs):
        '''
        A player is defined by :
        - his role (as taker or in the defense)
        - his hand (initially 18 cards)
        '''
        self.role = kwargs.get('role',None)
        self.hand = hand.copy()

    def play_card(self,current_trick,taker_id,tricks,**kwargs):
        '''
        Returns the choice of a card from the player.
        Removes the chosen card from his hand.
        '''
        is_first_player=kwargs.get("is_first",False)
        if is_first_player:
            card = self.open(tricks)
            if card is None:
                print(f"[Player.play_card] ERROR IN OPEN FUNC -> returned NONE")
        else:
            card = self.answer(current_trick,taker_id,tricks)
            if card is None:                
                print(f"[Player.play_card] ERROR IN ANSWER FUNC -> returned NONE")
        # print(f"[Player.play_card] {self.role} hand is : {self.hand}")
        # print(f"[Player.play_card] chosen card is : {card}")
        self.hand.remove(card)
        return card

    # TRICK + PLAYER FUNCTION
    def open(self, tricks):
        '''
        Implements the way of opening for each 3 role
        '''
        # masters = [master(color,tricks) for color in COLOR_VALUES]
        masters = [tricks.master(color) for color in COLOR_VALUES]
        # print(f"[Player.open] masters are : {masters}")

        if self.role is 'TAKER':
            # try to play strong figures
            # TODO modify ! this is stupid
            for card in self.hand:
                if card in masters:
                    if card is None:
                        print('[Player.open] ERROR 1')
                    print(f"[Player.open] TAKER opens with STRONG FIGURE")
                    return card

            # try to play 'longe'
            for color in COLOR_VALUES:
                color_cards_in_hand = get_color_cards(self.hand,color)
                color_mean = 14-sum([1 for trick in tricks.tricks for card in trick if get_color(card) is color])-len(color_cards_in_hand)/3
                if len(color_cards_in_hand) > color_mean + 3:
                    if get_card_points(card) < 2.5:
                        card=color_cards_in_hand[0]         
                        if card is None:
                            print('[Player.open] ERROR 2')
                        print(f"[Player.open] TAKER opens with PLAY LONGE")
                        return card

            # make trumps fall
            #*3/7 makes player play his 3rd trump when having 7, which should be acceptable
            # TODO check if trump value is coherent (7<val<12 is optimal)
            trump_count = get_trump_count(self.hand)
            trump_mean = (22 - sum([1 for trick in tricks.tricks for card in trick if is_trump(card)]) - trump_count)/3
            if trump_count >  trump_mean + 3:                
                card=get_trump_cards(self.hand)[int(trump_count*3/7)]
                if card is None:
                    print('[Player.open] ERROR 3')
                print(f"[Player.open] TAKER decides to force trump fall")
                return card

            # TODO define what else can be done
            print(f'[Player.open] {self.role} opened with random card')
            card = random.choice(self.hand)
            if card is None:
                print('[Player.open] ERROR 6')
            return card

        elif self.role is 'OPENER':            
            tricks.color_turns
            # try to open new color
            for color in tricks.color_turns:
                if tricks.color_turns[color] == 0:
                    color_cards_in_hand = get_color_cards(self.hand,color)
                    good_opener = [color_card for color_card in color_cards_in_hand if not is_figure(color_card)]
                    if len(good_opener) > 0:
                        card=good_opener[-1]
                        if card is None:
                            print('[Player.open] ERROR 4')
                        print(f"[Player.open] {self.role} opens NEW COLOR {get_color(card)}")
                        return card
            # TODO define what else can be done
            card = random.choice(self.hand)
            if card is None:
                print('[Player.open] ERROR 6')
            print(f"[Player.open] {self.role} opens with RANDOM CARD")
            return card
        else:
            # roles other than TAKER and OPENER
            # TODO change this !!!
            card = random.choice(self.hand)
            if card is None:
                print('[Player.open] ERROR 5')            
            print(f"[Player.open] {self.role} opens with RANDOM CARD")
            return card
            
        #     # re-open colors
        #     # TODO manage taker cutting
        #     # TODO manage usefulness of opening (figures left)
        #     for color in hand:
        #         if figures fall count < 3:
        #             return re-open color

        #     # TODO define what else can be done
        #     return random.choice(hand)

        # elif self.role is 'RELAUNCHER':
        #     # try to relaunch color
        #     # try to get information if figures in color

    # TRICK + PLAYER FUNCTION
    def answer(self, current_trick, taker_id, tricks):
        '''
        If a player doesn't open, he has to answer to the opening card
        '''
        opening = current_trick[0]

        # Answer to a trump opening
        if is_trump(opening):
            if get_trump_count(self.hand) > 0:
                print(f"[Player.answer] {self.role} has to overtrump with one of {get_trump_count(self.hand)} trumps")
                return self.cutOrClimb(current_trick,taker_id) if opening!=0 else self.open(tricks)
            else:
                print(f"[Player.answer] player can't play trump and discards")
                return self.discard(current_trick,taker_id,tricks)
        # Answer to a color opening
        else:            
            color=get_color(opening)
            cards_in_color=get_color_cards(self.hand,color)            
            # print(f"[Player.answer] opening color is {color} and cards_in_color is {cards_in_color}")
            if len(cards_in_color)>0:
                # TODO compute risk of playing figure
                # print(f"[Player.answer] {self.role} CAN answer in color")
                if len(cards_in_color)==1:
                    print(f"[Player.answer] {self.role} CAN answer in color - plays LAST CARD in color")
                    return cards_in_color[0] 
                else: 
                    return self.play_color(current_trick,cards_in_color,color,tricks,taker_id)

            # cut : player has trumps, he must use them
            elif get_trump_count(self.hand) > 0:
                print(f"[Player.answer] {self.role} CAN NOT answer : he trumps or overtrumps")
                return self.cutOrClimb(current_trick,taker_id)

            # discard : player has no trump, nor cards in color
            else:
                print(f"[Player.answer] {self.role} CAN NOT answer nor trump : he discards")
                return self.discard(current_trick,taker_id,tricks)

    # TRICK + PLAYER FUNCTION
    def play_color(self,current_trick,cards_in_color,color,tricks,taker_id):
        '''
        Player has to answer in color if he can except if he has Trump Fool.
        He might want to take risk, or not.        
        '''
        holding_card = holder(current_trick)
        # taker is safe if last
        if self.role is 'TAKER':
            safe = len(current_trick) is 3
        # player isnt taker -> safe if taker hasnt played
        # TODO take cuts into account (what if RELAUNCHER cuts ?!)
        else:
            safe = len(current_trick)>taker_id
        
        # risk 0 is safe -> risk 100 is unsafe
        risk = tricks.compute_cut_risk(color,self.role)

        #play figure if safe and figure can master trick
        #TODO what if ally holds trick ?!
        if safe and get_card_value(holding_card) < get_card_value(cards_in_color[-1]) and is_figure(cards_in_color[-1]):  
            print(f"[Player.answer] {self.role} CAN answer in color - plays FIGURE")
            return cards_in_color[-1]
        # play figure if not too risky and master in color
        elif tricks.master(color)==cards_in_color[-1] and risk < 50 and is_figure(cards_in_color[-1]):
            return cards_in_color[-1]
        else:
            print(f"[Player.answer] {self.role} CAN answer in color - plays LOWEST card in color")
            return cards_in_color[0]
            
        print(f"[Player.answer] {self.role} CAN answer in color with RANDOM")
        return random.choice(cards_in_color)
        
    
    # TRICK + PLAYER FUNCTION
    def cutOrClimb(self,current_trick,taker_id):
        '''Player has to trump or overtrump.'''    
        player_trumps = get_trump_cards(self.hand)

        # player has 1 trump : he must play it
        # TODO take fool into consideration
        if len(player_trumps) is 1:
            return player_trumps[0]

        trick_trumps = [card for card in current_trick if is_trump(card)]
        ref = max(trick_trumps) if len(trick_trumps) > 0 else 0
        
        # TODO define what is safe to TAKER
        # safe = False if taker_id > len(current_trick) else not holder(current_trick)==current_trick[taker_id]
        safe = False if taker_id > len(current_trick) else True if taker_id==len(current_trick) else not holder(current_trick)==current_trick[taker_id]

        # climb or cut
        if max(player_trumps) > ref:
            # try play 1
            if 1 in player_trumps and safe and 1>ref:
                return 1
            for trump in player_trumps:
                if trump > ref: return trump
        # discard
        else:
            #try play 1
            if 1 in player_trumps and safe:
                return 1
            #discard anything
            else:
                sort_cards(player_trumps)
                for card in player_trumps:
                    if card != 1:
                        return card
                return player_trumps[0]

    # TRICK + PLAYER FUNCTION
    def discard(self,current_trick,taker_id,tricks):
        '''
        Never safe to discard as TAKER.
        Safe to discard if TAKER not holding.
        If SAFE -> Policy is to discard FIGURES with priority given to cut colors.
        '''
        # TODO update cut_color for player (as long as he has no more trumps !)                    
        if sum(value == True for value in tricks.cut_colors[self.role].values())==0:
            for color in COLOR_VALUES:                
                tricks.cut_colors[self.role][color]=False
            # print(f"[Player.discard] {self.role} discarded and got his cuts reset")

        safe = False if taker_id >= len(current_trick) else not holder(current_trick)==current_trick[taker_id]
        
        if safe:
            # TODO is discarding figures the best option ? what if taker out of trumps ?
            # discard figure in color cut by TAKER
            for color in tricks.cut_colors['TAKER']:
                if tricks.cut_colors['TAKER'][color]:
                    color_cards=get_color_cards(self.hand,color)
                    # check if player has cards in cut colors
                    if len(color_cards)>0:
                        color_cards.sort(key=get_index,reverse=True)
                        # play figures
                        for card in color_cards:
                            if is_figure(card):
                                print(f'[discard] {self.role} chose to discard in cut color')
                                return card
            #TODO get an idea of the game state : losing ? winning ? if losing then discard other figures !
            # for now we simply discard any possible figure
            for color in COLOR_VALUES:
                color_cards=get_color_cards(self.hand,color)
                # check if player has cards in cut colors
                if len(color_cards)>0:
                    color_cards.sort(key=get_index,reverse=True)
                    # play figures
                    for card in color_cards:
                        if is_figure(card):
                            print(f'[discard] {self.role} choses to discard figure')
                            return card
            # TODO default will be discarding lowest -> get more value
        else:
            # TODO think about what to do if unsafe ?
            # ex : discard card in color cut by TAKER
            pass
        
        # player has nothing of value : he discards his lowest card
        lowest=self.hand[0]
        for card in self.hand:
            if get_card_value(card)<get_card_value(lowest):
                lowest = card
        print(f'[Player.discard] {self.role} chose to discard his lowest card')
        return lowest