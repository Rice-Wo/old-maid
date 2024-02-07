try:
    from .utility import *
except:
    from utility import *

import random


class blackjack_game:
    def __init__(self, user: str|int):
        self.id = str(user)
        self.data = get_data('blackjack')

        self.player_hand = []
        self.computer_hand = []

    def generate_randomdeck(self) -> list: #生成一個打亂後的撲克牌組
        deck = []
        for suit in ['黑桃', '紅心', '方塊', '梅花']:
            for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
                deck.append(suit+rank)
        random.shuffle(deck)
        return deck 

    def get_card(self, deck: list) -> str:
        return deck.pop()

    def calculate_points(self, hand: list) -> int:
        point = 0
        for card in hand:
            if card[2] in ['J', 'Q', 'K']:
                point += 10
            elif card[2] == 'A':
                point += 11
            else:
                point += int(card[2:])
        return point




if __name__ == '__main__':
    user = 'test'
    bj = blackjack_game(user)

    deck = bj.generate_randomdeck()
    
    hand = [bj.get_card(deck) for _ in range(2)]
    point = bj.calculate_points(hand)
    print(hand)
    print(point)
    