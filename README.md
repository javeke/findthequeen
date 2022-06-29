# Multiplayer Find the Queen Game

**Find the Queen** is a simple multiplayer game played between two players where one is the 
dealer and one is the spotter. The dealer selects 1 of 3 positions to hide the "Queen" and the 
spotter tries to find the "Queen" in 1 of those 3 positions.
The objective of the game is for the dealer to successfully hide the queen from the player for 5 rounds while the spotter will try to find the queen.

During the game, you will notice that the users' password and the dealer's choice are always hidden.

## Requirements

You will need to have **Python 3** downloaded and installed in order to start the game.

Follow this [link](https://www.python.org/downloads/) to download **Python 3** in case you do not have it already.


## Starting The Game

To start the game, you will need to launch the game server first.

Run this command

`python server.py`

After the server has started, run the following command to start connecting to the server as a player.
Replace the `HOST` with the actual host ip address that the server is running on. Ensure that both 
device are able to connect over a network if server and client are running on different machines.

You may need to run `ipconfig` on Windows or `ip addr` on Linux to determine the correct ip address to use
based on the number of network adapters you have installed on your machine.

`python client.py <HOST>`


## Docker Install

There is a Docker image available for the server at [Find The Queen Server](https://hub.docker.com/r/javeke/ftqserver)

Run this command to pull the docker image from Docker Hub

`docker pull javeke/ftqserver`

Then run this command to start the server using docker

`docker run -p 7621:7621 javeke/ftqserver`


You can also choose to build the docker image yourself with the `Dockerfile.server` that is in the repository

Run  `docker build <YOUR_DOCKER_USERNAME>/ftqserver:latest -f Dockerfile.server .`

Then in order to run with this image use the command below

`docker run -p 7621:7621 <YOUR_DOCKER_USERNAME>/ftqserver:latest`



### Docker Note

Bare in mind, if you are running the server using docker, you will need to supply the proper ip address to the client. If the docker host is the same machine as the client application then use `127.0.0.1` for the 
ip address, otherwise more configuration will be required to set up this communication.
