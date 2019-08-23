class AnnotatedObject:
    """Represents an annotated object. Any number of annotations can be attached as (key,value) pairs, i.e. each annotation is identified with a unique key."""

    def __init__(self):
        """Create a new instance with empty annotations."""
        self.annotations = dict()

    def set_annotation(self, key, value):
        """
        Annotate node with some (key,value) pair.

        :param key: key used to retrieve the annotation
        :param value: actual annotation
        """
        self.annotations[key] = value

    def get_annotation(self, key):
        """
        Retrieve a previously attached annotation identified with the given key.

        :param key: key specified when adding the annotation
        :return: retrieved annotation, if present, else None
        """
        return self.annotations[key] if key in self.annotations else None

    def remove_annotation(self, key):
        """
        Remove the annotation identified with the given key.

        :param key: key with which the annotation is identified
        :return: True if the annotation is successfully removed
        :rtype: bool
        """
        if key not in self.annotations:
            return False
        del self.annotations[key]
        return True

    def has_annotation(self):
        """
        Indicates whether this node has any annotations.

        :return: True if this node has annotations
        :rtype: bool
        """
        return len(self.annotations) != 0

    def num_annotations(self):
        """
        Get the number of currently attached annotations.

        :return: number of annotations
        :rtype: int
        """
        return len(self.annotations)

    def get_annotations(self):
        """
        Get all attached annotations.

        :return: dictionary containing all anootations as (key, value) pairs
        :rtype: dict
        """
        return self.annotations

class Node(AnnotatedObject):
    """Represents a node in a graph. Nodes are identified with a string label (name) which should be unique among all nodes in a graph. Nodes with the same name are considered equal and an error will be thrown when attempting to add equal nodes to any graph. An unlimited number of annotations can be added to a node, e.g. during execution of a specific algorithm."""

    def __init__(self, name):
        """
        Create a new node with given name.

        :param name: node name
        :type name: Node
        """
        super().__init__()
        self.name = name

    def __str__(self):
        """

        :return: formatted string representation
        :rtype: str
        """
        return f"{self.name}{' ' + self.get_annotations() if self.has_annotation() else ''}"

    def __eq__(self, other):
        """
        Compares nodes for equality based on their name.

        :param other: other object to compare for equality
        :type other: Node
        :return: True if the given other object is also a node with the same name
        :rtype: bool
        """
        if not isinstance(other, Node):
            return False

        return self.name == other.name

    def __hash__(self):
        """
        Hash code computation based on node name.

        :return: hash code
        :rtype: int
        """
        hash_ = 3
        return 53 * hash_ + hash(self.name)

    def __repr__(self):
        return f"Node({repr(self.name)})"

class Edge(AnnotatedObject):
    """Represents an edge in a graph. The edge can be directed or undirected. It is assumed that for directed edges, the first node is the source node and the second node is the destination node. For undirected edges it does not mean anything whether a node is the first or second node.
    Edges may have a weight but they are not required to. Besides the weight, an unlimited number of additional annotations can also be added to any edge as (key,value) pairs.
    This class is not intended to be directly instantiated. Explicit directed or undirected edges can be created using one of the constructors of DirectedEdge or UnDirectedEdge"""

    def __init__(self, node1, node2, weight = None):
        """
        Create an edge

        :param node1: first node (source for directed edges)
        :type node1: Node
        :param node2: second node (destination for directed edges)
        :type: node2: Node
        :param weight: associated weight (None for unweighted edges)
        :type weight: float
        """
        super().__init__()
        self.__node1 = node1
        self.__node2 = node2
        self.weight = weight

    @property
    def node1(self):
        """
        Get first node. In case of a directed edge, this node is assumed to be the source node.

        :return: first node
        :rtype: Node
        """
        return self.__node1

    @property
    def node2(self):
        """
        Get second node. In case of a directed edge, this node is assumed to be the destination node.

        :return: second node
        :rtype: Node
        """
        return self.__node2

    def get_nodes(self):
        """
        Get a list containing both nodes (arbitrary order).

        :return: list containing both nodes
        :rtype: list(Node)
        """
        return [self.__node1, self.__node2]

    def contains(self, node):
        """
        Check whether this edge contains the given node.

        :param node: node
        :type node: Node
        :return: True if n is one of both nodes of this edge
        :rtype: bool
        """
        return node == self.__node1 or node == self.__node2

