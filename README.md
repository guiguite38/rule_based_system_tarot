# Rule Based System for Tarot
## Created by Guillaume Grosse

## Project in a nutshell

Humain-crafted rule based system (RBS) aiming at implementing an ensemble of rules and conventions in French Tarot* so that the "players" make oriented decisions, increasing their individual chance of victory.

*French Tarot rules are available here : https://www.pagat.com/tarot/frtarot.html


## Running the project
- run main.py
- or run game_modelisation.ipynb python notebook


## Context
Project : Knowledge Representation
Course : Artificial Intelligence
Enginneering Schools Associated : ENSC and ENSEIRB  
Duration : 2 month


## Main features

player.py
---------
General class to manage a player hand and gameplay.
Main RBS features :
- open() -> "What should I do if I must play the first card of the trick ?"
- answer() -> "What card should I play if I am not the first player (hence, what should I answer ?) ?"


game.py
-------
Class designed to handle main game aspects : dealing, bids, ecart and trick succession.
Main RBS features :
- estimate_win_factor() -> "How great are my chances of victory ?"
- incorporate_dog() -> "If I am Taker and may realize an 'ecart' (depends on biding), what cards should be put aside ?"
- bid() -> "Is my hand strong enough to 'take' ?"


tricks.py
---------
Class used to easily access data about past tricks, and resulting information about the game (ex: strongest card in color).
Main RBS features:
- compute_cut_risk() -> "Can I play safely in this color ?"


tarot_lib.py
------------
Library of general functions and variables, used to handle some aspects of the cards, hands, tricks and biding.
Main RBS features:
- QUANTILES : general distribution of estimated win factors, used for bids.


game_modelisation.ipynb
-----------------------
Notebook version of the code computed through main and other .py files.


## Possible improvements

Reducing  random play in open() and answer() functions would lead to significantly better results.


## Note concerning TODO mentions

This was an ambitious project compared to the amount of time I was given, which leads to some undevelopped ideas (tagged TODO).
I left them to reflect my methodology and reflexions while elaborating this rule based system :)
