from modules.script_callbacks import on_ui_settings
from modules.shared import OptionInfo, opts

import gradio as gr
import shutil
import re
import os


flavors: tuple[str] = (
    "latte",
    "frappe",
    "macchiato",
    "mocha",
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

    on_waves_change()


def on_flavor_change():
    shutil.copy(
        os.path.join(script_path, "flavors", f"{opts.ctp_flavor}.css"),
        os.path.join(script_path, "style.css"),
    )

    on_accent_change()


def on_waves_change():
    with open(os.path.join(script_path, "style.css"), "r+") as file:
        style = file.read()

    _edit = False
    animated: bool = "gradio-app" in style
    animating: bool = opts.oled_waves

    if animated and (not animating):
        style = style.split("body gradio-app")[0]
        _edit = True

    if (not animated) and animating:
        with open(os.path.join(script_path, "flavors", "waves.css"), "r") as waves:
            anim = waves.read()
        style = f"{style}{anim}"
        _edit = True

    if not _edit:
        return

    with open(os.path.join(script_path, "style.css"), "w") as file:
        file.write(style)


def on_settings():
    args = {"section": ("ctp", "Catppuccin Theme"), "category_id": "ui"}

    opts.add_option(
        "ctp_flavor",
        OptionInfo(
            default="mocha",
            label="Catppuccin Flavor",
            component=gr.Radio,
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
            component=gr.Radio,
            component_args={"choices": accents},
            onchange=on_accent_change,
            **args,
        ),
    )

    opts.add_option(
        "oled_waves",
        OptionInfo(
            default=False,
            label="Background Animation",
            component=gr.Checkbox,
            onchange=on_waves_change,
            **args,
        ).info("mainly for OLED monitor"),
    )


on_ui_settings(on_settings)
