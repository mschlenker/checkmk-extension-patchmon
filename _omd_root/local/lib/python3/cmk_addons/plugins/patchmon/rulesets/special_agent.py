#!/usr/bin/env python3
# Shebang needed only for editors

from cmk.rulesets.v1.form_specs import (
    Password,
    migrate_to_password,
    Dictionary,
    DefaultValue,
    DictElement,
    FixedValue,
    Integer,
    String,
    TimeSpan,
    TimeMagnitude,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    BooleanChoice
)    
from cmk.rulesets.v1.rule_specs import (
    SpecialAgent,
    Topic,
    Help,
    Title
)
from cmk.rulesets.v1 import Label

def _formspec():
    return Dictionary(
        title=Title("PatchMon connection"),
        help_text=Help(
            "Retrieve update information from a PatchMon server and create piggyback data from it."
        ),
        elements={
            "baseurl": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Base URL of PatchMon"),
                    help_text=Help(
                        "Specify the absolute URL of the PatchMon server queried including the "
                        "protocol http:// or https://. Trailing slashes can be omitted."
                    ),
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
                    help_text=Help(
                        "Specify which of the host names present in PatchMon should be used to "
                        "create the host name for the piggyback section used by Checkmk."
                    ),
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
                    help_text=Help(
                        "Declare the interval used for caching and re-fetching the host list from "
                        "Patchmon. The value specified should be lower than the PatchMon agent "
                        "reporting interval used."
                    ), 
                    displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MINUTE, TimeMagnitude.HOUR],
                    prefill=DefaultValue(2100.0),
                ),
            ),
            "checkinterval": DictElement(
                required=True,
                parameter_form=TimeSpan(
                    title=Title("Interval for retrieving patch information"),
                    help_text=Help(
                        "Declare the interval used for caching and re-fetching the individual "
                        "host statistics from Patchmon. The value specified should be the same or "
                        "slightly higher than the PatchMon agent reporting interval used."
                    ), 
                    displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MINUTE, TimeMagnitude.HOUR],
                    prefill=DefaultValue(4800.0),
                ),
            ),
            "maxexec": DictElement(
                required=True,
                parameter_form=TimeSpan(
                    title=Title("Maximum execution time"),
                    help_text=Help(
                        "Specify the maximum time the special agent should spend retrieving host "
                        "information. In environments with many hosts, this helps to spread the "
                        "load on both the PatchMon and the Checkmk server by effectively dividing "
                        "the requests necessary into smaller batches. Never go above 60 seconds "
                        "since this will result in special agent timeouts. Sensible values are "
                        "between 2 and 30 seconds."
                    ), 
                    displayed_magnitudes=[TimeMagnitude.SECOND],
                    prefill=DefaultValue(15.0),
                ),
            ),
            "reboot": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    title=Title("Reboot info"),
                    label=Label("Query if reboot is necessary"),
                    help_text=Help(
                        "Decide whether to query the \"reboot needed\" flag. This adds one "
                        "REST-API call and leads to the creation of the agent section "
                        "\"patchmon_reboot\". You can omit this if you already query this flag by "
                        "other means, for example the Checkmk agent."
                    ),
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

