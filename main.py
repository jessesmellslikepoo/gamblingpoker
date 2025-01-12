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
        card_run = False
        three_kind = False
        four_kind = False
        run_fail = False
        is_flush = True
        roy_flush = False
        pair_count = 0
        num_count = 1
        for card in sorted_cards:
            if isinstance(card, Card):
                num_of_cards.append(card.get_val())
                suit_of_cards.append(card.get_suit())

        # checking for a run and a pair  
        for i in range(len(num_of_cards) - 1):
            # run checking...
            if not run_fail and num_of_cards[i] != num_of_cards[i + 1] - 1:
                run_fail = True
            # pair checking... 
            if num_of_cards[i] == num_of_cards[i + 1]:
                num_count += 1
            else:
                pair_count += num_count // 2
                num_count = 1
        pair_count += num_count // 2
        if not run_fail and num_of_cards[-2] + 1 == num_of_cards[-1]:
            card_run = True
        for i in range(len(sorted_cards) - 1):
            if num_of_cards[0] == 10 and card_run: 
                roy_flush = True
                break
            if sorted_cards[i].get_suit() != sorted_cards[i + 1].get_suit():
                is_flush = False
                break

        if roy_flush:
            points = (cls.get_total_card_val() + 300) * cls.markiplier
        elif card_run and is_flush:
            points = (cls.get_total_card_val() + 250) * cls.markiplier
            return points
        elif card_run:
            points = (cls.get_total_card_val() + 200) * cls.markiplier
            return points

        if is_flush:
            points = (cls.get_total_card_val() + 50) * cls.markiplier
            return points
        

        # three of a kind/four of a kind
        for i in range(len(num_of_cards) - 3):
            if num_of_cards[i] == num_of_cards[i + 1] == num_of_cards[i + 2] == num_of_cards[i + 3]:
                four_kind = True 
                break
            elif num_of_cards[i] == num_of_cards[i + 1] == num_of_cards[i + 2]:
                three_kind = True
                break

        # checks for pairs, full house, and three of a kind/four of a kind.
        if pair_count > 0:
            if three_kind:
                # full house
                points = cls.get_total_card_val() + 225 * pair_count * cls.markiplier
                return points
            # regular pair 
            points = cls.get_total_card_val() + 50 * pair_count * cls.markiplier
            return points 
        if three_kind:
            points = (cls.get_total_card_val() + 60) * cls.markiplier
            return points
        if four_kind:
            points = (cls.get_total_card_val() + 80) * cls.markiplier
            return points

        for i in range(len(num_of_cards)):
            if num_of_cards[i] == 13:
                high_card = True
        if high_card:
            points (cls.get_total_card_val + 20) * cls.markiplier
