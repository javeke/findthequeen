import json
from game.Player import Player
from game.PlayerRole import PlayerRole
from game.server.Round import Round
from utils.utilities import UTF_FORMAT, utf8_encode
import random

class Game:

  GAME_ROUNDS = 5

  def __init__(self, player1: Player, player2: Player):
    self.player1 = player1
    self.player2 = player2
    self.winner = None

  def start(self):
    self.player1.socketConnection.send(utf8_encode("START"))
    self.player2.socketConnection.send(utf8_encode("START"))

    randomRole = random.choice([PlayerRole.DEALER, PlayerRole.SPOTTER])

    self.player1.role = randomRole
    self.player2.role = PlayerRole(1 - randomRole.value)

    for _ in range(Game.GAME_ROUNDS):
      round = None
      if self.player1.role == PlayerRole.DEALER:
        round = Round(self.player1, self.player2)
      else:
        round = Round(self.player2, self.player1)
      
      round_winner = round.start_round()

      if round_winner.username == self.player1.username:
        self.player1.points += 1
      else:
        self.player2.points += 1

      self.player1.socketConnection.send(
        bytes(json.dumps({
          "me":{
            "username": self.player1.username,
            "score": self.player1.points
          },
          "other":{
            "username": self.player2.username,
            "score": self.player2.points
          }
        }), encoding=UTF_FORMAT)
      )

      self.player2.socketConnection.send(
        bytes(json.dumps({
          "me":{
            "username": self.player2.username,
            "score": self.player2.points
          },
          "other":{
            "username": self.player1.username,
            "score": self.player1.points
          }
        }), encoding=UTF_FORMAT)
      )

      # RECEIVED
      self.player1.socketConnection.recv(1024).decode(encoding=UTF_FORMAT)
      # RECEIVED
      self.player2.socketConnection.recv(1024).decode(encoding=UTF_FORMAT)
      
      self.player1.role = self.player2.role
      self.player2.role = PlayerRole(1 - self.player2.role.value)


  def declare_winner(self):
    if self.player1.points > self.player2.points:
      self.player1.socketConnection.send(
        bytes(json.dumps({
          "result":"Victory",
          "winner":{
            "username": self.player1.username,
            "score": self.player1.points
          },
          "loser":{
            "username": self.player2.username,
            "score": self.player2.points
          }
        }), encoding=UTF_FORMAT)
      )

      self.player2.socketConnection.send(
        bytes(json.dumps({
          "result":"Defeat",
          "winner":{
            "username": self.player1.username,
            "score": self.player1.points
          },
          "loser":{
            "username": self.player2.username,
            "score": self.player2.points
          }
        }), encoding=UTF_FORMAT)
      )
      return self.player1


    self.player1.socketConnection.send(
      bytes(json.dumps({
        "result":"Defeat",
        "loser":{
          "username": self.player1.username,
          "score": self.player1.points
        },
        "winner":{
          "username": self.player2.username,
          "score": self.player2.points
        }
      }), encoding=UTF_FORMAT)
    )

    self.player2.socketConnection.send(
      bytes(json.dumps({
        "result":"Victory",
        "winner":{
          "username": self.player1.username,
          "score": self.player1.points
        },
        "loser":{
          "username": self.player2.username,
          "score": self.player2.points
        }
      }), encoding=UTF_FORMAT)
    )
    return self.player2