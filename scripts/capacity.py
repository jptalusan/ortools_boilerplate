"""Vehicles Routing Problem (VRP) with Time Windows."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


penalty = 10_000  # large penalty to discourage skipping

def create_data_model():
    """Stores the data for the problem."""
    data = {}

    # You should replace this with your own travel time matrix, which can be from OSRM etc...
    data["time_matrix"] = [
        [0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7],
        [6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14],
        [9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9],
        [8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16],
        [7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14],
        [3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8],
        [6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5],
        [2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10],
        [3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6],
        [2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5],
        [6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4],
        [6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10],
        [4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8],
        [4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6],
        [5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2],
        [9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9],
        [7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0],
    ]
    data["pickups_deliveries"] = [
        [1, 6],   # pickup at 1, deliver at 6
        [2, 10],  # pickup at 2, deliver at 10
        [4, 3],   # pickup at 4, deliver at 3
        [5, 9],   # pickup at 5, deliver at 9
        [7, 8],   # pickup at 7, deliver at 8
        [15, 11], # pickup at 15, deliver at 11
        [13, 12], # pickup at 13, deliver at 12
        [16, 14], # pickup at 16, deliver at 14
    ]
    data["time_windows"] = [
        (0, 20),  # depot - keep flexible
        (0, 8),   # 1 (pickup) - early window, travel time 1->6 is 8
        (0, 10),  # 2 (pickup) - early window, travel time 2->10 is 4
        (8, 10),  # 3 (delivery) - must be after pickup at 4
        (5, 8),   # 4 (pickup) - early window, travel time 4->3 is 1
        (0, 8),   # 5 (pickup) - early window, travel time 5->9 is 2
        (8, 24),  # 6 (delivery) - must be after pickup at 1 + travel time
        (0, 6),   # 7 (pickup) - early window, travel time 7->8 is 4
        (6, 24),  # 8 (delivery) - must be after pickup at 7 + travel time
        (8, 24),  # 9 (delivery) - must be after pickup at 5 + travel time
        (10, 24), # 10 (delivery) - must be after pickup at 2 + travel time
        (10, 12),  # 11 (delivery) - must be after pickup at 15 + travel time
        (6, 24),  # 12 (delivery) - must be after pickup at 13 + travel time
        (0, 6),   # 13 (pickup) - early window, travel time 13->12 is 1
        (8, 24),  # 14 (delivery) - must be after pickup at 16 + travel time
        (8, 10),   # 15 (pickup) - early window, travel time 15->11 is 3
        (0, 24),   # 16 (pickup) - early window, travel time 16->14 is 2
    ]
    data["max_return_time"] = 15  # All vehicles must return to depot by time 20
    data["demands"] = [0, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, -1, -1, 1, -1, 1, 1]
    data["vehicle_capacities"] = [4, 4, 4, 4]  # Each vehicle can carry max 4 people
    data["num_vehicles"] = 4
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    print(f"Routing Status: {routing.status()}")
    time_dimension = routing.GetDimensionOrDie("Time")
    capacity_dimension = routing.GetDimensionOrDie("Capacity")
    total_time = 0
    total_load = 0
    
    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        max_load = 0  # Track maximum load for this route
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            time_var = time_dimension.CumulVar(index)
            capacity_var = capacity_dimension.CumulVar(index)
            current_load = solution.Value(capacity_var)
            max_load = max(max_load, current_load)  # Update max load
            plan_output += (
                f"{node_index}"
                f" Load({current_load})"
                f" Time({solution.Min(time_var)},{solution.Max(time_var)})"
                " -> "
            )
            index = solution.Value(routing.NextVar(index))
            
        # Final node (depot)
        node_index = manager.IndexToNode(index)
        time_var = time_dimension.CumulVar(index)
        capacity_var = capacity_dimension.CumulVar(index)
        plan_output += (
            f"{node_index}"
            f" Load({solution.Value(capacity_var)})"
            f" Time({solution.Min(time_var)},{solution.Max(time_var)})\n"
        )
        
        final_load = solution.Value(capacity_var)
        final_time = solution.Min(time_var)
        plan_output += f"Maximum load of the route: {max_load}\n"
        plan_output += f"Time of the route: {final_time}min\n"
        print(plan_output)
        
        total_time += final_time
        total_load += max_load
    
    skipped_requests = []
    for i, request in enumerate(data["pickups_deliveries"]):
        pickup_node = request[0]
        delivery_node = request[1]
        pickup_index = manager.NodeToIndex(pickup_node)
        delivery_index = manager.NodeToIndex(delivery_node)
        
        # Check if pickup was skipped (node points to itself)
        pickup_skipped = solution.Value(routing.NextVar(pickup_index)) == pickup_index
        delivery_skipped = solution.Value(routing.NextVar(delivery_index)) == delivery_index
        
        if pickup_skipped or delivery_skipped:
            skipped_requests.append(f"Request {i+1}: pickup {pickup_node} -> delivery {delivery_node}")
    
    if skipped_requests:
        print(f"Skipped {len(skipped_requests)} pickup/delivery requests:")
        for request in skipped_requests:
            print(f"  {request}")
    else:
        print("\nAll pickup/delivery requests were completed!")

    print(f"Total time of all routes: {total_time}min")
    print(f"Total load of all routes: {total_load}")


def main():
    """Solve the VRP with time windows."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["time_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["time_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # ===== ADD CAPACITY CONSTRAINTS =====
    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    # Add Time Windows constraint.
    time = "Time"
    routing.AddDimension(
        transit_callback_index,
        30,  # allow waiting time
        30,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time,
    )
    time_dimension = routing.GetDimensionOrDie(time)
    # time_dimension.SetGlobalSpanCostCoefficient(100)

    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data["time_windows"]):
        if location_idx == data["depot"]:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    # Add time window constraints for each vehicle start and end nodes.
    depot_idx = data["depot"]
    for vehicle_id in range(data["num_vehicles"]):
        # Start node (departure from depot)
        start_index = routing.Start(vehicle_id)
        time_dimension.CumulVar(start_index).SetRange(
            data["time_windows"][depot_idx][0], data["time_windows"][depot_idx][1]
        )
        
        # End node (return to depot) - must return by max return time
        end_index = routing.End(vehicle_id)
        time_dimension.CumulVar(end_index).SetRange(0, data["max_return_time"])  # Must return by max return time

    # Instantiate route start and end times to produce feasible times.
    for i in range(data["num_vehicles"]):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    # ----- 4. Make nodes optional with penalties ------ (Add it within the pickup and dropoff constraint below)
    for node in range(1, len(data["demands"])):  # skip depot
        routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

    # ===== ADD PICKUP AND DELIVERY CONSTRAINTS =====
    for request in data["pickups_deliveries"]:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        # # Make the pickup/delivery pair optional as a unit
        # routing.AddDisjunction([pickup_index, delivery_index], penalty)

        routing.AddPickupAndDelivery(pickup_index, delivery_index)

        # Ensure pickup happens before delivery
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index)
        )
        routing.solver().Add(
            time_dimension.CumulVar(pickup_index) <= time_dimension.CumulVar(delivery_index)
        )
        

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )
    # search_parameters.local_search_metaheuristic = (
    #     routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)

    search_parameters.time_limit.FromSeconds(10)  # Increased time limit
    search_parameters.log_search = False
    
    # Add these for more verbose logging
    # search_parameters.solution_limit = 50  # Stop after finding 50 solutions
    # search_parameters.lns_time_limit.FromSeconds(5)  # Large neighborhood search time
    
    # Print search parameters to verify they're set
    print("Search parameters set, starting solve...")
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    # print(solution)
    if solution:
        print_solution(data, manager, routing, solution)

if __name__ == "__main__":
    main()