import csv
import math


class Driver:
    """
    A driver in our graph. Holds information about various F1 drivers (2010-2020).

    Instance Attributes:
        - driver_name (str): the driver's name
        - constructor_to_elo (dict): maps constructor names to the ELO calculated for that race/season
        - final_elo (float): the driver's overall ELO, computed as the average of the ELOs across all constructors they've raced for

    Representation Invariants:
        - driver_name != ''
        - all keys in constructor_to_elo are valid constructor names
    """
    driver_name: str
    constructor_to_elo: dict[str, float]
    final_elo: float

    def __init__(self, driver_name: str) -> None:
        """Initialize a new Driver with the given name."""
        self.driver_name = driver_name
        self.constructor_to_elo = {}
        self.final_elo = 0.0

    def calculate_driver_elo(self, f1_graph: "F1Graph", pole_points: float | int, qual_points: float | int,
                             teammate_position: float | int, name: str) -> None:
        """
        Calculate and update the driver's ELO for a given race for a specific constructor.
        The ELO for the race is computed as a weighted sum of pole_points, qual_points, and teammate_position.

        Preconditions:
         - f1_graph is an instance of F1Graph
         - pole_points, qual_points, teammate_position are numeric (int or float)
         - name is a valid constructor name
        """
        constructor = None
        for constr in f1_graph.database:
            if constr.constructor_name == name:
                constructor = constr
                break

        if constructor is None:
            constructor = Constructor(name)
            f1_graph.add_constructor(constructor)

        # Weighting factors
        weighting_for_pole_points = 0.6
        weighting_for_qual_points = 0.3
        weighting_for_teammate_position = 0.1

        elo_rating = math.ceil((weighting_for_pole_points * pole_points) +
                               (weighting_for_qual_points * qual_points) +
                               (weighting_for_teammate_position * teammate_position))

        if name in self.constructor_to_elo:
            self.constructor_to_elo[name] += elo_rating
        else:
            self.constructor_to_elo[name] = elo_rating

        constructor.all_driver_elo[self] = self.constructor_to_elo[name]
        constructor.calculate_elo()

    def calculate_final_elo(self) -> float:
        """
        Compute the driver's overall final ELO as the average of the ELOs from all constructors.
        The result is rounded up to the nearest integer.
        """
        if len(self.constructor_to_elo) == 0:
            self.final_elo = 0.0
        else:
            avg = sum(self.constructor_to_elo.values()) / len(self.constructor_to_elo)
            self.final_elo = math.ceil(avg)
        return self.final_elo

    def __hash__(self):
        """ Hash based on driver's name."""
        return hash(self.driver_name)

    def __eq__(self, other) -> bool:
        """ Check if this Driver is equal to another object."""
        return isinstance(other, Driver) and self.driver_name == other.driver_name


class Constructor:
    """
    A constructor in our graph. Holds information about various F1 teams (2010-2020).

    Instance Attributes:
        - constructor_name (str): the constructor's name
        - all_driver_elo (dict): maps Driver objects to their ELO values for this constructor
        - constructor_elo (float): the overall ELO of the constructor (average of driver ELOs)

    Representation Invariants:
        - constructor_name != ''
        - constructor_elo >= 0.0
    """
    constructor_name: str
    all_driver_elo: dict[Driver, float]
    constructor_elo: float

    def __init__(self, constructor_name: str) -> None:
        """Initialize a new Constructor with the given name."""
        self.constructor_name = constructor_name
        self.all_driver_elo = {}
        self.constructor_elo = 0.0

    def calculate_elo(self) -> float:
        """
        Calculate the constructor's overall ELO as the average of all driver ELOs.
        Returns the average, rounded up to the nearest integer.
        """
        total_elo = sum(self.all_driver_elo.values())
        count = len(self.all_driver_elo)
        if count == 0:
            self.constructor_elo = 0.0
        else:
            self.constructor_elo = math.ceil(total_elo / count)
        return self.constructor_elo

    def __hash__(self):
        """ Hash based on constructor's name."""
        return hash(self.constructor_name)

    def __eq__(self, other) -> bool:
        """ Check if this Constructor is equal to another object."""
        return isinstance(other, Constructor) and self.constructor_name == other.constructor_name


class F1Graph:
    """
    A graph representing F1 drivers and constructors and their ELO ratings.

    Instance Attributes:
        - database (set): a set of all Constructor objects in the graph.
        - drivers (dict): a mapping from driver names to Driver objects.
        - edges (set): a set of tuples (Driver, Constructor) representing connections.
    """
    database: set[Constructor]
    drivers: dict[str, Driver]
    edges: set[tuple[Driver, Constructor]]

    def __init__(self) -> None:
        self.database = set()
        self.drivers = {}
        self.edges = set()

    def add_constructor(self, constructor: Constructor) -> None:
        """Add a constructor to the graph's database."""
        self.database.add(constructor)

    def add_driver(self, driver: Driver) -> None:
        """Add a driver to the graph's driver mapping."""
        self.drivers[driver.driver_name] = driver

    def add_edge(self, driver: Driver, constructor: Constructor) -> None:
        """Add an edge representing that the driver raced for the constructor."""
        self.edges.add((driver, constructor))


def load_f1_graph(file_path: str) -> F1Graph:
    """
    Load the F1 data from the given CSV file, update driver and constructor ELOs,
    and return an F1Graph object containing the data.

    The CSV file is expected to have columns:
    raceId, year, driverId, constructorId, finish_points, grid, position,
    racer_name, constructor_name, qual_points, teammate_points
    """
    f1_graph = F1Graph()

    with open(file_path) as file:
        reader = csv.DictReader(file)

        for row in reader:
            finish_points = float(row['finish_points'])
            racer_name = row['racer_name']
            constructor_name = row['constructor_name']
            qual_points = int(row['qual_points'])
            teammate_points_str = row['teammate_points']
            teammate_points = float(teammate_points_str) if teammate_points_str else 0.0

            constructor = None
            for constr in f1_graph.database:
                if constr.constructor_name == constructor_name:
                    constructor = constr
                    break
            if constructor is None:
                constructor = Constructor(constructor_name)
                f1_graph.add_constructor(constructor)

            driver = None
            if racer_name in f1_graph.drivers:
                driver = f1_graph.drivers[racer_name]
            else:
                for drv in constructor.all_driver_elo.keys():
                    if drv.driver_name == racer_name:
                        driver = drv
                        break
            if driver is None:
                driver = Driver(racer_name)
                f1_graph.add_driver(driver)
                constructor.all_driver_elo[driver] = 0.0

            driver.calculate_driver_elo(f1_graph,
                                        pole_points=finish_points,
                                        qual_points=qual_points,
                                        teammate_position=teammate_points,
                                        name=constructor_name)
            constructor.all_driver_elo[driver] = driver.constructor_to_elo[constructor_name]
            constructor.calculate_elo()
            f1_graph.add_edge(driver, constructor)

    for driver in f1_graph.drivers.values():
        driver.calculate_final_elo()

    return f1_graph
