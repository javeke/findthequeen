from secrets import choice
from game.Player import Player
from game.PlayerRole import PlayerRole
from utils.utilities import utf8_encode
from getpass import getpass


class RoundClient:

  def __init__(self, player: Player, role=None) -> None:
    self.player = player
    self.role = role
    self.choice = None

  def start_round(self):
    # Starting round
    print("Starting round")

    # Player role
    self.role = int(self.player.socketConnection.recv(1024).decode()) 
    print(self.role)
    if self.role == PlayerRole.DEALER.value:
      print("Select a choice (1, 2, 3):")
      self.choice = getpass("Choice: ")
      self.player.socketConnection.send(utf8_encode(self.choice))
      print("Awaiting spotter's choice")
      # RECEIVED CHOICE
      self.player.socketConnection.recv(1024).decode()
      self.player.socketConnection.send(utf8_encode("RECEIVED"))
    
    else:
      print("Awaiting dealer's choice")
      # RECEIVED CHOICE
      self.player.socketConnection.recv(1024).decode()
      print("Select a choice (1, 2, 3):")
      self.choice = input("Choice: ")
      self.player.socketConnection.send(utf8_encode(self.choice))


    result = self.player.socketConnection.recv(1024).decode()

    if result == "CORRECT":
      print("You guessed correctly. You won this round!")
    else:
      print("You chose incorrectly. You lost this round.")

    return result