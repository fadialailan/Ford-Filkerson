import queue

"""
a class to hold the flow network, used in Q1
"""
class FlowNetwork:
    """
    Constuctor

    param:
        number_of_nodes: the number of nodes in the flow network

    complexity:
        time: O(number_of_nodes)
        space: O(number_of_nodes)
    """
    def __init__(self, number_of_nodes):
        self.number_of_nodes = number_of_nodes
        self.edges = []

        self.nodes = [None]*number_of_nodes
        for index in range(number_of_nodes):
            self.nodes[index] = Node(index)

        self.nodes[0].type = Node.TYPE_SOURCE
        self.nodes[1].type = Node.TYPE_END

        self.source_node = self.nodes[0]
        self.end_node = self.nodes[1]


    """
    a function to add an edge

    param
        capacity: the capacity of the edge
        from_node: the node the edge will start from
        to_node: the node the edge will go to
    return
        forward_edge: the generated forward edge
        reverse_edge: the generated reverse edge

    complexity:
        time: O(1)
        space: O(1)
    """
    def addEdge(self, capacity, from_node, to_node):
        (forward_edge, reverse_edge) = FlowEdge.createPair(capacity, self.nodes[from_node], self.nodes[to_node])
        self.nodes[from_node].forward_edges.append(forward_edge)
        self.nodes[to_node].reverse_edges.append(reverse_edge)

        self.edges.append(forward_edge)

        return (forward_edge, reverse_edge)

    """
    basicly a BFS algorithim that find a path from the source node to the end node

    parameters: None

    return: None

    complexity:
        time: O(V+E)
        space: O(V)

        where V is the number of vertices rechable from the source node
        and E is the number of edges rechable from the source node

    """
    def findAugumentingPath(self):
        self.resetNodes()
        discovered_queue = queue.Queue(self.number_of_nodes)
        current_node = self.source_node
        current_node.discovered = True
        running = True
        while running:
            for current_edge in current_node.forward_edges+current_node.reverse_edges:
                if not current_edge.isUsable():
                    continue
                current_target = current_edge.target
                if current_target.discovered == False:
                    current_target.discovered = True
                    current_target.parent = current_node
                    current_target.parent_connection = current_edge
                    discovered_queue.put_nowait(current_target)
                    if current_target.type == Node.TYPE_END:
                        running = False
                        break
            if discovered_queue.empty():
                return None
            current_node = discovered_queue.get_nowait()
        current_node = self.end_node
        output = [current_node]
        while current_node.parent != None:
            output.append(current_node.parent)
            current_node = current_node.parent
        return output[::-1]

    """
    the ford filkerson algorithim

    parameters: None

    return: None

    complexity:
        time: O(F*E)
        space: O(V)

        where V is the number of vertices rechable from the source node
        and E is the number of edges rechable from the source node
        and F is the maximum flow of the network
    """
    def fordFulkerson(self):
        augumenting_path = self.findAugumentingPath()

        while augumenting_path != None:

            min_available_flow = float("inf")
            for index in range(1, len(augumenting_path)):
                current_edge = augumenting_path[index].parent_connection
                available_flow = current_edge.availabeFlow()
                if available_flow < min_available_flow:
                    min_available_flow = available_flow

            for index in range(1, len(augumenting_path)):
                current_edge = augumenting_path[index].parent_connection
                current_edge.increaseFlow(min_available_flow)

            augumenting_path = self.findAugumentingPath()



    def resetNodes(self):
        for node in self.nodes:
            node.reset()


