import math
import random
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Define generic base coordinates for warehouses to anchor the route
base_coords = {
    'A': (34.0522, -118.2437), # Los Angeles
    'B': (40.7128, -74.0060),  # New York
    'C': (41.8781, -87.6298),  # Chicago
    'D': (29.7604, -95.3698),  # Houston
    'F': (37.7749, -122.4194)  # San Francisco
}

def generate_random_coordinate(base_lat, base_lon, radius_km=30):
    """Generate fake delivery destinations within a driving radius."""
    lat_offset = (random.uniform(-1, 1) * radius_km) / 111.0
    lon_offset = (random.uniform(-1, 1) * radius_km) / (111.0 * math.cos(math.radians(base_lat)))
    return (base_lat + lat_offset, base_lon + lon_offset)

def calculate_distance(coord1, coord2):
    """Haversine distance in KM."""
    R = 6371.0
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def create_distance_matrix(locations):
    """Create a matrix of distances multiplied by 1000 for OR-Tools integer requirements."""
    matrix = []
    for from_node in locations:
        row = []
        for to_node in locations:
            dist = int(calculate_distance(from_node, to_node) * 1000)
            row.append(dist)
        matrix.append(row)
    return matrix

def optimize_route(warehouse, packages):
    if not packages:
        return None
    
    # Fallback warehouse if missing
    if warehouse not in base_coords:
        warehouse = 'A' 
        
    depot_coord = base_coords[warehouse]
    
    # Seed randomly for reproduction if needed
    # Generate coordinates for packages
    delivery_coords = [generate_random_coordinate(depot_coord[0], depot_coord[1]) for _ in packages]
    
    locations = [depot_coord] + delivery_coords
    
    # Set up routing variables
    data = {}
    data['distance_matrix'] = create_distance_matrix(locations)
    data['num_vehicles'] = 1
    data['depot'] = 0
    
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        
        # Base Distance
        dist = data['distance_matrix'][from_node][to_node]
        
        # PRIORITY MODIFIER:
        # If the target node (package) is highly delayed/important, naturally reduce the perceived cost 
        # specifically from the depot to encourage visiting it earlier in the TSP.
        # This is a soft heuristic to pull important packages to the front.
        if from_node == 0 and to_node != 0:
            pkg_idx = to_node - 1
            pkg_info = packages[pkg_idx]
            
            # Reduce cost by 50% if the ML model thinks this package is at risk of delay
            if pkg_info.get("delayed_warning", False):
                dist = int(dist * 0.5)
                
            # Reduce cost further for highly important products
            if pkg_info.get("data", {}).get("Product_importance") == "high":
                dist = int(dist * 0.7)
                
        return dist

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    # Solve parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve!
    solution = routing.SolveWithParameters(search_parameters)

    if not solution:
        return None
        
    # Extract route
    index = routing.Start(0)
    sequence = []
    total_distance = 0
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        sequence.append(node_index)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        # Use actual distance calculation so fake priority drops don't skew final numbers
        total_distance += calculate_distance(locations[previous_index], locations[manager.IndexToNode(index)])
    
    # Don't forget return to depot calculation
    # total_distance += calculate_distance(locations[sequence[-1]], locations[0])
    
    # Shift indices to account for depot being index 0
    package_sequence = [node - 1 for node in sequence if node != 0]
    
    return {
        "ordered_indices": package_sequence,
        "total_distance_km": round(total_distance, 2),
        "locations": [{"lat": c[0], "lng": c[1]} for c in delivery_coords],
        "depot_location": {"lat": depot_coord[0], "lng": depot_coord[1]}
    }
