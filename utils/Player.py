from socket import socket

from utils.PlayerRole import PlayerRole


class Player:

  def __init__(self, username: str, socketConnection: socket, role: PlayerRole = None):
    self.username = username
    self.socketConnection = socketConnection
    self.role = role
    self.points = 0