class DirectedEdge(Edge):
    """Represents a directed edge. This type of edges can be added to a directed graph. An edge (a,b) is not equal to a corresponding edge (b,a)."""

    def __init__(self, *args, **kwargs):
        """
        Create a directed edge from a source to a destination node with given weight. See constructor of Edge.
        """
        super().__init__(*args, **kwargs)

    def is_directed(self):
        """
        Always returns true as this is a directed edge.

        :return: True
        :rtype: bool
        """
        return True

    def get_source(self):
        """
        Get the source node of this edge.

        :return: source node
        :rtype: Node
        """
        return self.node1

    def get_destination(self):
        """
        Get the destination node of this edge.

        :return: destination node
        :rtype: Node
        """
        return self.node2

    def __str__(self):
        """
        Create a string representation of the directed edge, formatted as (source,destination).

        :return: string representation
        :rtype: str
        """
        return f"({self.get_source()}, {self.get_destination()})"

class UndirectedEdge(Edge):
    """Represents an undirected edge. This type of edges can be added to a undirected graph. Edges {a,b} and {b,a} are equal."""

    def __init__(self, *args, **kwargs):
        """
        Create an undirected edge from a source to a destination node with given weight. See constructor of Edge.
        """
        super().__init__(*args, **kwargs)

    def is_directed(self):
        """
        Always returns False as this is an undirected edge.

        :return: False
        :rtype: bool
        """
        return False

    def __str__(self):
        """
        Create a string representation of the undirected edge, formatted as {a,b}.

        :return: string representation
        :rtype: str
        """
        return f'{{{self.node1}, {self.node2}}}'

