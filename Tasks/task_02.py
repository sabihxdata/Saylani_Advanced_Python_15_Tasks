'''Task 02 | Longest Valid Window
Concepts: Sliding window, dictionaries
Problem: Write longest_unique_window(text) to find the longest contiguous substring with no repeated characters. Return the substring, start index, and length.
Requirements: Target O(n) time. On equal-length windows, select the earliest. Treat spaces and punctuation as characters.
Sample / expected behavior: Input: "abcabcbb" -> ("abc", 0, 3); "" -> ("", 0, 0). '''


def longest_unique_window(text):

    char_index = {}

    start = 0
    longest_substring = ""
    longest_start = 0
    longest_length = 0

    for end in range(len(text)):

        character = text[end]

        if character in char_index and char_index[character] >= start:
            start = char_index[character] + 1

        char_index[character] = end

        current_length = end - start + 1

        if current_length > longest_length:

            longest_length = current_length
            longest_start = start
            longest_substring = text[start:end + 1]

    return longest_substring, longest_start, longest_length




print(longest_unique_window("abcabcbb"))
print(longest_unique_window("abcdef"))
print(longest_unique_window("pwwkew"))
print(longest_unique_window(""))
print(longest_unique_window("a b c a"))
print(longest_unique_window("aabbcc"))