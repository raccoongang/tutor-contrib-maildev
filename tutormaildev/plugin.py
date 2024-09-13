import os
import typing as t
from glob import glob

import importlib_resources
from tutor import hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

# Handle version suffix in nightly mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

HERE = os.path.abspath(os.path.dirname(__file__))

config: dict[str, dict[str, t.Any]] = {
    "defaults": {
        "VERSION": __version__,
        "WEB_PORT": 1080,
        "SMTP_HOST": "maildev",
        "SMTP_PORT": 1025,
        "PUBLIC_HOST": "maildev.{{ LMS_HOST }}",
        "DOCKER_IMAGE": "maildev/maildev",
    },
}

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"MAILDEV_{key}", value) for key, value in config.get("defaults", {}).items()]
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
