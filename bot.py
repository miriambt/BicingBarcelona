import telegram
from data import *
from telegram.ext import Updater
from telegram.ext import CommandHandler
import os

TOKEN = '881647707:AAHJuAV_jyipzKQCJGKnlfKqk21a-q62FVo'

''' Iniciates the conversation with the Bot and, by default, creates a graph with d = 1000.'''
def start(bot, update, user_data):
    name = update.message.chat.first_name
    message = "Hello, " + name + "!"
    bot.send_message(chat_id=update.message.chat_id, text=message)
    G = CreateGraph_nlogn()
    user_data['graph'] = G


''' Prints all the name of all the possible commands and a short explanation in order to help the user run the bot.'''
def help_(bot, update):
    message = 'This Bot answers textually and graphically (with maps) questions related to geometric graphs defined on the stations of the bicing of Barcelona. \n\
            It answers the following commands: \n\
            /start: initiates a conversation with the Bot.  \n\
            /authors: writes the name of the authors of the project and their emails.  \n\
            /graph <distance>: creates a graph with nodes and edges at distance lower than d. By default, d = 1000  \n\
            /nodes: prints the numbers of stations at distance lower than d. \n\
            /edges: print the number of edges in the graph.  \n\
            /components: prints the number of connex components in the graph.  \n\
            /plotgraph: shows an image corresponding to a map, with the corresponding nodes of the graph (in red) and the edges(in blue).  \n\
            /route origin, destination: shows an image corresponding to the shortest path between the origin and the destination. It also prints the expected time that takes you to the destination. \n\
            /distribute <bikes, docks>: prints the route and the number of bikes that a hypothetical vehicle should carry in order to guarantee that every station of the Bicing company in Barcelona has n bicycles and m empty docks.'

    bot.send_message(chat_id=update.message.chat_id, text=message)


''' Writes the name of the authors of the project and their emails.'''
def authors(bot, update):
    integrant1 = "Joan Vaquer Perelló (joan.vaquer@est.fib.upc.edu)"
    integrant2 = "Míriam Barrabés i Torrella (miriam.barrabes.i@est.fib.upc.edu)"
    bot.send_message(chat_id=update.message.chat_id, text=integrant1)
    bot.send_message(chat_id=update.message.chat_id, text=integrant2)


''' If given an argument, creates a graph with nodes and edges at distance lower than the distance given.
If the distance is >= 300, the graph is created in nlog(n) time.
On the contrary, the graph is created in quadratic time.'''
def graph(bot, update, user_data, args):
    bot.send_message(chat_id=update.message.chat_id, text="Creating graph")
    if not args:
        G = CreateGraph_nlogn()
    else:
        if int(args[0]) >= 300:
            G = CreateGraph_nlogn(int(args[0]))
        else:
            G = CreateGraph_nn(int(args[0]))

    bot.send_message(chat_id=update.message.chat_id, text="Graph created!")
    user_data['graph'] = G


''' Prints the number of nodes (stations) of the graph.'''
def number_nodes(bot, update, user_data):
    n = nodes(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text=n)


''' Prints the number of edges of the graph.'''
def number_edges(bot, update, user_data):
    e = edges(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text=e)


''' Prints the number of connected components of the graph.'''
def connex_components(bot, update, user_data):
    c = components(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text=c)


''' Shows an image corresponding to a map, with the corresponding nodes (red) and edges(blue)'''
def plotgraph(bot, update, user_data):
    try:
        path = str(update.message.chat.id) + '.png'
        draw_graph(user_data['graph'], path)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(path, 'rb'))
        os.remove(path)
    except:
        print("error")


''' Concatenates all the words in one string'''
def concatenate(args):
    paraula = args[0]
    n = len(args)
    for i in range(1, n):
        paraula += ' ' + args[i]
    return paraula


''' Given an hour, it decomposes it in hours, minutes and seconds, and returns this values in a string.'''
def hours_to_string(hour):
    seconds = hour*3600
    h = int(seconds//3600)
    m = int((seconds % 3600)//60)
    s = int((seconds % 3600) % 60)
    time = str(h) + " hours, " + str(m) + " minutes and " + str(s) + " seconds"
    return time


''' Given a route, shows an image corresponding to the shortest path between the origin and the destination.
It also prints the expected time until the user arrives to the destination.'''
def route(bot, update, user_data, args):
    path1 = str(update.message.chat.id) + 'jm.png'
    p = concatenate(args)
    a = ShortestPath(user_data['graph'], p, path1)
    if a is not "Adress not found":
        bot.send_message(chat_id=update.message.chat_id,
                         text="Searching for the fastest path...")
        bot.send_photo(chat_id=update.message.chat_id, photo=open(path1, 'rb'))
        b = hours_to_string(a)
        bot.send_message(chat_id=update.message.chat_id, text=b)
        os.remove(path1)
    else:
        bot.send_message(chat_id=update.message.chat_id, text=a)


''' Prints the route and the number of bikes that a hypothetical vehicle should carry in order to guarantee that every station
of the Bicing company in Barcelona has 'n' bicycles and 'm' empty docks.'''
def distribute(bot, update, user_data, args):
    requiredBikes = int(args[0])
    requiredDocks = int(args[1])
    totalkm, maxcost, err = distribute(
        user_data['graph'], requiredBikes, requiredDocks)
    if err and totalkm == 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text="No solution could be found")
    elif err and totalkm == 2:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Fatal Error: Incorrect graph model.")
    else:
        message1 = "The total cost of transferring bikes is:" + \
            str(int((totalkm))/1000) + " km."
        message2 = "The move of maxmimum cost is:" + \
            str(int((maxcost[0]*1000))/1000) + " km*bikes, between the stations " + \
            str(maxcost[1]) + " and " + str(maxcost[2])
        bot.send_message(chat_id=update.message.chat_id, text=message1)
        bot.send_message(chat_id=update.message.chat_id, text=message2)


# Declares a constant with the access token that reads from token.txt
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# As soon as the bot receives a message with some of the commands bwlow, it will execute the corresponding function
dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
dispatcher.add_handler(CommandHandler('help', help_))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler(
    'graph', graph, pass_user_data=True, pass_args=True))
dispatcher.add_handler(CommandHandler(
    'plotgraph', plotgraph, pass_user_data=True))
dispatcher.add_handler(CommandHandler(
    'nodes', number_nodes, pass_user_data=True))
dispatcher.add_handler(CommandHandler(
    'edges', number_edges, pass_user_data=True))
dispatcher.add_handler(CommandHandler(
    'components', connex_components, pass_user_data=True))
dispatcher.add_handler(CommandHandler(
    'route', route, pass_user_data=True, pass_args=True))
dispatcher.add_handler(CommandHandler(
    'distribute', distribute, pass_user_data=True, pass_args=True))

# Starts up the bot
updater.start_polling()
