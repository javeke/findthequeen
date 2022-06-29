# Multiplayer Find the Queen Game

**Find the Queen** is a simple multiplayer game played between two players where one is the 
dealer and one is the spotter. The dealer selects 1 of 3 positions to hide the "Queen" and the 
spotter tries to find the "Queen" in 1 of those 3 positions.
The objective of the game is for the dealer to successfully hide the queen from the player for 5 rounds while the spotter will try to find the queen.

## Requirements

You will need to have **Python 3** downloaded and installed in order to start the game.

Follow this [link](https://www.python.org/downloads/) to download **Python 3** in case you do not have it already.


## Starting The Game

To start the game, you will need to launch the game server first.

Run this command

`python server.py`

After the server has started, run the following command to start connecting to the server as a player.
Replace the `HOST` with the actual host ip address and that the server is running on. Ensure that both 
device have network connectivity.

`python client.py <HOST>`