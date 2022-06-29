import json
from time import sleep
from utils.Player import Player
from utils.PlayerRole import PlayerRole
from round import Round
from utils.utilities import UTF_FORMAT, utf8_encode
import random
from utils.logger import logging

class Game:

  GAME_ROUNDS = 5

  def __init__(self, player1: Player, player2: Player):
    self.player1 = player1
    self.player2 = player2
    self.winner = None

  def start(self):
    logging.info("Starting game")
    self.player1.socketConnection.send(utf8_encode("START"))
    self.player2.socketConnection.send(utf8_encode("START"))

    randomRole = random.choice([PlayerRole.DEALER, PlayerRole.SPOTTER])

    self.player1.role = randomRole
    self.player2.role = PlayerRole(1 - randomRole.value)

    for round_number in range(Game.GAME_ROUNDS):
      round = None
      if self.player1.role == PlayerRole.DEALER:
        round = Round(self.player1, self.player2)
      else:
        round = Round(self.player2, self.player1)
      
      logging.info(f"Starting round {round_number+1}")
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

      sleep(1)
      
      self.player1.role = self.player2.role
      self.player2.role = PlayerRole(1 - self.player2.role.value)


  def declare_winner(self):
    logging.info("Declaring the winner")
    
    if self.player1.points > self.player2.points:
      self.player1.socketConnection.send(
        bytes(json.dumps({
          "result":"Victory",
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
          "result":"Defeat",
          "other":{
            "username": self.player1.username,
            "score": self.player1.points
          },
          "me":{
            "username": self.player2.username,
            "score": self.player2.points
          }
        }), encoding=UTF_FORMAT)
      )

      sleep(1)
      return self.player1


    self.player1.socketConnection.send(
      bytes(json.dumps({
        "result":"Defeat",
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
        "result":"Victory",
        "other":{
          "username": self.player1.username,
          "score": self.player1.points
        },
        "me":{
          "username": self.player2.username,
          "score": self.player2.points
        }
      }), encoding=UTF_FORMAT)
    )
    sleep(1)
    return self.player2