class Graph:

    def __init__(self):
        self.nodes = set()
        self.outgoing = dict()
        self.incoming = dict()

    def contains_node(self, node):
        """
        Check whether a specific node is contained in the graph.

        :param node: node
        :type node: Node
        :return: True if the given node is contained in the graph
        :rtype: bool
        """
        return node in self.nodes

    def get_node_from_name(self, name):
        """
        Get a graph node based on its name. If the graph does not contain any node with this name, None is returned.

        :param name: node name
        :return: the graph node with the given name; None if the graph does not contain a node with this name
        :rtype Node
        """
        nodes = [node for node in self.nodes if node.name == name]
        return nodes[0] if len(nodes) > 0 else None

    def add_node(self, node):
        """
        Add a node to the graph. If a node with the same name is already contained in the graph, calling this method does not have any effect and False is returned.

        :param node: node to add to the graph
        :type node: Node
        :return: True if the node was successfully added
        :rtype: bool
        """
        assert node is not None, "Can not add null node."
        if not isinstance(node, Node):
            node = Node(node)

        if self.contains_node(node):
            return None

        self.nodes.add(node)
        self.outgoing[node] = dict()
        self.incoming[node] = dict()

        return node

    def remove_node(self, node):
        """
        Remove a node from the graph. All incident edges are also removed. If the given node is not contained in the graph False is returned and calling this method does not have any effect.

        :param node: node to be removed
        :type node: Node
        :return: True if the node has been successfully removed
        :rtype: bool
        """
        if not isinstance(node, Node):
            assert node in self.nodes, 'unknown node'

        if not self.contains_node(node):
            return False

        self.nodes.remove(node)
        for neighbour in self.outgoing[node]:
            del self.incoming[neighbour][node]
        for neighbour in self.incoming[node]:
            del self.outgoing[neighbour][node]

        del self.outgoing[node]
        del self.incoming[node]

        return True

    def get_all_nodes(self):
        """
        Get all nodes contained in the graph.

        :return: list of all graph nodes
        :rtype: list(Node)
        """
        return self.nodes

    def num_nodes(self):
        """
        Get the number of nodes (order) of the graph.

        :return: number of nodes
        :rtype: int
        """
        return len(self.nodes)

    def contains_edge(self, edge):
        """
        Check whether the graph contains a given edge.

        :param edge: edge
        :type edge: Edge
        :return: True if the given edge is contained in the graph
        :rtype: bool
        """
        if edge is None or edge.node1 not in self.outgoing:
            return False

        edges = self.outgoing[edge.node1]
        return edge.node2 in edges and edge in edges[edge.node2]

    def add_edge(self, edge):
        assert edge is not None, 'Edge cannot be None'
        assert self.contains_node(edge.node1), f'Node {edge.node1} does not exist'
        assert self.contains_node(edge.node2), f'Node {edge.node2} does not exist'

        if edge.node2 not in self.outgoing[edge.node1]:
            self.outgoing[edge.node1][edge.node2] = set()
        self.outgoing[edge.node1][edge.node2].add(edge)
        if edge.node1 not in self.incoming[edge.node2]:
            self.incoming[edge.node2][edge.node1] = set()
        self.incoming[edge.node2][edge.node1].add(edge)

        if not edge.is_directed():
            if edge.node1 not in self.outgoing[edge.node2]:
                self.outgoing[edge.node2][edge.node1] = set()
            self.outgoing[edge.node2][edge.node1].add(edge)
            if edge.node2 not in self.incoming[edge.node1]:
                self.incoming[edge.node1][edge.node2] = set()
            self.incoming[edge.node1][edge.node2].add(edge)

        return True

    def get_edges(self, sourcenode, destnode):
        if not self.contains_node(sourcenode):
            return set()

        out = self.outgoing[sourcenode]
        if destnode not in out:
            return set()

        return out[destnode]

    def contains_edge_between(self, sourcenode, destnode):
        """
        Check whether there is an edge from the given source node to the given destination node.

        :param sourcenode: source node
        :type sourcenode: Node
        :param destnode: destination node
        :type destnode: Node
        :return: True if both nodes are contained in the graph, with an edge between them
        :rtype: bool
        """
        return len(self.get_edges(sourcenode, destnode)) != 0

    def remove_edge(self, edge):
        """
        Remove an edge from the graph. If the edge is not present or either the source or destination nodes are not contained in the graph, False is returned and calling this method does not have any effect.

        :param edge: edge to be removed
        :type edge: Edge
        :return: True if the edge has been successfully removed
        :rtype: bool
        """
        if not self.contains_edge(edge):
            return False

        self.outgoing[edge.node1][edge.node2].remove(edge)
        self.incoming[edge.node2][edge.node1].remove(edge)

        if not edge.is_directed():
            self.incoming[edge.node1][edge.node2].remove(edge)
            self.outgoing[edge.node2][edge.node1].remove(edge)

        return True

    def remove_edge_between(self, sourcenode, destnode):
        """
        Remove the edge from the given source node to the given destination node. If such edge is not present or either the source or destination nodes are not contained in the graph, None is returned and calling this method does not have any effect. Else, the removed edge is returned.

        :param sourcenode: source node
        :type sourcenode: Node
        :param destnode: destination node
        :type destnode: Node
        :return: removed edge if it was present; else None
        :rtype: Edge
        """
        edges = list(self.get_edges(sourcenode, destnode))
        if not edges:
            return None

        edge = edges[0]
        self.remove_edge(edge)

        return edge

    def get_all_edges(self):
        """
        Get a list containing all edges from the graph.

        :return: list of all edges
        :rtype: list(Edge)
        """
        result = set()
        for node1 in self.outgoing:
            for node2 in self.outgoing[node1]:
                result |= self.outgoing[node1][node2]
        return result

    def num_edges(self):
        """
        Get the number of edges (size) of the graph.

        :return: number of edges
        :rtype: int
        """
        return len(self.get_all_edges())

    def get_neighbours(self, node):
        """
        Get all neighbours of a given node n. A node m is defined to be a neighbour of n if there is an edge from n to m.

        :param node: given node
        :type node: Node
        :return: list of neighbours of n
        :rtype: list(Node)
        """
        assert node in self.nodes, f'Node {node} not found in graph.'
        return {neighbour for neighbour in self.outgoing[node] if len(self.outgoing[node][neighbour]) != 0}

    def get_outgoing_edges(self, node):
        """
        Get a list of outgoing edges from a given node n.

        :param node: given node
        :type node: Node
        :return: list of outgoing edges
        :rtype: list(Edge)
        """
        assert node in self.nodes, f'Node {node} not found in graph.'
        result = set()
        for neighbour in self.outgoing[node]:
            result |= self.outgoing[node][neighbour]

        return result

    def get_out_degree(self, node):
        """
        Get the out degree of a node in the graph. The out degree corresponds to the number of outgoing edges.

        :param node: node
        :type node: Node
        :return: out degree of the given node
        :rtype: int
        """
        return len(self.get_outgoing_edges(node))

    def get_incoming_edges(self, node):
        """
        Get a list of incoming edges in a given node n.

        :param node: given node
        :type node: Node
        :return: list of incoming edges
        :rtype: list(Edge)
        """
        assert node in self.nodes, f'Node {node} not found in graph.'
        result = set()
        for neighbour in self.incoming[node]:
            result |= self.incoming[node][neighbour]
        return result

    def get_in_degree(self, node):
        """
        Get the in degree of a node in the graph. The in degree corresponds to the number of incoming edges.

        :param node: node
        :type node: Node
        :return: in degree of the given node
        :rtype: int
        """
        return len(self.get_incoming_edges(node))

