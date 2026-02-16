#!/usr/bin/env python3
# Shebang needed only for editors

from cmk.server_side_calls.v1 import noop_parser, SpecialAgentConfig, SpecialAgentCommand

def command_function(params, host_config):
    args = [
        "--baseurl", str(params['baseurl']), 
        "--name", str(params['name'][0]),
        "--secret", params['password'],
        "--list", str(float(params['listinterval'])),
        "--check", str(float(params['checkinterval'])),
        "--maxexec", str(float(params['maxexec'])),
    ]
    if params["reboot"]:
        args.append("--reboot")
    yield SpecialAgentCommand(command_arguments=args)

special_agent_ometemp = SpecialAgentConfig(
    name="patchmon",
    parameter_parser=noop_parser,
    commands_function=command_function
)

