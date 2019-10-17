"""A dead-simple implementation of a graph data structure in Python."""


class DiGraph:
    """A simple directed graph data structure."""

    def __init__(self):
        self.adj = dict()

    def add_node(self, label):
        self.adj[label] = set()

    def add_edge(self, u_label, v_label):
        for x in {u_label, v_label}:
            if x not in self.adj:
                self.adj[x] = set()

        self.adj[u_label].add(v_label)

    def nodes(self):
        yield from self.adj.keys()

    def edges(self):
        for u, neighbors in self.adj.items():
            for v in neighbors:
                edge = frozenset((u, v))
                yield (u, v)

    def neighbors(self, u_label):
        for v in self.adj[u_label]:
            yield v

    def has_node(self, label):
        return label in self.adj

    def has_edge(self, u_label, v_label):
        return v_label in self.adj[u_label]


class Graph:
    """A simple graph data structure."""

    def __init__(self):
        self.adj = dict()

    def add_node(self, label):
        self.adj[label] = set()

    def add_edge(self, u_label, v_label):
        for x in {u_label, v_label}:
            if x not in self.adj:
                self.adj[x] = set()

        self.adj[u_label].add(v_label)
        self.adj[v_label].add(u_label)

    def nodes(self):
        yield from self.adj.keys()

    def edges(self):
        seen = set()

        for u, neighbors in self.adj.items():
            for v in neighbors:
                edge = frozenset((u, v))
                if edge not in seen:
                    seen.add(edge)
                    yield (u, v)
                else:
                    continue

    def neighbors(self, u_label):
        for v in self.adj[u_label]:
            yield v

    def has_node(self, label):
        return label in self.adj

    def has_edge(self, u_label, v_label):
        return v_label in self.adj[u_label]
