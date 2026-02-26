from collections import Counter

from ..scales import Scales


class TestScalesAll:
    def test_scales_all_basic(self):
        s = Scales(c=12)
        result = s.all()
        assert result.shape[0] == 2**12
        assert s.n_scales == 2**12

    def test_scales_all_with_d(self):
        s = Scales(c=12, d=7)
        result = s.all()
        assert result.shape[0] == s.n_scales

    def test_scales_all_c_small(self):
        for c in range(1, 8):
            s = Scales(c=c)
            s.all()
            assert 2**c == s.n_scales


class TestScalesPitchClasses:
    def test_pitch_classes_basic(self):
        s = Scales(c=12, d=7)
        result = s.pitch_classes()
        assert isinstance(result, list)
        assert len(result) == s.n_scales
        for pc in result:
            assert len(pc) == 7

    def test_pitch_classes_no_d(self):
        s = Scales(c=12)
        result = s.pitch_classes()
        assert isinstance(result, list)
        assert len(result) == 2**12


class TestScalesIntervalVectors:
    def test_interval_vectors_basic(self):
        s = Scales(c=12, d=7)
        result = s.interval_vectors()
        assert isinstance(result, list)
        assert len(result) == s.n_scales
        for iv in result:
            assert isinstance(iv, Counter)

    def test_interval_vectors_no_d(self):
        s = Scales(c=12)
        result = s.interval_vectors()
        assert isinstance(result, list)
        assert len(result) == 2**12


class TestScalesProperties:
    def test_scales_c_attribute(self):
        s = Scales(c=12)
        assert s.c == 12

    def test_scales_d_attribute(self):
        s = Scales(c=12, d=7)
        assert s.d == 7

    def test_scales_d_none(self):
        s = Scales(c=12)
        assert s.d is None