"""
an edge class to be used in the flow network
"""
class FlowEdge:

    FORWARD_EDGE = 0
    REVERSE_EDGE = 1

    """
    constructor

    parameters:
        capacity: capacity of the edge
        source: the edge's source
        target: the edge's target

    return: None

    complexiy:
        time: O(1)
        space: O(1)
    """
    def __init__(self, capacity, source,  target):
        self.type = FlowEdge.FORWARD_EDGE
        self.capacity = capacity
        self.flow = 0
        self.opposite_edge = None

        self.source = source
        self.target = target

    """
    creates a forward edge and a reverse edge

    parameters:
        capacity: capacity of the edges
        source: the forward edge's source
        target: the forward edge's target

    return:
        forward_edge: the generated forward edge
        reverse_edge: the generated reverse edge

    complexiy:
        time: O(1)
        space: O(1)
    """
    def createPair(capacity, from_node, to_node):
        forward_edge = FlowEdge(capacity, from_node, to_node)
        reverse_edge = FlowEdge(capacity, to_node ,from_node)

        reverse_edge.type = FlowEdge.REVERSE_EDGE
        reverse_edge.flow = reverse_edge.capacity
        reverse_edge.flow = capacity

        FlowEdge.linkEdges(forward_edge, reverse_edge)

        return (forward_edge, reverse_edge)

    """
    a function to link to edges

    parameters:
        edge1: the first edge to link
        edge2: the second edge to link

    return: None

    complexity:
        time: O(1)
        space: O(1)
    """
    def linkEdges(edge1, edge2):
        edge1.opposite_edge = edge2
        edge2.opposite_edge = edge1

    """
    a function to check if an edge can be part of the
    augumentation graph

    parameters:None

    return: True if it can be used, False otherwise

    complexity:
        time: O(1)
        space: O(1)
    """
    def isUsable(self):
        return self.availabeFlow() > 0

    """
    a function to calculate the available flow in an edge

    parameters:None

    return: the available flow

    complexity:
        time: O(1)
        space: O(1)
    """
    def availabeFlow(self):
        return self.capacity - self.flow

    """
    a function to increase flow in an edge
    and adjust its reverse edge to match

    parameters:
        extra_flow: how much flow to add

    return: None

    complexity:
        time: O(1)
        space: O(1)
    """
    def increaseFlow(self, extra_flow):
        self.flow += extra_flow
        self.opposite_edge.flow -= extra_flow


"""
a class to be a node in the flow network
"""
class Node:

    TYPE_SOURCE = 0
    TYPE_END = 1
    TYPE_NORMAL = 2

    """
    constructor

    parameters:
        name: name of the node

    complexity:
        time: O(1)
        space: O(1)
    """
    def __init__(self, name):
        self.forward_edges = []
        self.reverse_edges = []
        self.type = Node.TYPE_NORMAL
        self.parent = None
        self.parent_connection = None
        self.visited = False
        self.discovered = False
        self.name = name

    """
    a function to reset the node, useful for calling BFS
    multiple times

    parameters:None

    return:None

    complexity:
        time: O(1)
        space: O(1)
    """
    def reset(self):
        self.parent = None
        self.visited = False
        self.discovered = False

    """
    a function to calculate the total flow out of a node

    parameters:None

    return: total flow

    complexity:
        time: O(E)
        space: O(1)

    where E is the total amount of forward edges of the node
    """
    def calculateOutFlow(self):
        total = 0
        for edge in self.forward_edges:
            total += edge.flow
        return total



if __name__ == "__main__":
    #example
    graph = FlowNetwork(10) # input the number of vertices
    graph.nodes # this is the list of node
    assert(10 == len(graph.nodes))

    graph.source_node # this is the first node in list of nodes
    assert(graph.source_node == graph.nodes[0])

    graph.end_node # this is the second node in the list of nodes
    assert(graph.end_node == graph.nodes[1])

    graph.nodes[2:] # this is the list of nodes in between

    (forward_edge, reverse_edge) = graph.addEdge(10, 0, 1) # this is how to add an edge
    #the ford Fulkerson needs the for every edge a reverse edge as well
    #I do return this if needed (and the source the implementation needs this) but it shouldn't be needed

    graph.fordFulkerson() # this will run the Ford Fulkerson algorithm

    graph.source_node.calculateOutFlow # this is an easy way to find the total flow the the graph

    assert(10 == graph.source_node.calculateOutFlow())

    print("all clear?")




