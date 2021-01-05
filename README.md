# rule_based_system_tarot
Humain-crafted rule set aiming at interpreting information about a card game (tarot) and reacting in an appropriate way.

The idea here is to implement an ensemble of rules and conventions in French Tarot* so that the "players" make oriented decisions, which increases their individual chance of victory.

--- IMPORTANT NOTICE ---
There are 2 ways of running this project :
- either by running main.py
- alternatively, you can run the "game_modelisation.ipynb" python notebook

--- MAIN FEATURES ---
in Player class :
- open() -> "What should I do if I must play the first card of the trick ?"
- answer() -> "What card should I play if first player has already chosen a color ?"

in Game class :
- estimate_win_factor() -> "How great are my chances of victory ?"
- incorporate_dog() -> "If I am Taker and may realize an 'ecart' (depends on biding), what cards should be put aside ?"

in Tricks class :
- compute_cut_risk() -> "Is playing this card safe ?"


--- NOTE CONCERNING WIP MENTIONS ---
This was an ambitious project compared to the amount of time I was given, which leads to some undevelopped ideas (tagged TODO).
I left them to reflect my methodology and reflexions while elaborating this rule based system :)

*French Tarot rules are available here : https://www.pagat.com/tarot/frtarot.html
