#!/usr/bin/env python3

from cmk.rulesets.v1 import Label, Title
from cmk.rulesets.v1.form_specs import ServiceState, BooleanChoice, DefaultValue, DictElement, Dictionary, Float, LevelDirection, SimpleLevels
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic

def _parameter_form():
    return Dictionary(
        elements = {
            "stateregular": DictElement(
                parameter_form = ServiceState(
                    title = Title("Service state when regular updates are missing"),
                    prefill = DefaultValue(ServiceState.WARN),
                ),
                required = True,
            ),
            "statesecurity": DictElement(
                parameter_form = ServiceState(
                    title = Title("Service state when security updates are missing"),
                    prefill = DefaultValue(ServiceState.CRIT),
                ),
                required = True,
            ),
            "statereboot": DictElement(
                parameter_form = ServiceState(
                    title = Title("Service state when reboot need is detected"),
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

