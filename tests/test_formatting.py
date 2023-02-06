import pytest

from aratools.formatting import truncated_word_generator


@pytest.mark.parametrize(
    "text, max_char",
    [
        ("Hello my name is mister verylongword and I enjoy verylongverbing", 6),
        ("Hello my name is mister verylongword and I enjoy verylongverbing", 50),
        ("Superduperdupermegalongword", 6),
    ],
)
def test_truncated_word_generator(text, max_char):
    generator = truncated_word_generator(text, max_char)
    reconstruct = ""
    for w in generator:
        assert len(w) <= max_char
        if "-" in w:
            reconstruct += w.replace("-", "")
        else:
            reconstruct += w + " "
    assert reconstruct[:-1] == text
