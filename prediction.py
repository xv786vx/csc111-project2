from entities import load_f1_graph, Driver, Constructor, F1Graph

def simulate_whatif_for_nodes(f1_graph: F1Graph, driver_name: str, constructor_name: str):
    """
    Given a driver name and a constructor name, simulate the what‑if scenario:
      - cmpute whatif_rating as the average of the driver's final elo and the constructor's elo.
      - update the driver's record with the new what‑if rating.
      - add an edge to the graph.
      - recalculate and return the driver's new overall final elo.

    Preconditions:
      - f1_graph must be a valid F1Graph instance with a non-empty database.
      - driver_name must be a non-empty string corresponding to an existing driver in f1_graph.
      - constructor_name must be a non-empty string 
    """

    all_drivers = {}
    for constr in f1_graph.database:
        for drv in constr.all_driver_elo.keys():
            all_drivers[drv.driver_name] = drv
    all_constructors = {constr.constructor_name: constr for constr in f1_graph.database}
    
    driver = all_drivers.get(driver_name)
    constructor = all_constructors.get(constructor_name)

    prev_final_elo = driver.final_elo
    whatif_rating = int((driver.final_elo + constructor.constructor_elo) / 2)
    
    driver.constructor_to_elo[constructor_name] = whatif_rating
    f1_graph.add_edge(driver, constructor)
    
    new_final_elo = driver.calculate_final_elo()
    return prev_final_elo, whatif_rating, new_final_elo

def simulate_whatif(f1_graph: F1Graph) -> None:
    """
    Prompt the user for a driver and a constructor, run the simulation, and print the results.
    Preconditions:
      - f1_graph must be a valid F1Graph instance with drivers and constructors loaded.
      - The user must enter valid, non-empty strings for both driver and constructor that exist in f1_graph.
      
    """
    all_drivers = {}
    for constr in f1_graph.database:
        for drv in constr.all_driver_elo.keys():
            all_drivers[drv.driver_name] = drv
    all_constructors = {constr.constructor_name: constr for constr in f1_graph.database}

    driver_name = input("Enter driver: ").strip()
    constructor_name = input("Enter constructor: ").strip()

    result = simulate_whatif_for_nodes(f1_graph, driver_name, constructor_name)
    if result is None:
        return
    prev_final_elo, whatif_rating, new_final_elo = result

