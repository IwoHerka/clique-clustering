from __future__ import print_function

import networkx as nx


class Status:
    def __init__(self):
        self.com2nodes = {}
        self.internals = {}
        self.node2com = {}
        self.degrees = {}
        self.n_edges = 0

    def init(self, graph, part=None):
        self.n_edges = graph.size()
        self.internals = {}
        self.com2nodes = {}
        self.node2com = {}
        self.com_mods = {}
        self.degrees = {}

        count = 0

        for node in graph.nodes():
            self.node2com[node] = count

            if not count in self.com2nodes:
                self.com2nodes[count] = set()
                self.com_mods[count] = 0

            self.com2nodes[count].add(node)

            deg = float(graph.degree(node))

            if deg < 0:
                error = "Bad graph type ({})".format(type(graph))
                raise ValueError(error)

            self.degrees[count] = deg
            self.internals[count] = 0
            count += 1


class State:
    def __init__(self):
        self.com_t = None
        self.com_s = None
        self.internals_t = None
        self.internals_s = None
        self.degrees_t = None
        self.degrees_s = None
        self.mod_s = None
        self.mod_t = None
        self.nodes_s = None
        self.nodes_t = None
        self.moved = []

    def reverse(self, status):
        status.internals[self.com_t] = self.internals_t
        status.internals[self.com_s] = self.internals_s
        status.degrees[self.com_t] = self.degrees_t
        status.degrees[self.com_s] = self.degrees_s
        status.com_mods[self.com_s] = self.mod_s
        status.com_mods[self.com_t] = self.mod_t
        status.com2nodes[self.com_t] = self.nodes_t
        status.com2nodes[self.com_s] = self.nodes_s

        for v in self.moved:
            status.node2com[v] = self.com_s


def merge_coms(l_comA, l_comB, G, status, state=None):
    """
    Merge communities.
    """
    if l_comA == l_comB:
        return l_comA

    comA = status.com2nodes[l_comA]
    comB = status.com2nodes[l_comB]

    if len(comA) > len(comB):
        target = comA
        t_label = l_comA
        source = comB
        s_label = l_comB
    else:
        target = comB
        t_label = l_comB
        source = comA
        s_label = l_comA

    if state:
        state.com_t = t_label
        state.com_s = s_label
        state.internals_s = status.internals[s_label]
        state.internals_t = status.internals[t_label]
        state.degrees_s = status.degrees[s_label]
        state.degrees_t = status.degrees[t_label]
        state.mod_s = status.com_mods[s_label]
        state.mod_t = status.com_mods[t_label]
        state.nodes_s = status.com2nodes[s_label].copy()
        state.nodes_t = status.com2nodes[t_label].copy()

    diff = source - target

    for v in diff:
        degree = G.degree(v)
        in_degree = 0

        for n in G.neighbors(v):
            in_degree += 1 if status.node2com[n] == t_label else 0

        status.internals[t_label] += in_degree
        status.degrees[t_label] += degree
        status.node2com[v] = t_label
        status.com2nodes[t_label].add(v)

        if state:
            state.moved.append(v)

    del status.internals[s_label]
    del status.degrees[s_label]
    del status.com2nodes[s_label]
    del status.com_mods[s_label]

    return t_label


def cliq2com(G, clique, status):
    '''
       Merge clique into community.
       This method takes set of points and merges them
       into community, updating status along the way.
       -----------------------------------------------
       Parmeters:
         [clique]: set of vertices
         [G]: NetworkX's DiGraph
         [status]: graph's Status
    '''

    communities = list(set([status.node2com[v] for v in clique]))
    last = communities[0]

    for com in communities:
        last = merge_coms(last, com, G, status)

    return last


def modularity(status, changed=None):
    '''
        (Re)calculate modularity.
    '''

    if not changed:
        changed = set(status.node2com.values())

    links = float(status.n_edges)
    result = 0.

    for community in changed:
        degree = status.degrees.get(community, 0.)
        in_degree = status.internals.get(community, 0.)
        status.com_mods[community] = in_degree / links - ((degree / (2. * links)) ** 2)

    return sum(status.com_mods.values())


def cluster(G):
    max_mod = -1
    touched = set()
    status = Status()
    status.init(G)

    polys = [frozenset(c) for c in nx.find_cliques(G) if len(c) > 2]
    polys.sort(key=lambda p: -len(p))

    print('Phase 1... {} cliques'.format(len(polys)))

    for p in polys:
        inter = 0

        for v in p:
            inter += 1 if v in touched else 0

        if len(p) - inter + 1 < 3:
            continue

        touched = touched.union(p)

        new_com = cliq2com(G, p, status)
        new_mod = modularity(status, [new_com])

        if new_mod > max_mod:
            max_mod = new_mod
            status = status
        else:
            continue

    merged = set()
    visited_pairs = set()
    coms = set(status.node2com.values())

    print('Phase 2... {} communities'.format(len(coms)))

    for com in coms:
        if com in merged:
            continue

        for com_ in coms:
            if com == com_ or com_ in merged or frozenset([com, com_]) in visited_pairs:
                continue

            visited_pairs.add(frozenset([com, com_]))

            state = State()
            new_com = merge_coms(com, com_, G, status, state)
            new_mod = modularity(status, [new_com])

            if new_mod > max_mod:
                max_mod = new_mod
                merged.add(com + com_ - new_com)
                break
            else:
                state.reverse(status)

    print('Final modularity: {}'.format(modularity(status, 0)))
    return status.node2com
