from secrets import choice
from utils.Player import Player
from utils.PlayerRole import PlayerRole
from utils.utilities import utf8_encode
from getpass import getpass


class RoundClient:

  def __init__(self, player: Player, role=None) -> None:
    self.player = player
    self.role = role
    self.choice = None

  def start_round(self):
    # Starting round
    print("Starting round\n")

    # Player role
    self.role = int(self.player.socketConnection.recv(1024).decode()) 
    role_name = PlayerRole(self.role).name
    print(f"For this round you are the {role_name}")
    if self.role == PlayerRole.DEALER.value:
      print("***Your choice will be hidden***")
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
      print("You guessed correctly. You won this round!\n\n")
    else:
      print("You chose incorrectly. You lost this round.\n\n")

    return result