from ..scales import Scales


def test_generate_scales():
    for c in range(15):
        assert 2**c == Scales(cardinality=c).shape[0]
