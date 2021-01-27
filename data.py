import json
import urllib.request
from staticmap import StaticMap, CircleMarker, Line
from haversine import haversine
from jutge import read
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from geopy.geocoders import Nominatim


''' Returns a graph with all the nodes corresponding to the stations of the Bicing company in Barcelona,
downloaded from the url below, and all the edges between nodes at distance <= dist.
Its cost is quadratic.'''
def CreateGraph_nn(dist=1000):
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = pd.DataFrame.from_records(pd.read_json(
        url)['data']['stations'], index='station_id')
    G = nx.Graph()
    for st in bicing.itertuples():
        coord1 = (st.lat, st.lon)
        G.add_node(coord1)
        for dt in bicing.itertuples():
            coord2 = (dt.lat, dt.lon)
            distcoords = haversine(coord1, coord2)
            if dist >= distcoords*1000 and distcoords != 0:
                G.add_edge(coord1, coord2, weight=distcoords/10)
    return G


''' Returns the bounding box of a list of nodes.'''
def bbox(G):
    nodes = list(G.nodes())
    max_x, min_x = nodes[0][0], nodes[0][0]
    max_y, min_y = nodes[0][1], nodes[0][1]
    for node in nodes:
        if node[0] < min_x:
            min_x = node[0]
        if node[0] > max_x:
            max_x = node[0]
        if node[1] < min_y:
            min_y = node[1]
        if node[1] > max_y:
            max_y = node[1]

    return min_x, min_y, max_x, max_y


''' Given a graph, a dist, and a pair of nodes, adds a new edge in the graph between these nodes
if the distance between them is <= than dist.'''
def new_edge(G, dist, node, elem):
    distcoords = haversine(node, elem)
    if dist >= distcoords*1000 and distcoords != 0:
        G.add_edge(node, elem, weight=distcoords/10)
    return G


''' Returns a graph with all the nodes corresponding to the stations of the Bicing company in Barcelona,
downloaded from the url below, and all the edges between nodes at distance <= dist.
Its cost is nlogn.'''
def CreateGraph_nlogn(dist=1000):
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = pd.DataFrame.from_records(pd.read_json(
        url)['data']['stations'], index='station_id')
    G = nx.Graph()

    for st in bicing.itertuples():
        coord1 = (st.lat, st.lon)
        G.add_node(coord1)
    # We found the bounding box that contains all the nodes of the graph and divide it in subsquares, as explained in class.
    min_x, min_y, max_x, max_y = bbox(G)
    total_weight = haversine((min_x, min_y), (max_x, min_y))
    total_height = haversine((min_x, min_y), (min_x, max_y))
    rows = total_height//(dist/1000)+1
    cols = total_weight//(dist/1000)+1

    # We create an empty dictionary and update all the lists of nodes related to each key number of the list.
    # The key number corresponds to a number between 1 and rows*cols.
    d = {}
    for i in range(int(cols*rows)):
        d.update({i+1: []})

    for node in G.nodes():
        casella_x = haversine(node, (min_x, node[1]))//(dist/1000) + 1
        casella_y = haversine(node, (node[0], max_y))//(dist/1000) + 1
        casella = (casella_y-1)*cols + casella_x
        d[casella].append(node)

    for casella in d:
        if casella <= cols and casella % cols != 0:
            for node in d[casella]:
                # We look at the nodes in the same subsquare.
                for elem in d[casella]:
                    G = new_edge(G, dist, node, elem)
                # We look at the nodes in right subsquare.
                for elem in d[casella+1]:
                    G = new_edge(G, dist, node, elem)
                # We look at the nodes in the below subsquare.
                for elem in d[casella+cols]:
                    G = new_edge(G, dist, node, elem)
                # We look at the nodes in the up-right subsquare.
                for elem in d[casella+cols+1]:
                    G = new_edge(G, dist, node, elem)

        elif (casella > cols*(rows-1)) and (casella % cols != 0):
            for node in d[casella]:
                # We look at the nodes in the same subsquare.
                for elem in d[casella]:
                    G = new_edge(G, dist, node, elem)
                # We look at the nodes in right subsquare.
                for elem in d[casella+1]:
                    G = new_edge(G, dist, node, elem)
                # We look at the nodes in the up-right subsquare.
                for elem in d[casella-cols+1]:
                    G = new_edge(G, dist, node, elem)

        elif casella % cols == 0 and cols*rows != casella:
            for node in d[casella]:
                # We look at the nodes in the same subsquare.
                for elem in d[casella]:
                    G = new_edge(G, dist, node, elem)
                # We look at the nodes in the below subsquare.
                for elem in d[casella+cols]:
                    G = new_edge(G, dist, node, elem)

        elif cols*rows != casella:
            for node in d[casella]:
                for elem in d[casella]:
                    G = new_edge(G, dist, node, elem)
                # We look at the nodes in right subsquare.
                for elem in d[casella+1]:
                    G = new_edge(G, dist, node, elem)
                # We look at the nodes in the below subsquare.
                for elem in d[casella+cols]:
                    G = new_edge(G, dist, node, elem)
                # We look at the nodes in the down-right subsquare.
                for elem in d[casella+cols+1]:
                    G = new_edge(G, dist, node, elem)
                # We look at the nodes in the up-right subsquare.
                for elem in d[casella-cols+1]:
                    G = new_edge(G, dist, node, elem)

    return G


