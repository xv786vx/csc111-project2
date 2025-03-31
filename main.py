"""CSC111 Winter 2025: Computational Proof of F1 Driver Performance Under Distinct Constructors (Graphs Visualization)

Module Description
==================

This module contains Python functions that you can use to visualize our graph.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of teachers and TAs
in CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2025 Pranay Chopra, Sambhav Athreya, Sumedh Gadepalli, and Firas Adnan Jalil.
"""

import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_cytoscape as cyto

cyto.load_extra_layouts()
from prediction import simulate_whatif_for_nodes
from entities import load_f1_graph, Driver, Constructor, F1Graph

FILE_PATH = r"preprocessing/final_data.csv"
global_f1_graph = load_f1_graph(FILE_PATH)

elements = []

for driver in global_f1_graph.drivers.values():
    elements.append({
        "data": {
            "id": f"driver-{driver.driver_name}",
            "label": driver.driver_name,
            "group": "driver"
        },
        "classes": "driver-node"
    })

for constructor in global_f1_graph.database:
    elements.append({
        "data": {
            "id": f"constructor-{constructor.constructor_name}",
            "label": constructor.constructor_name,
            "group": "constructor"
        },
        "classes": "constructor-node"
    })

for edge in global_f1_graph.edges:
    driver, constructor = edge
    elements.append({
        "data": {
            "id": f"edge-{driver.driver_name}-{constructor.constructor_name}",
            "source": f"driver-{driver.driver_name}",
            "target": f"constructor-{constructor.constructor_name}"
        },
        "classes": "real-edge"
    })

app = dash.Dash(__name__)
server = app.server

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        <title>Formula 1 Driver ELO Simulator</title>
        <link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400;700&display=swap" rel="stylesheet">
        {%metas%}
        {%css%}
        {%title%}
        {%scripts%}
        <style>
            html, body {
                margin: 0; 
                padding: 0; 
                background-color: #1B1F23; 
                height: 100%; 
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

layout_store = dcc.Store(id="layout-store", data={"name": "fcose"})

app.layout = html.Div(
    style={
        "width": "100vw",
        "height": "100vh",
        "postiion": "relative",
        "display": "flex",
        "flexDirection": "row",
        "fontFamily": "'Red Hat Display', sans-serif",
        "backgroundColor": "#1B1F23",
        "color": "white",
        "margin": "0",
        "padding": "0"
    },
    children=[
        html.Img(
            src="https://www.formula1.com/etc/designs/fom-website/images/f1_logo.svg",
            style={"position": "absolute",
                   "top": "20px",
                   "left": "20px",
                   "width": "100px",
                   "zIndex": "1000"}
        ),
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            layout={
                "name": "fcose",
                "randomize": True,
                "idealEdgeLength": 150,
                "nodeRepulsion": 12000,
                "nodeSeparation": 200,
                "gravity": 0.1,
                "packComponents": True,
                "animate": True
            },
            style={"width": "70vw", "height": "100vh"},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "grabbable": "true",
                        "label": "data(label)",
                        "font-size": "20px",
                        "text-halign": "center",
                        "text-valign": "center",
                        "background-color": "#3C3F44",
                        "color": "#FFFFFF",
                        "width": "80px",
                        "height": "80px",
                        "border-width": "0px"
                    }
                },
                {"selector": ".driver-node", "style": {"background-color": "#2978F0"}},
                {"selector": ".constructor-node", "style": {"background-color": "#22A55F"}},
                {"selector": ".real-edge", "style": {"line-color": "#888888", "width": 2}},
                {"selector": ".hypothetical-edge",
                 "style": {"line-color": "#FFAA00", "line-style": "dashed", "width": 3}},
                {"selector": ".hypothetical-edge:selected",
                 "style": {"line-color": "#FF5500", "width": 5}}
            ],
            boxSelectionEnabled=False,
            autounselectify=False,
            minZoom=0.2,
            maxZoom=3,
            userPanningEnabled=True,
            userZoomingEnabled=True,
            autoungrabify=False
        ),
        dcc.Store(id="node-store", data=[]),
        layout_store,

        dcc.Store(id="edge-store", data=None),

        dcc.Interval(id="freeze-layout-interval", interval=5000, n_intervals=0, max_intervals=1),
        html.Div(
            style={
                "width": "30vw",
                "height": "100vh",
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "flex-start",
                "padding": "20px",
                "backgroundColor": "#1B1F23"
            },
            children=[
                html.H2("Formula 1 Driver ELO Simulator", style={"textAlign": "center", "marginTop": "0"}),
                html.P(
                    "Tap one driver node, then tap one constructor node, then press the button below to add a hypothetical edge.",
                    style={"textAlign": "center", "marginBottom": "10px"}
                ),
                html.Button(
                    "Add Hypothetical Edge",
                    id="add-edge-btn",
                    n_clicks=0,
                    style={
                        "fontSize": "18px",
                        "padding": "10px",
                        "backgroundColor": "#333",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "marginBottom": "20px"
                    }
                ),
                html.Button(
                    "Remove Hypothetical Edge",
                    id="remove-edge-btn",
                    n_clicks=0,
                    style={
                        "fontSize": "18px",
                        "padding": "10px",
                        "backgroundColor": "#AA3333",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "marginBottom": "20px"
                    }
                ),
                html.Div(
                    id="simulation-output",
                    style={"textAlign": "center", "marginBottom": "20px", "fontSize": "16px"}
                ),
                dash_table.DataTable(
                    id="simulation-table",
                    columns=[
                        {"name": "Driver", "id": "Driver"},
                        {"name": "Constructor", "id": "Constructor"},
                        {"name": "Prev. ELO", "id": "PrevELO"},
                        {"name": "What-If ELO", "id": "HypoELO"},
                        {"name": "New Final ELO", "id": "NewFinalELO"}
                    ],
                    data=[],
                    row_selectable='single',
                    style_table={"overflowX": "auto"},
                    style_header={
                        "backgroundColor": "#111111",
                        "color": "white",
                        "fontWeight": "bold"
                    },
                    style_data={"backgroundColor": "#1B1F23", "color": "white"},
                    style_cell={
                        "textAlign": "center",
                        "fontSize": "16px",
                        "fontFamily": "'Red Hat Display', sans-serif"
                    }
                )
            ]
        )
    ]
)


