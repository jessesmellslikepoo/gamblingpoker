import pygame
import json
import random

pygame.init()
screen = pygame.display.set_mode((1600, 800))
pygame.display.set_caption("I LOVE ABGs")
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 20)
BROWN = (75, 70, 60)
BLACK = (0, 0, 0)
font = pygame.font.Font("minecraft_font.ttf", 24)
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (1600, 800))

class Game():
    def __init__(self):
        self.totalHands = 3
        self.totalDiscards = 3
        self.chipBase = 100
        self.roundCount = 0
        self.CursorPos = 0
        self.minChip = 0
        self.chipsHeld = 0

    def frame_loop(self):
        self.events()
        self.changes()
        self.render()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.next_turn()

    def changes(self):
        pass

    def render(self):
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, BROWN, (10, 12, 314, 147))
        pygame.draw.rect(screen, BROWN, (10, 160, 314, 147))
        pygame.draw.rect(screen, BROWN, (10, 322, 314, 300))
        minchiptext_surface = font.render(f"Min Req. Chips: {self.calcMinChips()}", True, BLACK)
        minchiptext_rect = minchiptext_surface.get_rect(center=(10 + 314 // 2, 12 + 147 // 2))
        screen.blit(minchiptext_surface, minchiptext_rect)
        handtext_surface = font.render(f"Hands Remaining: {self.totalHands}", True, BLACK)
        handtext_rect = handtext_surface.get_rect(center=(10 + 314 // 2, 200))
        screen.blit(handtext_surface, handtext_rect)
        disctext_surface = font.render(f"Discards Remaining: {self.totalDiscards}", True, BLACK)
        disctext_rect = disctext_surface.get_rect(center=(10 + 314 // 2, 260))
        screen.blit(disctext_surface, disctext_rect)


    def next_turn(self):
        self.totalHands -= 1
        if self.totalHands == 0: self.finishRound()
        elif self.getPlayerChips() >= self.calcMinChips(): self.finishRound()

    def finishRound(self):
        if self.getPlayerChips() >= self.calcMinChips():
            self.roundCount += 1
            self.totalHands = 3
            self.totalDiscards = 3
            self.calcMinChips()
        else: pygame.quit()

    def calcMinChips(self):
        self.minChip = self.chipBase + (self.roundCount * 10)
        return self.minChip
    
    def getPlayerChips(self):
        return self.chipsHeld
             
class Card():
    # 200 points = run 
    # 50 points = 1 pair of cards
    # 100 points = 2 pairs of cards
    # 60 points = three of a kind

    deck_of_cards = []
    player_cards = []
    held_cards = [] # two cards a player holds on to until the next round in case they want to use them.
    type_of_suits = ["Clubs", "Diamonds", "Hearts", "Spades"] # used to store the valid suits a Card has.
    markiplier = 1 # multiplier, in case if it was confusing because of the funny reference.
    def __init__(self, suit, number, img_path): 
        """
        parameters: suit, number, img_path 
        A constructor used to initalize each attribute of a specific Card object.
        """
        self.suit = suit
        self.number = number
        self.image = pygame.image.load(img_path)

    def get_suit(self):
        return self.suit
    
    def get_val(self):
        return self.number
    
    def get_img(self):
        return self.image
    
    @classmethod
    def init_deck_of_Cards(cls):
        '''
        Class method that initalizes the deck_of_cards, starting with clubs. See type_of_suits for more info.
        '''
        for i in range(4):
            curr_suit = cls.type_of_suits[i]
            for j in range(2, 14):
                # Follows a specific directory format for the img_path when appended. (cards/the suit/the number.png)
                cls.deck_of_cards.append(Card(curr_suit, j, "cards/" + curr_suit + "/" + j + ".png"))
     
    @classmethod
    def get_deck_of_cards(cls):
        return cls.deck_of_cards
    
    @classmethod
    def get_player_cards(cls):
        return cls.player_cards
    
    def deal(self):
        '''
        used to deal cards to a player from the deck_of_cards, which it is then removed. Instance method.
        '''
        Card.deck_of_cards.remove(self)
        Card.player_cards.append(self) 
    
    def discard_player_card(self):
        '''
        used to discard unused cards to a player.
        the player will usually hold two Card objects in held_cards
        '''
        Card.player_cards.remove(self)
        Card.held_cards.append(self)
    

    @classmethod
    def clear_player(cls):
        '''
        a bit self explanatory but first adds the cards back to deck_of_cards, and then clears the player_cards list.
        '''
        cls.deck_of_cards.extend(cls.player_cards)
        cls.player_cards.clear()

    @classmethod
    def get_total_card_val(cls):
        '''
        Self explanatory. Adds the total value of the cards in player_cards.
        '''
        total_val = 0
        for card in cls.player_cards:
                # checks each index is a Card object in order to use. This is because in Python, a list doesn't need to contain a specific datatype.
                if isinstance(card, Card): 
                    total_val += card.get_val()
        return total_val

    @classmethod
    def get_possible_combination(cls):
        '''
        gets every possible combination using a mix of booleans to check for a condition to win. 
        If the dealer has a higher amount of points than the player, then the player loses, and vice versa.
        '''
        num_of_cards = []
        suit_of_cards = []
        # checks if each player card is an actual Card object. This is in order to use specific unique Card methods on a list.
        check_player_cards = [card for card in cls.player_cards if isinstance(card, Card)]
        # sorts cards based on a sorting key, that each Card object should be sorted based on the numeric value, and then on what each suit alphabetically is.
        sorted_cards = sorted(check_player_cards, key = lambda card : (card.get_val(), card.get_suit()))
        card_run = False
        three_kind = False
        four_kind = False
        run_fail = False
        is_flush = True
        pair_count = 0
        for card in sorted_cards:
            if isinstance(card, Card):
                num_of_cards.append(card.get_val())
                suit_of_cards.append(card.get_suit())

        # checking for a run and a pair  
        for i in range(len(num_of_cards) - 1):
            # run calculating...
            if not run_fail and num_of_cards[i] != num_of_cards[i + 1] - 1:
                run_fail = True
            # flush calculating...
            if is_flush and sorted_cards[i].get_suit() != sorted_cards[i + 1].get_suit():
                is_flush = False
            # pair calculating...
            num_of_common_cards = num_of_cards.count(num_of_cards[i])
            if num_of_common_cards == 2:
                pair_count += 0.5
            # three/four of a kind calculating...
            elif num_of_common_cards == 3:
                three_kind = True
            elif num_of_common_cards == 4:
                four_kind = True
        pair_count += pair_count // 2 # floors pair_count because each card counts for 0.5 of a pair_count
        if not run_fail:
            card_run = True
        # condition check for royal flush
        if num_of_cards[0] == 10 and card_run and is_flush:
            points = (cls.get_total_card_val() + 300) * cls.markiplier
        # condition check for straight flush
        elif card_run and is_flush:
            points = (cls.get_total_card_val() + 250) * cls.markiplier
            return points
        # condition check for straight
        elif card_run:
            points = (cls.get_total_card_val() + 200) * cls.markiplier
            return points
        
        # condition check for flush
        if is_flush:
            points = (cls.get_total_card_val() + 50) * cls.markiplier
            return points
        
        # checks for pairs, full house, and three of a kind/four of a kind.
        if three_kind:
            points = (cls.get_total_card_val() + 60) * cls.markiplier
            return points
        if four_kind:
            points = (cls.get_total_card_val() + 80) * cls.markiplier
            return points
        if pair_count > 0:
            # condition check for full house.
            if three_kind:
                points = cls.get_total_card_val() + 225 * pair_count * cls.markiplier
                return points
            # condition check for regular pairs.  
            points = cls.get_total_card_val() + 50 * pair_count * cls.markiplier
            return points 

        for i in range(len(num_of_cards)):
            # check for a high card.
            if num_of_cards[i] == 13:
                high_card = True
        # conditional for a high card.
        if high_card:
            points = (cls.get_total_card_val + 20) * cls.markiplier
            return points
        
class Dealer():

    dealer_config_paths = ["dealers/test1.json", "dealers/test2.json", "dealers/test3.json"]

    def __init__(self, chosen_dealer = False):

        if chosen_dealer:
            self.config_path = random.choice(Dealer.dealer_config_paths)
        else:
            self.config_path = "dealers/" + chosen_dealer + ".json"
        
        # Open Json config to read
        with open(self.config_path, 'r') as file:
            dealer_data = json.load(file)

            self.name = dealer_data["name"] # Save name

            self.portrait_img = pygame.image.load(dealer_data["portrait_img_path"]) # Save portrait img as pygame img obj

            self.hands_img = pygame.image.load(dealer_data["hands_img_path"]) # Save hands img as pygame img obj

            self.liked_cards = dealer_data["liked_cards"]

            self.disliked_cards = dealer_data["disliked_cards"]


    # Getter method for name
    def getName(self):
        return self.name
    
    # Getter method for portrait img
    def getPortraitImg(self):
        return self.portrait_img
    
    # Getter method for hands img
    def getHandsImg(self):
        return self.hands_img

    def choseAndDealCard(self):

        # TEMPORARY CODE, JUST PICKS RANDOM CARD FROM DECK AND DEALS. NEED TO ACTUALLY IMPLEMENT

        deck_cards = Card.get_deck_cards() # Note method to get deck cards not implemented yet

        random.choice(deck_cards).player_deal()

        pass

def main():
    # Initialize your class that will run everything
    gameplay = Game()

    while True:
        screen.fill("purple")

        # Run the primary method in your class that will run every frame
        gameplay.frame_loop()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
