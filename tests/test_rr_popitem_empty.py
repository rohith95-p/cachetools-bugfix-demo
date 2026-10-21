import pytest
import cachetools


def test_rr_popitem_empty_with_min_choice():
    cache = cachetools.RRCache(maxsize=2, choice=min)
    with pytest.raises(KeyError) as excinfo:
        cache.popitem()
    assert excinfo.value.args[0] == "RRCache is empty"


def test_rr_popitem_empty_with_max_choice():
    cache = cachetools.RRCache(maxsize=2, choice=max)
    with pytest.raises(KeyError) as excinfo:
        cache.popitem()
    assert excinfo.value.args[0] == "RRCache is empty"


def test_rr_popitem_empty_with_next_iter_choice():
    cache = cachetools.RRCache(maxsize=2, choice=next)
    with pytest.raises(KeyError) as excinfo:
        cache.popitem()
    assert excinfo.value.args[0] == "RRCache is empty"


def test_rr_popitem_empty_with_custom_choice_that_raises_value_error():
    def my_choice(seq):
        raise ValueError("custom")
    cache = cachetools.RRCache(maxsize=2, choice=my_choice)
    with pytest.raises(KeyError) as excinfo:
        cache.popitem()
    assert excinfo.value.args[0] == "RRCache is empty"


def test_rr_popitem_empty_with_custom_choice_that_raises_runtime_error():
    def my_choice(seq):
        raise RuntimeError("custom")
    cache = cachetools.RRCache(maxsize=2, choice=my_choice)
    with pytest.raises(KeyError) as excinfo:
        cache.popitem()
    assert excinfo.value.args[0] == "RRCache is empty"


def test_rr_popitem_non_empty_works():
    cache = cachetools.RRCache(maxsize=2, choice=min)
    cache[1] = "one"
    cache[2] = "two"
    # Should not raise
    key, value = cache.popitem()
    assert key in (1, 2)
    assert value in ("one", "two")
    # Second pop
    key2, value2 = cache.popitem()
    assert key2 not in (key,)  # the other key
    assert value2 not in (value,)
    # Now empty
    with pytest.raises(KeyError) as excinfo:
        cache.popitem()
    assert excinfo.value.args[0] == "RRCache is empty"


def test_rr_popitem_empty_cache_after_clear():
    cache = cachetools.RRCache(maxsize=2, choice=min)
    cache[1] = "one"
    cache.clear()
    with pytest.raises(KeyError) as excinfo:
        cache.popitem()
    assert excinfo.value.args[0] == "RRCache is empty"


def test_rr_popitem_single_item_then_empty():
    cache = cachetools.RRCache(maxsize=2, choice=min)
    cache[1] = "one"
    key, value = cache.popitem()
    assert key == 1
    assert value == "one"
    with pytest.raises(KeyError) as excinfo:
        cache.popitem()
    assert excinfo.value.args[0] == "RRCache is empty"