class SimpleGraph(Graph):

    def __init__(self):
        super().__init__()

    def add_edge(self, edge):
        """
        Add an edge to the graph. The nodes of the edge should already be present in the graph, else an assertion is thrown. If the graph already contains an edge with the same source and destination, calling this method does not have any effect and False is returned.

        :param edge: edge to be added to the graph
        :type edge: Edge
        :return: True if the edge is successfully added
        :rtype: bool
        """
        assert edge is not None, "Edge can not be none."
        if self.contains_edge_between(edge.node1, edge.node2):
            return False
        super().add_edge(edge)

    def get_edge_between(self, source, dest):
        """
        Get the edge that goes from the given source node to the given destination node, if any.

        :param source: source node
        :type source: Node
        :param dest: destination node
        :type dest: Node
        :return: the edge between the given nodes, if both nodes are contained in the graph and connected with an edge in the given direction; else None is returned
        :rtype: Edge
        """
        edges = list(super().get_edges(source, dest))
        return None if len(edges) == 0 else edges[0]

class DirectedGraph(SimpleGraph):
    """Represents a directed graph."""

    def __init__(self, graph = None):
        """
        Copy constructor. Creates a copy of the given directed graph. All nodes and edges (including weights) are copied. Assigned annotations, if any, are not copied to the new graph.

        :param graph: directed graph to copy, when None an empty directed graph will be created
        :type graph: DirectedGraph
        """
        super().__init__()

        if isinstance(graph, DirectedGraph):
            mapping = dict()
            for node in graph.get_all_nodes():
                newnode = Node(node.name)
                super().add_node(newnode)
                mapping[node] = newnode

            for edge in graph.get_all_edges():
                node1 = mapping[edge.node1]
                node2 = mapping[edge.node2]
                copy = DirectedEdge(node1, node2, edge.weight)
                super().add_edge(copy)

    def add_edge_between(self, source, destination):
        """
        Adds an edge from the given source to destination node. Both nodes should already be contained in the graph, else an assertion is thrown. If an edge is already present from the given source to destination node, None is returned and the graph is not modified, else the newly added edge is returned.

        :param source: source node
        :type source: Node
        :param destination: destination node
        :type destination: Node
        :return: added edge, None if edge between nodes already present
        :rtype: DirectedEdge
        """
        if super().contains_edge_between(source, destination):
            return None

        edge = DirectedEdge(source, destination)
        super().add_edge(edge)
        return edge

class UnDirectedGraph(SimpleGraph):

    def __init__(self, graph = None):
        """
        Copy constructor. Creates a copy of the given undirected graph. All nodes and edges (including weights) are copied. Assigned annotations, if any, are not copied to the new graph.

        :param graph: undirected graph to copy, when None an empty undirected graph will be created
        :type graph: UnDirectedGraph
        """
        super().__init__()

        if isinstance(graph, UnDirectedGraph):
            mapping = dict()
            for node in graph.get_all_nodes():
                newnode = Node(node.name)
                super().add_node(newnode)
                mapping[node] = newnode

            for edge in graph.get_all_edges():
                node1 = mapping[edge.node1]
                node2 = mapping[edge.node2]
                copy = UndirectedEdge(node1, node2, edge.weight)
                super().add_edge(copy)

    def add_edge_between(self, source, destination):
        """
        Adds an edge from the given source to destination node. Both nodes should already be contained in the graph, else an assertion is thrown. If an edge is already present from the given source to destination node, None is returned and the graph is not modified, else the newly added edge is returned.

        :param source: source node
        :type source: Node
        :param destination: destination node
        :type destination: Node
        :return: added edge, None if edge between nodes already present
        :rtype: UnDirectedEdge
        """
        if super().contains_edge_between(source, destination) or super().contains_edge_between(destination, source):
            return None

        edge = UndirectedEdge(source, destination)
        super().add_edge(edge)
        return edge

    def get_incident_edges(self, node):
        """
        Get the list of incident edges of a given node n.

        :param node: given node
        :type node: Node
        :return: list of incident edges
        :rtype: list(UnDirectedEdge)
        """
        return super().get_outgoing_edges(node)

    def get_degree(self, node):
        """
        Get the degree of a node in the graph. The degree corresponds to the number of incident edges.

        :param node: node
        :type node: Node
        :return: degree of the given node
        :rtype: int
        """
        return super().get_out_degree(node)

