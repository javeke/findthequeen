import json
import socket
from utils.Player import Player
from game_client import GameClient
from utils.utilities import UTF_FORMAT, utf8_encode
from getpass import getpass
import sys

def run(HOST_IP):

  # Constants
  PORT = 7621

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as player:

    player.connect((HOST_IP, PORT))

    # Receive ACCEPT
    player.recv(1024).decode() 
    
    print("Welcome To Find The Queen")

    print("Please enter your username")
    username = input("Username: ")

    player.send(utf8_encode(username))
    # Receive RECEIVED
    player.recv(1024).decode() 

    print("***Your password will be hidden***")
    print("Please enter your password")
    password = getpass("Password: ")

    player.send(utf8_encode(password))
    # Receive RECEIVED
    player.recv(1024).decode() 

    player.send(utf8_encode("AWAITING VALIDITY"))

    # Waiting for another player
    validity = json.loads(player.recv(1024).decode(encoding=UTF_FORMAT))
    player.send(utf8_encode("RECEIVED"))

    if validity["valid"]:
      print("Waiting for another player")

      # Waiting for start signal
      print(player.recv(1024).decode())
      game_player = Player(username, player)
      game =  GameClient(game_player)

      game.start()
      game.declare_winner()

      print("\n\n")
      print(player.recv(1024).decode(encoding=UTF_FORMAT))

    else:
      print("Invalid credentials")
      print("Closing connection...")

        

if __name__ == "__main__":

  if len(sys.argv) != 2:
    print("Please provide the ip address of the server")
    sys.exit(1)

  host_ip_address = sys.argv[1]
  run(host_ip_address)
