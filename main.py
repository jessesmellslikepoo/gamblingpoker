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
font = pygame.font.Font("./minecraft_font.ttf", 24)
background_image = pygame.image.load('./background.png')
background_image = pygame.transform.scale(background_image, (1600, 800))

class Game():
    def __init__(self):
        Card.init_deck_of_Cards()
        self.totalHands = 3
        self.totalDiscards = 3
        self.chipBase = 100
        self.roundCount = 0
        self.minChip = 0
        self.chipsHeld = 0
        self.dealer = Dealer()
        self.card_positions = []
        self.mouse_released = False # Avoids holding down, I'm trying NOT to make a billion chips.

        for _ in range(7):
            self.dealer.chose_and_deal_card()

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
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_w
            ):
                if self.totalDiscards != 0:
                     Card.held_cards[0].discard_player_card()
                     self.totalDiscards -= 1
                     self.dealer.chose_and_deal_card()
            if (
                event.type == pygame.MOUSEBUTTONDOWN
            ):
                self.handleCardClick()
    


    def changes(self):
        pass

    def render(self):
        screen.blit(background_image, (0, 0))
        self.renderUI()
        self.renderDealer()
        self.renderPlayerCards()

    def renderPlayerCards(self):
        x_offset = 350
        y_position = 600
        card_spacing = 165 

        for index, card in enumerate(Card.get_player_cards()):
            x_position = x_offset + index * card_spacing
            self.card_positions.append((card, pygame.Rect(x_position, y_position, 155, 250)))
            
            card_rect = pygame.Rect(x_offset + index * card_spacing, y_position, 155, 250)
            scaled_image = pygame.transform.scale(card.get_img(), (155, 250))
            screen.blit(scaled_image, (x_position, y_position))

            if card.selected:
                pygame.draw.rect(screen, (0, 255, 0), card_rect, 5) #Gotta make sure i can unselected it later too lmaoooo
            else:   
                pygame.draw.rect(screen, (0, 0, 0), card_rect, 5) 

    def renderUI(self):
        pygame.draw.rect(screen, BROWN, (10, 12, 314, 147))
        pygame.draw.rect(screen, BROWN, (10, 160, 314, 147))
        pygame.draw.rect(screen, BROWN, (10, 322, 314, 300))
        minchiptext_surface = font.render(f"Min Req. Chips: {self.calcMinChips()}", True, BLACK)
        minchiptext_rect = minchiptext_surface.get_rect(center=(10 + 324 / 2, 120))
        screen.blit(minchiptext_surface, minchiptext_rect)
        playerchiptext_surface = font.render(f"Player Chips: {self.chipsHeld}", True, BLACK)
        playerchiptext_rect = playerchiptext_surface.get_rect(center=(10 + 324 / 2, 60))
        screen.blit(playerchiptext_surface, playerchiptext_rect)
        handtext_surface = font.render(f"Hands Remaining: {self.totalHands}", True, BLACK)
        handtext_rect = handtext_surface.get_rect(center=(10 + 314 / 2, 200))
        screen.blit(handtext_surface, handtext_rect)
        disctext_surface = font.render(f"Discards Remaining: {self.totalDiscards}", True, BLACK)
        disctext_rect = disctext_surface.get_rect(center=(10 + 314 / 2, 260))
        screen.blit(disctext_surface, disctext_rect)
        roundcounttext_surface = font.render(f"Round: {self.roundCount}", True, BLACK)
        disctext_rect = roundcounttext_surface.get_rect(center=(1500, 40))
        screen.blit(roundcounttext_surface, disctext_rect)

    def renderDealer(self):
        screen.blit(self.dealer.get_portrait_img(), (20, 330))
        dealertext_surface = font.render(f"{self.dealer.name}", True, BLACK)
        dealertext_rect = dealertext_surface.get_rect(center=(170, 640))
        screen.blit(dealertext_surface, dealertext_rect)
        screen.blit(self.dealer.get_hands_img(), (400, 0))

    def next_turn(self):
        self.totalHands -= 1
        self.play_selected_cards()
        if self.totalHands == 0: self.finishRound()
        elif self.getPlayerChips() >= self.calcMinChips(): self.finishRound()

    def finishRound(self):
        if self.getPlayerChips() >= self.calcMinChips():
            self.roundCount += 1
            self.totalHands = 3
            self.totalDiscards = 3
            self.calcMinChips()
        else: pygame.quit()

    def calcMinChips(self): # I made this better.
        base_growth_rate = 1.5  # base
        pfactor = max(1, self.roundCount / 2)  # round exp.

        self.minChip = int(self.chipBase * (base_growth_rate ** self.roundCount) * pfactor)
        return self.minChip
    
    def getPlayerChips(self):
        return self.chipsHeld

    def handleCardClick(self):
        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:  # Left-click (button 1)
            for idx, card in enumerate(Card.get_player_cards()):
                x_offset = 350 + idx * 165
                y_position = 600
                card_rect = pygame.Rect(x_offset, y_position, 155, 250)

                # Col check!
                if card_rect.collidepoint(mouse_pos) and not card.selected:
                    if len(Card.held_cards) < 5:
                        card.selected = True
                        Card.held_cards.append(card)
                        print(f"Card {card.get_val()} of {card.get_suit()} added to held")
                    else:
                        print("You can only select up to 5 cards.")
        elif pygame.mouse.get_pressed()[2]:  # Right-click (button 3, not 2...)
            for idx, card in enumerate(Card.get_player_cards()):
                x_offset = 350 + idx * 165
                y_position = 600
                card_rect = pygame.Rect(x_offset, y_position, 155, 250)

                # Allow deselection regardless of the selection count
                if card_rect.collidepoint(mouse_pos) and card.selected:
                    card.selected = False
                    Card.held_cards.remove(card)
                    print(f"Card {card.get_val()} of {card.get_suit()} removed from held")

    def play_selected_cards(self):
        if not Card.held_cards:
            print("No cards selected to play.")
            return 0  # No points if no cards are selected.
        if len(Card.held_cards) != 5:
            print("Hand will not play! Must play 5 cards!")
        else:
            # Move selected cards to player_cards for combination calculation
            Card.player_cards.extend(Card.held_cards)
            Card.held_cards.clear()

            # Calculate the combination and points
            points = Card.get_possible_combination()

            # Clear player cards after playing
            Card.clear_player()

            print(f"Played selected cards! Combination points: {points}")
            self.chipsHeld += points
             