class DirectedMultiGraph(Graph):

    def __init__(self, graph = None):
        """
        Copy constructor. Creates a copy of the given directed multigraph. All nodes and edges (including weights) are copied. Assigned annotations, if any, are not copied to the new graph.

        :param graph: directed multigraph to copy, when None an empty directed multigraph will be created
        :type graph: DirectedMultiGraph
        """
        super().__init__()
        if isinstance(graph, DirectedMultiGraph):
            mapping = dict()
            for node in graph.get_all_nodes():
                newnode = Node(node.name)
                super().add_node(newnode)
                mapping[node] = newnode

            for edge in graph.get_all_edges():
                node1 = mapping[edge.node1]
                node2 = mapping[edge.node2]
                copy = DirectedEdge(node1, node2, edge.weight)
                super().add_edge(copy)

    def add_edge_between(self, source, destination):
        """
       Adds an edge from the given source to destination node. Both nodes should already be contained in the graph, else an assertion is thrown. The newly added edge is returned.

       :param source: source node
       :type source: Node
       :param destination: destination node
       :type destination: Node
       :return: added edge, None if edge between nodes already present
       :rtype: DirectedEdge
       """
        edge = DirectedEdge(source, destination)
        super().add_edge(edge)
        return edge

class UndirectedMultiGraph(Graph):

     def __init__(self, graph = None):
        """
        Copy constructor. Creates a copy of the given undirected multigraph. All nodes and edges (including weights) are copied. Assigned annotations, if any, are not copied to the new graph.

        :param graph: undirected multigraph to copy, when None an empty undirected multigraph will be created
        :type graph: UndirectedMultiGraph
        """
        super().__init__()
        if isinstance(graph, UndirectedMultiGraph):
            mapping = dict()
            for node in graph.get_all_nodes():
                newnode = Node(node.name)
                super().add_node(newnode)
                mapping[node] = newnode

            for edge in graph.get_all_edges():
                node1 = mapping[edge.node1]
                node2 = mapping[edge.node2]
                copy = UndirectedEdge(node1, node2, edge.weight)
                super().add_edge(copy)

        def add_edge_between(self, source, destination):
            """
            Adds an edge from the given source to destination node. Both nodes should already be contained in the graph, else an assertion is thrown. The newly added edge is returned.

            :param source: source node
            :type source: Node
            :param destination: destination node
            :type destination: Node
            :return: added edge, None if edge between nodes already present
            :rtype: UnDirectedEdge
            """
            edge = UndirectedEdge(source, destination)
            super().add_edge(edge)
            return edge

        def get_incident_edges(self, node):
            """
            Get the list of incident edges of a given node n.

            :param node: given node
            :type node: Node
            :return: list of incident edges
            :rtype: list(UndirectedEdge)
            """
            return super().get_outgoing_edges(node)

        def get_degree(self, node):
            """
            Get the degree of a node in the graph. The degree corresponds to the number of incident edges.

            :param node: node
            :type node: Node
            :return: degree of the given node
            :rtype: int
            """
            return super().get_out_degree(node)


class WalkNode:

    def __init__(self, node):
        """
        Creates a single node to use in a walk

        :param node: the node belonging to the walknode
        :type node: Node
        """
        self.content = node
        self.next = None
        self.previous = None


