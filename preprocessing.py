"""CSC111 Winter 2025: Computational Proof of F1 Driver Performance Under Distinct Constructors (Data Processing)

Module Description
==================

This module contains code that processes our dataset into useable content.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of teachers and TAs
in CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2025 Pranay Chopra, Sambhav Athreya, Sumedh Gadepalli, and Firas Adnan Jalil.
"""
import pandas as pd

races = pd.read_csv('races.csv')
results = pd.read_csv('results.csv')
qual_pos = pd.read_csv('qualifying.csv')
constructors = pd.read_csv('constructors.csv')
drivers = pd.read_csv('drivers.csv')
laptimes = pd.read_csv('lap_times.csv')

qual_points_map = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1
}

filtered_races = races[(races['year'] >= 2010) & (races['year'] <= 2020)]

filtered_data = pd.merge(
    filtered_races[['raceId', 'year']],
    results[['raceId', 'driverId', 'constructorId', 'points', 'grid', 'position']],
    on='raceId',
    how='inner'
)

include_racer_names = pd.merge(
    filtered_data,
    drivers[['driverId', 'forename', 'surname']],
    on='driverId',
    how='left'
)

include_racer_names['racer_name'] = include_racer_names['forename'] + ' ' + include_racer_names['surname']
include_racer_names.drop(['forename', 'surname'], axis=1, inplace=True)

# include_lap_times = pd.merge(
#     include_racer_names,
#     laptimes[['raceId', 'driverId', 'lap', 'time']],
#     on=['raceId', 'driverId'],
#     how='left'
# )

include_constructors = pd.merge(
    include_racer_names,
    constructors[['constructorId', 'name']],
    on='constructorId',
    how='left'
)
include_constructors.rename(columns={'name': 'constructor_name'}, inplace=True)

final_df = include_constructors.sort_values(by=['year', 'raceId']).reset_index(drop=True).rename(columns={
    'points': 'finish_points',
})

final_df['qual_points'] = final_df['grid'].map(qual_points_map).fillna(0).astype(int)

# NEW: Teammate comparison logic starts here

# Clean position data (convert to numeric, handle DNFs)
final_df['position'] = pd.to_numeric(final_df['position'], errors='coerce')

# Filter groups with exactly 2 drivers per constructor-race
group_sizes = final_df.groupby(['raceId', 'constructorId']).size()
valid_groups = group_sizes[group_sizes == 2].index
df_filtered = final_df[final_df.set_index(['raceId', 'constructorId']).index.isin(valid_groups)]

# Self-merge to pair teammates
merged = pd.merge(
    df_filtered,
    df_filtered,
    on=['raceId', 'constructorId'],
    suffixes=('_A', '_B')
)
merged = merged[merged['driverId_A'] < merged['driverId_B']]  # Remove duplicate pairs

# Assign points based on position comparison
merged['teammate_points_A'] = (
        (merged['position_A'] < merged['position_B']).astype(int)
        + (merged['position_A'] == merged['position_B']).astype(int) * 0.5
)
merged['teammate_points_B'] = 1 - merged['teammate_points_A']

# Reshape to long format
points_a = merged[['raceId', 'constructorId', 'driverId_A', 'teammate_points_A']].rename(
    columns={'driverId_A': 'driverId', 'teammate_points_A': 'teammate_points'}
)
points_b = merged[['raceId', 'constructorId', 'driverId_B', 'teammate_points_B']].rename(
    columns={'driverId_B': 'driverId', 'teammate_points_B': 'teammate_points'}
)
points = pd.concat([points_a, points_b], ignore_index=True)

# Merge points back into final DataFrame
final_df = pd.merge(
    final_df,
    points,
    on=['raceId', 'constructorId', 'driverId'],
    how='left'
)

# Teammate comparison logic ends here


# print(final_df)
final_df.to_csv('final_data.csv', index=False)
