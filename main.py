import pygame
class Card():
    deck_of_cards = []
    player_cards = []
    held_cards = [] 
    markiplier = 1
    def __init__(self, suit, number, face, img_path):
        self.suit = suit
        self.number = number
        self.face = face
        self.image = pygame.image.load(img_path)
        Card.deck_of_cards.append(self)

    def get_suit(self):
        return self.suit
    
    def get_val(self):
        return self.number
    
    def get_img(self):
        return self.image
    
    def get_face(self):
        return self.face

    def add():
        test = Card.markiplier + 1
        return test
    
    def player_deal(self):
        Card.deck_of_cards.remove(self)
        Card.player_cards.append(self) 
    
    def remove_player_card(self):
        Card.player_cards.remove(self)
        Card.held_cards.append(self)
    
    @classmethod
    def clear_player(cls):
        cls.deck_of_cards.extend(cls.player_cards)
        cls.player_cards.clear()

    @classmethod
    def get_total_card_val(cls):
        total_val = 0 
        for card in cls.player_cards:
            if isinstance(card, Card):
                total_val += card.get_val()
        return total_val
