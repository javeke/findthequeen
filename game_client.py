import json
from utils.Player import Player
from round_client import RoundClient
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

      print(f"My Score - {scores['me']['score']} \t\t  {scores['other']['username']} Score - {scores['other']['score']}")

  
  def declare_winner(self):
    game_result = self.player.socketConnection.recv(1024).decode(encoding=UTF_FORMAT)
    
    final_results = json.loads(game_result)

    if final_results["result"] == "Victory":
      print("\n\n")
      print("Victory")
      print("Final Score")
      print(f'My Score - {final_results["me"]["score"]} \t\t {final_results["other"]["username"]} Score - {final_results["other"]["score"]}')
    
    else:
      print("\n\n")
      print("Defeat")
      print("Final Score")
      print(f'My Score - {final_results["me"]["score"]} \t\t {final_results["other"]["username"]} Score - {final_results["other"]["score"]}')
