"""
Basic logic for Task 4: Advanced text analysis.
Tasks: 
a) count words with length < 7;
b) find shortest word ending with 'a';
c) sort all words by length descending.
"""

def get_cleaned_words(text):
    """Helper to split text and remove commas/dots."""
    raw_words = text.replace(',', ' ').replace('.', ' ').split()
    return raw_words

def count_small_words(words, max_len=7):
    """a) Count words with length less than 7 symbols."""
    return len([word for word in words if len(word) < max_len])

def find_shortest_word_ending_a(words):
    """b) Find the shortest word ending with 'a' (case insensitive)."""
    target_words = [word for word in words if len(word) >= 2 and word.lower().endswith('a')]
    if not target_words:
        return None
    return min(target_words, key=len)

def sort_words_by_length(words):
    """c) Return list of words sorted by length descending."""
    return sorted(words, key=len, reverse=True)