#!/usr/bin/env python3

from cmk.rulesets.v1 import Label, Title, Help
from cmk.rulesets.v1.form_specs import (
    ServiceState,
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic
)

def _parameter_form():
    return Dictionary(
        help_text = Help(
            "Specify the default states of the two services \"PatchMon patches\" and \"PatchMon "
            " reboot\"."
        ),
        elements = {
            "stateregular": DictElement(
                parameter_form = ServiceState(
                    title = Title("Service state when regular updates are missing"),
                    help_text = Help(
                        "Apply the state specified here to the patch service if updates are "
                        "missing, but none of these updates is classified as security update."
                    ),
                    prefill = DefaultValue(ServiceState.WARN),
                ),
                required = True,
            ),
            "statesecurity": DictElement(
                parameter_form = ServiceState(
                    title = Title("Service state when security updates are missing"),
                    help_text = Help(
                        "Apply the state specified here to the patch service if updates are "
                        "missing and at least one of these update is classified as security "
                        "update."
                    ),
                    prefill = DefaultValue(ServiceState.CRIT),
                ),
                required = True,
            ),
            "statereboot": DictElement(
                parameter_form = ServiceState(
                    title = Title("Service state when reboot need is detected"),
                    help_text = Help(
                        "Apply the state specified here to the reboot service if the flag \"reboot "
                        "needed\" is detected by PatchMon."
                    ),
                    prefill = DefaultValue(ServiceState.CRIT),
                ),
                required = True,
            ),
        }
    )

rule_spec_patchmon_patches = CheckParameters(
    name = "patchmon_patches",
    title = Title("PatchMon patches"),
    topic = Topic.OPERATING_SYSTEM,
    parameter_form = _parameter_form,
    condition = HostAndItemCondition(item_title=Title("PatchMon patches")),
)

