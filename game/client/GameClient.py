import json
from game.Player import Player
from game.client.RoundClient import RoundClient
from utils.utilities import UTF_FORMAT, utf8_encode

class GameClient:

  GAME_ROUNDS = 5

  def __init__(self, player: Player):
    self.player = player

  def start(self):
    # Starting game message
    print("Starting game")

    for _ in range(GameClient.GAME_ROUNDS):
      round = RoundClient(self.player)
      round.start_round()

      round_result = self.player.socketConnection.recv(1024).decode(encoding=UTF_FORMAT)
      scores = json.loads(round_result)

      print(f"{scores['me']['username']} - {scores['me']['score']} \t\t  {scores['other']['username']} - {scores['other']['score']}")

      self.player.socketConnection.send(utf8_encode("RECEIVED"))

  
  def declare_winner(self):
    game_result = self.player.socketConnection.recv(1024).decode(encoding=UTF_FORMAT)

    final_results = json.loads(game_result)

    if final_results["result"] == "Victory":
      print("\n\n")
      print("Victory")
      print("Final Score")
      print(f'{final_results["winner"]["username"]} - {final_results["winner"]["score"]} \t\t {final_results["loser"]["username"]} - {final_results["loser"]["score"]}')
    
    else:
      print("\n\n")
      print("Defeat")
      print("Final Score")
      print(f'{final_results["winner"]["username"]} - {final_results["winner"]["score"]} \t\t {final_results["loser"]["username"]} - {final_results["loser"]["score"]}')