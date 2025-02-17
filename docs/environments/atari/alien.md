---
title: Alien
---

# Alien

```{figure} ../../_static/videos/atari/alien.gif
:width: 120px
:name: Alien
```

This environment is part of the <a href='..'>Atari environments</a>. Please read that page first for general information.

|   |   |
|---|---|
| Action Space | Discrete(18) |
| Observation Shape | (210, 160, 3) |
| Observation High | 255 |
| Observation Low | 0  |
| Import | `gymnasium.make("ALE/Alien-v5")` |

For more Alien variants with different observation and action spaces, see the variants section.

## Description

You are stuck in a maze-like space ship with three aliens. You goal is to destroy their eggs that are scattered all over the ship while simultaneously avoiding the aliens (they are trying to kill you). You have a flamethrower that can help you turn them away in tricky situations. Moreover, you can occasionally collect a power-up (pulsar) that gives you the temporary ability to kill aliens.

    For a more detailed documentation, see [the AtariAge page](https://atariage.com/manual_html_page.php?SoftwareID=815)

## Actions

Alien has the action space `Discrete(18)` with the table below lists the meaning of each action's meanings.
As Alien uses the full set of actions then specifying `full_action_space=True` will not modify the action space of the environment if passed to `gymnasium.make`.

| Value   | Meaning         |
|---------|-----------------|
| `0`     | `NOOP`          |
| `1`     | `FIRE`          |
| `2`     | `UP`            |
| `3`     | `RIGHT`         |
| `4`     | `LEFT`          |
| `5`     | `DOWN`          |
| `6`     | `UPRIGHT`       |
| `7`     | `UPLEFT`        |
| `8`     | `DOWNRIGHT`     |
| `9`     | `DOWNLEFT`      |
| `10`    | `UPFIRE`        |
| `11`    | `RIGHTFIRE`     |
| `12`    | `LEFTFIRE`      |
| `13`    | `DOWNFIRE`      |
| `14`    | `UPRIGHTFIRE`   |
| `15`    | `UPLEFTFIRE`    |
| `16`    | `DOWNRIGHTFIRE` |
| `17`    | `DOWNLEFTFIRE`  |

## Observations

Atari environment have two possible observation types, the observation space is listed below.
See variants section for the type of observation used by each environment id.

- `obs_type="rgb" -> observation_space=Box(0, 255, (210, 160, 3), np.uint8)`
- `obs_type="ram" -> observation_space=Box(0, 255, (128,), np.uint8)`

Additionally, `obs_type="grayscale"` cause the environment return a grayscale version of the rgb array for observations with the observation space being `Box(0, 255, (210, 160), np.uint8)`
### Rewards

You score points by destroying eggs, killing aliens, using pulsars, and collecting special prizes. When you are caught
by an alien, you will lose one of your lives. The number of lives you have depends on the game flavor. For a
table of scores corresponding to the different achievements, consult [the AtariAge page](https://atariage.com/manual_html_page.php?SoftwareID=815).

## Variants

Alien has the following variants of the environment id which have the following differences in observation,
the number of frame-skips and the repeat action probability.

| Env-id                    | obs_type=   | frameskip=   | repeat_action_probability=   |
|---------------------------|-------------|--------------|------------------------------|
| Alien-v0                  | `"rgb"`     | `(2, 5)`     | `0.25`                       |
| Alien-ram-v0              | `"ram"`     | `(2, 5)`     | `0.25`                       |
| Alien-ramDeterministic-v0 | `"ram"`     | `4`          | `0.25`                       |
| Alien-ramNoFrameskip-v0   | `"ram"`     | `1`          | `0.25`                       |
| AlienDeterministic-v0     | `"rgb"`     | `4`          | `0.25`                       |
| AlienNoFrameskip-v0       | `"rgb"`     | `1`          | `0.25`                       |
| Alien-v4                  | `"rgb"`     | `(2, 5)`     | `0.0`                        |
| Alien-ram-v4              | `"ram"`     | `(2, 5)`     | `0.0`                        |
| Alien-ramDeterministic-v4 | `"ram"`     | `4`          | `0.0`                        |
| Alien-ramNoFrameskip-v4   | `"ram"`     | `1`          | `0.0`                        |
| AlienDeterministic-v4     | `"rgb"`     | `4`          | `0.0`                        |
| AlienNoFrameskip-v4       | `"rgb"`     | `1`          | `0.0`                        |
| ALE/Alien-v5              | `"rgb"`     | `4`          | `0.25`                       |
| ALE/Alien-ram-v5          | `"ram"`     | `4`          | `0.25`                       |

## Difficulty and modes

It is possible to specify various flavors of the environment via the keyword arguments `difficulty` and `mode`.
A flavor is a combination of a game mode and a difficulty setting. The table below lists the possible difficulty and mode values
along with the default values.

| Available Modes   | Default Mode   | Available Difficulties   | Default Difficulty   |
|-------------------|----------------|--------------------------|----------------------|
| `[0, 1, 2, 3]`    | `0`            | `[0, 1, 2, 3]`           | `0`                  |

## Version History

A thorough discussion of the intricate differences between the versions and configurations can be found in the general article on Atari environments.

* v5: Stickiness was added back and stochastic frameskipping was removed. The environments are now in the "ALE" namespace.
* v4: Stickiness of actions was removed
* v0: Initial versions release
