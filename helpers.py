import matplotlib.pyplot as plt
import networkx as nx


def relabel(dictionary):
    """
    Go through dictionary and rename all keys from 1 to N.
    """
    count = 0
    new_values = dict([])
    ret = dictionary.copy()

    for key in dictionary.keys():
        value = dictionary[key]
        new_value = new_values.get(value, -1)

        if new_value == -1:
            new_values[value] = count
            new_value = count
            count += 1

        ret[key] = new_value

    return ret


def draw(G, partition, pos=None):
    size = float(len(set(partition.values())))
    pos = pos if pos else nx.spring_layout(G)
    count = 0.

    for com in set(partition.values()):
        count += 1
        list_nodes = [v for v in partition.keys() if partition[v] == com]

        nx.draw_networkx_nodes(
            G,
            pos,
            list_nodes,
            node_size=20,
            node_color=plt.cm.jet(count / size)
        )

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()