@app.callback(
    Output("node-store", "data"),
    Input("cytoscape", "tapNodeData"),
    Input("simulation-output", "children"),
    State("node-store", "data")
)
def update_or_clear_node_store(tapNodeData, simulation_output, storeData):
    """
    Update the node store when a node is tapped.
    If simulation_output contains an error about node selection, clear the node store.

    Preconditions:
      - tapNodeData is a dict representing the tapped node's data, or None.
      - simulation_output is a string.
      - storeData is a list of dicts representing currently stored nodes, or None.
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        return storeData

    # Determine which input triggered the callback
    trigger_prop = ctx.triggered[0]['prop_id']

    # If the simulation output triggered the callback and contains the error message, clear the store.
    if "simulation-output" in trigger_prop:
        if simulation_output and "Please tap exactly 2 nodes" in simulation_output:
            return []
        return storeData

    # Otherwise, update the node store based on the tapNodeData.
    if tapNodeData is None:
        return storeData
    if storeData is None:
        storeData = []
    if any(node.get("id") == tapNodeData.get("id") for node in storeData):
        storeData = [node for node in storeData if node.get("id") != tapNodeData.get("id")]
        return storeData
    if len(storeData) >= 2:
        storeData = [tapNodeData]
    else:
        storeData.append(tapNodeData)
    return storeData


@app.callback(
    Output("layout-store", "data"),
    Input("freeze-layout-interval", "n_intervals")
)
def freeze_layout(n_intervals):
    """
    Freeze the layout once the interval fires.

    Preconditions:
      - n_intervals is an integer; expected to be >= 1 when the interval fires.

    """
    if n_intervals and n_intervals >= 1:
        return {"name": "preset"}
    return dash.no_update


@app.callback(
    Output("cytoscape", "layout"),
    Input("layout-store", "data")
)
def update_cytoscape_layout(layout_data):
    """
    Update the Cytoscape layout property based on the layout-store.

    Preconditions:
      - layout_data is a dict representing the layout configuration (e.g. {"name": "preset"}).
    """
    if layout_data:
        return layout_data
    return dash.no_update


@app.callback(
    Output("edge-store", "data"),
    Input("cytoscape", "tapEdgeData"),
)
def update_edge_store(tapped_edge):
    """Track which edge was last tapped in the cytoscape graph"""
    # Only store hypothetical edges
    if tapped_edge and tapped_edge.get('id', '').startswith('hypothetical-'):
        return tapped_edge
    return None


@app.callback(
    [
        Output("cytoscape", "elements"),
        Output("simulation-table", "data"),
        Output("simulation-output", "children")
    ],
    [
        Input("add-edge-btn", "n_clicks"),
        Input("remove-edge-btn", "n_clicks")
    ],
    [
        State("node-store", "data"),
        State("cytoscape", "elements"),
        State("simulation-table", "data"),
        State("simulation-table", "selected_rows"),
        State("edge-store", "data")  # New state parameter
    ]
)
def manage_edges(add_n_clicks, remove_n_clicks, node_store, current_elements, table_data, selected_rows, edge_store):
    """
    Manage both adding and removing hypothetical edges when the respective buttons are clicked.
    Now supports removing edges by either:
    1. Selecting them in the table and clicking remove
    2. Clicking directly on the edge in the graph and clicking remove
    """
    # Initial message and data checks
    message = "Tap a driver and a constructor node, then click a button to add/remove an edge."

    # Determine which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_elements, table_data, message
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    # Handle adding edge (existing functionality unchanged)
    if trigger == "add-edge-btn":
        if not node_store or len(node_store) != 2:
            return current_elements, table_data, "Please tap exactly 2 nodes (one driver, one constructor)."

        node1, node2 = node_store
        if node1["group"] == node2["group"]:
            return current_elements, table_data, "Selected nodes must be from different bipartite groups."

        driver_name, constructor_name = (node1["label"], node2["label"]) if node1["group"] == "driver" else (
            node2["label"], node1["label"])

        # Check if edge already exists
        if any(
                elem.get("data", {}).get("source") == f"driver-{driver_name}" and
                elem.get("data", {}).get("target") == f"constructor-{constructor_name}"
                for elem in current_elements
        ):
            return current_elements, table_data, f"{driver_name} is already adjacent to {constructor_name}."

        # Simulate the what-if scenario
        result = simulate_whatif_for_nodes(global_f1_graph, driver_name, constructor_name)
        if result is None:
            return current_elements, table_data, "Simulation failed: invalid names."

        prev_elo, whatif_rating, new_final_elo = result

        # Add hypothetical edge
        new_edge = {
            "data": {
                "id": f"hypothetical-{driver_name}-{constructor_name}",
                "source": f"driver-{driver_name}",
                "target": f"constructor-{constructor_name}"
            },
            "classes": "hypothetical-edge"
        }
        current_elements.append(new_edge)

        # Add new row to simulation table
        new_row = {
            "Driver": driver_name,
            "Constructor": constructor_name,
            "PrevELO": prev_elo,
            "HypoELO": whatif_rating,
            "NewFinalELO": new_final_elo
        }
        table_data.append(new_row)

        message = f"Hypothetical edge added for {driver_name} with {constructor_name}."

    # Handle removing edge (updated functionality)
    elif trigger == "remove-edge-btn":
        removed = False
        new_elements = current_elements.copy()
        new_table_data = table_data.copy()

        # Option 1: Remove via edge selection in graph
        if edge_store and edge_store.get('id', '').startswith('hypothetical-'):
            edge_id = edge_store['id']
            # Extract names from edge ID
            parts = edge_id.split('-')
            driver_name = parts[1]
            constructor_name = parts[2]

            # Remove edge from elements
            new_elements = [elem for elem in new_elements if elem.get('data', {}).get('id') != edge_id]
            # Remove corresponding row from table
            new_table_data = [row for row in new_table_data if not (
                    row['Driver'] == driver_name and row['Constructor'] == constructor_name
            )]
            removed = True
            message = f"Removed hypothetical edge between {driver_name} and {constructor_name}."

        # Option 2: Remove via table selection
        if selected_rows and not removed:
            for idx in reversed(sorted(selected_rows)):
                if idx < len(new_table_data):
                    row = new_table_data.pop(idx)
                    driver_name = row['Driver']
                    constructor_name = row['Constructor']
                    edge_id = f"hypothetical-{driver_name}-{constructor_name}"
                    new_elements = [elem for elem in new_elements if elem.get('data', {}).get('id') != edge_id]
            message = "Removed selected hypothetical edges."
            removed = True

        if not removed:
            message = "Please select a hypothetical edge (click on it) or select table rows to remove."

        return new_elements, new_table_data, message

    return current_elements, table_data, message


if __name__ == "__main__":
    app.run(debug=True)