class Walk:

    def __init__(self, nodes = None):
        """
        Creates a new walk

        :param nodes: when None, the walk will be empty, otherwise it will consist of these nodes
        :type nodes: list
        """
        if nodes is None:
            self.head = None
            self.tail = None
            self.length = 0
        else:
            assert isinstance(nodes, list), f"expected list or None, got {type(nodes)}"
            
            if all(isinstance(node, Node) for node in nodes):
                walknodes = [WalkNode(node) for node in nodes]
            else:
                walknodes = [WalkNode(Node(node)) for node in nodes]

            self.head = walknodes[0]
            self.tail = walknodes[-1]
            self.length = len(walknodes)

            for index in range(0, len(nodes)):
                if index > 0:
                    walknodes[index-1].next = walknodes[index]
                if index < len(nodes) - 1:
                    walknodes[index+1].previous = walknodes[index]
           
    def __repr__(self):
        contents = [node for node in self.get_all_nodes()]
        return f"Walk({contents!r})"

    def get_all_nodes(self):
        """
        Returns all nodes part of this walk.

        :rtype: list
        """
        result = []
        current = self.head
        while current is not None:
            result.append(current.content)
            current = current.next
        return result

    def prepend(self, node):
        """
        Prepends a node to a walk

        :param node: the node to prepend
        :type node: Node
        """
        walknode = WalkNode(node)
        walknode.next = self.head
        if self.head is not None:
            self.head.previous = walknode
            self.head = walknode
        else:
            self.head = self.tail = walknode
        self.length += 1

    def append(self, node):
         """
        Appends a node to a walk

        :param node: the node to append
        :type node: Node
        """
        walknode = WalkNode(node)
        walknode.previous = self.tail
        if self.tail is not None:
            self.tail.next = walknode
            self.tail = walknode
        else:
            self.head = self.tail = walknode
        self.length += 1

    def insert_in_walk(self, walk, after):
        before = after.next
        after.next = walk.head
        walk.head.previous = after
        if before is not None:
            before.previous = walk.tail
        walk.tail.next = before

    def insert_at(self, node, index):
        assert 0 <= index <= self.length, f"index {index} does not exist"

        cindex = 0
        previous_node, next_node = None, self.head
        while index < cindex:
            previous_node, next_node = next_node, next_node.next
            cindex += 1

        walk = Walk([node])
        self.insert_in_walk(walk, previous_node, next_node)
        length += 1

    def insert(self, after, walk):
        """
        Extend the walk

        :param after: the node after which we will extend
        :type after: Node
        :param walk: the walk that will be inserted
        :type walk: Walk
        """
        walknode = self.head
        while walknode is not None and walknode.content != after:
            walknode = walknode.next
        if walknode is not None:
            self.insert_in_walk(walk, walknode)

def fill_graph(graph, data, weights = None):
    nodes = dict()
    for key in data:
        node = Node(key)
        nodes[key] = node
        graph.add_node(node)

    for node in data:
        for neighbour in data[node]:
            graph.add_edge_between(nodes[node], nodes[neighbour])

    if weights is not None:
        set_weights(graph, weights)

    return graph


def set_weights(graph, weights):
    for edge in weights:
        source, dest = [graph.get_node_from_name(nodename) for nodename in edge]
        weight = weights[edge]
        for edge in graph.get_edges(source, dest):
            edge.weight = weight

def directed_graph_from_dict(data, weights = None):
    """
    Creates a directed graph from a dictionary. The keys of the dictionary correspond to the nodes of the graph and the value for a key correspond to the incident nodes of the node that key represents
    :param data: the dictionary containing the neighbour information
    :type data: dict
    :param weights: the weights for each edge
    :type weights: dict
    :return: the corresponding undirected graph
    :rtype: DirectedGraph
    """
    result = DirectedGraph()
    return fill_graph(result, data, weights = weights)

def directed_multigraph_from_dict(data, weights = None):
    """
    Creates a directed multigraph from a dictionary. The keys of the dictionary correspond to the nodes of the graph and the value for a key correspond to the incident nodes of the node that key represents
    :param data: the dictionary containing the neighbour information
    :type data: dict
    :param weights: the weights for each edge
    :type weights: dict
    :return: the corresponding undirected graph
    :rtype: DirectedMultiGraph
    """
    result = DirectedMultiGraph()
    return fill_graph(result, data, weights = weights)


def undirected_graph_from_dict(data, weights = None):
    """
    Creates an undirected graph from a dictionary. The keys of the dictionary correspond to the nodes of the graph and the value for a key correspond to the incident nodes of the node that key represents
    :param data: the dictionary containing the neighbour information
    :type data: dict
    :param weights: the weights for each edge
    :type weights: dict
    :return: the corresponding undirected graph
    :rtype: UnDirectedGraph
    """
    result = UnDirectedGraph()
    return fill_graph(result, data, weights = weights)

def undirected_multigraph_from_dict(data, weights = None):
    """
    Creates an undirected multigraph from a dictionary. The keys of the dictionary correspond to the nodes of the graph and the value for a key correspond to the incident nodes of the node that key represents
    :param data: the dictionary containing the neighbour information
    :type data: dict
    :param weights: the weights for each edge
    :type weights: dict
    :return: the corresponding undirected graph
    :rtype: UnDirectedMultiGraph
    """
    result = UnDirectedMultiGraph()
    return fill_graph(result, data, weights = weights)
