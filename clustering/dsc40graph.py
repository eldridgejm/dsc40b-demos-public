"""A dead-simple implementation of a graph data structure in Python."""


class _EdgeView:

    def __init__(self, adj, number_of_edges):
        self._adj = adj
        self._number_of_edges = number_of_edges

    def __contains__(self, edge):
        """Average case: Theta(1)"""
        u, v = edge
        try:
            return v in self._adj[u]
        except KeyError:
            return False

    def __len__(self):
        """Average case: Theta(1)"""
        return self._number_of_edges

    def __repr__(self):
        edgestr = ', '.join(f'({repr(u)}, {repr(v)})' for (u,v) in self)
        return f'EdgeView[{edgestr}]'


class _UndirectedEdgeView(_EdgeView):

    def __iter__(self):
        seen = set()

        for u, neighbors in self._adj.items():
            for v in neighbors:
                edge = frozenset((u, v))
                if edge not in seen:
                    seen.add(edge)
                    yield (u, v)
                else:
                    continue


class _DirectedEdgeView(_EdgeView):

    def __iter__(self):
        for u, neighbors in self._adj.items():
            for v in neighbors:
                yield (u, v)


class _Graph:

    def __init__(self, _edge_view_factory):
        self.adj = dict()
        self._number_of_edges = 0
        self._edge_view_factory = _edge_view_factory

    def add_node(self, label):
        """Average case: Theta(1)."""
        if label not in self.nodes:
            self.adj[label] = set()

    @property
    def nodes(self):
        return self.adj.keys()

    @property
    def edges(self):
        return self._edge_view_factory(self.adj, self._number_of_edges)


class UndirectedGraph(_Graph):

    def __init__(self, _edge_view_factory=_UndirectedEdgeView):
        super().__init__(_edge_view_factory)

    def add_edge(self, u_label, v_label):
        """Average case: Theta(1)."""
        if u_label == v_label:
            raise ValueError('Undirected graphs have no self loops.')

        for x in {u_label, v_label}:
            if x not in self.adj:
                self.adj[x] = set()

        if (u_label, v_label) not in self.edges:
            self.adj[u_label].add(v_label)
            self.adj[v_label].add(u_label)
            self._number_of_edges += 1

    def remove_edge(self, u_label, v_label):
        self.adj[u_label].remove(v_label)
        self.adj[v_label].remove(u_label)
        self._number_of_edges -= 1

    def remove_node(self, node):
        if node not in self.nodes:
            return

        for neighbor in self.adj[node]:
            self.adj[neighbor].discard(node)
            self._number_of_edges -= 1

        del self.adj[node]

    def neighbors(self, u_label, sort=False):
        neighbors = self.adj[u_label]
        if sort:
            return sorted(neighbors)
        else:
            return neighbors


class DirectedGraph(_Graph):

    def __init__(self, _edge_view_factory=_DirectedEdgeView):
        super().__init__(_edge_view_factory)
        self.back_adj = dict()

    def add_edge(self, u_label, v_label):
        """Average case: Theta(1)."""
        for x in {u_label, v_label}:
            if x not in self.adj:
                self.adj[x] = set()
            if x not in self.back_adj:
                self.back_adj[x] = set()

        self.adj[u_label].add(v_label)
        self.back_adj[v_label].add(u_label)
        self._number_of_edges += 1

    def remove_edge(self, u_label, v_label):
        self.adj[u_label].remove(v_label)
        self._number_of_edges -= 1

    def remove_node(self, node):
        if node not in self.nodes:
            return

        # in case there is a self-loop, since we can't modify set while iterating
        if node in self.back_adj[node]:
            self.adj[node].discard(node)
            self.back_adj[node].discard(node)
            self._number_of_edges -= 1

        for parent in self.back_adj[node]:
            self.adj[parent].discard(node)
            self._number_of_edges -= 1

        self._number_of_edges -= len(self.adj[node])
        del self.adj[node]

    def predecessors(self, node):
        return self.back_adj[node]

    def successors(self, node):
        return self.adj[node]

    def neighbors(self, node, sort=False):
        if sort:
            return sorted(self.successors(node))
        else:
            return self.successors(node)
