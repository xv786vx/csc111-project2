import csv
import math

class Driver:
    """
    A driver in our graph. Holding information about the various drivers in F1 from 2010-2020

   Instance Attributes:
       - driver_name (str): the name for the driver given by the dataset
       - constructor_to_elo (dict): a dictionary that maps the constructor that the racer drover for a particular season to the elo (calculated by our formula)

   Representation Invariants:
       - name != ''
       - all(x==Constructor for x in constructor_to_elo) -- NOTE: the key have to be a constructor name
   """

    driver_name: str
    constructor_to_elo: dict[str, float] # the keys are the names of the constructors raced for, and the values are their corresponding ELOs

    def __init__(self, driver_name: str) -> None:
        """Initialize a new Driver with the given name.

        Preconditions:
            - driver_name is a non-empty string
        """
        self.driver_name = driver_name
        self.constructor_to_elo = {}

    def calculate_driver_elo(self, f1_graph: "F1Graph", pole_points: float|int, qual_points: float|int, teammate_position: float|int, name: str) -> None:
        """Return the elo for a driver for one race. Take into consideration the position the driver placed (pole_points),
          the position the driver qualified (qual_points), and how the driver did against thier teammate in a given race
          (teammate_position). Use different weightings to give different considerations varying impacts.

          Preconditions:
           - f1_graph is an instance of F1Graph
            - pole_points, qual_points, teammate_position are numeric values (int or float)
            - name is a valid string representing the constructor's name
          """
        constructor = None
        for constr in f1_graph.database:
            if constr.constructor_name == name:
                constructor = constr
                break

        if constructor is None:
            constructor = Constructor(name)
            f1_graph.add_constructor(constructor)

        # Intialize our weighting
        weighiting_for_pole_points = 0.6
        weighiting_for_qual_points = 0.3
        weighting_for_teammate_position = 0.1

        elo_rating = math.ceil(((weighiting_for_pole_points * pole_points) + (weighiting_for_qual_points * qual_points) +
                (weighting_for_teammate_position * teammate_position)))

        if name in self.constructor_to_elo:
            self.constructor_to_elo[name] += elo_rating

        else:
            self.constructor_to_elo[name] = elo_rating

        constructor.all_driver_elo[self] = self.constructor_to_elo[name]

        constructor.calculate_elo()


class Constructor:
    """A constructor in our graph. Holding information about the various teams in F1 from 2010-2020

   Instance Attributes:
       - constructor_name (str): the name for the constructor given by the dataset
       - constructor_elo (int): the average of all the racers that have driven for a constructor in the last 10 years
      -  all_driver_elo (dict): a dictionary of drivers and their respective ELOs for a constructor

   Representation Invariants:
       - name != ''
       - constructor_elo >= 0.0
   """
    constructor_name: str
    all_driver_elo: dict[Driver: float]
    constructor_elo: float


    def __init__(self, constructor_name):
        """
         Initialize a new Constructor with the given name.

        Preconditions:
            - constructor_name is a non-empty string

        """
        self.constructor_name = constructor_name
        self.all_driver_elo = {}
        self.constructor_elo = 0

    def calculate_elo(self) -> float:
        """
        Calculate the constructor's average ELO based on the ELOs of all drivers who have raced for them.

        Returns the average ELO for the constructor, rounded up to the nearest integer.

        Preconditions:
            - all_driver_elo is a non-empty dictionary
        """
        total_elo_so_far = 0
        count = 0
        for driver, elo in self.all_driver_elo.items():
            total_elo_so_far += elo
            count += 1

        if count == 0:
            return 0.0

        self.constructor_elo = math.ceil(total_elo_so_far / count)

        return self.constructor_elo

class F1Graph:
    """
    A graph representing F1 drivers and constructors and their ELO ratings.

    Instance Attributes:
        - database (set): a set of all constructors in the graph

    Representation Invariants:
        - database is a set of Constructor objects
    """
    database: set[Constructor]

    def __init__(self):

        self.database = set()

    def add_constructor(self, constructor: Constructor) -> None:
        '''
        Add a constructor to the database of an F1Graph instance.

        Preconditions:
        - constructor is an instance of the Constructor class
        '''
        self.database.add(constructor)

def load_f1_graph(file_path: str) -> F1Graph:
    """
     Load the F1 data from the given CSV file and create the F1Graph, and returns an F1 Graph object containing the data
     from the CSV file.

     Preconditions:
     - file_path is a valid string pointing to a CSV file
     - file_path is structured in the following format: raceId,year,driverId,constructorId,finish_points,grid,position,
     racer_name,constructor_name,qual_points,teammate_points
    """

    f1_graph = F1Graph()

    with open(file_path) as file:
        reader = csv.DictReader(file)

        for row in reader:
            race_id = int(row['raceId'])
            year = int(row['year'])
            driver_id = int(row['driverId'])
            constructor_id = int(row['constructorId'])
            finish_points = float(row['finish_points'])
            grid_position = int(row['grid'])

            position_str = row['position']
            if position_str:
                position = float(position_str)
            else:
                position = 0.0

            racer_name = row['racer_name']
            constructor_name = row['constructor_name']
            qual_points = int(row['qual_points'])

            teammate_points_str = row['teammate_points']
            if teammate_points_str:
                teammate_points = float(teammate_points_str)
            else:
                teammate_points = 0.0

            constructor = None
            for constr in f1_graph.database:
                if constr.constructor_name == constructor_name:
                    constructor = constr
                    break

            if constructor is None:
                constructor = Constructor(constructor_name)
                f1_graph.add_constructor(constructor)

            driver = None
            for drv in constructor.all_driver_elo.keys():
                if drv.driver_name == racer_name:
                    driver = drv
                    break

            if driver is None:
                driver = Driver(racer_name)
                constructor.all_driver_elo[driver] = 0.0

            driver.calculate_driver_elo(f1_graph,
                    pole_points=finish_points,
                    qual_points=qual_points,
                    teammate_position=teammate_points,
                    name=constructor_name
            )

            constructor.all_driver_elo[driver] = driver.constructor_to_elo[constructor_name]

            constructor.calculate_elo()

    return f1_graph


if __name__ == "__main__":
    file_path = r"C:\Users\sumed\Downloads\csc111-project2\preprocessing\final_data.csv"
    f1_graph = load_f1_graph(file_path)

    # Example of accessing and printing data from the f1_graph
    for constructor in f1_graph.database:
        print(f"Constructor: {constructor.constructor_name}, ELO: {constructor.constructor_elo}")
        for driver, elo in constructor.all_driver_elo.items():
            print(f"Driver: {driver.driver_name}, ELO: {elo}")
