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
        "display": "flex",
        "flexDirection": "row",
        "fontFamily": "'Red Hat Display', sans-serif",
        "backgroundColor": "#1B1F23",
        "color": "white",
        "margin": "0",
        "padding": "0"
    },
    children=[
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
                {"selector": ".hypothetical-edge", "style": {"line-color": "#FFAA00", "line-style": "dashed", "width": 3}}
            ],
            boxSelectionEnabled=False,
            autounselectify=False,
            minZoom=0.2,
            maxZoom=3
        ),
        dcc.Store(id="node-store", data=[]),
        layout_store,

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
    State("node-store", "data")
)
def update_node_store(tapNodeData, storeData):
    """
    Callback to update the node store when a node is tapped.
    
    Preconditions:
      - tapNodeData is a dict representing the tapped node's data, or None.
      - storeData is a list of dicts representing currently stored nodes, or None.
    """
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
    [
        Output("cytoscape", "elements"),
        Output("simulation-table", "data"),
        Output("simulation-output", "children")
    ],
    Input("add-edge-btn", "n_clicks"),
    State("node-store", "data"),
    State("cytoscape", "elements"),
    State("simulation-table", "data")
)
def add_hypothetical_edge(n_clicks, node_store, current_elements, table_data):
    """
    callback to add a hypothetical edge when the "Add Hypothetical Edge" button is clicked.
    
    Preconditions:
      - n_clicks is an integer representing the number of button clicks (must be > 0).
      - node_store is a list of two node dicts (one driver and one constructor) that were tapped.
      - current_elements is the current list of Cytoscape elements.
      - table_data is the current data in the simulation table.
    """
    if not n_clicks:
        return current_elements, table_data, "Tap a driver and a constructor node, then click the button."

    if not node_store or len(node_store) != 2:
        return current_elements, table_data, "Please tap exactly 2 nodes (one driver, one constructor)."

    node1, node2 = node_store
    if node1.get("group") == node2.get("group"):
        return current_elements, table_data, "Selected nodes must be from different bipartite groups."

    if node1["group"] == "driver":
        driver_name = node1["label"]
        constructor_name = node2["label"]
    else:
        driver_name = node2["label"]
        constructor_name = node1["label"]

    if any(
        elem.get("data", {}).get("source") == f"driver-{driver_name}" and
        elem.get("data", {}).get("target") == f"constructor-{constructor_name}"
        for elem in current_elements
    ):
        return current_elements, table_data, f"{driver_name} is already adjacent to {constructor_name}."

    from prediction import simulate_whatif_for_nodes
    result = simulate_whatif_for_nodes(global_f1_graph, driver_name, constructor_name)
    if result is None:
        return current_elements, table_data, "Simulation failed: invalid names."
    prev_elo, whatif_rating, new_final_elo = result

    new_edge = {
        "data": {
            "id": f"hypothetical-{driver_name}-{constructor_name}",
            "source": f"driver-{driver_name}",
            "target": f"constructor-{constructor_name}"
        },
        "classes": "hypothetical-edge"
    }
    current_elements.append(new_edge)

    new_row = {
        "Driver": driver_name,
        "Constructor": constructor_name,
        "PrevELO": prev_elo,
        "HypoELO": whatif_rating,
        "NewFinalELO": new_final_elo
    }
    table_data.append(new_row)

    message = f"Hypothetical edge added for {driver_name} with {constructor_name}."
    return current_elements, table_data, message

if __name__ == "__main__":
    app.run(debug=True)
