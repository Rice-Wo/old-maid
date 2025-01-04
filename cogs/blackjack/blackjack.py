try:
    from .utility import *
except:
    from utility import *

import random
import logging


class blackjack_game:
    def __init__(self):
        self.player_hand = []
        self.computer_hand = []
        self.deck = []
        self.player_point = 0
        self.com_point = 0

    def generate_randomdeck(self) -> list: #生成一個打亂後的撲克牌組
        self.deck = []
        for suit in ['黑桃', '紅心', '方塊', '梅花']:
            for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
                self.deck.append(suit+rank)
        random.shuffle(self.deck)
        return self.deck 

    def get_card(self, deck: list) -> str:
        logging.debug(f'{len(self.deck)}')
        return deck.pop()

    def calculate_points(self, hand: list) -> int:
        point = 0
        A_num = 0
        for card in hand:
            if card[2] in ['J', 'Q', 'K']: 
                point += 10
            elif card[2] == 'A':
                A_num += 1 
            else:
                point += int(card[2:])
        point += A_num

        for _ in range(A_num):
            if point <= 11:
                point += 10

        return point
    

        

    def game_start(self)-> None:
        self.generate_randomdeck()
        self.player_hand = [self.get_card(self.deck) for _ in range(2)]
        self.computer_hand= [self.get_card(self.deck) for _ in range(2)]


    
    def game_add_card(self)-> None:
        self.player_hand.append(self.get_card(self.deck))
        self.player_point = self.calculate_points(self.player_hand)
            
    def game_end(self, hard=False)-> None:
        self.com_point = self.calculate_points(self.computer_hand)
        com_point = self.com_point
        if hard == False:
            while com_point < 17:
                self.computer_hand.append(self.get_card(self.deck))
                com_point = self.calculate_points(self.computer_hand)
        self.com_point = com_point
        self.player_point = self.calculate_points(self.player_hand)        



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    user = 'test'
    bj = blackjack_game(user)   
    bj.game_start()
    while True:
        print(bj.player_hand)
        wh = input('+=add card - =end')
        if wh == '+':
            bj.game_add_card()
        else:
            bj.game_end()
            player_point = bj.calculate_points(bj.player_hand)
            com_point = bj.calculate_points(bj.computer_hand)
            break
    print(f'player = {bj.player_hand}, {bj.player_point}')
    print(f'com = {bj.computer_hand}, {bj.com_point}')