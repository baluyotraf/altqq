"""Utility test methods that do not belong to other groups."""

import re


def clean_whitespaces(text: str) -> str:
    """Standardize the white spaces in a text.

    Args:
        text (str): Text to standardize whitespace.

    Returns:
        str: Text with a standardized whitespace.
    """
    strip = text.strip()
    split = re.split(r"\s+", strip)
    join = " ".join(split)
    return join
