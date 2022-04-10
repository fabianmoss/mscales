from ..scales import Scales


def test_generate_scales():
    for c in range(15):
        s = Scales(cardinality=c)
        scales = s.all()
        assert 2**c == scales.n_scales
