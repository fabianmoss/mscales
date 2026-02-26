import numpy as np
import pytest
from ..basic import PitchClass, PitchClassInterval, PitchClassSet


class TestPitchClass:
    def test_pitch_class_init(self):
        pc = PitchClass(0, c=12)
        assert pc.p == 0
        assert pc.c == 12

    def test_pitch_class_wrap_around(self):
        pc = PitchClass(15, c=12)
        assert pc.p == 3

    def test_pitch_class_repr(self):
        pc = PitchClass(5, c=12)
        assert repr(pc) == "PitchClass(5)"

    def test_pitch_class_str(self):
        pc = PitchClass(7, c=12)
        assert str(pc) == "7"

    def test_pitch_class_neg(self):
        pc = PitchClass(5, c=12)
        result = -pc
        assert result == -5 % 12

    def test_pitch_class_add_with_interval(self):
        pc = PitchClass(5, c=12)
        interval = PitchClassInterval(2, c=12)
        result = pc + interval
        assert isinstance(result, PitchClass)
        assert result.p == 7

    def test_pitch_class_add_type_error(self):
        pc = PitchClass(5, c=12)
        with pytest.raises(TypeError):
            _ = pc + 2

    def test_pitch_class_sub_with_interval(self):
        pc = PitchClass(7, c=12)
        interval = PitchClassInterval(2, c=12)
        result = pc - interval
        assert isinstance(result, PitchClass)
        assert result.p == 5

    def test_pitch_class_eq(self):
        pc1 = PitchClass(5, c=12)
        pc2 = PitchClass(5, c=12)
        assert pc1 == pc2


class TestPitchClassInterval:
    def test_interval_init(self):
        interval = PitchClassInterval(5, c=12)
        assert interval.i == 5
        assert interval.c == 12

    def test_interval_repr(self):
        interval = PitchClassInterval(3, c=12)
        assert repr(interval) == "PitchClassInterval(3)"

    def test_interval_str(self):
        interval = PitchClassInterval(7, c=12)
        assert str(interval) == "7"

    def test_interval_add_interval(self):
        i1 = PitchClassInterval(3, c=12)
        i2 = PitchClassInterval(5, c=12)
        result = i1 + i2
        assert isinstance(result, PitchClassInterval)
        assert result.i == 8

    def test_interval_add_pitch_class(self):
        interval = PitchClassInterval(5, c=12)
        pc = PitchClass(7, c=12)
        result = interval + pc
        assert isinstance(result, PitchClass)
        assert result.p == 0

    def test_interval_add_type_error(self):
        interval = PitchClassInterval(5, c=12)
        with pytest.raises(TypeError):
            _ = interval + "string"

    def test_interval_sub_interval(self):
        i1 = PitchClassInterval(7, c=12)
        i2 = PitchClassInterval(3, c=12)
        result = i1 - i2
        assert isinstance(result, (int, np.integer))


