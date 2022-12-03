import random

import pytest

from main import SearchEngine


@pytest.fixture
def search_engine():
    return SearchEngine()


class TestSearchEngine:
    def test_search_engine(self, search_engine):
        keys = ["book of mormons", "book", "book of mormons", "boot", "boolean", "boolean", "boolean", "boolean",
                "book of mormons", "book"]

        for key in keys:
            search_engine.search(key)

        suggestions: list[str] = search_engine.suggest('boo')
        assert suggestions[0] == 'boolean'
        assert suggestions[1] == 'book of mormons'
        assert suggestions[2] == 'book'
        assert suggestions[3] == 'boot'

    def test_search_engine_replace_entry(self, search_engine):
        keys = ["book of mormons", "book of mormons", "book", "book", "boolean", "boolean",
                "boot", "boot", "boot"]

        for key in keys:
            search_engine.search(key)

        suggestions: list[str] = search_engine.suggest('boo')
        assert suggestions[0] == 'boot'
        assert suggestions[1] == 'book of mormons'
        assert suggestions[2] == 'book'

    def test_with_different_input(self):
        keys = ["abaca", "abacay", "abacas", "abacate",
                "abacaxi", "abaci", "abacinate", "abacination",
                "abacisci", "abaciscus", "abacist", "aback",
                "abacli"]

        engine = SearchEngine(len(keys))

        # add each item multiple times its index in the list
        index = 1
        for key in keys:
            for i in range(0, index):
                engine.search(key)
            index += 1

        suggestions: list[str] = engine.suggest('ab')
        assert len(suggestions) == len(keys)
        index = len(keys)-1
        # assert that the suggestions are in the right order
        for i in keys:
            assert suggestions[index] == i
            index -= 1

    def test_search_engine_replace_entry_random_search(self):
        search_engine = SearchEngine(3)
        keys = ["book of mormons", "book", "book", "boolean", "boolean", "boolean",
                "boot", "boot", "boot", "boot"]
        distinct_index: list[int] = list()

        while len(distinct_index) < len(keys):
            x = random.randint(0, len(keys) - 1)
            if x in distinct_index:
                continue
            search_engine.search(keys[x])
            distinct_index.append(x)

        suggestions: list[str] = search_engine.suggest('boo')
        assert suggestions[0] == 'boot'
        assert suggestions[1] == 'boolean'
        assert suggestions[2] == 'book'

    def test_search_engine_empty_list(self, search_engine):
        keys = ["book of mormons", "book of mormons", "book", "book", "boolean", "boolean",
                "boot", "boot", "boot"]

        search_engine = SearchEngine()

        for key in keys:
            search_engine.search(key)

        suggestions: list[str] = search_engine.suggest('foo')
        assert len(suggestions) == 0
