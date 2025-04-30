from modules.script_callbacks import on_ui_settings
from modules.shared import OptionInfo, opts

import shutil
import re
import os

script_path = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))


def on_accent_change():
    with open(os.path.join(script_path, "style.css"), "r+") as file:
        style = file.read()

    pattern = re.compile(r"--ctp-accent:\s*(.*)")
    style = re.sub(
        pattern,
        f"--ctp-accent: var(--ctp-{opts.accent_color});",
        style,
        count=1,
    )

    with open(os.path.join(script_path, "style.css"), "w") as file:
        file.write(style)


def on_flavor_change():
    shutil.copy(
        os.path.join(script_path, "flavors", f"{opts.ctp_flavor}.css"),
        os.path.join(script_path, "style.css"),
    )

    on_accent_change()


def on_settings():
    from gradio import Radio

    args = {"section": ("ctp", "Catppuccin Theme"), "category_id": "ui"}

    flavors: tuple[str] = (
        "latte",
        "frappe",
        "macchiato",
        "mocha",
        "burnt",
    )

    accents: tuple[str] = (
        "rosewater",
        "flamingo",
        "pink",
        "mauve",
        "red",
        "maroon",
        "peach",
        "yellow",
        "green",
        "teal",
        "sky",
        "blue",
        "sapphire",
        "lavender",
    )

    opts.add_option(
        "ctp_flavor",
        OptionInfo(
            default="mocha",
            label="Catppuccin Flavor",
            component=Radio,
            component_args={"choices": flavors},
            onchange=on_flavor_change,
            **args,
        ),
    )

    opts.add_option(
        "accent_color",
        OptionInfo(
            default="maroon",
            label="Accent",
            component=Radio,
            component_args={"choices": accents},
            onchange=on_accent_change,
            **args,
        ),
    )


on_ui_settings(on_settings)
