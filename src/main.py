from trie import Trie, TrieNode

MAX_TOP_SUGGESTIONS = 10


class SearchHitEntry:
    def __init__(self, word: str, hits: int):
        self.word: str = word
        self.hits: int = hits


class SearchEngine:
    def __init__(self, max_top_suggestions: int = MAX_TOP_SUGGESTIONS):
        self.max_top_suggestions = max_top_suggestions
        self.trie = Trie()
        self.node_to_top_suggestions: dict[TrieNode, list[SearchHitEntry]] = {}
        self.trends_score: dict[str, SearchHitEntry] = {}

    def search(self, key: str):
        path: list[TrieNode] = self.trie.insert(key)

        if key not in self.trends_score:
            self.trends_score[key] = SearchHitEntry(key, 0)

        # Update the word score tracking
        entry: SearchHitEntry = self.trends_score[key]
        entry.hits += 1

        # remove word last node
        path.pop()

        # for each node in the path of the new key
        # add the key to its list of suggestions if applicable
        # and sort the list
        for node in path:
            if node not in self.node_to_top_suggestions.keys():
                self.node_to_top_suggestions[node] = list()

            node_top_suggestions: list[SearchHitEntry] = self.node_to_top_suggestions.get(node)
            key_in_node_top_suggestions = self.trends_score[key] in node_top_suggestions

            if len(node_top_suggestions) < self.max_top_suggestions and not key_in_node_top_suggestions:
                node_top_suggestions.append(self.trends_score[key])
            else:
                # List of suggestions has reached its max size
                # check if the new entry score is higher than the last entry
                last_entry: SearchHitEntry = node_top_suggestions[-1]
                new_entry_hits = self.trends_score[key].hits

                if last_entry.hits <= new_entry_hits and not key_in_node_top_suggestions:
                    # pop out last entry to make room for the new entry
                    node_top_suggestions.pop()
                    node_top_suggestions.append(self.trends_score[key])

            # Keep the top suggestion sorted after each search
            node_top_suggestions.sort(key=lambda x: x.hits, reverse=True)

    def suggest(self, key) -> list[str]:
        key_node = self.trie.get_node(key)
        top_suggestions: list[str] = list()

        if key_node in self.node_to_top_suggestions.keys():
            for i in self.node_to_top_suggestions[key_node]:
                top_suggestions.append(i.word)

        return top_suggestions