class TestPitchClassSet:
    def test_pcset_init_from_list(self):
        pcs = PitchClassSet([0, 2, 4, 7, 9])
        assert isinstance(pcs.pcs, np.ndarray)
        assert len(pcs.pcs) == 5

    def test_pcset_init_from_set(self):
        pcs = PitchClassSet({0, 2, 4, 7, 9})
        assert len(pcs.pcs) == 5

    def test_pcset_init_from_string(self):
        pcs = PitchClassSet("02479")
        assert len(pcs.pcs) == 5
        assert np.array_equal(pcs.pcs, np.array([0, 2, 4, 7, 9]))

    def test_pcset_init_string_with_te(self):
        pcs = PitchClassSet("14TE")
        assert len(pcs.pcs) == 4

    def test_pcset_init_type_error(self):
        with pytest.raises(TypeError):
            _ = PitchClassSet(123)

    def test_pcset_repr(self):
        pcs = PitchClassSet([0, 2, 4])
        assert "PitchClassSet" in repr(pcs)

    def test_pcset_str(self):
        pcs = PitchClassSet([0, 2, 4])
        assert "0" in str(pcs) and "2" in str(pcs) and "4" in str(pcs)

    def test_pcset_len(self):
        pcs = PitchClassSet([0, 2, 4, 7, 9])
        assert len(pcs) == 5

    def test_pcset_eq(self):
        pcs1 = PitchClassSet([0, 2, 4])
        pcs2 = PitchClassSet([0, 2, 4])
        pcs3 = PitchClassSet([0, 2, 5])
        assert pcs1 == pcs2
        assert pcs1 != pcs3

    def test_pcset_sort(self):
        pcs = PitchClassSet([7, 0, 4, 2])
        result = pcs.sort()
        assert np.array_equal(result.pcs, np.array([0, 2, 4, 7]))

    def test_pcset_to_vector(self):
        pcs = PitchClassSet([0, 2, 4, 7, 9])
        result = pcs.to_vector()
        assert isinstance(result, np.ndarray)
        assert result.shape == (12,)
        assert result.sum() == 5
        assert result[0] == 1
        assert result[2] == 1
        assert result[1] == 0

    def test_pcset_transpose(self):
        pcs = PitchClassSet([0, 2, 4])
        result = pcs.transpose(2)
        assert np.array_equal(result.pcs, np.array([2, 4, 6]))

    def test_pcset_invert(self):
        pcs = PitchClassSet([0, 2, 4])
        result = pcs.invert(0)
        assert np.array_equal(result.pcs, np.array([0, 10, 8]))

    def test_pcset_complement(self):
        pcs = PitchClassSet([0, 2, 4, 5, 7, 9, 11])
        result = pcs.complement()
        assert result.d + pcs.d == 12
        assert len(set(result.pcs) & set(pcs.pcs)) == 0

    def test_pcset_normal_form_major(self):
        pcs = PitchClassSet([0, 2, 4, 5, 7, 9, 11])
        result = pcs.normal_form()
        assert isinstance(result, PitchClassSet)

    def test_pcset_normal_form_single(self):
        pcs = PitchClassSet([7])
        result = pcs.normal_form()
        assert isinstance(result, PitchClassSet)

    def test_pcset_prime_form_major(self):
        pcs = PitchClassSet([0, 2, 4, 5, 7, 9, 11])
        result = pcs.prime_form()
        assert isinstance(result, PitchClassSet)

    def test_pcset_interval_vector(self):
        pcs = PitchClassSet([0, 1, 4, 6])
        result = pcs.interval_vector()
        assert isinstance(result, np.ndarray)
        assert result.sum() == 6

    def test_pcset_maximally_even_diatonic(self):
        pcs = PitchClassSet([0, 2, 4, 5, 7, 9, 11])
        result = pcs.maximally_even()
        assert isinstance(result, bool)

    def test_pcset_spectrum(self):
        pcs = PitchClassSet([0, 2, 4, 5, 7, 9, 11])
        result = pcs.spectrum(1)
        assert isinstance(result, set)

    def test_pcset_myhill(self):
        pcs = PitchClassSet([0, 2, 4, 5, 7, 9, 11])
        result = pcs.myhill()
        assert isinstance(result, bool)

    def test_pcset_cardinality_equals_variety(self):
        pcs = PitchClassSet([0, 2, 4, 5, 7, 9, 11])
        result = pcs.cardinality_equals_variety()
        assert isinstance(result, bool)

    def test_pcset_sum(self):
        pcs = PitchClassSet([0, 2, 4])
        assert pcs.sum() == 6

    def test_pcset_retrograde(self):
        pcs = PitchClassSet([0, 2, 4])
        result = pcs.retrograde()
        assert isinstance(result, PitchClassSet)

    def test_pcset_inversion(self):
        pcs = PitchClassSet([0, 2, 4])
        result = pcs.inversion()
        assert isinstance(result, PitchClassSet)

    def test_pcset_matrix(self):
        pcs = PitchClassSet([0, 2, 4])
        result = pcs.matrix()
        assert isinstance(result, np.ndarray)
        assert result.shape[0] == 3
