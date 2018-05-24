"""Tests for models."""

from markov.models import Vertex, Model


def test_vertex():
    v = Vertex()
    v.update("abab")
    v.update("baba")
    v.update("abab")
    assert set(v.items()) == set([("abab", 2), ("baba", 1)])

    results = set()
    for i in range(100):
        results.add(v.get_edge())

    assert results == set(["abab", "baba"])


def test_model_1():
    m = Model(1)

    m.process(["a", "b", "a", "bab"])
    m.process(["a", "b", "c", "bab"])

    assert set(m.keys()) == set([("a",), ("b",), ("c",)])
    assert set(m[("a",)].items()) == set([(("b",), 2), (("bab",), 1)])
    assert set(m[("b",)].items()) == set([(("a",), 1), (("c",), 1)])
    assert set(m[("c",)].items()) == set([(("bab",), 1)])


def test_model_2():
    m = Model(2)

    m.process(["a", "b", "a", "bab"])
    m.process(["a", "b", "c", "bab"])

    assert set(m.keys()) == set([("a", "b",), ("b", "a",), ("b", "c",)])
    assert set(m[("a", "b",)].items()) == set([
        (("b", "a",), 1), (("b", "c",), 1)])
    assert set(m[("b", "a",)].items()) == set([(("a", "bab",), 1)])
    assert set(m[("b", "c",)].items()) == set([(("c", "bab",), 1)])
