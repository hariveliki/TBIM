#!/usr/bin/env python
# coding: utf-8

# # Import

# Import topologicpy modules
from topologicpy.Topology import Topology
from topologicpy.CellComplex import CellComplex
from topologicpy.Cell import Cell
from topologicpy.Color import Color
from topologicpy.Dictionary import Dictionary
from topologicpy.Plotly import Plotly
from topologicpy.Face import Face


# Import Python file with plot functions
import TBIM

import os
import sys
from pprint import pprint

# Set True to Plot
plot = True


# # CellComplex
# Create a simple test cell complex
# test_cell = Cell.Box(width=1, length=1, height=1)
# test_complex = CellComplex.ByCells([test_cell])
# TBIM.Plot_CellsByKey(test_complex)

json_path = "BIM/TBIM_Topologic.json"
if os.path.exists(json_path):
    print(f"File exists at {json_path}")
else:
    print(f"File not found at {json_path}")

cellComplexList = Topology.ByJSONPath("BIM/TBIM_Topologic.json")
cellComplex = cellComplexList[0]
pprint(dir(cellComplex))
print(f"Type: {type(cellComplex)}")
print(f"Is CellComplex: {isinstance(cellComplex, CellComplex)}")
print(f"Topology type: {cellComplex.GetTypeAsString()}")
print(f"Is container type: {cellComplex.IsContainerType()}")

# cellComplex.Cells() adds cells to cells_list
cells_list = []
cellComplex.Cells(cellComplex, cells_list)
cellComplex = CellComplex.ByCells(cells_list)

plot_occupancy_type = False
plot_circulation_type = False
plot_area_per_occupant = False
plot_is_heated = False
plot_face_exposure = False
plot_wall_type_name = False
plot_u_value = False
plot_width = False
plot_graph = False

# OccupancyType
if plot_occupancy_type:
    TBIM.Plot_CellsByKey(
        cellComplex=cellComplex,
        key="pr_OccupancyType",
        keyType="str",
        colorScale="turbo",
        unitsString="",
    )

# CirculationType
if plot_circulation_type:
    TBIM.Plot_CellsByKey(
        cellComplex,
        key="pr_CirculationType",
        keyType="str",
        colorScale="turbo",
        unitsString="",
    )


# AreaPerOccupant
if plot_area_per_occupant:
    TBIM.Plot_CellsByKey(
        cellComplex,
        key="pr_AreaPerOccupantPeak",
        keyType="num",
        colorScale="viridis",
        unitsString="sqm/pp",
    )


# IsHeated
if plot_is_heated:
    TBIM.Plot_CellsByKey(
        cellComplex,
        key="pr_IsHeated",
        keyType="num",
        colorScale="inferno",
        unitsString="bool",
    )


# ## Faces

# FaceExposure
if plot_face_exposure:
    TBIM.Plot_FacesByKey(
        cellComplex,
        CellComplex.Decompose(cellComplex)["externalVerticalFaces"],
        key="pr_FaceExposure",
        keyType="str",
        colorScale="turbo",
        unitsString="",
    )


# WallTypeName
if plot_wall_type_name:
    TBIM.Plot_FacesByKey(
        cellComplex,
        CellComplex.Decompose(cellComplex)["externalVerticalFaces"]
        + CellComplex.Decompose(cellComplex)["internalVerticalFaces"],
        key="pr_WallTypeName",
        keyType="str",
        colorScale="turbo",
        unitsString="",
    )


# ## Apertures

# U-Value
if plot_u_value:
    TBIM.Plot_AperturesByKey(
        cellComplex,
        CellComplex.Decompose(cellComplex)["externalVerticalFaces"],
        "pr_UValue",
    )


# Width
if plot_width:
    TBIM.Plot_AperturesByKey(
        cellComplex,
        CellComplex.Decompose(cellComplex)["externalVerticalFaces"],
        "pr_Width",
    )

## Graph
if plot_graph:
    TBIM.Plot_PassageGraph(cellComplex, vertexSize=5, edgeWidth=3)