class Card():
    # 200 points = run 
    # 50 points = 1 pair of cards
    # 100 points = 2 pairs of cards
    # 60 points = three of a kind

    """
    Attributes:
    deck_of_cards (any, should be Card): deck_of_cards when the program is first run is empty, but can easily be initialized by calling the class method
    init_deck_of_cards, which then initalizes all 52 cards in the deck.
    player_cards (any, should be Card): the current player_cards the individual is holding at that moment (which should never exceed 5). 
    held_cards (any, should be Card): the current discarded cards that are usable in the next round (which should never exceed 2).
    TYPE_OF_SUITS (string list): The valid suits that a Card object can use, this is will always be CONSTANT, therefore, it should never change. 
    markiplier (int var): Funny reference, I know. It's a multiplier that can be changed by the Game class in order to make stakes more intense for points.
    """

    deck_of_cards = []
    player_cards = []
    held_cards = [] # two cards a player holds on to until the next round in case they want to use them.
    TYPE_OF_SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"] # used to store the valid suits a Card has.
    markiplier = 1 # multiplier, in case if it was confusing because of the funny reference.
    
    def __init__(self, suit, number, img_path): 
        """
        parameters: suit, number, img_path 
        A constructor used to initalize each attribute of a specific Card object.
        This is a constructor, there is no return, and the init_deck_of_cards is dependent on this constructor.
        """
        self.selected = False
        self.suit = suit
        self.number = number
        self.image = pygame.image.load(img_path)

    def get_suit(self):
        """
        parameters: self (only represents a Card object, will not be included in documentation for the rest of the parameters to avoid redudancy.)
        An instance getter method for the Card suit. 
        return: the Card object's suit. 
        """
        return self.suit
    
    def get_val(self):
        """
        An instance getter method for the Card value.
        return: the Card object's number/value.
        """
        return self.number
    
    def get_img(self):
        """
        An instance getter method for the image.
        return: the card object's image that uses pygame to load.
        """
        return self.image
    
    @classmethod
    def init_deck_of_Cards(cls):
        """
        Void class method that initalizes the deck_of_cards, starting with clubs. See class documentation for more info.
        parameters: cls (only mentioned once since like self, it is redudnant)
        Follows a specific folder format for each img_path in order for organization. 
        return: void, which means none.
        """
        for i in range(4):
            curr_suit = cls.TYPE_OF_SUITS[i]
            for j in range(2, 14):
                # Follows a specific directory format for the img_path when appended. (cards/the suit/the number.png)
                cls.deck_of_cards.append(Card(curr_suit, j, "assets/cards/" + curr_suit + "/" + str(j) + ".png"))
    @classmethod
    def set_multiplier(cls, num):
        """
        parameters: num
        Void class method that simply sets the multiplier based on the num argument. 
        """
        cls.markiplier = num
     
    @classmethod
    def get_deck_of_cards(cls):
        """
        A class getter method for the list deck_of_cards.
        return: deck_of_cards
        """
        return cls.deck_of_cards
    
    @classmethod
    def get_player_cards(cls):
        """
        A class getter method for the list player_cards. 
        return: player_cards
        """
        return cls.player_cards
    
    def deal(self):
        """
        A instance void method for dealing a card to the player.
        """
        Card.deck_of_cards.remove(self)
        Card.player_cards.append(self) 
    
    def discard_held_card(self):
        """
        A void instance method for discarding a Card object in held_cards. 
        the player will hold two Card objects
        """
        Card.held_cards.remove(self)
        Card.deck_of_cards.append(self)

    def discard_player_card(self):
        Card.held_cards.append(self)
        Card.player_cards.remove(self)

    @classmethod
    def clear_player(cls):
        """
        A class void method that clears the player.
        """
        cls.deck_of_cards.extend(cls.held_cards) # adds the cards back into the deck of cards
        cls.held_cards.clear()

    @classmethod
    def get_total_card_val(cls):
        """
        A class int method that returns the total value of every Card in player_cards.
        returns: total_val 
        attributes:
        total_val (int var): resets with every method call and then is added when in loop. 
        """
        total_val = 0
        for card in cls.held_cards:
                # checks each index is a Card object in order to use. This is because in Python, a list doesn't need to contain a specific datatype.
                if isinstance(card, Card): 
                    total_val += card.get_val()
        return total_val

    @classmethod
    def get_possible_combination(cls):
        """
        A class int method that goes through every possible combination in order to win the game. This should be updated every time a new card is presented.
        Attributes:
        num_of_cards (int list): num_of_cards is the specific value(s) of player_cards. 
        suit_of_cards (str list): suit_of_cards is the specific amount of strings in player_cards. 
        check_player_cards (Card list): takes player_cards and makes a list of the cards using list comprehension. 
        sorted_cards (Card list): takes check_player_cards and makes sorts it based on value, and the suit secondary (e.g 10 clubs, 4 diamonds, 2 spades, etc...) 
        three_kind (boolean var): a check to ensure a three of a kind took place.
        four_kind (boolean var): a check to ensure a four of a kind took place.
        run_fail (boolean var): a check to ensure a run either failed or passed.
        is_flush (boolean var): a check to ensure a flush has taken place.
        pair_count (int var): a pair count that uses .count and counts from a double and then floor divides in order to check for a pair. (e.g pair count is 1.5, the floor counts the pair_count now as 1)
        """
        num_of_cards = []
        suit_of_cards = []
        # checks if each player card is an actual Card object. This is in order to use specific unique Card methods on a list.
        check_held_cards = [card for card in cls.held_cards if isinstance(card, Card)]
        # sorts cards based on a sorting key, that each Card object should be sorted based on the numeric value, and then on what each suit alphabetically is.
        sorted_cards = sorted(check_held_cards, key = lambda card : (card.get_val(), card.get_suit()))
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
        # condition check for royal flush
        if num_of_cards[0] == 10 and not run_fail and is_flush:
            points = (cls.get_total_card_val() + 300) * cls.markiplier
            return points
        # condition check for straight flush
        elif not run_fail and is_flush:
            points = (cls.get_total_card_val() + 250) * cls.markiplier
            return points
        # condition check for four of a kind
        if four_kind:
            points = (cls.get_total_card_val() + 80) * cls.markiplier
            return points
        if pair_count > 0:
        # condition check for full house.
        if three_kind:
            points = cls.get_total_card_val() + 225 * pair_count * cls.markiplier
            return points
        # condition check for flush
        if is_flush:
            points = (cls.get_total_card_val() + 50) * cls.markiplier
            return points
        # condition check for straight
        elif not run_fail:
            points = (cls.get_total_card_val() + 200) * cls.markiplier
            return points
        
        # condition check for flush
        if is_flush:
            points = (cls.get_total_card_val() + 50) * cls.markiplier
            return points
        # condition check for three of a kind
        if three_kind:
            points = (cls.get_total_card_val() + 60) * cls.markiplier
            return points
        # condition for one pair/two pairs of cards
        if pair_count > 0:
            points = cls.get_total_card_val() + 50 * pair_count * cls.markiplier
        # finally, check for the highest card for points.
        points = (cls.get_total_card_val() + 20) * cls.markiplier

        
        
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

        random.choice(deck_cards).deal()



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
