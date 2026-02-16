#!/usr/bin/env python3

from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, Result, State, Metric, check_levels
import itertools
import json

def parse_patchmon_patches(string_table):
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed

def discover_patchmon_patches(section):
    yield Service()
    
def discover_patchmon_reboot(section):
    if "needs_reboot" in section:
        yield Service()

def check_patchmon_patches(params, section):
    sec = section['security_updates']
    tot = section['outdated_packages']
    if sec > 0:
        yield Result(state=State(params['statesecurity']), summary=str(sec)  + " important security updates missing (" + str(tot) + " total)!")
    elif tot > 0:
        yield Result(state=State(params['stateregular']), summary=str(tot) + " updates are missing.")
    else:
        yield Result(state=State.OK, summary="No updates are missing.")
    yield Result(state=State.OK, summary="View on PatchMon: " + section['url'])
    yield Metric(
        name = "packages_outdated",
        value = tot,
    )
    yield Metric(
        name = "packages_security",
        value = sec,
    )
    
def check_patchmon_reboot(section):
    if section['needs_reboot'] > 0:
        yield Result(state=State.CRIT, summary="Reboot required, reason given: " + section['reboot_reason'])
    else:
        yield Result(state=State.OK, summary="No reboot needed.")

agent_section_patchmon_patches = AgentSection(
    name = "patchmon_patches",
    parse_function = parse_patchmon_patches,
)

check_plugin_patchmon_patches = CheckPlugin(
    name = "patchmon_patches",
    service_name = "PatchMon patches",
    discovery_function = discover_patchmon_patches,
    check_function = check_patchmon_patches,
    check_default_parameters = { "stateregular": int(State.WARN), "statesecurity": int(State.CRIT) },
    check_ruleset_name = "patchmon_patches",
)

check_plugin_patchmon_reboot = CheckPlugin(
    name = "patchmon_reboot",
    sections = [ "patchmon_patches" ],
    service_name = "PatchMon reboot required",
    discovery_function = discover_patchmon_reboot,
    check_function = check_patchmon_reboot,
)
