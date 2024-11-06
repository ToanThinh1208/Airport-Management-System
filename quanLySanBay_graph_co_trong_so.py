import math
import heapq

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class RouteNode:
    def __init__(self, routeId, departureId, destinationId, aircraftType, price):
        self.routeId = routeId
        self.departureId = departureId
        self.destinationId = destinationId
        self.aircraftType = aircraftType
        self.price = price  # Add distance attribute

class AirportNode:
    def __init__(self, airportId, airportType, distance):
        self.airportId = airportId
        self.airportType = airportType
        self.distance = distance

class AirportSystem:
    def __init__(self):
        self.head = None
        self.headRoute = None

    def addAirport(self, new_airport):
        new_airport = Node(new_airport)
        if self.head is None:
            new_airport.next = self.head
            self.head = new_airport
            return True
        else:
            tmp = self.head
            while tmp:
                if tmp.data.airportId == new_airport.data.airportId:
                    return False
                if tmp.next is None:
                    tmp.next = new_airport
                    return True
                tmp = tmp.next
            tmp.next = new_airport
    def deleteAirport(self, airportId):
        if self.head is None:
            return False
        while self.headRoute and (
            self.headRoute.data.departureId == airportId
            or self.headRoute.data.destinationId == airportId
        ):
            self.headRoute = self.headRoute.next

        temp = self.headRoute
        while temp:
            next_route = temp.next
            if (
                temp.data.departureId == airportId
                or temp.data.destinationId == airportId
            ):
                self.deleteRoute(temp.data.routeId)
            temp = next_route

        if self.head.data.airportId == airportId:
            val = self.head.data
            self.head = self.head.next
            return val
        else:
            temp = self.head
            while temp and temp.next:
                if temp.next.data.airportId == airportId:
                    val = temp.next.data
                    temp.next = temp.next.next
                    return val
                temp = temp.next
        return False

    def updateAirport(self, airportId, distance, newAirportType):
        if self.head is None:
            return False
        tmp = self.head
        while tmp:
            if tmp.data.airportId != airportId:
                tmp.data.distance = distance
                tmp.data.airportType = newAirportType
                return True
            tmp = tmp.next

    def displayAirport(self):
        if self.head is None:
            print("Airport system doesn't have any airport")
            return
        temp = self.head
        while temp:
            airport = temp.data
            print(
                f"Airport ID: {airport.airportId} | Distance: {airport.distance} | Airport Type: {airport.airportType}"
            )
            temp = temp.next

    def calculate_cost(self, departureId, destinationId, price):
        route = self.findRoute(departureId, destinationId)
        if route:
            return price
        return False

    def find_shortest_route(self, departureId, destinationId):
        # Check if both departure and destination airports exist
        if not any(node.data.airportId == departureId for node in self._iterate_nodes(self.head)):
            print("Departure airport does not exist.")
            return False
        if not any(node.data.airportId == destinationId for node in self._iterate_nodes(self.head)):
            print("Destination airport does not exist.")
            return False

        # Initialize distances with infinity and previous nodes for path reconstruction
        distances = {node.data.airportId: float("inf") for node in self._iterate_nodes(self.head)}
        distances[departureId] = 0
        previous_nodes = {node.data.airportId: None for node in self._iterate_nodes(self.head)}

        # Use a priority queue to track the next airport to process based on shortest distance
        unvisited_nodes = set(distances.keys())
        current_airport = departureId

        while unvisited_nodes:
            # Choose the unvisited node with the smallest distance
            current_airport = min((node for node in unvisited_nodes), key=lambda node: distances[node])

            # Exit if the smallest distance is infinity, meaning no more reachable nodes
            if distances[current_airport] == float("inf"):
                break

            # Iterate over routes to find neighbors and update distances
            for route in self._iterate_nodes(self.headRoute):
                if route.data.departureId == current_airport and route.data.destinationId in unvisited_nodes:
                    neighbor = route.data.destinationId
                    distance = route.data.price  # assuming 'price' is used as the distance or cost metric

                    # Calculate new distance to neighbor
                    new_distance = distances[current_airport] + distance
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous_nodes[neighbor] = current_airport

            # Mark current airport as visited
            unvisited_nodes.remove(current_airport)

        # Build the shortest path
        path = []
        current = destinationId
        if distances[destinationId] == float("inf"):
            print("No available path between departure and destination.")
            return False

        # Trace back the path from destination to departure using previous nodes
        while current:
            path.insert(0, current)
            current = previous_nodes[current]

        # Collect the shortest path's routes details
        routes_shortest_path = []
        for i in range(len(path) - 1):
            route = self.findRoute(path[i], path[i + 1])
            if route:
                routes_shortest_path.append(route.data)

        return path, distances[destinationId], routes_shortest_path

    def _iterate_nodes(self, start_node):
        # Generator for iterating nodes
        current = start_node
        while current:
            yield current
            current = current.next

    def findRoute(self, departureId, destinationId):
        # Find the route node between two given airports
        temp = self.headRoute
        while temp:
            if temp.data.departureId == departureId and temp.data.destinationId == destinationId:
                return temp
            temp = temp.next
        return False


    def addRoute(self, newRoute):
        new_route = Node(newRoute)
        if new_route.data.departureId == new_route.data.destinationId:
            return False
        if self.headRoute is None:
            self.headRoute = new_route
            return True
        else:
            temp = self.headRoute
            while temp:
                if temp.data.routeId == new_route.data.routeId:
                    return False
                if temp.next is None:
                    temp.next = new_route
                    return True
                temp = temp.next
            temp.next = new_route
            return True

    def deleteRoute(self, routeId):
        if self.headRoute is None:
            return False
        if self.headRoute.data.routeId == routeId:
            val = self.headRoute.data
            self.headRoute = self.headRoute.next
            return val
        else:
            temp = self.headRoute
            while temp and temp.next:
                if temp.next.data.routeId == routeId:
                    val = temp.next.data
                    temp.next = temp.next.next
                    return val
                temp = temp.next
        return False

    def displayRoute(self):
        if self.headRoute is None:
            print("Airport system doesn't have any routes.")
            return
        temp = self.headRoute
        while temp:
            route = temp.data
            print(
                f"RouteID: {route.routeId} | DepartureID: {route.departureId} | DestinationID: {route.destinationId} | Aircraft_Type: {route.aircraftType} | Distance: {route.price}"
            )
            temp = temp.next
