#!/usr/bin/env python3

from cmk.graphing.v1 import Title
from cmk.graphing.v1.graphs import Graph, MinimalRange
from cmk.graphing.v1.metrics import Color, DecimalNotation, Metric, Unit, StrictPrecision
from cmk.graphing.v1.perfometers import Closed, FocusRange, Open, Perfometer

metric_packages_outdated = Metric(
    name = "packages_outdated",
    title = Title("Number of outdated packages"),
    unit = Unit(DecimalNotation(""), StrictPrecision(0)),
    color = Color.YELLOW,
)

metric_packages_security = Metric(
    name = "packages_security",
    title = Title("Number of missing security updates"),
    unit = Unit(DecimalNotation(""), StrictPrecision(0)),
    color = Color.RED,
)

graph_packages_outdated_and_security = Graph(
    name="packages_outdated_and_security",
    title=Title("Outdated packages and security updates"),
    simple_lines=[
        "packages_outdated",
        "packages_security",
    ],
)
