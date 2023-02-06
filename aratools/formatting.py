import copy
from collections.abc import Generator


def format_text(tbox_width: int, text: str, fsize: int) -> str:
    """
    Format text to fit horizontally inside of textbox
    """
    # make a copy, don't modify original
    text = str(text)
    max_text_width = int(tbox_width / (0.62 * fsize))
    if len(text) < max_text_width:
        return text
    words = truncated_word_generator(text, max_text_width)
    lines = []
    new_text = ""
    for w in words:
        if len(new_text + w) + 1 > max_text_width:
            lines.append(copy.copy(new_text))
            new_text = ""
        new_text += w + " "
    lines.append(new_text)
    return "\n".join(lines)


def truncated_word_generator(text: str, max_char: int) -> Generator[str, None, None]:
    """
    Returns a generator that yields words from a text and breaks up words with hyphens
    when they exceed a max length
    """
    words = text.split()
    while len(words):
        w = words.pop(0)
        while len(w) > max_char:
            yield w[: max_char - 1] + "-"
            w = w[max_char - 1 :]
        yield w
