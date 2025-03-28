class Constructor:
    """A constructor in our graph. Holding information about the various teams in F1 from 2010-2020

   Instance Attributes:
       - constructor_name (str): the name for the constructor given by the dataset
       - constructor_elo (int): the average of all the racers that have driven for a constructor in the last 10 years

   Representation Invariants:
       - name != ''
       - constructor_elo >= 0.0
   """
    constructor_name: str
    constructor_elo: float

    def __init__(self, constructor_name):
        self.constructor_name = constructor_name
        self.constructor_elo = 0


class Driver:
    """
    A driver in our graph. Holding information about the various drivers in F1 from 2010-2020

   Instance Attributes:
       - driver_name (str): the name for the driver given by the dataset
       - constructor_to_elo (dict): a dictionary that maps the constructor that the racer drover for a particular season to the elo (caluclated by our formula)

   Representation Invariants:
       - name != ''
       - all(x==Constructor for x in constructor_to_elo) -- NOTE: the key have to be a constructor class (is this the right implemenation)
   """

    driver_name: str
    constructor_to_elo: dict[Constructor: float]

    def __init__(self, driver_name: str) -> None:
        """Initialize a new Driver with the given .

        This vertex is initialized with no elo, as it is then calculated from the formula in (add file name).

        Preconditions:
            -
        """
        self.driver_name = driver_name
        self.constructor_to_elo = {}


class Race:
    race_name: str
    constructor: str
