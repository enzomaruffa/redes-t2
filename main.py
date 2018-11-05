# -*- coding: utf-8 -*-

import connection
import sys

from random import shuffle

# -------------------------------------------
# Card class
class Card:

	colors = {
	 	"RED": "\033[91m",
	 	"YELLOW": "\033[93m",
		"BLUE": "\033[96m",
		"GREEN": "\033[92m",
	}

	def __init__(self, card_type, num, color):
		self.card_type = card_type # NORMAL, SKIP, DRAW 
		self.num = num
		self.color = color 

	def __str__(self):
		if (self.card_type == "NORMAL"):
			return Card.colors.get(self.color) + "NUM: " + str(self.num) +"\033[00m"
		elif (self.card_type == "SKIP"):
			return Card.colors.get(self.color) + "TYPE: " + str(self.card_type) + "\033[00m"
		else:
			return Card.colors.get(self.color) + "NUM: +" + str(self.num) + "\033[00m"


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
	print("Creating deck...")
	print("Creating numeric cards...")
	numeric_cards = [Card("NORMAL", num, color) for color in colors for num in range(1, 11)]
	print("Creating +2 cards...")
	draw_cards = [Card("DRAW", 2, color) for color in colors for i in range(0, 2)]
	print("Creating skip turn cards...")
	reverse_cards = [Card("SKIP", -1, color) for color in colors for i in range(0, 2)]

	deck = numeric_cards + draw_cards + reverse_cards
	shuffle(deck)

	return deck

def print_player_cards():
	print("Player cards: ")
	for index, card in enumerate(cards):
		print("[" + str(index+1) + "] - " + str(card))

def play(card):
	print("You've chosen this card:")
	print(str(card))

	cards.remove(card)
	connection.send_play(self_name, card)

def play_menu():
	print("Your turn to play!")
	print("Last card is: ")
	print(last_card)

	global valid_draw

	if not has_play_possibility(cards, last_card):
		print("None of your cards are valid!")
		print_player_cards()
		global bought_single_card
		if not bought_single_card:
			input("Press enter to buy cards!")
			force_buy()
		else:
			bought_single_card = False
			print("You've already bought the mandatory 1 card")
			#print("[DEBUG] bought_single_card now: " + str(bought_single_card))
			input("Press enter to pass your turn")
			pass_turn()
	else:
		if (last_card != None and last_card.card_type == "DRAW" and valid_draw):
			print("You can choose between playing (adding +2 to the stack) or buying " + str(last_card.num) + " cards.")
			answer = (input("0 - Play\n1 - Buy\n"))
			while (answer not in ["0", "1"]):
				answer = (input("0 - Play\n1 - Buy\n"))

			if (answer == "0"):
				play_routine()
			else:
				input("Press enter to buy cards!")
				force_buy()	
		else:
			play_routine()

def play_routine():
	global valid_draw
	valid_draw = True

	print("Your cards are: ")
	print_player_cards()
	
	card_index = int(input("Choose a card by its row number: ")) - 1
	while (card_index > len(cards) or not is_valid_play(cards[card_index], last_card)):
		card_index = int(input("Invalid card! Choose another: ")) - 1

	play(cards[card_index])


def is_valid_play(card, other_card):
	if last_card == None:
		return True

	if (card.card_type == "NORMAL"):
		return (card.color == other_card.color or card.num == other_card.num)
	if (card.card_type == "SKIP"):
		return (card.color == other_card.color or other_card.card_type == "SKIP")
	if (card.card_type == "DRAW"):
		return (card.color == other_card.color or other_card.card_type == "DRAW")

def has_play_possibility(cards, last_card):
	if last_card == None:
		return True

	if (last_card.card_type == "NORMAL"):
		for card in cards:
			if (last_card.color == card.color or last_card.num == card.num):
				return True
		return False
	if (last_card.card_type == "SKIP"):
		for card in cards:
			if ("SKIP" == card.card_type or last_card.color == card.color):
				return True
		return False
	if (last_card.card_type == "DRAW"):
		for card in cards:
			if ("DRAW" == card.card_type or (last_card.color == card.color and bought_single_card)):
				return True
		return False

def force_buy():
	if (last_card.card_type == "DRAW" and valid_draw):
		print("Buying " + str(last_card.num) + " cards")
		request_cards(last_card.num)
	else:
		global bought_single_card
		bought_single_card = True
		print("Buying 1 card")
		request_cards(1)

def pass_turn():
	connection.pass_token(self_name)
	##print("[DEBUG - Pass Turn] Sending token to next player ")
	global token
	token = False

def request_cards(amount):
	connection.request_cards(self_name, dealer, amount)

# -------------------------------------------

game_started = False

players = ["A", "B", "C", "D"]

self_name = sys.argv[1]
print("Playing as: " + self_name)

connection.setup_connection(self_name)

dealer = connection.get_dealer()

cards_per_player = 7
colors = ["BLUE", "RED", "GREEN", "YELLOW"]
deck = []
cards = []
last_card = None
token = False

# Card buy limits
bought_single_card = False # Checks if player has bought his single card per turn, if needed
valid_draw = True # Checks if draw cards has been "drawed"

