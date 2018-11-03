# -*- coding: utf-8 -*-

import connection
import sys

from random import shuffle

# -------------------------------------------
# Card class
class Card:
	def __init__(self, card_type, num, color):
		self.card_type = card_type # NORMAL, REVERSE, DRAW 
		self.num = num
		self.color = color 

	def __str__(self):
		return "TYPE: " + self.card_type + ". NUM: " + str(self.num) + ". COLOR: " + self.color 

# -------------------------------------------

def is_dealer():
	return self_name == dealer;

def get_card_from_deck(deck):
	if len(deck) <= 0:
		deck += pile
		shuffle(deck)
	card = deck.pop()
	return card

def get_cards_from_deck(deck, amount):
	cards = []
	for i in range(0, amount):
		cards.append(get_card_from_deck(deck))
	return cards


def create_deck():
	numeric_cards = [Card("NORMAL", num, color) for color in colors for num in range(1, 11)]
	draw_cards = [Card("DRAW", 2, color) for color in colors for i in range(0, 2)]
	reverse_cards = [Card("REVERSE", -1, color) for color in colors for i in range(0, 2)]

	deck = numeric_cards + draw_cards + reverse_cards
	shuffle(deck)

	"""
	for card in deck:
		print(card)

	for player in players:
		initial_cards = get_cards_from_deck(deck, 7)
		connection.send_cards_to(player, initial_cards)
	"""
	return deck

#def print_cards():

def play():
	if (rounds == 0):
		print("You are the first to play!")


# -------------------------------------------

rounds = 0

players = ["A", "B", "C", "D"]

self_name = sys.argv[1]
print("Playing as: " + self_name)

connection.setup_connection(self_name)

dealer = connection.get_dealer()

cards_per_player = 7
colors = ["BLUE", "RED", "GREEN", "YELLOW"]
deck = create_deck()
pile = []
cards = []
last_card = None
game_direction = 1

# Creates the deck
if is_dealer():
	input("Press enter to start game!")

not_sent_cards = ["A", "B", "C", "D"] # People who haven't received their cards yet

# Sends first message
connection.send_cards_to(self_name, not_sent_cards[0], get_cards_from_deck(deck, 7))
	
# Game loop
while True:
	message = connection.wait_message() # buffer size is 1024 bytes

	# Message's target is this player
	if (self_name == message.target):
		print("[DEBUG] Received message from " + message.target)
		
		if message.type == "CARD_PAYLOAD":
			pile += message.content.cards

	# Message has been received by every other player
	if (self_name == message.sender):
		print("[DEBUG] Received message from " + message.target)
		if (len(not_sent_cards.isEmpty) > 0):
			connection.send_cards_to(self_name, not_sent_cards[0], get_cards_from_deck(deck, 7))





