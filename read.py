from openalea.rsml import rsml2mtg
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
    g= rsml2mtg(fn)

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
            diams = diameters.get(axis_id, [])

            if g.parent(axis_id) is None:
                # create the axis at segment level
                vid = g2.add_component(complex_id=axis_id, label='Segment', 
                                      x=poly[0][0], y=poly[0][1], 
                                      time=time_v[0], 
                                      time_hours=time_hours_v[0],
                                      diameter= diams[0] if diams else 0.)
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
                            diameter= diams[0] if diams else 0.,
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
                            diameter= diams[i+1] if diams else 0.,
                            )
                indexes[axis_id].append(vid)
    return g2

def split(g):
    return algo.split(g)

def convert_nx(g):
    """ Ariadne Main  : 
    https://github.com/Salk-Harnessing-Plants-Initiative/Ariadne/blame/main/src/ariadne_roots/main.py#L807 
    """
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
    Plot the NetworkX using matplotlib.
    """
    import matplotlib.pyplot as plt
  

    if ax is None:
        fig, ax = plt.subplots()

    edgelist = list(g.edges())
    nodelist = list(g.nodes())

    rotated_pos = {node: (attrs["pos"][0], -attrs["pos"][1]) for node, attrs in g.nodes(data=True)}
    colors = list([v for k, v in g.nodes(data='time') if v is not None])
    
    fig = nx.draw_networkx(
        g,
        edgelist=edgelist,
        nodelist=nodelist,
        node_color=colors if colors else None,
        edge_color=colors[1:] if colors else None,
        pos=rotated_pos,
        with_labels=False,
        width=1,
        node_size=5,
        arrows=False,
        ax=ax
    )

    ax.set_aspect('equal')

    return fig

def plot_mpl_mtg(g, ax=None, **kwargs):
    """
    Plot the MTG using matplotlib.
    """
    import matplotlib.pyplot as plt
  

    if ax is None:
        fig, ax = plt.subplots()
    
    max_scale = g.max_scale()
    
    nodelist = list(g.vertices(scale=max_scale))
    edgelist = [(g.parent(nid), nid) for nid in nodelist if g.parent(nid)]

    pos = g.property('pos')
    rotated_pos = {vid: (pos[vid][0], -pos[vid][1]) for vid in nodelist}
    colors = None #list([v for k, v in g.nodes(data='time') if v is not None])

    g.is_directed = lambda : True
    g.is_multigraph  = lambda : False
    g.adj = dict( (vid, dict((cid,{}) for cid in cids)) for vid, cids in g._children.items())
    
    fig = nx.draw_networkx(
        g,
        edgelist=edgelist,
        nodelist=nodelist,
        node_color=colors if colors else None,
        edge_color=colors[1:] if colors else None,
        pos=rotated_pos,
        with_labels=False,
        width=1,
        node_size=5,
        arrows=False,
        ax=ax
    )

    ax.set_aspect('equal')

    return fig
def save_json(g, fn):
    """
    Save the MTG to a JSON file.
    """

    data = json_graph.adjacency_data(g)
    #data = json_graph.tree_data(g, root=0)
    with open(fn, 'w') as f:
        json.dump(data, f, indent=2)
    return True

def load_json(fn):
    """
    Load JSON file into a NX graph.
    """
    with open(fn) as f:
        data = json.load(f)
    
    g = json_graph.adjacency_graph(data)
    return g


def discretize_mtg(g_c, segment_length = 1.0e-4, resolution = 1.0e-4):
    # F. Bauget 2020-03-18 : RSML continuous from rsml2mtg()  to hydroroot disctrete copied from rsml
    # don't use parent node because rsml from other places don't have them but only coordinates of polylines
    """
    Convert MTG from continuous to discrete usable in HydroRoot

    Does the reverse of `discrete_to_continuous`:
      - Add a sequence of segments to all axes from their `geometry` attribute


    Based only on the coordinates of the polylines:
        - calculation of the euclidian distance between points of polylines then add the segment needed
        - to place a lateral on its parent axe, we calcul the distance between the 1st point of the lateral
          and the vertices of the parent axe and take the shortest distance to select the branshing vertex on the axe


    :params g_c: (MTG) - the continuous MTG to convert
    :params segment_length: (Float) - the segment length in meter (m)
    :params resolution: (float) - the resolution of the polylines coordinates, in polylines unit per meter (unit/m)
    :returns:
        - g discrete MTG

    Remark: At this stage (2022-08-22) only the root length and the branching position are used to simulate architecture
    in hydroponic solution. The exact position in 3D is not stored in the discrete MTG form.
    """

    # F. Bauget 2022-08-22 : changed int() to round() below to reduce difference between the root length of the MTG and
    #                       the RSML. This difference comes from the fact a constant vertex length is used

    geometry = g_c.property('geometry')

    _order = 0 # _order = 0 => 1st axe <=> primary root

    g = MTG()
    rid = seg = g.add_component(g.root)

    rnid = g.node(rid)
    rnid.base_length = 0.
    rnid.length = segment_length
    rnid.label = 'S'
    rnid.order = _order
    rnid.edge_type = '<'


    axe_segments = {}

    for axe in continuous.toporder(g_c, g_c.max_scale()):
        # get segment on parent branch
        p_axe = g_c.parent(axe)
        v = axe
        _order = 0
        while g_c.parent(v) is not None:
            v = g_c.parent(v)
            _order += 1


        if p_axe is not None:
            # parent axe
            pos_axe = np.array(geometry[p_axe])
            # vec_axe = np.diff(pos_axe,axis=0)**2
            # _length_axe = np.sqrt(np.sum(vec_axe, axis = 1))*resolution

        pos = np.array(geometry[axe])
        vec = np.diff(pos,axis=0)**2
        _length = np.sqrt(np.sum(vec, axis = 1)) * resolution


        if _order == 0:
            # primary root
            axe_segments[(axe, 0)] = seg # the first
            if _length[0] > 0.0:
                n = round(_length[0]/segment_length)
                if n == 0: n = 1
            for j in range(n):
                seg = g.add_child(seg, edge_type='<', label = 'S', length = segment_length, order = _order)

        else:
            min = 1.0e10
            for i, p in enumerate(pos_axe):
                # search for the smallest distance between each nodes of p_axe and the 1st node of the child
                distance = np.sqrt(np.sum((p-pos[0])**2.0))
                if distance < min:
                    min = distance
                elif i > 1:
                    break

            seg = axe_segments[(p_axe, i - 1)] # branching vertex on parent axe

            seg = g.add_child(seg, edge_type='+', label = 'S', length = segment_length, order = _order)
            if _length[0] > 0.0:
                n = round(_length[0]/segment_length)
                if n == 0: n = 1
            for j in range(n-1):
                seg = g.add_child(seg, edge_type='<', label = 'S', length = segment_length, order = _order)

        axe_segments[(axe, 1 )] = seg

        # create the other segments
        for i, l in enumerate(_length[1:]):
            if l > 0.0:
                n = round(l/segment_length)
                if n == 0: n = 1
            for j in range(int(n)):
                seg = g.add_child(seg, edge_type = '<', label = 'S', length = segment_length, order = _order)
            axe_segments[(axe, i + 2)] = seg


    return g