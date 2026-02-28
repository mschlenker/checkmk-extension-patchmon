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
    messages = [
        "No updates are missing. View on PatchMon: {url}.",
        "{tot} updates missing. View on PatchMon: {url}.",
        "{sec} important security updates missing ({tot}  total)! View on PatchMon: {url}."
    ]
    if sec > 0:
        yield Result(
            state=State(params['statesecurity']),
            summary=messages[2].format(url=section['url'], tot=tot, sec=sec)
        )
    elif tot > 0:
        yield Result(
            state=State(params['stateregular']),
            summary=messages[1].format(url=section['url'], tot=tot)
        )
    else:
        yield Result(
            state=State.OK,
            summary=messages[0].format(url=section['url'])
        )
    yield Metric(
        name = "packages_outdated",
        value = tot,
    )
    yield Metric(
        name = "packages_security",
        value = sec,
    )

def check_patchmon_reboot(params, section):
    if not "needs_reboot" in section:
        yield Result(
            state=State.UNKNOWN,
            summary="Reboot information missing. Did someone change the special agent configuration?"
        )
        return
    if section['needs_reboot'] > 0:
        yield Result(
            state=State(params['statereboot']),
            summary="Reboot required, reason given: " + section['reboot_reason']
        )
    else:
        yield Result(
            state=State.OK,
            summary="No reboot needed."
        )

agent_section_patchmon_patches = AgentSection(
    name = "patchmon_patches",
    parse_function = parse_patchmon_patches,
)

check_plugin_patchmon_patches = CheckPlugin(
    name = "patchmon_patches",
    service_name = "PatchMon patches",
    discovery_function = discover_patchmon_patches,
    check_function = check_patchmon_patches,
    check_default_parameters = { 
        "stateregular": int(State.WARN), 
        "statesecurity": int(State.CRIT), 
        "statereboot": int(State.CRIT) 
    },
    check_ruleset_name = "patchmon_patches",
)

check_plugin_patchmon_reboot = CheckPlugin(
    name = "patchmon_reboot",
    sections = [ "patchmon_patches" ],
    service_name = "PatchMon reboot required",
    discovery_function = discover_patchmon_reboot,
    check_function = check_patchmon_reboot,
    check_default_parameters = { 
        "stateregular": int(State.WARN), 
        "statesecurity": int(State.CRIT), 
        "statereboot": int(State.CRIT) 
    },
    check_ruleset_name = "patchmon_patches",
)
