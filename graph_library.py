class AnnotatedObject:

    def __init__(self):
        self.annotations = dict()

    def set_annotation(self, key, value):
        self.annotations[key] = value

    def get_annotation(self, key):
        return self.annotations[key] if key in self.annotations else None

    def remove_annotation(self, key):
        if key not in self.annotations:
            return False
        del self.annotations[key]
        return True

    def has_annotation(self):
        return len(self.annotations) != 0

    def num_annotations(self):
        return len(self.annotations)

    def get_annotations(self):
        return self.annotations

class Node(AnnotatedObject):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"{self.name}{' ' + self.get_annotations() if self.has_annotation() else ''}"

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False

        return self.name == other.name

    def __hash__(self):
        hash_ = 3
        return 53 * hash_ + hash(self.name)

    def __repr__(self):
        return f"Node({repr(self.name)})"

class Edge(AnnotatedObject):

    def __init__(self, node1, node2, weight = None):
        super().__init__()
        self.__node1 = node1
        self.__node2 = node2
        self.weight = weight

    @property
    def node1(self):
        return self.__node1

    @property
    def node2(self):
        return self.__node2

    def get_nodes(self):
        return [self.__node1, self.__node2]

    def contains(self, node):
        return node == self.__node1 or node == self.__node2

class DirectedEdge(Edge):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_directed(self):
        return True

    def get_source(self):
        return self.node1

    def get_destination(self):
        return self.node2

    def __str__(self):
        return f"({self.get_source()}, {self.get_destination()})"

class UndirectedEdge(Edge):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_directed(self):
        return False

    def __str__(self):
        return f'{{{self.node1}, {self.node2}}}'

class Graph:

    def __init__(self):
        self.nodes = set()
        self.outgoing = dict()
        self.incoming = dict()

    def contains_node(self, node):
        return node in self.nodes

    def get_node_from_name(self, name):
        return [node for node in self.nodes if node.name == name][0]

    def add_node(self, node):
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
        return self.nodes

    def num_nodes(self):
        return len(self.nodes)

    def contains_edge(self, edge):
        if edge is None or edge.node1 not in self.outgoing:
            return False

        edges = self.outgoing[edge.node1]
        return edge.node2 in edges and edge in edges[edge.node2]

    def add_edge(self, edge):
        assert edge is not None, 'Edge cannot be None'
        assert self.contains_node(edge.node1), f'Node {edge.node1} does not exist'
        assert self.contains_node(edge.node2), f'Node {edge.node2} does not exist'

        if self.contains_edge(edge):
            return False

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
        return len(self.get_edges(sourcenode, destnode)) != 0

    def remove_edge(self, edge):
        if not self.contains_edge(edge):
            return False

        self.outgoing[edge.node1][edge.node2].remove(edge)
        self.incoming[edge.node2][edge.node1].remove(edge)

        if not edge.is_directed():
            self.incoming[edge.node1][edge.node2].remove(edge)
            self.outgoing[edge.node2][edge.node1].remove(edge)

        return True

    def remove_edge_between(self, sourcenode, destnode):
        edges = list(self.get_edges(sourcenode, destnode))
        if not edges:
            return None

        edge = edges[0]
        self.remove_edge(edge)

        return edge

    def get_all_edges(self):
        result = set()
        for node1 in self.outgoing:
            for node2 in self.outgoing[node1]:
                result |= self.outgoing[node1][node2]
        return result

    def num_edges(self):
        return len(self.get_all_edges())

    def get_neighbours(self, node):
        assert node in self.nodes, f'Node {node} not found in graph.'
        return {neighbour for neighbour in self.outgoing[node] if len(self.outgoing[node][neighbour]) != 0}

    def get_outgoing_edges(self, node):
        assert node in self.nodes, f'Node {node} not found in graph.'
        result = set()
        for neighbour in self.outgoing[node]:
            result |= self.outgoing[node][neighbour]

        return result

    def get_out_degree(self, node):
        return len(self.get_outgoing_edges())

    def get_incoming_edges(self, node):
        assert node in self.nodes, f'Node {node} not found in graph.'
        result = set()
        for neighbour in self.incoming[node]:
            result |= self.incoming[node][neighbour]
        return result

    def get_in_degree(self, node):
        return len(self.get_incoming_edges(node))

class SimpleGraph(Graph):

    def __init__(self):
        super().__init__()

    def add_edge(self, edge):
        assert edge is not None, "Edge can not be none."
        if self.contains_edge_between(edge.node1, edge.node2):
            return False
        super().add_edge(edge)

    def get_edge(self, source, dest):
        edges = list(super().get_edges(source, dest))
        return None if len(edges) == 0 else edges[0]

class DirectedGraph(SimpleGraph):

    def __init__(self, graph = None):
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
        if super().contains_edge_between(source, destination):
            return None

        edge = DirectedEdge(source, destination)
        super().add_edge(edge)
        return edge

class UnDirectedGraph(SimpleGraph):

    def __init__(self, graph = None):
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
        if super().contains_edge_between(source, destination):
            return None

        edge = UndirectedEdge(source, destination)
        super().add_edge(edge)
        return edge

    def get_incident_edges(self, node):
        return super().get_outgoing_edges(node)

    def get_degree(self, node):
        return super().get_out_degree(node)

class DirectedMultiGraph(Graph):

    def __init__(self, graph = None):
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
        edge = DirectedEdge(source, destination)
        super().add_edge(edge)
        return edge

class UndirectedMultiGraph(Graph):

     def __init__(self, graph = None):
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
                copy = UnDirectedEdge(node1, node2, edge.weight)
                super().add_edge(copy)

        def add_edge_between(self, source, destination):
            edge = UndirectedEdge(source, destination)
            super().add_edge(edge)
            return edge

        def get_incident_edges(self, node):
            return super().get_outgoing_edges(node)

        def get_degree(self, node):
            return super().get_out_degree(node)

def set_weights(graph, weights):
    for edge in weights:
        source, dest = [graph.get_node_from_name(nodename) for nodename in edge]
        weight = weights[edge]
        for edge in graph.get_edges(source, dest):
            edge.weight = weight

def directed_graph_from_dict(data, weights = None):
    result = DirectedGraph()
    nodes = dict()
    for key in data:
        node = Node(key)
        nodes[key] = node
        result.add_node(node)

    for node in data:
        for neighbour in data[node]:
            result.add_edge_between(nodes[node], nodes[neighbour])

    if weights is not None:
        set_weights(result, weights)

    return result

def undirected_graph_from_dict(data, weights = None):
    result = UnDirectedGraph()
    nodes = dict()
    for key in data:
        node = Node(key)
        nodes[key] = node
        result.add_node(node)

    for node in data:
        for neighbour in data[node]:
            if not result.contains_edge_between(nodes[node], nodes[neighbour]):
                result.add_edge_between(nodes[node], nodes[neighbour])

    if weights is not None:
        set_weights(result, weights)

    return result
