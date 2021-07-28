# -*- coding: utf-8 -*-
from distutils.util import strtobool
from typing import Any


def per_channel_to_python(value: str) -> Any:
    try:
        return float(value)
    except ValueError:
        try:
            return strtobool(value)
        except ValueError:
            pass
    return False
