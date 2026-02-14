#!/usr/bin/env python3
# Shebang needed only for editors

from cmk.rulesets.v1.form_specs import Password, migrate_to_password, Dictionary, DefaultValue, DictElement, FixedValue, Integer, String, TimeSpan, TimeMagnitude, CascadingSingleChoice, CascadingSingleChoiceElement
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic, Help, Title

def _formspec():
    return Dictionary(
        title=Title("PatchMon connection"),
        help_text=Help("Retrieve update information from a PatchMon server and create piggyback data from it."),
        elements={
            "baseurl": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Base URL of PatchMon"),
                ),
            ),
            "password": DictElement(
                required=True,
                parameter_form=Password(
                    title=Title("Login credentials"),
                    migrate=migrate_to_password,
                ),
            ),
            "name": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("Host name selection"),
                    prefill=DefaultValue("friendly_name"),
                    elements=[
                        CascadingSingleChoiceElement(
                            title=Title("Friendly name"),
                            name="friendly_name",
                            parameter_form=FixedValue(value=None),
                        ),
                        CascadingSingleChoiceElement(
                            title=Title("Host name"),
                            name="hostname",
                            parameter_form=FixedValue(value=None),
                        ),
                        CascadingSingleChoiceElement(
                            title=Title("UUID"),
                            name="id",
                            parameter_form=FixedValue(value=None),
                        ),
                    ],
                ),
            ),
            "listinterval": DictElement(
                required=True,
                parameter_form=TimeSpan(
                    title=Title("Interval for retrieving the host list"),
                    displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MINUTE, TimeMagnitude.HOUR],
                    prefill=DefaultValue(1800.0),
                ),
            ),
            "checkinterval": DictElement(
                required=True,
                parameter_form=TimeSpan(
                    title=Title("Interval for retrieving patch information"),
                    displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MINUTE, TimeMagnitude.HOUR],
                    prefill=DefaultValue(5400.0),
                ),
            ),
            "maxexec": DictElement(
                required=True,
                parameter_form=TimeSpan(
                    title=Title("Maximum execution time"),
                    displayed_magnitudes=[TimeMagnitude.SECOND],
                    prefill=DefaultValue(30.0),
                ),
            ),
        }
    )

rule_spec_patchmon = SpecialAgent(
    topic=Topic.OPERATING_SYSTEM,
    name="patchmon",
    title=Title("PatchMon update info"),
    parameter_form=_formspec
)

