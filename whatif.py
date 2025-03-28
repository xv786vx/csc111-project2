from typing import Dict, Set
import networkx as nx
import matplotlib.pyplot as plt

class F1BipartiteGraph:
    drivers: Dict[str, int]
    constructors: Dict[str, int]
    driver_to_constructors: Dict[str, Set[str]]

    def __init__(self) -> None:
        self.drivers = {
            'Lewis Hamilton': 1800,
            'Max Verstappen': 1780,
            'Fernando Alonso': 1750,
            'Sebastian Vettel': 1720,
            'Charles Leclerc': 1700,
            'George Russell': 1680,
            'Lando Norris': 1660,
            'Carlos Sainz': 1640,
            'Daniel Ricciardo': 1620,
            'Sergio Perez': 1600
        }

        self.constructors = {
            'Mercedes': 1800,
            'Red Bull': 1780,
            'Ferrari': 1750,
            'McLaren': 1700,
            'Alpine': 1650,
            'Aston Martin': 1630,
            'AlphaTauri': 1600,
            'Alfa Romeo': 1550,
            'Williams': 1500,
            'Haas': 1500
        }

        self.driver_to_constructors = {
            'Lewis Hamilton': {'McLaren', 'Mercedes'},
            'Max Verstappen': {'Red Bull'},
            'Fernando Alonso': {'Renault', 'Ferrari', 'McLaren', 'Alpine', 'Aston Martin'},
            'Sebastian Vettel': {'BMW Sauber', 'Toro Rosso', 'Red Bull', 'Ferrari', 'Aston Martin'},
            'Charles Leclerc': {'Sauber', 'Ferrari'},
            'George Russell': {'Williams', 'Mercedes'},
            'Lando Norris': {'McLaren'},
            'Carlos Sainz': {'Toro Rosso', 'Renault', 'McLaren', 'Ferrari'},
            'Daniel Ricciardo': {'HRT', 'Toro Rosso', 'Red Bull', 'Renault', 'McLaren'},
            'Sergio Perez': {'Sauber', 'McLaren', 'Force India', 'Racing Point', 'Red Bull'}
        }

        self.graph = self.create_graph()

    def get_whatif_rating(self, driver: str, constructor: str) -> float:
        driver_elo = self.drivers[driver]
        constructor_elo = self.constructors[constructor]
        return (driver_elo + constructor_elo) / 2

    def create_graph(self) -> nx.Graph:
        graph = nx.Graph()

        for driver, driver_elo in self.drivers.items():
            graph.add_node(driver, bipartite='driver', elo=driver_elo)

        for constructor, constructor_elo in self.constructors.items():
            graph.add_node(constructor, bipartite='constructor', elo=constructor_elo)

        for driver, constructors in self.driver_to_constructors.items():
            for constructor in constructors:
                if constructor in self.constructors:
                    graph.add_edge(driver, constructor)

        return graph

    def add_connection_and_adjust_elo(self, driver: str, constructor: str) -> None:
        self.driver_to_constructors[driver].add(constructor)
        
        old_driver_elo = self.drivers[driver]
        constructor_elo = self.constructors[constructor]
        new_driver_elo = (old_driver_elo + constructor_elo) / 2
        self.drivers[driver] = int(new_driver_elo)  

        print(f"updated from {old_driver_elo} to {self.drivers[driver]}.")

if __name__ == '__main__':
    f1_graph = F1BipartiteGraph()

    driver_name = input("Select a driver: ").strip()
    constructor_name = input("Select a constructor: ").strip()
    f1_graph.add_connection_and_adjust_elo(driver_name, constructor_name)

