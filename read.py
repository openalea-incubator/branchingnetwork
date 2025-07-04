import rsml
from openalea.mtg import traversal, algo

import networkx as nx
import numpy as np

import json
from networkx.readwrite import json_graph

from pathlib import Path

from matplotlib import cm, pyplot as plt

data = Path('data')/'UC1_HIRROS_arabidopsis'

fn = next(data.glob('*.rsml'))

def distance_polyline(p1, p2):
    """
    Compute the distance between two polylines.
    """
    p1 = np.array(p1)
    p2 = np.array([p2[0]])

    point_p2 = p2[0]
    distances = np.linalg.norm(p1 - point_p2, axis=1)
    # Index of the closest point in p1
    closest_index = np.argmin(distances)
    closest_point = p1[closest_index]
    # Distance to the closest point
    distance = np.linalg.norm(closest_point - point_p2)
    if distance > 20:
        print("Distance to the closest point ", distance)

    return closest_index 


# Be carefull, the diameter is not of the
def convert_fine_mtg(fn):
    # the conversion of the MTG is at the axis level, not at the segment level.
    g= rsml.rsml2mtg(fn)

    plants = g.vertices(scale=1)

    geometry = g.property('geometry')
    time = g.property('time')
    time_hours = g.property('time_hours')
    diameters = g.property('diameter')

    indexes = {}

    g2 = g.copy()
    for pid in plants:
        aid =  next(g.component_roots_iter(pid))
        for axis_id in traversal.pre_order2(g, vtx_id=aid):
            poly = geometry[axis_id]
            time_v = time[axis_id]
            time_hours_v = time_hours[axis_id]
            diams = diameters[axis_id]

            if g.parent(axis_id) is None:
                # create the axis at segment level
                vid = g2.add_component(complex_id=axis_id, label='Segment', 
                                      x=poly[0][0], y=poly[0][1], 
                                      time=time_v[0], 
                                      time_hours=time_hours_v[0],
                                      diameter= diams[0])
                indexes[axis_id] = [vid]
            else:
                # find the closest point in the parent axis
                parent_axis = g.parent(axis_id)
                parent_poly = geometry[parent_axis]
                closest_index = distance_polyline(parent_poly, poly)

                pid = indexes[parent_axis][closest_index]
                vid, complex_ = g2.add_child_and_complex(
                            parent=pid,
                            child=None,
                            complex=axis_id, 
                            edge_type=g.edge_type(axis_id),
                            label='Segment', 
                            x=poly[0][0], y=poly[0][1], 
                            time=time_v[0], 
                            time_hours=time_hours_v[0],
                            diameter= diams[0],
                            )
                indexes[axis_id] = [vid]

            for i, (x,y) in enumerate(poly[1:]):
                vid = g2.add_child(
                            parent=vid,
                            child=None,
                            edge_type='<',
                            label='Segment', 
                            x=x, y=y, 
                            time=time_v[i+1], 
                            time_hours=time_hours_v[i+1],
                            diameter= diams[i+1],
                            )
                indexes[axis_id].append(vid)
    return g2

def split(g):
    return algo.split(g)

def convert_nx(g):

    orders = algo.orders(g)
    g.properties()['root_deg'] = orders
    max_scale = g.max_scale()
    root_id = next(g.component_roots_at_scale_iter(g.root, scale=max_scale))

    root_coord =[g.node(root_id).x, g.node(root_id).y]

    edge_list = []
    nodes = list(traversal.pre_order2(g, vtx_id=root_id))
    for v in nodes:
        parent = g.parent(v)
        if parent is None:
            continue

        edge_list.append((parent, v))

    g_nx = nx.from_edgelist(edge_list, create_using=nx.DiGraph)

    props = ['x', 'y', 'time', 'time_hours', 'diameters', 'label', 'diameter', 'root_deg']
    for node in nodes:
        for prop in props:
            _prop = g.property(prop)
            if node in _prop:
                g_nx.nodes[node][prop] = _prop.get(node)

    # Adaptater to Ariadne 
    # Compute LR_index
    axis_root = g.complex(root_id)
    lr_index = dict((vid, i) for i, vid in enumerate(traversal.pre_order2(g, vtx_id=axis_root)))

    for node in nodes:
        g_nx.nodes[node]['LR_index'] = lr_index[g.complex(node)] if lr_index[g.complex(node)] else None

    for node in g_nx.nodes:
        x= g_nx.nodes[node]['x']-root_coord[0]
        y= g_nx.nodes[node]['y']-root_coord[1]
        g_nx.nodes[node]['pos'] = [x, y]
        
    tree_nx = nx.convert_node_labels_to_integers(g_nx)
    return tree_nx


def rsml2nx(fn):
    g = convert_fine_mtg(fn)

    gs = split(g)
    dgs = [convert_nx(g) for g in gs]
    return dgs

                
def test_all():
    """
    Test the conversion of the MTG to a fine MTG and then to a networkx graph.
    """
    g = convert_fine_mtg(fn)

    gs = split(g)
    dgs = [convert_nx(g) for g in gs]
    return dgs


def times(g):
    """
    Return the time property of the MTG.
    """
    _time =  g.property('time')

    _times = []
    for t in _time.values():
        if isinstance(t, list):
            _times.extend(t)
        else:
            _times.append(t)

    _times = set(_times)
    _times = sorted(_times)
    return list(_times)
                

def plot_mpl(g, ax=None, **kwargs):
    """
    Plot the MTG using matplotlib.
    """
    import matplotlib.pyplot as plt
  

    if ax is None:
        fig, ax = plt.subplots()

    edgelist = list(g.edges())
    nodelist = list(g.nodes())

    rotated_pos = {node: (attrs["pos"][0], -attrs["pos"][1]) for node, attrs in g.nodes(data=True)}
    colors = list(v for k, v in g.nodes(data='time'))
    
    fig = nx.draw_networkx(
        g,
        edgelist=edgelist,
        nodelist=nodelist,
        node_color=colors,
        edge_color=colors[1:],
        pos=rotated_pos,
        with_labels=False,
        width=1,
        node_size=5,
        arrows=False,
        ax=ax
    )

    plt.gca().set_aspect('equal')

    return fig

def save_json(g, fn):
    """
    Save the MTG to a JSON file.
    """

    data = json_graph.tree_data(g, root=0)
    with open(fn, 'w') as f:
        json.dump(data, f, indent=2)
    return True

