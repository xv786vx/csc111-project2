# Formula 1 ELO Rating Simulator

An interactive web application that analyzes Formula 1 driver and constructor performance using ELO rating systems and enables "what-if" scenario simulations to explore how driver ratings would change if they raced for different teams.

## Authors

Developed by: Firas Adnan Jalil, Sambhav Athreya, Pranay Chopra and Sumedh Gadepalli

## Overview

This project examines the intricate relationship between Formula 1 drivers and constructors by implementing an ELO rating system and providing an interactive visualization tool. The application allows users to:

- Visualize the bipartite relationship between drivers and constructors (2010-2020)
- Add hypothetical edges to simulate driver-constructor pairings that never occurred
- Analyze how these alternative pairings would affect driver ELO ratings
- Explore the balance between individual driver skill and team performance

## Features

- **Interactive Network Visualization**: Bipartite graph showing drivers (blue nodes) and constructors (green nodes) with draggable nodes for custom positioning
- **What-If Simulation**: Add hypothetical edges between drivers and constructors to see projected ELO changes
- **Real-Time Analysis**: Dynamic table showing previous ELO, hypothetical ELO, and new final ELO ratings
- **Edge Management**: Add and remove hypothetical connections with visual feedback (dashed orange lines for hypothetical edges)
- **Responsive Interface**: Built with Dash and Cytoscape for smooth user interaction and organic "spider web" layout
- **Interactive Layout**: Drag nodes to reposition them; layout freezes after initial computation to maintain consistency

## ELO Calculation Methodology

### Driver ELO Calculation
Driver ELO ratings are calculated using a weighted formula incorporating:
- **Race finishing positions** (60% weight)
- **Qualifying positions** (30% weight) 
- **Head-to-head teammate performance** (10% weight)

```
Driver ELO = Σ(Weighted Score_i) / n
```
where n is the number of races in the season.

### Constructor ELO Calculation
Constructor ELO ratings are computed as the average of all drivers who raced for the team:

```
Constructor ELO = Σ(Driver ELO_j) / m
```
where m is the number of drivers who raced for the constructor.

### Hypothetical ELO Simulation
When simulating alternative pairings, the hypothetical ELO is calculated as:

```
E_hypo = (E_driver + E_constructor) / 2
```

## Project Structure

```
F1-ELO-Simulator/
├── preprocessing/
│   └── data/
│       ├── constructors.csv
│       ├── drivers.csv
│       ├── lap_times.csv
│       ├── qualifying.csv
│       ├── races.csv
│       ├── results.csv
│       └── final_data.csv
├── entities.py          # Core data structures (Driver, Constructor, F1Graph)
├── prediction.py        # What-if simulation logic
├── app.py              # Dash web application
├── requirements.txt    # Python dependencies
└── README.md
```

## Installation

### Prerequisites
- Python 3.13 or higher
- Required Python packages (see requirements.txt)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/f1-elo-simulator.git
   cd f1-elo-simulator
   ```

2. **Download and extract the dataset**
   - Download the `preprocessing.zip` file and extract it into the main project directory
   - Ensure the dataset files are properly located in `preprocessing/data/`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install the required libraries individually:
   ```bash
   pip install dash dash-cytoscape dash-table
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   - The Dash server will start and display a message like: `Running on http://127.0.0.1:8050`
   - Control+Click the link or type it directly into your web browser

## Usage Guide

### Basic Navigation
1. **View the Graph**: The application displays an interactive bipartite graph with:
   - Blue nodes representing drivers
   - Green nodes representing constructors
   - Gray edges showing historical driver-constructor relationships
   - **Draggable nodes**: Click and drag any node to reposition it for better visualization

2. **Add Hypothetical Edges**:
   - Click on a driver node (blue)
   - Click on a constructor node (green) that is not already connected to the selected driver
   - Press the "Add Hypothetical Edge" button
   - A dashed orange edge will appear representing the hypothetical pairing
   - The graph layout remains stable after initial positioning to prevent disruption

3. **View Simulation Results**:
   - The table on the right automatically updates with detailed simulation results:
     - **Previous ELO**: The driver's original overall ELO rating
     - **What-If ELO**: The computed hypothetical ELO for the new driver-constructor pairing  
     - **New Final ELO**: The driver's updated overall ELO after incorporating the hypothetical pairing
   - Results show how the alternative pairing would affect the driver's performance rating

4. **Remove Hypothetical Edges**:
   - **Option 1**: Click directly on any dashed orange edge in the graph, then press "Remove Hypothetical Edge"
   - **Option 2**: Select rows in the results table and press the red "Remove Hypothetical Edge" button
   - The edge and corresponding table data will be removed immediately

### Data Requirements
The application expects CSV data with the following columns:
- `finish_points`: Points earned from final race position
- `qual_points`: Points earned from qualifying position  
- `teammate_points`: Head-to-head performance against teammates
- `racer_name`: Driver name
- `constructor_name`: Constructor/team name

## Technical Implementation

### Core Classes

- **Driver**: Manages individual driver ELO ratings across different constructors
- **Constructor**: Manages team ELO ratings based on driver performance
- **F1Graph**: Bipartite graph structure connecting drivers and constructors

### Key Functions

- `load_f1_graph()`: Loads CSV data and builds the F1Graph structure
- `simulate_whatif_for_nodes()`: Performs what-if scenario calculations
- `calculate_driver_elo()`: Computes weighted ELO ratings for drivers
- `calculate_final_elo()`: Calculates overall driver ELO across all constructors

### Visualization Technology

- **Dash**: Web application framework
- **Cytoscape**: Interactive network visualization
- **Plotly**: Data visualization components

## Dataset

This project uses historical Formula 1 data from 2010-2020, originally sourced from:
[Kaggle Formula 1 World Championship Dataset (1950-2020)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)

The dataset includes:
- Race results and points
- Qualifying positions
- Constructor information
- Driver details
- Lap times

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Research Applications

This tool can be used to explore questions such as:
- How much of a driver's success is attributable to their skill versus their team?
- What would happen if top drivers switched teams?
- Which constructors maximize or minimize driver potential?
- How do driver-constructor combinations affect overall performance?

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Formula 1 for providing the inspiration and data structure
- Kaggle community for the comprehensive F1 dataset
- Dash and Plotly communities for excellent visualization tools
