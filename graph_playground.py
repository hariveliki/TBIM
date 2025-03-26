import random

from topologicpy.Dictionary import Dictionary
from topologicpy.Graph import Graph
from topologicpy.Topology import Topology
from topologicpy.CellComplex import CellComplex
from topologicpy.Cluster import Cluster


def get_vertices_by_occupancy_type(graph, occupancy_type):
    result = []
    vertices = Graph.Vertices(graph)

    for vertex in vertices:
        vertex_dict = Topology.Dictionary(vertex)
        if vertex_dict:
            if ecolution:
                vertex_type = Dictionary.ValueAtKey(vertex_dict, "space_type")
            else:
                vertex_type = Dictionary.ValueAtKey(vertex_dict, "pr_OccupancyType")
            if not vertex_type:
                continue
            if occupancy_type in vertex_type:
                result.append(vertex)

    return result


def get_all_keys(vertex):
    vertex_dict = Topology.Dictionary(vertex)
    return Dictionary.Keys(vertex_dict)


def get_all_values(vertex):
    vertex_dict = Topology.Dictionary(vertex)
    return Dictionary.Values(vertex_dict)


def get_specific_value(vertex, key):
    vertex_dict = Topology.Dictionary(vertex)
    return Dictionary.ValueAtKey(vertex_dict, key)


def get_adjacent_vertices(graph, vertex):
    return Graph.AdjacentVertices(graph, vertex)


def query_space_property(graph, space_type, property_key):
    """
    Query properties of specific spaces in the graph
    Example: query_space_property(g, "Toilet", "pr_IsHeated")
    """
    results = []
    vertices = Graph.Vertices(graph)

    for vertex in vertices:
        vertex_dict = Topology.Dictionary(vertex)
        if vertex_dict:
            if ecolution:
                occupancy_type = Dictionary.ValueAtKey(vertex_dict, "space_type")
            else:
                occupancy_type = Dictionary.ValueAtKey(vertex_dict, "pr_OccupancyType")
            if not occupancy_type:
                continue
            if isinstance(occupancy_type, str):
                if space_type.lower() in occupancy_type.lower():
                    keys = Dictionary.Keys(vertex_dict)
                    if property_key in keys:
                        property_value = Dictionary.ValueAtKey(
                            vertex_dict, property_key
                        )
                        results.append(
                            {
                                "vertex": vertex,
                                "occupancy": occupancy_type,
                                "property": property_value,
                            }
                        )

                    # If property not found in vertex, check adjacent spaces
                    else:
                        adjacent_vertices = Graph.AdjacentVertices(graph, vertex)
                        for adj_vertex in adjacent_vertices:
                            adj_dict = Topology.Dictionary(adj_vertex)
                            if adj_dict:
                                adj_keys = Dictionary.Keys(adj_dict)
                                if property_key in adj_keys:
                                    property_value = Dictionary.ValueAtKey(
                                        adj_dict, property_key
                                    )
                                    results.append(
                                        {
                                            "vertex": vertex,
                                            "occupancy": occupancy_type,
                                            "property": property_value,
                                            "from_adjacent": True,
                                        }
                                    )
            elif isinstance(occupancy_type, list):
                for occupancy in occupancy_type:
                    if space_type.lower() in occupancy.lower():
                        keys = Dictionary.Keys(vertex_dict)
                        if property_key in keys:
                            property_value = Dictionary.ValueAtKey(
                                vertex_dict, property_key
                            )
                            results.append(
                                {
                                    "vertex": vertex,
                                    "occupancy": occupancy,
                                    "property": property_value,
                                }
                            )

    return results


if __name__ == "__main__":
    ecolution = True
    if ecolution:
        tbim = Topology.ByJSONPath("ecolution_tbim.json")
        tbim_ = Cluster.ByTopologies(tbim, transferDictionaries=True)
        tbim_final = Topology.SelfMerge(tbim_, transferDictionaries=True)
        graph = Graph.ByTopology(
            tbim_final,
            viaSharedTopologies=True,
            toExteriorTopologies=True,
            storeBREP=True,
        )
        faces = Topology.Faces(tbim_final)
        vertices = Graph.Vertices(graph)
        Topology.TransferDictionaries(sources=faces, sinks=vertices)
    else:
        cellComplexList = Topology.ByJSONPath("BIM/TBIM_Topologic.json")
        cellComplex = cellComplexList[0]
        cells_list = []
        cellComplex.Cells(cellComplex, cells_list)
        cellComplex = CellComplex.ByCells(cells_list)
        g = Graph.ByTopology(cellComplex)

    # Print available keys from random vertices to check property names
    if not ecolution:
        vertices = Graph.Vertices(g)
    if vertices:
        n = 20
        sampled_vertices = random.sample(vertices, n)
        for vertex in sampled_vertices:
            vertex_dict = Topology.Dictionary(vertex)
            if vertex_dict:
                print("Available keys in vertices:", Dictionary.Keys(vertex_dict))
                print("-" * 50)

    # Example usage:
    if ecolution:
        toilet_heating = query_space_property(graph, "bedroom", "condition_state")
    else:
        toilet_heating = query_space_property(g, "Toilet", "pr_IsHeated")
    for result in toilet_heating:
        print(f"\nFound {result['occupancy']}")
        print(f"Has heating: {result['property']}")
        if result.get("from_adjacent"):
            print("(Information from adjacent space)")
        print("-" * 50)
