"""CSC111 Winter 2025: Computational Proof of F1 Driver Performance Under Distinct Constructors (What-If Prediction)

Module Description
==================

This module contains Python functions that contain formulas to predict simulations that tell us
perfromance elo.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of teachers and TAs
in CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2025 Pranay Chopra, Sambhav Athreya, Sumedh Gadepalli, and Firas Adnan Jalil.
"""

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
