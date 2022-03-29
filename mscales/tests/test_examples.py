from ..scales import generate_scales


def test_generate_scales():
    for c in range(15):
        assert 2**c == generate_scales(c=c).shape[0]
