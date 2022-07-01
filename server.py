import json
import socket
from game import Game
from utils.Player import Player
from utils.logger import logging
from service import auth
from utils.utilities import utf8_encode, UTF_FORMAT

def run():

  # Constants
  HOST_IP = socket.gethostbyname(socket.gethostname())
  PORT = 7621
  BACKLOG_SIZE = 2
  SOCKET_TIMEOUT = 1

  # Initialization
  game_started = False
  connected_players = []

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.settimeout(SOCKET_TIMEOUT)
    server.bind((HOST_IP, PORT))
    server.listen(BACKLOG_SIZE)

    while True:
      try:
        player, address = server.accept()
        logging.info("Accepting player")
        player.send(utf8_encode("ACCEPT"))

        username = player.recv(1024).decode(encoding=UTF_FORMAT)
        player.send(utf8_encode("RECEIVED"))

        password = player.recv(1024).decode(encoding=UTF_FORMAT)
        player.send(utf8_encode("RECEIVED"))

        logging.info("Validating player credentials")
        # AWAITING VALIDITY
        player.recv(1024).decode()
        isValid = auth.validate_credentials(username, password)

        if isValid:
          logging.info("Player credentials validated")
          logging.info("Player connected")

          connected_players.append({"username": username, "player": player})

          player.send(bytes(json.dumps({ "valid":True, "players":1 }), encoding=UTF_FORMAT))
          # RECEIVED
          player.recv(1024).decode()
          
          # Game logic  

          if len(connected_players) == 2:
            game_started = True
            player1 = Player(connected_players[0]["username"], connected_players[0]["player"])
            player2 = Player(connected_players[1]["username"], connected_players[1]["player"])

            game = Game(player1, player2)

            game.start()
            game.declare_winner()

            logging.info("Game Over")
            

            player1.socketConnection.send(utf8_encode("Thanks For Playing"))
            player2.socketConnection.send(utf8_encode("Thanks For Playing"))

            game_started = False
            connected_players = []

        else:
          logging.info("Player credentials invalid")
          player.sendall(bytes(json.dumps({ "valid":False }), encoding=UTF_FORMAT))
          
      except OSError:
        if not game_started:
          logging.info(f"Waiting on players to join at {HOST_IP}:{PORT}")
        else:
          logging.info("Game in progress")


if __name__ == "__main__":
  logging.info("Starting socket server")
  run()