''' Plots an image corresponding to a map, with the corresponding nodes (red) and edges(blue).'''
def draw_graph(G, user_image_path):
    m_bcn = StaticMap(800, 800)
    for edge in G.edges():
        lat1, lon1 = edge[0][0], edge[0][1]
        node1 = (lon1, lat1)
        lat2, lon2 = edge[1][0], edge[1][1]
        node2 = (lon2, lat2)
        marker1 = CircleMarker(node1, 'red', 6)
        marker2 = CircleMarker(node2, 'red', 6)
        m_bcn.add_marker(marker1)
        m_bcn.add_marker(marker2)
        m_bcn.add_line(Line((node1, node2), 'blue', 1))
    image = m_bcn.render()
    image.save(user_image_path)

''' Returns the number of nodes (stations) of the graph.'''
def nodes(G):
    return G.number_of_nodes()

''' Returns the number of edges of the graph.'''
def edges(G):
    return G.number_of_edges()

''' Returns the number of connected components of the graph.'''
def components(G):
    return nx.number_connected_components(G)

''' Given an adress, it translates it to its corresponding coordinates.'''
def addressesTOcoordinates(addresses):
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)
    except:
        return None

''' Given two adresses, plots the minimum route between them.
It also returns the expected time until the user arrives to the destination.'''
def ShortestPath(G, adresses, user_image_path):
    coords = addressesTOcoordinates(adresses)
    if coords is None:
        a = "Adress not found"
        return a
    else:
        coord_origen, coord_desti = coords
        G.add_node(coord_origen)
        G.add_node(coord_desti)

        for node in G.nodes():
            distcoords1 = haversine(coord_origen, node)
            G.add_edge(coord_origen, node, weight=distcoords1/4)
            distcoords2 = haversine(coord_desti, node)
            G.add_edge(coord_desti, node, weight=distcoords2/4)

        F = nx.dijkstra_path(G, coord_origen, coord_desti)
        G = nx.Graph()
        length = len(F)
        time = 0
        for i in range(length-1):
            G.add_edge(F[i], F[i+1])
            if i == 0 or i == length-2:
                time += haversine(F[i], F[i+1])/4
            else:
                time += haversine(F[i], F[i+1])/10

        draw_graph(G, user_image_path)
        return time


''' Given a graph, returns a list with all the indices of the nodes.'''
def index(G):
    list = []
    for node in G.nodes():
        list.append(node.Index)
    return list


''' Returns the route and the number of bikes that a hypothetical vehicle should carry in order to guarantee that
every station of the Bicing company in Barcelona has 'n' bicycles and 'm' empty docks.'''
def distribute(G2, requiredBikes, requiredDocks):
    url_status = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_status'
    bikes = pd.DataFrame.from_records(pd.read_json(
        url_status)['data']['stations'], index='station_id')
    G = nx.DiGraph()
    G.add_node('TOP')  # The green node
    demand = 0
    for st in bikes.itertuples():
        idx = st.Index
        if idx not in index(G2):
            continue
        stridx = str(idx)

        # The blue (s), black (g) and red (t) nodes of the graph
        a_idx, n_idx, r_idx = 's'+stridx, 'g'+stridx, 't'+stridx
        G.add_node(g_idx)
        G.add_node(s_idx)
        G.add_node(t_idx)

        b, d = st.num_bikes_available, st.num_docks_available
        req_bikes = max(0, requiredBikes - b)
        req_docks = max(0, requiredDocks - d)

        G.add_edge('TOP', s_idx)
        G.add_edge(t_idx, 'TOP')
        G.add_edge(s_idx, g_idx)
        G.add_edge(g_idx, t_idx)

        if req_bikes > 0:
            demand += req_bikes
            G.nodes[t_idx]['demand'] = req_bikes
            G.edges[s_idx, g_idx]['capacity'] = 0

        elif req_docks > 0:
            demand -= req_docks
            G.nodes[s_idx]['demand'] = -req_docks
            G.edges[g_idx, t_idx]['capacity'] = 0
    G.nodes['TOP']['demand'] = -(demand)

    for edge in G2.edges():
        coords1 = edge[0]
        coords2 = edge[1]
        id1 = coords1.Index
        id2 = coords2.Index
        w = G2[coords1][coords2]['weight']
        G.add_edge('n'+str(id1), 'n'+str(id2), cost=int(1000*peso), weight=w)
        G.add_edge('n'+str(id2), 'n'+str(id1), cost=int(1000*peso), weight=w)
    err = False

    try:
        flowCost, flowDict = nx.network_simplex(G, weight='cost')

    except nx.NetworkXUnfeasible:
        err = True
        return 1, "No solution could be found", err

    except:
        err = True
        return 2, "Fatal error: Incorrect graph model", err

    if not err:
        first = True
        totalkm = 0
        # We update the status of the stations according to the calculated transportation of bicycles
        for src in flowDict:
            if src[0] != 'g':
                continue
            idx_src = int(src[1:])
            for dst, b in flowDict[src].items():
                if dst[0] == 'g' and b > 0:
                    idx_dst = int(dst[1:])
                    totalkm += G.edges[src, dst]['weight']
                    cost = (G.edges[src, dst]['weight'] * b, idx_src, idx_dst)
                    if first:
                        maxcost = cost
                        first = False
                    elif maxcost[0] < cost[0]:
                        maxcost = cost
        return totalkm*1000, maxcost, err