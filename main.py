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
    held_cards = []
    type_of_suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    markiplier = 1
    def __init__(self, suit, number, img_path):
        self.suit = suit
        self.number = number
        self.image = pygame.image.load(img_path)
        Card.deck_of_cards.append(self)

    def get_suit(self):
        return self.suit
    
    def get_val(self):
        return self.number
    
    def get_img(self):
        return self.image
    
    @classmethod
    def init_deck_of_Cards(cls):
        for i in range(4):
            curr_suit = cls.type_of_suits[i]
            for j in range(2, 14):
                cls.deck_of_cards.append(Card(curr_suit, j, "card/" + curr_suit + "/" + j + ".png"))
                
    @classmethod
    def get_deck_of_cards(cls):
        return cls.deck_of_cards
    
    @classmethod
    def get_player_cards(cls):
        return cls.player_cards
    
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
        for i in range(len(sorted_cards) - 1):
            if sorted_cards[i].get_suit() != sorted_cards[i + 1].get_suit():
                is_flush = False
                break
        pair_count += num_count // 2
        if not run_fail and num_of_cards[-2] + 1 == num_of_cards[-1]:
            card_run = True
        if num_of_cards[0] == 10 and card_run and is_flush:
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
            points = (cls.get_total_card_val + 20) * cls.markiplier
            return points



class Dealer():
    """Represents a card dealer in the game.

    Attributes:
        dealer_config_paths (list of str): Paths to available dealer configuration files (class attribute).
        config_path (str): The path to the chosen dealer's configuration file (instance attribute).
        name (str): The dealer's name (instance attribute).
        portrait_img (pygame.Surface): The dealer's portrait image loaded as a Pygame surface obj (instance attribute).
        hands_img (pygame.Surface): The dealer's hands image loaded as a Pygame surface obj (instance attribute).
        liked_cards (list of lists of int, str or bool): Cards/card type the dealer likes, each column being a card/card type (instance attribute).
        disliked_cards (list of lists of int, str or bool): Cards/card type the dealer dislikes, each column being a card/card type (instance attribute).
    """

    dealer_config_paths = ["dealer_configs/chicken_man.json", "dealer_configs/drew_badhand.json", "dealer_configs/folden_freeman.json"]

    def __init__(self, chosen_dealer = False):
        """Initializes the dealer using its appropriate json config file.

        Args:
            chosen_dealer (bool or str): If False, a random dealer configuration is chosen.
                If a string, it is used as the dealer's specific configuration name.
        
        Raises:
            FileNotFoundError: If the dealer's json file does not exist/isn't found.
            KeyError: If the configuration file is missing required keys/tags (e.g "name").
        """

        if not chosen_dealer:
            self.config_path = random.choice(Dealer.dealer_config_paths)
        else:
            self.config_path = "dealer_configs/" + chosen_dealer + ".json"
        
        # Open Json config to read
        with open(self.config_path, 'r') as file:
            dealer_data = json.load(file)

            self.name = dealer_data["name"] # Save name

            self.portrait_img = pygame.image.load(dealer_data["portrait_img_path"]) # Save portrait img as Pygame surface obj

            self.hands_img = pygame.image.load(dealer_data["hands_img_path"]) # Save hands img as Pygame surface obj

            self.liked_cards = dealer_data["liked_cards"] # Saves the liked cards as a 2-d matrix/array (each column is liked type of/specific card)

            self.disliked_cards = dealer_data["disliked_cards"] # Saves the disliked cards as a 2-d matrix/array (each column is disliked type of/specific card)

    def get_name(self):
        """Gets/returns the dealer's name.

        Returns:
            str: The dealer's name.
        """

        return self.name
    
    def get_portrait_img(self):
        """Gets/returns the dealer's portrait image.

        Returns:
            pygame.Surface: The dealer's portrait image loaded as a Pygame surface obj.
        """
        return self.portrait_img
    
    def get_hands_img(self):
        """Gets/returns the dealer's hands image.

        Returns:
            pygame.Surface: The dealer's hands image loaded as a Pygame surface obj.
        """
        return self.hands_img

    def chose_and_deal_card(self):
        """Chooses and deals a card.

        Note:
            This is a placeholder implementation. It CURRENTLY randomly selects a card from the deck
            and deals it. NEEDED logic of smartly choosing a card needs to be implemented.
        """

        # TEMPORARY CODE, JUST PICKS RANDOM CARD FROM DECK AND DEALS. NEED TO ACTUALLY IMPLEMENT

        deck_cards = Card.get_deck_of_cards() # Note method to get deck cards not implemented yet

        random.choice(deck_cards).player_deal()



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