# Card Request stuff
return_token_target = None
send_card_amount = 0

last_received_message = None


# Creates the deck
if is_dealer():
	pile = []
	
	input("Press enter to start game!")
	
	deck = create_deck()
	
	not_sent_cards = ["A", "B", "C", "D"] # People who haven't received their cards yet
	connection.send_cards_to(self_name, not_sent_cards.pop(), get_cards_from_deck(deck, cards_per_player))

# Sends first message
	
# Game loop
while True:
	##print("[DEBUG - Game loop] Token? " + str(token))

	if (token):
		if not is_dealer() or return_token_target == None:
			play_menu()
		else:
			connection.send_cards_to(self_name, return_token_target, get_cards_from_deck(deck, send_card_amount))

	#print("[DEBUG] Waiting new message!")
	message = connection.wait_message() # buffer size is 1024 bytes

	# Somehow messages repeat (?)
	##print("[DEBUG] Received message dict:")
	#print(message.__dict__)
	##print("[DEBUG] Last received message:")
	#if (last_received_message != None):
	#	print(last_received_message.__dict__)

	if (message == last_received_message):
		#print("[DEBUG] Same message received twice!")
		message = connection.wait_message()

	last_received_message = message

	#print("[DEBUG] Message from " + message.sender + " to " + message.target + ". Type: " + message.type)

	# Blocks +2 effect from second player if the affected player isn't able to overcome it
	if message.type == "CARD_REQUEST":
		##print("[DEBUG] [ALL] Card request")
		send_card_amount = message.content
		if send_card_amount > 1:
			valid_draw = False


	# Message's target is this player
	if (self_name == message.target or message.target == "ALL"):
		if message.type == "CARD_PAYLOAD":
			#print("[DEBUG] [Target] Card payload")
			print("Just received " + str(len(message.content)) + " card(s)!")

			cards += message.content

			print_player_cards()

		if message.type == "TOKEN":
			#print("[DEBUG] [Target] Token")
			token = True

		if message.type == "CARD_REQUEST":
			#print("[DEBUG] [Target] Card request from " + message.sender)
			return_token_target = message.sender
			send_card_amount = message.content

		if message.type == "PLAY":
			#print("[DEBUG] [Target] Play")
			print("Player " + message.sender + " has just played a card.")
			card = message.content
			print(str(card))

			if (last_card != None and last_card.card_type == "DRAW" and card.card_type == "DRAW" and valid_draw):
				last_card.color = card.color
				last_card.num += card.num
			else:
				last_card = card

			valid_draw = True

			if (is_dealer()):
				pile.append(card)

		if message.type == "UNO":
			#print("[DEBUG] [Target] UNO")
			print("Player " + message.sender + " has shouted UNO!")

		if message.type == "WIN":
			#print("[DEBUG] [Target] WIN")
			print("Player " + message.sender + " has won the game!")
			connection.send_message(message)
			quit()

	# Message has been received by every other player
	if (self_name == message.sender):
		# Setup messages
		if (is_dealer() and len(not_sent_cards) > 0):
			#print("[DEBUG] Sending initial cards to " + not_sent_cards[-1])
			connection.send_cards_to(self_name, not_sent_cards.pop(), get_cards_from_deck(deck, cards_per_player))
		# Default behavior
		else:
			if message.type == "CARD_PAYLOAD":
				
				#print("[DEBUG] [Sender] Card payload")
				
				# First play
				if (is_dealer() and not game_started):
					game_started = True
					play_menu()
				elif (is_dealer() and return_token_target != None):
				 	token = False
				 	connection.pass_token(self_name, return_token_target)

				 	#print("[DEBUG] Returning token to " + return_token_target)

				 	# Return parameters
				 	return_token_target = None
				 	send_card_amount = 0

			if message.type == "PLAY":
				#print("[DEBUG] [Sender] Play")
				token = False

				if (len(cards) == 1):
					input("Press enter to shout UNO!")
					connection.uno(self_name)
				elif (len(cards) == 0):
					connection.win(self_name)

				if (last_card.card_type == "SKIP"):
					connection.pass_token_skip(self_name)
					#print("[DEBUG] Sending token to next-next player")
				else:
				 	connection.pass_token(self_name)
				 	#print("[DEBUG] Sending token to next player")

			if message.type == "TOKEN":
				None
				#print("[DEBUG] [Sender] Token")

			if message.type == "CARD_REQUEST":
				#print("[DEBUG] [Sender] Card request")

				token = False

				#print("[DEBUG] [Card Request] Sending token to " + dealer)
				connection.pass_token(self_name, dealer)

			if message.type == "UNO":
				if (last_card.card_type == "SKIP"):
					connection.pass_token_skip(self_name)
					#print("[DEBUG] Sending token to next-next player")
				else:
				 	connection.pass_token(self_name)
				 	#print("[DEBUG] Sending token to next player")
	else:
		#print("[DEBUG] Resending message!")
		##print("[DEBUG] Resent message: " + str(message.__dict__))
		connection.send_message(message)




