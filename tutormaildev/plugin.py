from __future__ import annotations

import os
import typing as t
from glob import glob

import importlib_resources
from tutor import hooks

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'MAILDEV_'.
        ("MAILDEV_ENABLED", False),
        ("MAILDEV_WEB_PORT", 1080),
        ("MAILDEV_SMTP_PORT", 1025),
        ("MAILDEV_PUBLIC_HOST", "maildev.{{ LMS_HOST }}"),
        ("MAILDEV_INDEX_PREFIX", "tutor_"),
        ("MAILDEV_DOCKER_IMAGE", "maildev/maildev")
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Add your new settings that override existing settings here.
        # Each new setting is a pair: (setting_name, new_value).
        ("EMAIL_PORT", "{{ MAILDEV_SMTP_PORT }}"),
    ]
)

@hooks.Filters.APP_PUBLIC_HOSTS.add()
def add_maildev_hosts(
    hosts: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if context_name == "dev":
        hosts.append("{{ MAILDEV_PUBLIC_HOST }}:{{ MAILDEV_WEB_PORT }}")
    else:
        hosts.append("{{ MAILDEV_PUBLIC_HOST }}")
    return hosts


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = str(
        importlib_resources.files("tutormaildev")
        / os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        str(importlib_resources.files("tutormaildev") / "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutormaildev/templates/maildev/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/maildev/build``.
    [
        ("maildev/build", "plugins"),
        ("maildev/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutormaildev/patches,
# apply a patch based on the file's name and contents.
for path in glob(str(importlib_resources.files("tutormaildev") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
