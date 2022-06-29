from game.Player import Player
from utils.utilities import utf8_encode
from utils.logger import logging

class Round:

  def __init__(self, dealer: Player, spotter: Player) -> None:
    self.dealer = dealer
    self.spotter = spotter
    self.dealer_choice = None
    self.spotter_choice = None
  

  def start_round(self):
    self.dealer.socketConnection.send(utf8_encode(str(self.dealer.role.value)))
    self.spotter.socketConnection.send(utf8_encode(str(self.spotter.role.value)))

    logging.info("Awaiting dealer's choice")
    # Awaiting dealer's choice
    self.dealer_choice = self.dealer.socketConnection.recv(1024).decode()

    logging.info("Recevied dealer's choice")
    self.spotter.socketConnection.send(utf8_encode("RECEIVED CHOICE"))

    logging.info("Awaiting spotter's choice")
    # Awaiting spotter's choice
    self.spotter_choice = self.spotter.socketConnection.recv(1024).decode()

    logging.info("Recevied spotter's choice")
    self.dealer.socketConnection.send(utf8_encode("RECEIVED CHOICE"))
    # RECEIVED
    self.dealer.socketConnection.recv(1024).decode()

    if self.spotter_choice == self.dealer_choice:
      self.spotter.socketConnection.send(utf8_encode("CORRECT"))
      self.dealer.socketConnection.send(utf8_encode("INCORRECT"))
      return self.spotter
    else:
      self.dealer.socketConnection.send(utf8_encode("CORRECT"))
      self.spotter.socketConnection.send(utf8_encode("INCORRECT"))
      return self.dealer