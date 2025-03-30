import formula_entites

# Elo calculation for driver for one race
def driver_elo_calculation(pole_points: int, qual_points: int, teammate_position: int) -> float:
    """Returun the elo for a driver for one race. Take into consideration the position the driver placed (pole_points),
    the position the driver qualified (qual_points), and how the driver did against thier teammate in a given race
    (teammate_position). Use different weightings to give different considerations varying impacts.
    """
    # Intialize our weighting
    weighiting_for_pole_points = 0.6
    weighiting_for_qual_points = 0.3
    weighting_for_teammate_position = 0.1

    return ((weighiting_for_pole_points * pole_points) + (weighiting_for_qual_points * qual_points) +
            (weighting_for_teammate_position * teammate_position))


# Elo calucations for consturctors (the average for 10 years)
def constructor_elo_calculation(constructor: formula_entites.Constructor, drivers: list[formula_entites.Driver]) -> float:
    """Returun the elo for a constructor for all 10 years of our dataset. Take an average of every driver that has
    raced for the constructor.
    """
    total_elo_so_far = 0
    count = 0

    # Iterate through every driver
    for driver in drivers:
        for driver_construcor, elo in driver.constructor_to_elo.items():  # Get both elo and constructor name from dict
            if driver_construcor.constructor_name == constructor.constructor_name:  # Ensure we are only doing it for the constructor we want
                total_elo_so_far += elo
                count += 1  # account for changes (instead of assuming 20)

    return total_elo_so_far / count


