import os.path
import re

from modules.script_callbacks import on_ui_settings
from modules.shared import OptionInfo, opts

SCRIPT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
FLAVORS = os.path.join(SCRIPT, "flavors")


def on_change():
    with open(os.path.join(FLAVORS, f"{opts.ctp_flavor}.css"), "r") as file:
        flavor = file.read()
    with open(os.path.join(FLAVORS, "base.css"), "r") as file:
        base = file.read()

    pattern = re.compile(r"--ctp-accent:\s*(.*)")
    flavor = re.sub(
        pattern,
        f"--ctp-accent: var(--ctp-{opts.accent_color});",
        flavor,
        count=1,
    )

    with open(os.path.join(SCRIPT, "style.css"), "w") as file:
        file.write("\n".join([flavor, base]))


def on_settings():
    from gradio import Radio

    args = {"section": ("ctp", "Catppuccin Theme"), "category_id": "ui"}

    flavors: tuple[str] = ("latte", "frappe", "macchiato", "mocha", "burnt")

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
            onchange=on_change,
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
            onchange=on_change,
            **args,
        ),
    )


on_ui_settings(on_settings)
