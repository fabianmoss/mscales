import numpy as np

from ..utils import (
    binary,
    find_ngrams,
    generate_scale,
    invert,
    invmod,
    is_distributionally_even,
    is_generated,
    j_function,
    pcset,
    transpose,
)


class TestGenerateScale:
    def test_generate_scale_basic(self):
        result = generate_scale(12, 7, 2)
        assert isinstance(result, np.ndarray)
        assert result.shape == (12,)

    def test_generate_scale_chromatic_12_diatonic_7(self):
        result = generate_scale(12, 7, 5)
        assert result.shape == (12,)

    def test_generate_scale_octotonic(self):
        result = generate_scale(12, 8, 3)
        assert result.shape == (12,)


class TestInvmod:
    def test_invmod_basic(self):
        result = invmod(np.array([5]), 12)
        assert result == 5

    def test_invmod_not_coprime(self):
        result = invmod(np.array([2, 4]), 12)
        assert result == 2


class TestIsGenerated:
    def test_is_generated_diatonic(self):
        s = generate_scale(12, 7, 2)
        assert is_generated(s)

    def test_is_generated_pentatonic(self):
        s = generate_scale(12, 5, 2)
        assert is_generated(s)

    def test_is_generated_false(self):
        s = np.array([1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0])
        assert not is_generated(s)


class TestIsDistributionallyEven:
    def test_is_distributionally_even_diatonic(self):
        s = generate_scale(12, 7, 2)
        assert is_distributionally_even(s)

    def test_is_distributionally_even_major(self):
        s = binary(pcset=np.array([0, 2, 4, 5, 7, 9, 11]), c=12)
        assert is_distributionally_even(s)


class TestJFunction:
    def test_j_function_basic(self):
        result = j_function(0, 12, 7, 0)
        assert isinstance(result, (int, np.integer))

    def test_j_function_values(self):
        result = j_function(3, 12, 7, 2)
        assert result >= 0


class TestTranspose:
    def test_transpose_basic(self):
        s = np.array([1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0])
        result = transpose(s, 2)
        assert isinstance(result, np.ndarray)
        assert result.shape == s.shape

    def test_transpose_zero(self):
        s = np.array([1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0])
        result = transpose(s, 0)
        assert np.array_equal(result, s)


class TestInvert:
    def test_invert_basic(self):
        s = np.array([1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0])
        result = invert(s, 0, 12)
        assert isinstance(result, np.ndarray)
        assert result.shape == s.shape

    def test_invert_at_i(self):
        s = np.array([1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0])
        result = invert(s, 2, 12)
        assert result.shape == s.shape


class TestPcset:
    def test_pcset_basic(self):
        s = np.array([1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0])
        result = pcset(s)
        assert isinstance(result, np.ndarray)
        assert len(result) == 5

    def test_pcset_values(self):
        s = np.array([1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0])
        result = pcset(s)
        expected = np.array([0, 2, 4, 8, 10])
        assert np.array_equal(result, expected)


class TestBinary:
    def test_binary_basic(self):
        result = binary(np.array([0, 2, 4, 7, 9]), 12)
        assert isinstance(result, np.ndarray)
        assert result.shape == (12,)
        assert result.sum() == 5


class TestFindNgrams:
    def test_find_ngrams_basic(self):
        result = list(find_ngrams([1, 2, 3, 4, 5], 2))
        assert len(result) == 4

    def test_find_ngrams_single(self):
        result = list(find_ngrams([1, 2, 3], 1))
        assert len(result) == 3

    def test_find_ngrams_equal_length(self):
        result = list(find_ngrams([1, 2], 2))
        assert len(result) == 1

    def test_find_ngrams_longer_n(self):
        result = list(find_ngrams([1, 2, 3], 5))
        assert len(result) == 0
