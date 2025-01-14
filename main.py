import pygame
import json
import random

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
        
        # Plan for this
        # Choose a card from deck of cards, then like call Card class function to actuall deal card.

        pass

    