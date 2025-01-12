import pygame 
class Card():
    # 200 points = run 
    # 50 points = 1 pair of cards
    # 100 points = 2 pairs of cards
    # 60 points = three of a kind

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

    @classmethod
    def get_possible_combination(cls):
        num_of_cards = []
        suit_of_cards = []
        # checks if each player card is an actual Card object. This is in order to use specific unique Card methods.
        check_player_cards = [card for card in cls.player_cards if isinstance(card, Card)]
        # sorts cards based on a sorting key, that each Card object should be sorted based on the numeric value, and then on what each suit alphabetically is.
        sorted_cards = sorted(check_player_cards, key = lambda card : (card.get_val(), card.get_suit()))
        prev_loc = None
        card_run = False
        is_pair = False
        three_kind = False
        pair_count = 0
        for card in sorted_cards:
            if isinstance(card, Card):
                num_of_cards.append(card.get_val())
                suit_of_cards.append(card.get_suit())

        # checking for a run 
        for i in range(len(num_of_cards) - 1):
            if prev_loc is not None:
                if prev_loc == num_of_cards[i] - 1:
                    prev_loc = num_of_cards[i]
                else:
                    prev_loc = None
                    break
            else:
                prev_loc = num_of_cards[i]
        if prev_loc == num_of_cards[-1]:
            card_run = True
        if card_run:
            points = (cls.get_total_card_val() + 200) * cls.markiplier
            return points

        # one pair of cards/two pairs.
        for i in range(len(num_of_cards) - 1):
            if num_of_cards[i] == num_of_cards[i + 1]:
                pair_count += 1
        if pair_count > 0:
            is_pair = True       
        if is_pair:
            points = cls.get_total_card_val() + 50 * pair_count * cls.markiplier
            return points

        # three of a kind
        for i in range(len(num_of_cards) - 2):
            if num_of_cards[i] == num_of_cards[i + 1] == num_of_cards[i + 2]:
                three_kind = True
                break
        if (three_kind):
            points = (cls.get_total_card_val() + 60) * cls.markiplier
