
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from requests import get
import requests
import csv
import re
import os

pages = {'basics':["https://www.geeksforgeeks.org/strings-in-c-2/",
  "https://www.geeksforgeeks.org/storage-for-strings-in-c/",
  "https://www.geeksforgeeks.org/stdstring-class-in-c/",
  "https://www.geeksforgeeks.org/string-class-in-java/",
  "https://www.geeksforgeeks.org/function-copy-string-iterative-recursive/",
  "https://www.geeksforgeeks.org/interesting-facts-about-strings-in-python-set-1/",
  "https://www.geeksforgeeks.org/interesting-facts-about-strings-in-python-set-2/",
  "https://www.geeksforgeeks.org/string-methods-python-set-1/",
  "https://www.geeksforgeeks.org/python-string-methods-set-2-len-count-center-ljust-rjust-isalpha-isalnum-isspace-join/",
  "https://www.geeksforgeeks.org/python-string-methods-set-3-strip-lstrip-rstrip-min-max-maketrans-translate-relplace/",
  "https://www.geeksforgeeks.org/reverse-a-string-using-recursion/",
  "https://www.geeksforgeeks.org/reverse-an-array-without-affecting-special-characters/",
  "https://www.geeksforgeeks.org/remove-all-duplicates-from-the-input-string/",
  "https://www.geeksforgeeks.org/pangram-checking/",
  "https://www.geeksforgeeks.org/how-to-split-a-string-in-cc-python-and-java/",
  "https://www.geeksforgeeks.org/remove-spaces-from-a-given-string/"],
  'character-counting': ["https://www.geeksforgeeks.org/return-maximum-occurring-character-in-the-input-string/",
  "https://www.geeksforgeeks.org/find-the-smallest-window-in-a-string-containing-all-characters-of-another-string/",
  "https://www.geeksforgeeks.org/c-program-find-second-frequent-character/",
  "https://www.geeksforgeeks.org/kth-non-repeating-character/",
  "https://www.geeksforgeeks.org/count-number-of-substrings-with-exactly-k-distinct-characters/",
  "https://www.geeksforgeeks.org/find-kth-character-of-decrypted-string/",
  "https://www.geeksforgeeks.org/count-characters-position-english-alphabets/",
  "https://www.geeksforgeeks.org/check-two-strings-k-anagrams-not/",
  "https://www.geeksforgeeks.org/count-words-in-a-given-string/",
  "https://www.geeksforgeeks.org/count-words-whose-th-letter-either-1-th-th-i1-th-letter-given-word/",
  "https://www.geeksforgeeks.org/count-substrings-with-same-first-and-last-characters/",
  "https://www.geeksforgeeks.org/maximum-consecutive-repeating-character-string/",
  "https://www.geeksforgeeks.org/count-strings-can-formed-using-b-c-given-constraints/",
  "https://www.geeksforgeeks.org/print-words-together-set-characters/",
  "https://www.geeksforgeeks.org/count-total-anagram-substrings/",
  "https://www.geeksforgeeks.org/substring-highest-frequency-length-product/",
  "https://www.geeksforgeeks.org/number-of-even-substrings-in-a-string-of-digits/",
  "https://www.geeksforgeeks.org/print-all-distinct-characters-of-a-string-in-order-3-methods/",
  "https://www.geeksforgeeks.org/smallest-window-contains-characters-string/",
  "https://www.geeksforgeeks.org/print-common-characters-two-strings-alphabetical-order-2/",
  "https://www.geeksforgeeks.org/program-count-occurrence-given-character-string/",
  "https://www.geeksforgeeks.org/minimum-sum-squares-characters-counts-given-string-removing-k-characters/",
  "https://www.geeksforgeeks.org/program-count-vowels-string-iterative-recursive/",
  "https://www.geeksforgeeks.org/number-distinct-permutation-string-can/",
  "https://www.geeksforgeeks.org/check-half-string-character-frequency-character/",
  "https://www.geeksforgeeks.org/count-words-appear-exactly-two-times-array-words/",
  "https://www.geeksforgeeks.org/check-if-frequency-of-all-characters-can-become-same-by-one-removal/",
  "https://www.geeksforgeeks.org/count-ways-increase-lcs-length-two-strings-one/",
  "https://www.geeksforgeeks.org/print-string-specified-character-occurred-given-no-times/",
  "https://www.geeksforgeeks.org/remove-characters-from-the-first-string-which-are-present-in-the-second-string/"],
  'anagram':["https://www.geeksforgeeks.org/check-whether-two-strings-are-anagram-of-each-other/",
  "https://www.geeksforgeeks.org/given-a-sequence-of-words-print-all-anagrams-together/",
  "https://www.geeksforgeeks.org/given-a-sequence-of-words-print-all-anagrams-together-set-2/",
  "https://www.geeksforgeeks.org/anagram-substring-search-search-permutations/",
  "https://www.geeksforgeeks.org/print-pairs-anagrams-given-array-strings/",
  "https://www.geeksforgeeks.org/remove-minimum-number-characters-two-strings-become-anagram/",
  "https://www.geeksforgeeks.org/check-two-strings-k-anagrams-not/",
  "https://www.geeksforgeeks.org/check-binary-representations-two-numbers-anagram/",
  "https://www.geeksforgeeks.org/given-a-sequence-of-words-print-all-anagrams-together-using-stl/",
  "https://www.geeksforgeeks.org/tag/anagram/"],
  'palindrom': ["https://www.geeksforgeeks.org/c-program-check-given-string-palindrome/",
  "https://www.geeksforgeeks.org/check-given-string-rotation-palindrome/",
  "https://www.geeksforgeeks.org/c-program-print-palindromes-given-range/",
  "https://www.geeksforgeeks.org/check-characters-given-string-can-rearranged-form-palindrome/",
  "https://www.geeksforgeeks.org/dynamic-programming-set-28-minimum-insertions-to-form-a-palindrome/",
  "https://www.geeksforgeeks.org/longest-palindromic-substring-set-2/",
  "https://www.geeksforgeeks.org/print-palindromic-partitions-string/",
  "https://www.geeksforgeeks.org/find-number-distinct-palindromic-sub-strings-given-string/",
  "https://www.geeksforgeeks.org/online-algorithm-for-checking-palindrome-in-a-stream/",
  "https://www.geeksforgeeks.org/given-a-string-print-all-possible-palindromic-partition/",
  "https://www.geeksforgeeks.org/count-palindromic-subsequence-given-string/",
  "https://www.geeksforgeeks.org/minimum-characters-added-front-make-string-palindrome/",
  "https://www.geeksforgeeks.org/palindrome-substring-queries/",
  "https://www.geeksforgeeks.org/suffix-tree-application-6-longest-palindromic-substring/",
  "https://www.geeksforgeeks.org/palindrome-pair-in-an-array-of-words-or-strings/",
  "https://www.geeksforgeeks.org/make-largest-palindrome-changing-k-digits/",
  "https://www.geeksforgeeks.org/lexicographically-first-palindromic-string/",
  "https://www.geeksforgeeks.org/recursive-function-check-string-palindrome/",
  "https://www.geeksforgeeks.org/minimum-number-appends-needed-make-string-palindrome/",
  "https://www.geeksforgeeks.org/longest-non-palindromic-substring/",
  "https://www.geeksforgeeks.org/minimum-number-deletions-make-string-palindrome/",
  "https://www.geeksforgeeks.org/minimum-steps-to-delete-a-string-after-repeated-deletion-of-palindrome-substrings/",
  "https://www.geeksforgeeks.org/count-of-palindromic-substrings-in-an-index-range/",
  "https://www.geeksforgeeks.org/minimum-insertions-to-form-a-palindrome-with-permutations-allowed/",
  "https://www.geeksforgeeks.org/nth-even-length-palindrome/",
  "https://www.geeksforgeeks.org/tag/palindrome/"],
  'binary-string': ["https://www.geeksforgeeks.org/change-bits-can-made-one-flip/",
  "https://www.geeksforgeeks.org/length-longest-sub-string-can-make-removed/",
  "https://www.geeksforgeeks.org/number-flips-make-binary-string-alternate/",
  "https://www.geeksforgeeks.org/efficient-method-2s-complement-binary-string/",
  "https://www.geeksforgeeks.org/count-binary-strings-k-times-appearing-adjacent-two-set-bits/",
  "https://www.geeksforgeeks.org/given-binary-string-count-number-substrings-start-end-1/",
  "https://www.geeksforgeeks.org/count-strings-with-consecutive-1s/",
  "https://www.geeksforgeeks.org/generate-all-binary-strings-from-given-pattern/",
  "https://www.geeksforgeeks.org/add-two-bit-strings/",
  "https://www.geeksforgeeks.org/count-number-binary-strings-without-consecutive-1s/",
  "https://www.geeksforgeeks.org/generate-binary-permutations-1s-0s-every-point-permutations/",
  "https://www.geeksforgeeks.org/check-string-follows-anbn-pattern-not/",
  "https://www.geeksforgeeks.org/binary-representation-of-next-number/",
  "https://www.geeksforgeeks.org/binary-representation-next-greater-number-number-1s-0s/",
  "https://www.geeksforgeeks.org/decimal-representation-given-binary-string-divisible-5-not/",
  "https://www.geeksforgeeks.org/check-binary-string-0-between-1s-not/",
  "https://www.geeksforgeeks.org/check-binary-string-0-1s-not-set-2-regular-expression-approach/",
  "https://www.geeksforgeeks.org/min-flips-of-continuous-characters-to-make-all-characters-same-in-a-string/",
  "https://www.geeksforgeeks.org/program-to-add-two-binary-strings/",
  "https://www.geeksforgeeks.org/convert-string-binary-sequence/",
  "https://www.geeksforgeeks.org/ways-remove-one-element-binary-string-xor-becomes-zero/",
  "https://www.geeksforgeeks.org/tag/binary-string/"],
  'subsequence': ["https://www.geeksforgeeks.org/number-subsequences-form-ai-bj-ck/",
  "https://www.geeksforgeeks.org/number-subsequences-string-divisible-n/",
  "https://www.geeksforgeeks.org/find-number-times-string-occurs-given-string/",
  "https://www.geeksforgeeks.org/count-distinct-subsequences/",
  "https://www.geeksforgeeks.org/count-distinct-occurrences-as-a-subsequence/",
  "https://www.geeksforgeeks.org/longest-common-subsequence-with-permutations-allowed/",
  "https://www.geeksforgeeks.org/repeated-subsequence-length-2/",
  "https://www.geeksforgeeks.org/maximum-length-prefix-one-string-occurs-subsequence-another/",
  "https://www.geeksforgeeks.org/count-distinct-occurrences-as-a-subsequence/",
  "https://www.geeksforgeeks.org/print-longest-common-sub-sequences-lexicographical-order/",
  "https://www.geeksforgeeks.org/printing-longest-common-subsequence/",
  "https://www.geeksforgeeks.org/given-number-find-number-contiguous-subsequences-recursively-add-9/",
  "https://www.geeksforgeeks.org/printing-longest-common-subsequence-set-2-printing/",
  "https://www.geeksforgeeks.org/given-number-string-find-number-contiguous-subsequences-recursively-add-9-set-2/",
  "https://www.geeksforgeeks.org/print-shortest-common-supersequence/",
  "https://www.geeksforgeeks.org/space-optimized-solution-lcs/",
  "https://www.geeksforgeeks.org/given-two-strings-find-first-string-subsequence-second/",
  "https://www.geeksforgeeks.org/shortest-common-supersequence/",
  "https://www.geeksforgeeks.org/longest-repeating-subsequence/",
  "https://www.geeksforgeeks.org/find-largest-word-dictionary-deleting-characters-given-string/",
  "https://www.geeksforgeeks.org/dynamic-programming-set-4-longest-common-subsequence/",
  "https://www.geeksforgeeks.org/minimum-number-of-palindromic-subsequences-to-be-removed-to-empty-a-binary-string/",
  "https://www.geeksforgeeks.org/count-palindromic-subsequence-given-string/",
  "https://www.geeksforgeeks.org/queries-subsequence-string/",
  "https://www.geeksforgeeks.org/tag/subsequence/"],
  'pattern-searching':["https://www.geeksforgeeks.org/searching-for-patterns-set-1-naive-pattern-searching/",
  "https://www.geeksforgeeks.org/searching-for-patterns-set-2-kmp-algorithm/",
  "https://www.geeksforgeeks.org/searching-for-patterns-set-3-rabin-karp-algorithm/",
  "https://www.geeksforgeeks.org/searching-for-patterns-set-5-finite-automata/",
  "https://www.geeksforgeeks.org/pattern-searching-set-7-boyer-moore-algorithm-bad-character-heuristic/",
  "https://www.geeksforgeeks.org/wildcard-character-matching/",
  "https://www.geeksforgeeks.org/anagram-substring-search-search-permutations/",
  "https://www.geeksforgeeks.org/manachers-algorithm-linear-time-longest-palindromic-substring-part-1/",
  "https://www.geeksforgeeks.org/manachers-algorithm-linear-time-longest-palindromic-substring-part-2/",
  "https://www.geeksforgeeks.org/manachers-algorithm-linear-time-longest-palindromic-substring-part-3-2/",
  "https://www.geeksforgeeks.org/manachers-algorithm-linear-time-longest-palindromic-substring-part-4/",
  "https://www.geeksforgeeks.org/z-algorithm-linear-time-pattern-searching-algorithm/",
  "https://www.geeksforgeeks.org/search-a-word-in-a-2d-grid-of-characters/",
  "https://www.geeksforgeeks.org/find-all-occurrences-of-the-word-in-a-matrix/",
  "https://www.geeksforgeeks.org/maximum-length-prefix-one-string-occurs-subsequence-another/",
  "https://www.geeksforgeeks.org/wildcard-pattern-matching/",
  "https://www.geeksforgeeks.org/replace-occurrences-string-ab-c-without-using-extra-space/",
  "https://www.geeksforgeeks.org/aho-corasick-algorithm-pattern-searching/",
  "https://www.geeksforgeeks.org/find-patterns-101-given-string/",
  "https://www.geeksforgeeks.org/find-patterns-101-given-string-set-2regular-expression-approach/",
  "https://www.geeksforgeeks.org/category/algorithm/pattern-searching/"],
  'miscellaneous': ["https://www.geeksforgeeks.org/a-program-to-check-if-strings-are-rotations-of-each-other/",
  "https://www.geeksforgeeks.org/print-all-the-duplicates-in-the-input-string/",
  "https://www.geeksforgeeks.org/write-a-c-program-to-print-all-permutations-of-a-given-string/",
  "https://www.geeksforgeeks.org/divide-a-string-in-n-equal-parts/",
  "https://www.geeksforgeeks.org/given-a-string-find-its-first-non-repeating-character/",
  "https://www.geeksforgeeks.org/print-list-items-containing-all-characters-of-a-given-word/",
  "https://www.geeksforgeeks.org/reverse-words-in-a-given-string/",
  "https://www.geeksforgeeks.org/run-length-encoding/",
  "https://www.geeksforgeeks.org/print-all-permutations-with-repetition-of-characters/",
  "https://www.geeksforgeeks.org/rearrange-a-string-so-that-all-same-characters-become-at-least-d-distance-away/",
  "https://www.geeksforgeeks.org/powet-set-lexicographic-order/",
  "https://www.geeksforgeeks.org/recursively-remove-adjacent-duplicates-given-string/",
  "https://www.geeksforgeeks.org/remove-a-and-bc-from-a-given-string/",
  "https://www.geeksforgeeks.org/find-first-non-repeating-character-stream-characters/",
  "https://www.geeksforgeeks.org/wildcard-character-matching/",
  "https://www.geeksforgeeks.org/an-in-place-algorithm-for-string-transformation/",
  "https://www.geeksforgeeks.org/lexicographic-rank-of-a-string/",
  "https://www.geeksforgeeks.org/print-number-ascending-order-contains-1-2-3-digits/",
  "https://www.geeksforgeeks.org/check-whether-a-given-string-is-an-interleaving-of-two-other-given-strings/",
  "https://www.geeksforgeeks.org/given-sorted-dictionary-find-precedence-characters/",
  "https://www.geeksforgeeks.org/find-excel-column-name-given-number/",
  "https://www.geeksforgeeks.org/c-program-sort-array-names-strings/",
  "https://www.geeksforgeeks.org/find-possible-words-phone-digits/",
  "https://www.geeksforgeeks.org/rearrange-a-string-so-that-all-same-characters-become-at-least-d-distance-away/",
  "https://www.geeksforgeeks.org/c-program-remove-spaces-string/",
  "https://www.geeksforgeeks.org/recursively-print-all-sentences-that-can-be-formed-from-list-of-word-lists/",
  "https://www.geeksforgeeks.org/check-if-a-given-sequence-of-moves-for-a-robot-is-circular-or-not/",
  "https://www.geeksforgeeks.org/find-the-longest-substring-with-k-unique-characters-in-a-given-string/",
  "https://www.geeksforgeeks.org/function-to-find-number-of-customers-who-could-not-get-a-computer/",
  "https://www.geeksforgeeks.org/find-maximum-depth-nested-parenthesis-string/",
  "https://www.geeksforgeeks.org/find-given-string-can-represented-substring-iterating-substring-n-times/",
  "https://www.geeksforgeeks.org/print-possible-strings-can-made-placing-spaces/",
  "https://www.geeksforgeeks.org/check-given-sentence-given-set-simple-grammer-rules/",
  "https://www.geeksforgeeks.org/remove-recurring-digits-in-a-given-number/",
  "https://www.geeksforgeeks.org/check-if-two-given-strings-are-at-edit-distance-one/",
  "https://www.geeksforgeeks.org/recursive-implementation-of-atoi/",
  "https://www.geeksforgeeks.org/length-of-the-longest-valid-substring/",
  "https://www.geeksforgeeks.org/check-if-two-given-strings-are-isomorphic-to-each-other/",
  "https://www.geeksforgeeks.org/print-string-of-odd-length-in-x-format/",
  "https://www.geeksforgeeks.org/transform-one-string-to-another-using-minimum-number-of-given-operation/",
  "https://www.geeksforgeeks.org/check-if-a-string-can-be-formed-from-another-string-using-given-constraints/",
  "https://www.geeksforgeeks.org/print-ways-break-string-bracket-form/",
  "https://www.geeksforgeeks.org/combinations-strings-can-used-dial-given-phone-number/",
  "https://www.geeksforgeeks.org/caesar-cipher/",
  "https://www.geeksforgeeks.org/print-concatenation-of-zig-zag-string-form-in-n-rows/",
  "https://www.geeksforgeeks.org/category/data-structures/c-strings/"]}

def scrape(links, raw_path, topic, subtopic):
    num_links = 0
    for i in links:
        url = i
        r = requests.get(url)
        if r.status_code == 404:
            print("No page for " + url)
        else:
            m = re.search("\/\/.*\/(.*)\/", url)
            if m:
                name = m.group(1)
            soup = BeautifulSoup(r.content, 'html.parser')
            path = os.path.join(raw_path, topic, subtopic)
            if not os.path.exists(path): 
                os.makedirs(path)
            o = open(os.path.join(path, str(name)+'.html'), 'w')
            o.write(str(soup.prettify().encode("utf-8")))
            o.close
            num_links += 1
    print(num_links)
    return num_links

for i in pages:
    subtopic = i
    link = pages[i]
    scrape(link, 'raw', 'strings', subtopic)


