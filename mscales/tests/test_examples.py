from ..scales import Scales


def test_generate_scales():
    for c in range(15):
        s = Scales(c=c)
        _ = s.all()
        assert 2**c == s.n_scales
