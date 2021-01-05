import random

#############
### CARDS ###
#############

FIGURES = ['J','P','Q','K']
FIGURES_NAMES = ["Jack","Knight","Queen","King"]
NON_FIGURES = ['1','2','3','4','5','6','7','8','9','10']
CARD_VALUES = NON_FIGURES + FIGURES

COLOR_VALUES = [ 'H', 'C', 'D', 'S']
COLOR_NAMES = ["Hearts","Clubs","Diamonds","Spades"]

TRUMPS = [ i for i in range(0,22)]
OUDLERS = [0, 1, 21]

COLOR_CARDS = [ COLOR_VALUES[j]+str(CARD_VALUES[i]) for j in range(4) for i in range(len(CARD_VALUES))]

PLAYING_CARDS = TRUMPS + COLOR_CARDS

### BIDS ###

BIDS=['PASS','TAKE','PUSH','GUARD','GUARD WITHOUT','GUARD AGAINST']    
BID_VALUES=[0,10,20,40,60,80]
# quantiles are computed from 1345 takings out of 10K bidings
QUANTILES=[1.005, 1.015, 1.035, 1.045, 1.065, 1.075, 1.105, 1.135, 1.185]
ROLES=['TAKER','OPENER','NEUTRAL','RELAUNCHER']


######################
### CARD FUNCTIONS ###
######################

def get_card_role(card):
    # TODO : check else clause validity
    return card[1:] if card not in TRUMPS else card

def is_figure(card):
    return get_card_role(card) in FIGURES

def is_non_figure(card):
    return get_card_role(card) in NON_FIGURES

def is_trump(card):
    return type(card) is int

def is_oudler(card):
    return card in OUDLERS

def get_color(card):
    return card[0] if not is_trump(card) else None


### TESTS ###
# sampling = random.sample(PLAYING_CARDS,2)

# for card in sampling:
#     print(f"\n=== Card : {card} ===\nCard value : {get_card_role(card)}\nis figure : {is_figure(card)}\nis not figure {is_non_figure(card)}\nis trump : {is_trump(card)}\nis oudler : {is_oudler(card)}\nhas color : {get_color(card)}")

###################################################
# Hand Management : Sorting, Showing, Information #
###################################################

# UTILITY FUNCTION
def get_index(card):
    '''Utility function used to sort cards.'''
    return PLAYING_CARDS.index(card)

# UTILITY FUNCTION
def get_card_value(card):
    return (get_index(card)-22)%14+1 if not is_trump(card) else 14+card if card!=0 else 0

# UTILITY FUNCTION
def sort_cards(hand):
    return hand.sort(key=get_index)

# UI FUNCTION
def to_string(card):
    if is_trump(card):
        if card != 0:
            return(f"Trump {card}")
        else:
            return(f"Trump Fool")
    else:
        return(f"{COLOR_NAMES[COLOR_VALUES.index(card[0])]} {FIGURES_NAMES[FIGURES.index(card[1:])] if is_figure(card) else card[1:]}")

# UI FUNCTION
def show_cards(cards):
    for card in cards:
        print(to_string(card))

# HAND FUNCTION
def get_trump_cards(hand):
    return [card for card in hand if is_trump(card)]
def get_trump_count(hand):
    return sum([1 for card in get_trump_cards(hand)])

# HAND FUNCTION
def get_color_cards(hand,color):
    return [card for card in hand if get_color(card)==color]
def get_color_count(hand,color):
    return sum([1 for card in get_color_cards(hand,color)])

### TESTS ###
# for card in PLAYING_CARDS:
#     print(get_card_value(card))


####################
# TRICK MANAGEMENT #
####################

def holder(trick):
    '''
    Is holding the highest card in opening color or biggest trump.
    Returns the card holding the trick so far.
    '''
    # 1 card played means holder is opener
    if len(trick) == 1:
        return trick[0]

    top_trump = 0
    # check if trump holds      
    for card in trick:
        if is_trump(card):
            if card > top_trump:
                top_trump=card
    if top_trump > 0:
        return top_trump

    # find holder in color -> there can be no trump in trick except Trump Fool
    else:
        color=get_color(trick[0]) if get_color(trick[0]) is not 0 else get_color(trick[1])
        # cards are valid if belonging to the color called for
        valid_cards = [card for card in trick if get_color(card) is color]
        sort_cards(valid_cards)
        return valid_cards[-1]


### TESTS ###
# for i in range(3):
#     trick = random.sample(PLAYING_CARDS, random.randint(2,4))
#     print(f"Trick is : {trick}")
#     print(f"Holding card is {to_string(holder(trick))}\n")


##########
# BIDING #
##########

CONTRACTS = [56,51,41,36]
POINTS = [1.5,2.5,3.5,4.5]

# CARD + SCORING FUNCTION
def get_card_points(card):
    if is_trump(card):        
        return 4.5 if card in OUDLERS else .5
    else:
        return .5 if card[1] in NON_FIGURES else POINTS[FIGURES.index(card[1])]

# HAND + SCORING FUNCTION
def compute_score(cards):
    return sum(get_card_points(card) for card in cards)

# HAND + SCORING FUNCTION
def get_contract(hand):
    return CONTRACTS[sum([1 for card in hand if is_oudler(card)])]