#!/usr/bin/env python3

from cmk.rulesets.v1 import Label, Title, Help
from cmk.rulesets.v1.form_specs import (
    ServiceState,
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    TimeSpan,
    TimeMagnitude,
    DictGroup,
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
            "use_grace": DictElement(
                parameter_form = Dictionary(
                    title = Title("Grace periods"),
                    help_text = Help(
                        "Specify grace periods for updates. Use this in case you have automatic "
                        "updates configured and only want to get nagged when one of these likely failed "
                        "after the default interval. For example, you might want to set the grace "
                        "period for normal updates to 26 hours if you have configured daily updates. "
                        "Using this option relies on the package list that is only queried when the similar "
                        "option in the special agent rule is configured."
                    ),
                    elements = {
                        "grace_normal": DictElement(
                            parameter_form = TimeSpan(
                                title = Title("Regular updates"),
                                displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MINUTE, TimeMagnitude.HOUR],
                                prefill=DefaultValue(0.0),
                            ),
                            required = True,
                        ),
                        "grace_security": DictElement(
                            parameter_form = TimeSpan(
                                title = Title("Security updates"),
                                displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MINUTE, TimeMagnitude.HOUR],
                                prefill=DefaultValue(0.0),
                            ),
                            required = True,
                        ),
                    },
                ),
                required = False,
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

