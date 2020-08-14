from room import Room
from player import Player
from world import World

# import Queue for BFS
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {}
visited = []
current_room = player.current_room
reverse_direction = {"n": "s", "s": "n", "w": "e", "e": "w"}


# adding Rooms(nodes) to the Map(graphs)

def add_room(room, graph):
    graph[room.id] = {}
    for exit in room.get_exits():
        graph[room.id][exit] = "?"


# exits not visited
def get_unvisited_exits(room):
    room_id = room.id
    unvisited_exits = []

    exits = room.get_exits()  # this gives us a List

    for exit in exits:
        if graph[room_id][exit] == "?":
            unvisited_exits.append(exit)
    return unvisited_exits


# to create the graph we will make a Depth First Traversal (recursively)

def create_graph(room, graph, visited):
    # check the room in the map{graph}
    if room.id not in graph:
        add_room(room, graph)
        # add visited room to visited list
        visited.append(room.id)

    # important! keep track of unvisited exits
    # loop trough unvisited exit
    # get the room in direction of unvisited exit
    # add that room to map(graph) and to visited
    # reverse exit
    unvisited_exits = get_unvisited_exits(room)
    if len(unvisited_exits) > 0:
        for exit in unvisited_exits:
            new_room = room.get_room_in_direction(exit)
            if new_room.id not in graph:
                add_room(new_room, graph)
                visited.append(new_room.id)

            reverse_exit = reverse_direction[exit]
            graph[room.id][exit] = new_room.id
            graph[new_room.id][reverse_exit] = room.id
            create_graph(new_room, graph, visited)

    if len(graph) == len(room_graph):
        return graph, visited

# now that we built our graph we will search it with BFS(breadth First Search)
# BFS best for finding the shortest path between two rooms
# need to keep track of visited, path, and direction


def bfs(starting_room, destination_room, graph):
    visited = set()
    room_queue = Queue()
    dir_queue = Queue()

    room_queue.enqueue([starting_room])
    dir_queue.enqueue([])

    while room_queue.size() > 0:
        room_path = room_queue.dequeue()
        # next direction to travel
        dir_path = dir_queue.dequeue()
        last_room = room_path[-1]
        if last_room not in visited:
            visited.add(last_room)
            if last_room == destination_room:
                return dir_path
            for direction in graph[last_room]:
                # add direction to both queues
                new_room_path = room_path + [graph[last_room][direction]]
                new_dir_path = dir_path + [direction]
                room_queue.enqueue(new_room_path)
                dir_queue.enqueue(new_dir_path)


# create the graph
room_graph, room_visited = create_graph(current_room, graph, visited)

for item in range(len(room_visited) - 1):
    path = bfs(room_visited[item], room_visited[item + 1], graph)
    traversal_path.extend(path)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
