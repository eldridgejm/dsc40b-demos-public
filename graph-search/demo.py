import pandas as pd
import numpy as np
import folium

from dsc40graph import UndirectedGraph, DirectedGraph


CITY_COORDINATES = pd.read_csv("city_coordinates.csv", delimiter=",")


def load_flight_graph():
    """Create a (random) flight graph between cities."""
    CITY_COORDINATES = pd.read_csv("city_coordinates.csv", delimiter=",")

    # Creating random Edges
    probability_of_edge = 0.07
    random_state = np.random.RandomState(seed=420)
    random_edges = random_state.choice(
        [0, 1],
        size=(len(CITY_COORDINATES), len(CITY_COORDINATES)),
        p=[1 - probability_of_edge, probability_of_edge],
    )
    np.fill_diagonal(random_edges, 0)

    for i in range(0, len(random_edges)):
        for j in range(i + 1, len(random_edges)):
            random_edges[i][j] = random_edges[j][i]

    graph = UndirectedGraph()
    names = CITY_COORDINATES.Name
    for i in names:
        graph.add_node(i)

    for i in range(len(random_edges)):
        origin = names.iloc[i]
        for destination in CITY_COORDINATES.Name[random_edges[i] == 1]:
            graph.add_edge(origin, destination)

    return graph


def plot_flight_map():
    """Plot a graph of flights."""
    CITY_COORDINATES = pd.read_csv("city_coordinates.csv", delimiter=",")
    flight_graph = load_flight_graph()
    flight_map = folium.Map(location=[39.764519, -104.995196], zoom_start=4)
    for node in flight_graph.nodes:
        folium.Marker(
            CITY_COORDINATES[CITY_COORDINATES.Name == node][
                ["Latitude", "Longitude"]
            ].values[0],
            popup=node,
        ).add_to(flight_map)

    for edge in flight_graph.edges:
        val = CITY_COORDINATES[
            (CITY_COORDINATES.Name == edge[0]) | (CITY_COORDINATES.Name == edge[1])
        ][["Latitude", "Longitude"]].values
        folium.PolyLine(val, color="blue", weight=1, opacity=1).add_to(flight_map)

    return flight_map


def plot_route(route):
    """Plot a particular flight route."""
    flight_map = folium.Map(location=[39.764519, -104.995196], zoom_start=4)
    flight_graph = load_flight_graph()
    for node in flight_graph.nodes:
        folium.Marker(
            CITY_COORDINATES[CITY_COORDINATES.Name == node][
                ["Latitude", "Longitude"]
            ].values[0],
            popup=node,
        ).add_to(flight_map)

    for edge in flight_graph.edges:
        val = CITY_COORDINATES[
            (CITY_COORDINATES.Name == edge[0]) | (CITY_COORDINATES.Name == edge[1])
        ][["Latitude", "Longitude"]].values
        folium.PolyLine(val, color="blue", weight=1, opacity=1).add_to(flight_map)

    if len(route) > 1:
        for i in range(len(route) - 1):
            key = route[i]
            destination = route[i + 1]
            val = CITY_COORDINATES[
                (CITY_COORDINATES.Name == key) | (CITY_COORDINATES.Name == destination)
            ][["Latitude", "Longitude"]].values
            folium.PolyLine(val, color="red", weight=5, opacity=1).add_to(flight_map)

    return flight_map
