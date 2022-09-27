__author__ = "Sander Schulhoff"
__email__ = "sanderschulhoff@gmail.com"

import os
import re
from functools import reduce

import numpy as np
from tqdm import tqdm
from utils import kill_strs, trim

import gymnasium as gym

LAYOUT = "env"

pattern = re.compile(r"(?<!^)(?=[A-Z])")

gym.logger.set_level(gym.logger.DISABLED)

all_envs = list(gym.envs.registry.values())
filtered_envs_by_type = {}

# Obtain filtered list
for env_spec in tqdm(all_envs):
    if any(x in str(env_spec.id) for x in kill_strs):
        continue

    # gymnasium.envs.env_type.env.EnvClass
    # ale_py.env.gym:AtariEnv
    split = env_spec.entry_point.split(".")
    # ignore gymnasium.envs.env_type:Env
    env_module = split[0]
    if len(split) < 4 and env_module != "ale_py":
        continue
    env_type = split[2] if env_module != "ale_py" else "atari"
    env_version = env_spec.version

    # ignore unit test envs and old versions of atari envs
    if env_module == "ale_py" or env_type == "unittest":
        continue

    try:
        env = gym.make(env_spec.id)
        split = str(type(env.unwrapped)).split(".")
        env_name = split[3]

        if env_type not in filtered_envs_by_type.keys():
            filtered_envs_by_type[env_type] = {}
        # only store new entries and higher versions
        if env_name not in filtered_envs_by_type[env_type] or (
            env_name in filtered_envs_by_type[env_type]
            and env_version > filtered_envs_by_type[env_type][env_name].version
        ):
            filtered_envs_by_type[env_type][env_name] = env_spec

    except Exception as e:
        print(e)

# Sort
filtered_envs = list(
    reduce(
        lambda s, x: s + x,
        map(
            lambda arr: sorted(arr, key=lambda x: x.name),
            map(lambda dic: list(dic.values()), list(filtered_envs_by_type.values())),
        ),
        [],
    )
)


# Update Docs
for i, env_spec in tqdm(enumerate(filtered_envs)):
    print("ID:", env_spec.id)
    env_type = env_spec.entry_point.split(".")[2]
    try:
        env = gym.make(env_spec.id)

        # variants dont get their own pages
        e_n = str(env_spec).lower()

        docstring = env.unwrapped.__doc__
        if not docstring:
            docstring = env.unwrapped.__class__.__doc__
        docstring = trim(docstring)

        # pascal case
        pascal_env_name = env_spec.id.split("-")[0]
        snake_env_name = pattern.sub("_", pascal_env_name).lower()
        title_env_name = snake_env_name.replace("_", " ").title()
        env_type_title = env_type.replace("_", " ").title()
        related_pages_meta = ""
        if i == 0 or not env_type == filtered_envs[i - 1].entry_point.split(".")[2]:
            related_pages_meta = "firstpage:\n"
        elif (
            i == len(filtered_envs) - 1
            or not env_type == filtered_envs[i + 1].entry_point.split(".")[2]
        ):
            related_pages_meta = "lastpage:\n"

        # path for saving video
        v_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "environments",
            env_type,
            snake_env_name + ".md",
        )

        front_matter = f"""---
AUTOGENERATED: DO NOT EDIT FILE DIRECTLY
title: {title_env_name}
{related_pages_meta}---
"""
        title = f"# {title_env_name}"
        gif = (
            "```{figure}"
            + f" ../../_static/videos/{env_type}/{snake_env_name}.gif"
            + f" \n:width: 200px\n:name: {snake_env_name}\n```"
        )
        info = (
            "This environment is part of the"
            + f"<a href='..'>{env_type_title} environments</a>."
            + "Please read that page first for general information."
        )
        env_table = "|   |   |\n|---|---|\n"
        env_table += f"| Action Space | {env.action_space} |\n"

        if env.observation_space.shape:
            env_table += f"| Observation Shape | {env.observation_space.shape} |\n"

            if hasattr(env.observation_space, "high"):
                high = env.observation_space.high

                if hasattr(high, "shape"):
                    if len(high.shape) == 3:
                        high = high[0][0][0]
                high = np.round(high, 2)
                high = str(high).replace("\n", " ")
                env_table += f"| Observation High | {high} |\n"

            if hasattr(env.observation_space, "low"):
                low = env.observation_space.low
                if hasattr(low, "shape"):
                    if len(low.shape) == 3:
                        low = low[0][0][0]
                low = np.round(low, 2)
                low = str(low).replace("\n", " ")
                env_table += f"| Observation Low | {low} |\n"
        else:
            env_table += f"| Observation Space | {env.observation_space} |\n"

        env_table += f'| Import | `gymnasium.make("{env_spec.id}")` | \n'

        if docstring is None:
            docstring = "No information provided"
        all_text = f"""{front_matter}
{title}

{gif}

{info}

{env_table}

{docstring}
"""
        file = open(v_path, "w", encoding="utf-8")
        file.write(all_text)
        file.close()
    except Exception as e:
        print(e)