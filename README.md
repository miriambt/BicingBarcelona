# BicingBot

The BicingBot project consists in the implementation of a Telegram Bot that answers commands related to geomentric graphs defined on the stations of the Bicing company in Barcelona, both textually and graphically (with maps). All the data regarding the stations is downloaded immediately. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to install the sofware, you must make sure you have all the libraries mentioned on the prerequisites.txt file installed and up to date. On the contrary, you will find the command lines that will help you with the installing in the same file. 
Moreover, in order to run the BicingBot, it is absolutely necessary to have previously installed the Telegram App.

### Installing

So as to uncompress the file, you must write the following command line on the terminal: 
	
	$ unzip bicingBot.zip
	
One simple way of installing the Telegram App is through their website. Check out the link below for full details. 

```
http://telegram.com.es/descargar-telegram/
```

## Commands

The project answers the following commands, all of them beggining with '/'.

### /start

Iniciates the conversation with the Bot and, by default, it creates a graph with d = 1000.

### /authors

Writes the name of the authors of the project and their emails.

### /graph <distance>

Creates a graph with nodes and edges at distance lower than distance "d". By default, d = 1000.

### /nodes

Prints the number of nodes (stations) of the graph.

### /edges

Prints the number of edges of the graph.

### /components

Prints the number of connected components of the graph.

### /plotgraph

Shows an image corresponding to a map, with the corresponding nodes (red) and edges(blue)

### /route <origin, destination>

Shows an image corresponding to the shortest path between the origin and the destination. It also prints the expected time until your destination. 
Walking sections can be made from the origin point to a bicing station, or from a bicing station to the destination point. Bicycle stretches can be made between pairs of bicing stations at a distance less than or equal to d, that is, through the edges of the graph. The average speed on foot is 4 km/h and by bike of 10 km/h. Trajectories are measured at bird's eye (straight line).

### /distribute <bikes, docks>

Prints the route and the number of bikes that a hypothetical vehicle should carry in order to guarantee that every station of the Bicing company in Barcelona has 'n' bicycles and 'm' empty docks. If the requirements are not possible,

```
No solution could be found
```
is printed.

### /help

It prints all the commands mentioned above in order to help the user run the bot.

## Deployment

In order to open the bot, click on 'https://t.me/bicingbcn_bot'.


## Authors

* **Míriam Barrabés i Torrella** 
* **Joan Vaquer Perelló**
