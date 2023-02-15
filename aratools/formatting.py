import copy
from collections.abc import Generator, Sequence


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


def equal_division_generator(
    numerator: int, denominator: int
) -> Generator[int, None, None]:
    """
    Divide an integer into equally sized blocks and yield them.
    If the remainder has value X, than the first X yielded values
    will be increased by 1.
    """
    assert numerator >= 0 and denominator > 0
    if numerator == 0:
        for _ in range(denominator):
            yield 0
    remainder = numerator % denominator
    ratio = numerator // denominator
    while numerator > 0:
        if remainder > 0:
            result = ratio + 1
            remainder -= 1
        else:
            result = ratio
        yield result
        numerator -= result


def weighted_division_generator(
    total: int, ratios: Sequence[float]
) -> Generator[int, None, None]:
    assert sum(ratios) == 1.0
    denominators = tuple(1 // r for r in ratios)
    results = (total // denominator for denominator in denominators)
    remainder = sum(total % denominator for denominator in denominators)
    return (
        int(res + rem)
        for res, rem in zip(
            results, equal_division_generator(int(remainder), len(ratios)), strict=True
        )
    )


# TODO this returns [50, 25] !!
print(list(weighted_division_generator(50, [0.6, 0.4])))
