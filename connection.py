
# -*- coding: utf-8 -*-

__name__ = "connection"

import socket
import pickle

# ENV file stuff
import os
from os.path import join, dirname

A_IP = "j21"
B_IP = "j18"
C_IP = "j24"
D_IP = "j25"

A_PORT = 4160
B_PORT = 4130
C_PORT = 4131
D_PORT = 4460

DEALER = "A"

listener_socket = None
sender_socket = None
dest_info = None

# -------------------------------------------
# Message class
class Message:
	def __init__(self, sender, target, msg_type, content=None):
		self.sender = sender # A, B, C, D, ...
		self.target = target # A, B, C, D, ..., ALL
		self.type = msg_type # CARD_PAYLOAD, TOKEN, PLAY, CARD_REQUEST
		self.content = content # ?

	def __eq__(self, other):
		if isinstance(other, Message):
			if self.sender == other.sender and self.target == other.target and self.type == other.type:
				return True
		return False

# -------------------------------------------
 
# ---------------------------------------
def get_dealer():
	return DEALER

def get_next_player(self_name):
	if (self_name == "A" ):
		return "B", B_IP, int(B_PORT)
	elif (self_name == "B"):
		return "C", C_IP, int(C_PORT)
	elif (self_name == "C"):
		return "D", D_IP, int(D_PORT)
	elif (self_name == "D"):
		return "A", A_IP, int(A_PORT)

def get_self_info(self_name):
	if (self_name == "A" ):
		return "A", A_IP, int(A_PORT)
	elif (self_name == "B"):
		return "B", B_IP, int(B_PORT)
	elif (self_name == "C"):
		return "C", C_IP, int(C_PORT)
	elif (self_name == "D"):
		return "D", D_IP, int(D_PORT)

def setup_connection(self_name):
	# sets send target
	target_name, target_ip, target_port = get_next_player(self_name)
	#print("[DEBUG] Connecting send socket to " + target_name)

	global sender_socket
	sender_socket = socket.socket(socket.AF_INET, # Internet
	                   socket.SOCK_DGRAM) # UDP

	global dest_info
	dest_info = (target_ip, target_port)	

	# sets listener socket
	global listener_socket
	self_name, self_ip, self_port = get_self_info(self_name)
	#print("[DEBUG] Setting listener " + self_name)

	listener_socket = socket.socket(socket.AF_INET, # Internet
	                   socket.SOCK_DGRAM) # UDP

	#print((self_ip, self_port))

	listener_socket.bind((self_ip, self_port))

def wait_message():
	data, addr = listener_socket.recvfrom(1024)
	message = pickle.loads(data)
	return message

def send_message(message):
	message_code = pickle.dumps(message)
	sender_socket.sendto(message_code, dest_info)

def send_cards_to(sender, target, cards):
	#print("[DEBUG] Sending cards to " + target)
	message = Message(sender, target, "CARD_PAYLOAD", cards)
	send_message(message)

def pass_token(sender, target=False):
	if (target):
		message = Message(sender, target, "TOKEN")
	else:
		target = get_next_player(sender)[0]
		message = Message(sender, target, "TOKEN")

	#print("[DEBUG] Sending token to " + target)

	send_message(message)

def pass_token_skip(sender):
	skipped_player = get_next_player(sender)[0]
	target = get_next_player(skipped_player)[0]

	pass_token(sender, target)

def send_play(sender, card):
	#print("[DEBUG] Sending played card to ALL")
	message = Message(sender, "ALL", "PLAY", card)
	"""for card in initial_cards:
		print(card)
	"""
	send_message(message)

def request_cards(sender, target, amount):
	#print("[DEBUG] Sending " + str(amount) +" card requests to " + target)
	message = Message(sender, target, "CARD_REQUEST", amount)
	send_message(message)

def uno(sender):
	#print("[DEBUG] Sending UNO!")
	message = Message(sender, "ALL", "UNO")
	send_message(message)

def win(sender):
	#print("[DEBUG] Sending win warning!")
	message = Message(sender, "ALL", "WIN")
	send_message(message)
# ---------------------------------------


 

