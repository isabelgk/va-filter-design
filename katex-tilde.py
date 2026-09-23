#!/usr/bin/env python3
"""mdbook preprocessor: escape the bare "~" that KaTeX emits for accents like \\tilde.

Left literal, pairs of these tildes are parsed as markdown strikethrough and
break the rendered math.
"""
import json
import re
import sys

LONE_TILDE = re.compile(r"(?<=>)~(?=<)")


def fix(items):
    for item in items:
        chapter = item.get("Chapter") if isinstance(item, dict) else None
        if chapter:
            chapter["content"] = LONE_TILDE.sub("&#126;", chapter["content"])
            fix(chapter.get("sub_items", []))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "supports":
        sys.exit(0)
    _context, book = json.load(sys.stdin)
    fix(book.get("items", book.get("sections", [])))
    json.dump(book, sys.stdout)