airportSystem = AirportSystem()
def get_integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_optional_integer_input(prompt):
    user_input = input(prompt).strip()
    if user_input == "":
        return None
    try:
        return int(user_input)
    except ValueError:
        print("Invalid input. Please enter a valid integer or leave blank.")
        return get_optional_integer_input(prompt)

def showMenu() -> None:
    print("+------------------------Airport System------------------------+")
    print("| 1. Add an Airport                 6. Find the Shortest Route |")
    print("| 2. Delete an Airport              7. Add a new Route         |")
    print("| 3. Update Airport Information     8. Delete a Route          |")
    print("| 4. Display Airport System         9. Display Route data      |")
    print("| 5. Calculate Cost                 10. Exit                   |")
    print("+--------------------------------------------------------------+")
def checkCorrectTypeInput(choice):
    return choice in ["l", "m", "s", "L", "M", "S"]
while True:
    showMenu()
    choice = get_integer_input("Input your choice: ")

    if choice == 1:
        try:
            airportId = get_integer_input("Input an Airport Id: ")
        except ValueError:
            print("Your airport ID must be an integer!")
            continue

        print("Input Location Coordinate")
        try:
            distance = get_integer_input("Input distance: ")
        except ValueError:
            print("Your distance must be an integer!")
            continue

        airportType = input("Input the Airport type: ")
        if not checkCorrectTypeInput(airportType):
            print("The airport type you entered is incorrect.")
        else:
            new_airport = AirportNode(airportId, airportType, distance)
            if airportSystem.addAirport(new_airport):
                print("Addition was successful.")
            else:
                print("Failed to add")

    elif choice == 2:
        try:
            airportId = get_integer_input("Input Airport Id to delete: ")
        except ValueError:
            print("Your airport ID must be an integer!")
            continue

        airport = airportSystem.deleteAirport(airportId)
        if airport:
            print("Details of the airport to be deleted")
            print(
                f"Airport ID: {airport.airportId} | Distance: {airport.distance} | Airport Type: {airport.airportType}"
            )
            print(f"Successfully deleted airport with ID {airportId}.")
        else:
            print("Deletion was unsuccessful.")

    elif choice == 3:
        try:
            airportId = get_integer_input("Input Airport Id to update: ")
        except ValueError:
            print("Your airport ID must be an integer!")
            continue

        newDistance = input("Input new Distance: ")
        newDistance = int(newDistance) if newDistance.isdigit() else None

        new_airportType = input("Input a new Airport type: ")
        if new_airportType and not checkCorrectTypeInput(new_airportType):
            print("The airport type you entered is incorrect.")
        else:
            if airportSystem.updateAirport(airportId, newDistance, new_airportType):
                print("Update was successful.")
            else:
                print("Update was unsuccessful")

    elif choice == 4:
        print("------------The Airport System display------------")
        airportSystem.displayAirport()

    elif choice == 5:
        try:
            departureId = get_integer_input("Input the departure ID: ")
            destinationId = get_integer_input("Input the destination ID: ")
        except ValueError:
            print("Departure ID and Destination ID must be integers.")
            continue

        price = input("Input your type to calculate: ")

        result = airportSystem.calculate_cost(departureId, destinationId, price)
        if result is not None:
            print(f"The result for {price} is {round(result, 2)}.")
        else:
            print("Calculation failed.")

    elif choice == 6:
        try:
            departureId = get_integer_input("Input the departure airport ID: ")
            destinationId = get_integer_input("Input the destination airport ID: ")
        except ValueError:
            print("Departure ID and Destination ID must be integers.")
            continue

        result = airportSystem.find_shortest_route(departureId, destinationId)
        if result:
            path, distance, routes_shortest_path = result
            print(
                f"Shortest path from {departureId} to {destinationId} is {' -> '.join(map(str, path))} with total distance {distance} miles."
            )
            for route in routes_shortest_path:
                print(
                    f"RouteID: {route.routeId}, DepartureID: {route.departureId}, DestinationID: {route.destinationId}, Aircraft_Type: {route.aircraftType}"
                )
        else:
            print("No available path found between the airports or airports do not exist.")

    elif choice == 7:
        try:
            routeId = get_integer_input("Input Route ID: ")
            departureId = get_integer_input("Input Departure Id: ")
            destinationId = get_integer_input("Input Destination Id: ")
            price = get_integer_input("Input: ")
        except ValueError:
            print("Route ID, Departure ID, and Destination ID must be integers.")
            continue

        aircraftType = input("Input Aircraft type: ")
        if not checkCorrectTypeInput(aircraftType):
            print("The aircraft type you entered is incorrect.")
        else:
            new_route = RouteNode(routeId, departureId, destinationId, aircraftType, price)
            if airportSystem.addRoute(new_route):
                print("Adding is successful")
            else:
                print("Failed to add")

    elif choice == 8:
        try:
            routeId = get_integer_input("Input Route Id to delete: ")
        except ValueError:
            print("Route ID must be an integer.")
            continue

        route = airportSystem.deleteRoute(routeId)
        if route:
            print(
                f"RouteID: {route.routeId} | DepartureID: {route.departureId} | DestinationID: {route.destinationId} | Aircraft_Type: {route.aircraftType} | Distance: {route.price}"
            )
            print(f"Successfully deleted route with ID {routeId}")
        else:
            print("Deletion was unsuccessful.")

    elif choice == 9:
        print("------------The Route List------------")
        airportSystem.displayRoute()

    elif choice == 10:
        print("Program has ended.")
        break

    else:
        print("Your choice is out of the valid range.")
