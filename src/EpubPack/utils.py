import re


def snakeCaseString(s: str) -> str:
    """Convert a string to an ascii acceptable string, where spaces are replaced with underscores."""
    import unicodedata

    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[-\s]+", "_", s)
    if s.startswith("the_"):
        s = s[4:]
    if s.startswith("a_"):
        s = s[2:]
    return s
