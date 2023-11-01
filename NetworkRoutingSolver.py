#!/usr/bin/python3


from CS312Graph import *
import time

class PQueue:
    def insert(self, node: CS312GraphNode) -> None:
        pass

    def decrease_key(self) -> None:
        pass

    def delete_min(self):
        pass
class ArrayPQueue(PQueue):
    def __init__(self) -> None:
        # queue will store a node
        self.queue: list = []
        # id_to_dist will store ids as keys with their distance from src node as values
        self.id_to_dist: dict = {}
    
    # Complexity: O(1)
    def insert(self, node: CS312GraphNode) -> None:
        # initially insert a node with distance infinity
        self.queue.append(node)
        self.id_to_dist[node.node_id] = float('inf')

    # Complexity: O(1)
    def decrease_key(self, node, new_dist) -> None:
        self.id_to_dist[node.node_id] = new_dist

    # Complexity: O(|V|)
    def delete_min(self) -> CS312GraphNode:
        min_dist = float('inf')
        min_node = None
        dist = None
        for node in self.queue:
            dist = self.id_to_dist[node.node_id]
            if dist <= min_dist:
                min_dist = dist
                min_node = node

        self.queue.remove(min_node)
        return min_node
        

class HeapPQueue(PQueue):
    # indexing: parent = i - 1 // 2, left child = 2i + 1, right child = 2i + 2
    def __init__(self) -> None:
        self.queue: list = []
        self.id_to_dist: dict = {}
        self.id_to_index: dict = {}

    # Complexity: O(log|V|)
    def insert(self, node: CS312GraphNode) -> None:
        self.queue.append(node)
        self.id_to_dist[node.node_id] = float('inf')
        self.bubbleup(node, len(self.queue) - 1)

    # Complexity: O(log|V|)
    def decrease_key(self, x, new_dist) -> None:
        self.id_to_dist[x.node_id] = new_dist
        self.bubbleup(x, self.id_to_index[x.node_id])

    # Complexity: O(log|V|)
    def delete_min(self) -> CS312GraphNode:
        # swap first and last elements
        tmp = self.queue[0]
        self.queue[0] = self.queue[len(self.queue) - 1]
        self.queue[len(self.queue) - 1] = tmp
        # remove last element
        min_node = self.queue.pop()
        # siftdown first element
        if len(self.queue) > 0:
            self.siftdown(self.queue[0], 0)
        return min_node


    # move node x, which is at index i, up to the proper place in the heap
    def bubbleup(self, x: CS312GraphNode, i):
        p = (i - 1) // 2
        
        while i != 0 and self.id_to_dist[self.queue[p].node_id] > self.id_to_dist[x.node_id]:
            self.queue[i] = self.queue[p]
            self.id_to_index[self.queue[p].node_id] = i
            i = p
            p = (i - 1) // 2
        
        self.queue[i] = x
        self.id_to_index[x.node_id] = i


    def siftdown(self, x, i):
        c = self.minchild(i)

        while c != 0 and self.id_to_dist[self.queue[c].node_id] < self.id_to_dist[x.node_id]:
            self.queue[i] = self.queue[c]
            self.id_to_index[self.queue[c].node_id] = i
            i = c
            c = self.minchild(i)

        self.queue[i] = x
        self.id_to_index[x.node_id] = i


    
    def minchild(self, i):
        if 2*i + 1 >= len(self.queue):
            return 0 # no children
    
        l= 2*i + 1
        r = 2*i + 2

        if r == len(self.queue):
            return l

        if self.id_to_dist[self.queue[l].node_id] < self.id_to_dist[self.queue[r].node_id]:
            return l
        else:
            return r

    

class NetworkRoutingSolver:
    def __init__( self):
        # node id to previous node id
        self.prev = {}

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        src: CS312GraphNode = self.network.nodes[self.source]
        dest: CS312GraphNode = self.network.nodes[self.dest]

        if self.prev[dest.node_id] == None:
            return {'cost': float('inf'), 'path': []}

        curr_node: CS312GraphNode = dest
        while curr_node != src:
            prev_id = self.prev[curr_node.node_id]
            prev_node = self.network.nodes[prev_id]
            correct_edge = None
            for edge in prev_node.neighbors:
                if edge.dest.node_id == curr_node.node_id:
                    correct_edge = edge
                    break
            path_edges.append( (correct_edge.src.loc, correct_edge.dest.loc, '{:.0f}'.format(correct_edge.length)) )
            total_length += correct_edge.length
            curr_node = prev_node
        
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap = False ):
        self.source: int = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)

        # initialize the priority queue
        pq: PQueue = None
        if use_heap:
            pq = HeapPQueue()
        else:
            pq = ArrayPQueue()

        # Loop through all nodes in the network and insert
        # them into the priority queue. Set their prev to null
        all_nodes = self.network.getNodes()
        for node in all_nodes:
            pq.insert(node)
            self.prev[node.node_id] = None

        pq.decrease_key(all_nodes[srcIndex], 0)

        while len(pq.queue) > 0:
            u = pq.delete_min()
            for edge in u.neighbors:
                v = edge.dest
                curr_dist = pq.id_to_dist[v.node_id]
                calc_dist = pq.id_to_dist[u.node_id] + edge.length
                if calc_dist < curr_dist:
                    self.prev[v.node_id] = u.node_id
                    pq.decrease_key(v, calc_dist)
                
        
        t2 = time.time()
        return (t2-t1)

