"""
Main Module: LW 3, Task 4
Developer: YARCEV A.A.
Description: Analysis of a specific text string.
Version: 1.0
Date: 2026-03-20
"""

import utils
import text_analysis

@utils.repeat_decorator
def main():
    """Main execution flow for Task 4."""
    source_text = ("So she was considering in her own mind, as well as she could, for the "
                   "hot day made her feel very sleepy and stupid, whether the pleasure of "
                   "making a daisy-chain would be worth the trouble of getting up and "
                   "picking the daisies, when suddenly a White Rabbit with pink eyes ran "
                   "close by her.")

    print("\n" + "="*60)
    print("TASK 4: TEXT ANALYSIS")
    print("="*60)
    print(f"Source text: {source_text[:70]}...")

    words = text_analysis.get_cleaned_words(source_text)

    # Task A
    small_words_count = text_analysis.count_small_words(words)
    print(f"\na) Number of words shorter than 7 symbols: {small_words_count}")

    # Task B
    shortest_a = text_analysis.find_shortest_word_ending_a(words)
    result_b = shortest_a if shortest_a else "Not found"
    print(f"b) Shortest word ending with 'a': {result_b}")

    # Task C
    sorted_list = text_analysis.sort_words_by_length(words)
    print("c) Words sorted by length (descending):")
    
    print(", ".join(sorted_list[:15]) + "...")

if __name__ == "__main__":
    main()