#!/usr/bin/env python3

from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, Result, State, Metric, check_levels
import itertools
import json

def parse_patchmon_server(string_table):
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed

def discover_patchmon_server(section):
    yield Service()

def check_patchmon_server(section):
    duration = section['duration']
    yield Metric(name="elapsed_time", value=duration)
    yield Result(state=State.OK, summary="The PatchMon server was queried in reasonable time. Data could be correctly consumed.")

agent_section_patchmon_server = AgentSection(
    name = "patchmon_server",
    parse_function = parse_patchmon_server,
)

check_plugin_patchmon_server = CheckPlugin(
    name = "patchmon_server",
    service_name = "PatchMon server stats",
    discovery_function = discover_patchmon_server,
    check_function = check_patchmon_server,
)

