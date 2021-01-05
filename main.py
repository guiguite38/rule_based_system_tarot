from tarot_lib import *
import player
import game
import tricks

def main():
    myGame = game.Game()
    bids = myGame.bid()
    print(f"[Game.TEST] bids are {bids[1]}")

    if bids[1].count('PASS')!=4:
        for player in myGame.players:
            if player.role is 'TAKER':
                myGame.taker_id=myGame.players.index(player)
                print(f"[Game.TEST] TAKER estimated win factor is : {myGame.estimate_win_factor(player.hand)} (max expected is around 1.25, below 1 is more risky)")
                # print(f"[Game.__init__]found {player.role}, id is {self.taker_id}")
        print(f"[Game.TEST] displaying roles {[player.role for player in myGame.players]}")

        myGame.incorporate_dog(myGame.players[myGame.taker_id])
        sort_cards(myGame.ecart)
        if myGame.contract not in ['GUARD WITHOUT','GUARD AGAINST']:
            print(f"[Game.TEST] TAKER has elected ecart={myGame.ecart}")
        myTakerHand=myGame.players[myGame.taker_id].hand
        sort_cards(myTakerHand)
        print(f"[Game.TEST] TAKER hand is {myTakerHand}")

        for i in range(18):
            myGame.play_trick()
        # myGame.tricks.to_string()
        score,contract=myGame.tricks.compute_final_score(myGame.ecart)
        print(f'\nTaker final score is {score} with contract {contract}')
        if score>=contract:
            print('Taker wins !')
        else:
            print('Defense wins !')
    # print(player.role for player in myGame.players)

if __name__ == "__main__":
    main()