#!/usr/bin/env python

from collections import deque
from collections.abc import Iterable
import heapq
import itertools
from typing import Dict, Generator, List, Tuple, Optional, Union,\
        Callable, Any

class KnuthMorrisPratt:
    """    
    Class implementing the Knuth-Morris-Pratt string searching
    algorithm, implemented to accept any finite ordered iterable
    object for both the pattern to be matched and the object(s)
    to be searched.

    Initialisation args:
        Required positional:
        pattern (iterable object): A finite ordered iterable
                object (e.g. a string) that is the pattern to be
                found as a contiguous subsequence in other similar
                iterable objects.
    
    Attributes:
        pattern_iter (iterable object): A finite ordered iterable
                object (e.g. a string) that is the pattern
                to be found as a contiguous subsequence in other
                similar iterable objects.
        lps (list of ints): A list with the same length as the number
                of elements in pattern_iter, representing the Longest
                Prefix Suffix (LPS) array for pattern_iter using the
                Knuth-Morris-Pratt (KMP) algorithm, in preparation for
                its use for finding the pattern in a given iterable
                object (see method matchStartGenerator()).
                For a string p of length n, the LPS array is a 1D integer
                array of length n, where the integer at a given index
                represents the longest non-prefix substring of p (i.e.
                a substring of p that does not begin at the start of p)
                ending at the corresponding index that matches a prefix
                of p. Alternatively, as the name suggests, the ith index
                represents the length of the longest proper prefix (i.e.
                a prefix that is not the whole string) of the string
                p[:i + 1] (i.e. the substring of p consisting of the
                first i + 1 characters of p) that is also a (proper)
                suffix of p[:i + 1].
    
    Methods:
        (For more detail see the documentation of the relevant method)
        
        constructLPS(): Constructs the Longest Prefix Suffix (LPS)
                array for attribute pattern_iter using the Knuth-Morris-
                Pratt algorithm in prepartion for use in identifying
                where pattern_iter occurs as a contiguous subsequence
                in some other similar finite ordered iterable objects.
        matchStartGenerator(): Creates a generator which yields the
                indices in a given finite ordered iterable object (where
                the first element of the object has index 0) which
                represent all the start indices of contiguous subsequences
                equal to pattern_iter, yielding these indices one
                at a time in strictly increasing order.
    """
    def __init__(self, pattern: Iterable[Any]):
        self._pattern_iter = pattern
    
    @property
    def pattern_iter(self):
        return self._pattern_iter
        
    @property
    def pattern(self):
        res = getattr(self, "_pattern", None)
        if res is None:
            p_iter = self._pattern_iter
            res = p_iter if hasattr(p_iter, "__getitem__") and\
                    hasattr(p_iter, "__len__") else list(p_iter)
            self._pattern = res
        return res
    
    @property
    def lps(self):
        res = getattr(self, "_lps", None)
        if res is None:
            res = self.constructLPS()
            self._lps = res
        return res
    
    def constructLPS(self) -> List[int]:
        """
        Constructs the Longest Prefix Suffix (LPS) array for the
        pattern represented by this KnuthMorrisPratt object (i.e. the
        attribute pattern) using the Knuth-Morris-Pratt (KMP)
        algorithm, in preparation for its use for finding the pattern
        in a given iterable object (see method matchStartGenerator()).
        For a string p of length n, the LPS array is a 1D integer array
        of length n, where the integer at a given index represents
        the longest non-prefix substring of p (i.e. a substring of p that
        does not begin at the start of p) ending at the corresponding
        index that matches a prefix of p. Alternatively, as the name
        suggests, the ith index represents the length of the longest
        proper prefix (i.e. a prefix that is not the whole string)
        of the string p[:i + 1] (i.e. the substring of p consisting of the
        first i + 1 characters of p) that is also a (proper) suffix of
        p[:i + 1].
        
        Returns:
            2-tuple whose index 0 contains the pattern iterable in a
            list with elements in the same order as in the pattern
            iterable object and whose index 1 contains a list of
            integers (int) representing the LPS array of pattern
           
        Example:
            >>> kmp = KnuthMorrisPratt("abacabcabacad")
            >>> kmp.generateLPS()
            [0, 0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5, 0]
            
            This signifies for instance that the longest non-prefix
            substring ending at index 11 that matches a prefix of the
            string "abacabcabacad" is length 5 (namely the substring
            "abaca").
        """
        p = self.pattern
        lps = [0]
        j = 0
        p_iter = iter(p)
        next(p_iter)
        for l in p_iter:
            while l != p[j]:
                if not j: break
                j = lps[j - 1]
            else:
                j += 1
            lps.append(j)
        return lps
    
    def matchStartGenerator(self, s: Iterable[Any])\
            -> Generator[Any, None, None]:
        """
        Generator that yields each and every index in the finite
        ordered iterable object s at which a contiguous subsequence
        (for strings, a substring) matching the pattern represented by
        this KnuthMorrisPratt object (i.e. the attribute pattern)
        starts, using the Knuth-Morris-Pratt (KMP) Algorithm.
        
        Args:
            Required positional:
            s (iterable): The finite ordered iterable object in
                    which the start indices of occurences of the
                    pattern represented by this KnuthMorrisPratt object
                    are to be yielded.
        
        Returns:
            Generator yielding integers (int) giving the indices of s
            at which every contiguous subsequence of s matching the
            pattern represented by this KnuthMorrisPratt object (i.e.
            the attribute pattern) start, in increasing order.
        
        Example:
            >>> kmp = KnuthMorrisPratt("bb")
            >>> for i in kmp.matchStartGenerator("casbababbbbbabbceab"):
            >>>     print(i)
            7
            8
            9
            10
            13
            
            This signifies that a substrings of this string exactly
            matching "bb" begin at precisely the (0-indexed) indices 7,
            8, 9, 10 and 13 and nowhere else in the string
            "casbababbbbbabbceab".
        """
        p = self.pattern
        m = len(p)
        if not m:
            # An empty string is a substring of any given string starting
            # from any position in the given string
            yield from range(len(s))
            return
        elif m > len(s):
            # If the pattern is longer than the string, no matches
            # are possible
            return
        lps = self.lps
        j = 0
        for i, l in enumerate(s):
            while l != p[j]:
                if not j: break
                j = lps[j - 1]
            else:
                j += 1
                if j != m: continue
                yield i - m + 1
                j = lps[-1]
        return

class ZAlgorithm:
    """    
    Class implementing the Z algorithm for string searching,
    implemented to accept any finite ordered iterable object for both
    the pattern to be matched and the object(s) to be searched.

    Initialisation args:
        Required positional:
        pattern (ordered iterable container): A finite ordered
                iterable object (e.g. a string) that is the pattern to
                be found as a contiguous subsequence in other similar
                finite ordered iterable objects.
    
    Attributes:
        pattern_iter (iterable object): A finite ordered iterable
                object that is the pattern to be found as a contiguous
                subsequence in other similar objects.
    
    Methods:
        (For more detail see the documentation of the relevant method)
        
        constructZArray(): Constructs the Z array for attribute
                pattern_iter.
        matchStartGenerator(): Creates a generator which yields the
                indices in a given finite ordered iterable object (where
                the first element of the object has index 0) which
                represent all the start indices of contiguous subsequences
                equal to pattern_iter, yielding these indices one
                at a time in strictly increasing order.
    """
    def __init__(self, pattern: Iterable[Any]):
        self._pattern_iter = pattern
    
    @property
    def pattern_iter(self):
        return self._pattern_iter
    
    @property
    def pattern(self):
        res = getattr(self, "_pattern", None)
        if res is None:
            p_iter = self._pattern_iter
            res = p_iter if hasattr(p_iter, "__getitem__") and\
                    hasattr(p_iter, "__len__") else list(p_iter)
            self._pattern = res
        return res
    
    def constructZArray(self, s: List[Any]) -> List[int]:
        """
        Constructs the Z array for the finite ordered iterable object
        s.
        For a string s of length n, the Z array is a 1D integer array of
        length n, where the integer at a given index represents
        the longest substring of s starting at the corresponding
        index that matches a prefix of s.
        
        Required positional:
            s (iterable): The finite ordered iterable object for
                    which the Z array is to be calculated.
        
        Returns:
            List of integers (int) representing the Z array
            of the finite ordered iterable object s.
        
        Example:
            >>> z_alg = ZAlgorithm("")
            >>> z_alg.constructZArray("abacabcabacad")
            [13, 0, 1, 0, 2, 0, 0, 5, 0, 1, 0, 1, 0]
            
            This signifies for instance that the longest substring
            starting at index 7 that matches a prefix of the chosen
            string (i.e. "abacabcabacad") is length 5 (namely the
            substring "abaca"- note that the next character of the
            substring starting at index 7 would be "d", which does not
            match the next character for any longer prefix, which would
            be "b").
        """
        n = len(s)
        res = [0] * n
        lft, rgt = 0, 1
        for i in range(1, n):
            if res[i - lft] < rgt - i:
                res[i] = res[i - lft]
                continue
            lft = i
            for rgt in range(max(rgt, i), n):
                if s[rgt] != s[rgt - lft]: break
            else: rgt = n
            res[i] = rgt - lft
        res[0] = n
        return res
        
    def matchStartGenerator(self, s: Iterable[Any], wild: Any="$")\
            -> Generator[Any, None, None]:
        """
        Generator that yields each and every index in the finite
        ordered iterable object s at which a contiguous subsequence
        (for strings, a substring) matching the pattern represented by
        this ZAlgorithm object (i.e. the attribute pattern)
        starts, using the Z Algorithm.
        
        Args:
            Required positional:
            s (iterable): The finite ordered iterable object in
                    which the start indices of occurences of the
                    pattern represented by this ZAlgorithm object
                    are to be yielded.
        
            Optional named:
            wild_char (str): A string character which does not appear
                    in the string s (used as a separator placed between
                    p and s when they are combined in a single string
                    during the implementation of the Z algorithm to
                    ensure that the start of s cannot be inappropriately
                    treated as being part of the pattern.
                Default: "$"
        
        Returns:
            Generator yielding integers (int) giving the indices of s
            at which every contiguous subsequence of s matching the
            pattern represented by this ZAlgorithm object (i.e.
            the attribute pattern) start, in increasing order.
        
        Example:
            
            >>> z_alg = ZAlgorithm("bb")
            >>> for i in z_alg.matchStartGenerator("casbababbbbbabbceab"):
            >>>     print(i)
            7
            8
            9
            10
            13
            
            This signifies that a substrings of this string exactly
            matching "bb" begin at precisely the (0-indexed) indices 7,
            8, 9, 10 and 13 and nowhere else in the string
            "casbababbbbbabbceab".
        """
        s2 = list(self.pattern)
        m = len(s2)
        s2.append(wild)
        for l in s:
            s2.append(l)
        n2 = len(s2)
        n = n2 - m - 1
        z_arr = self.constructZArray(s2)
        res = []
        for i in range(m + 1, n):
            if z_arr[i] == m:
                yield i - m - 1
        return


def rollingHash(s: Iterable, length: int, p_lst: Union[Tuple[int], List[int]]=(37, 53),
        md: int=10 ** 9 + 7, func: Optional[Callable]=None) -> Generator[int, None, None]:
    """
    Generator that yields the rolling hash values of each contiguous subset of
    the iterable s with length elements in order of their first element. The hash
    is polynomial-based around prime numbers as specified in p_lst modulo md.
    The elements of s are passed through the function func which transforms
    each possible input value into a distinct integer (by default, the identity
    if the elements of s are integers, and the ord() function if they are
    string characters).
    
    Args:
        Required positional:
            
    
    Modified version of rolling hash can be used to solve Leetcode #1554 (Premium)
    """
    if hasattr(s, "__len__") and len(s) < length:
        return
    if func is None:
        try: val = func(next(iter_obj))
        except StopIteration: return
        if isinstance(next(iter(s), str)):
            func = lambda x: ord(x)
        else: func = lambda x: x
    iter_obj = iter(s)
    n_p = len(p_lst)
    hsh = [0] * n_p
    val_qu = deque()
    for i in range(length):
        try: val = func(next(iter_obj))
        except StopIteration: return
        val_qu.append(val)
        for j, p in enumerate(p_lst):
            hsh[j] = (hsh[j] * p + val) % md
    yield tuple(hsh)
    mults = [pow(p, length, md) for p in p_lst]
    for i in itertools.count(length):
        try: val = func(next(iter_obj))
        except StopIteration: return
        val_qu.append(val)
        for j, p in enumerate(p_lst):
            hsh[j] = ((hsh[j] - mults[j] * val_qu.popleft()) * p + val) % md
        yield tuple(hsh)
    return

def rollingHashSearch(s: str, patterns: List[str],
        p_lst: Optional[Union[List[int], Tuple[int]]]=(31, 37),
        md: int=10 ** 9 + 7) -> Dict[str, List[int]]:
    
    ord_A = ord("A")
    def char2num(l: str) -> int:
        return ord(l) - ord_A
    
    pattern_dict = {}
    for pattern in patterns:
        length = len(pattern)
        pattern_dict.setdefault(length, {})
        hsh = next(rollingHash(pattern, length, p_lst=p_lst, md=md, func=char2num))
        pattern_dict[length].setdefault(hsh, set())
        pattern_dict[length][hsh].add(pattern)
    
    res = {}
    for length, hsh_dict in pattern_dict.items():
        for i, hsh in enumerate(rollingHash(s, length, p_lst=p_lst, md=md, func=char2num)):
            if hsh not in hsh_dict.keys(): continue
            pattern = s[i: i + length]
            if pattern not in hsh_dict[hsh]: continue
            res.setdefault(pattern, [])
            res[pattern].append(i)
    return res

class AhoCorasick:
    """
    Data structure used for simultaneous matching of multiple
    patterns in a text, with time complexity O(n + m + z) where
    n is the length of the string being searched, m is the sum
    of the lengths of the patterns and z is the total number of
    matches over all of the patterns in the string.
    
    Can use for solution of Leetcode: #139, #140 and Premium Leetcode:
    #616 and #758 (basically the same problem) and #1065
    """

    def __init__(self, words: List[str]):
        self.goto = [{}]
        self.failure = [-1]
        self.out = [0]
        self.out_lens = [0]
        self.words = words
        self.buildAutomaton()

    def buildAutomaton(self) -> None:
        for i, w in enumerate(self.words):
            j = 0
            for l in w:
                if l not in self.goto[j].keys():
                    self.goto[j][l] = len(self.goto)
                    self.goto.append({})
                    self.failure.append(0)
                    self.out.append(0)
                    self.out_lens.append(0)
                j = self.goto[j][l]
            self.out[j] |= 1 << i
            self.out_lens[j] |= 1 << len(w)
        
        queue = deque(self.goto[0].values())
        
        while queue:
            j = queue.popleft()
            for l, j2 in self.goto[j].items():
                j_f = self.failure[j]
                while j_f and l not in self.goto[j_f].keys():
                    j_f = self.failure[j_f]
                j_f = self.goto[j_f].get(l, 0)
                self.failure[j2] = j_f
                self.out[j2] |= self.out[j_f]
                self.out_lens[j2] |= self.out_lens[j_f]
                queue.append(j2)
        return
    
    def _findNext(self, j: int, l: str) -> int:
        while j and l not in self.goto[j].keys():
            j = self.failure[j]
        return self.goto[j].get(l, 0)
    
    def search(self, s: str) -> Dict[str, List[int]]:
        """
        Gives dictionary for the starting index of each occurrence
        of each of self.words in the string s.
        """
        j = 0
        res = {}
        for i, l in enumerate(s):
            j = self._findNext(j, l)
            bm = self.out[j]
            for idx, w in enumerate(self.words):
                if not bm: break
                if bm & 1:
                    res.setdefault(w, [])
                    res[w].append(i - len(w) + 1)
                bm >>= 1
        return res
    
    def searchEndIndices(self, s: str) -> Generator[Tuple[int, List[int]], None, None]:
        """
        Generator yielding a 2-tuple of each index of s (in ascending order)
        and a list of the corresponding indies of the patterns in self.words
        that have a match in s that ends exactly at that index of s.
        """
        j = 0
        for i, l in enumerate(s):
            j = self._findNext(j, l)
            bm = self.out[j]
            idx = 0
            res = []
            while bm:
                if bm & 1: res.append(idx)
                idx += 1
                bm >>= 1
            yield (i, res)
        return

    def searchLengths(self, s: str) -> Generator[Tuple[int], None, None]:
        j = 0
        for i, l in enumerate(s):
            j = self._findNext(j, l)
            bm = self.out_lens[j]
            length = 0
            res = []
            while bm:
                if bm & 1: res.append(length)
                length += 1
                bm >>= 1
            yield res
        return
    
def wordBreak(self, s: str, wordDict: List[str]) -> bool:
    """
    Solution to Leetcode #139 using Aho Corasick
    """
    ac = AhoCorasick(wordDict)
    arr = [False] * len(s)
    for i, lengths in enumerate(ac.searchLengths(s)):
        for j in lengths:
            if j == i + 1: arr[i] = True
            elif j > i + 1: break
            elif arr[i - j]: arr[i] = True
            if arr[i]: break
    return arr[-1]

def wordBreak2(self, s: str, wordDict: List[str]) -> List[str]:
    """
    Solution to Leetcode #140 using Aho Corasick
    """
    n = len(s)
    ac = AhoCorasick(wordDict)
    dp = [[] for _ in range(n)]
    for (i, inds) in ac.searchEndIndices(s):
        for j in inds:
            w = wordDict[j]
            if len(w) == i + 1:
                dp[i].append(w)
                continue
            for s2 in dp[i - len(w)]:
                dp[i].append(" ".join([s2, w]))
    return dp[-1]

def addBoldTag(self, s: str, words: List[str]) -> str:
    """
    Solution to Leetcode #616 and #758 (both Premium) using Aho Corasick
    """
    # Try to make faster
    
    # Using Aho-Corasick automaton

    n = len(s)
    if not n: return s
    ac = AhoCorasick(words)
    start_dict = ac.search(s)
    if not start_dict: return s
    rngs = []
    #print(start_dict)
    words = list(start_dict.keys())
    for i, w in enumerate(words):
        rngs.append([])
        length = len(w)
        for j in start_dict[w]:
            if not rngs[i] or j > rngs[i][-1][1]:
                rngs[i].append([j, j + length])
            else: rngs[i][-1][1] = j + length
    #print(rngs)
    heap = [[rng_lst[0][0], -rng_lst[0][1], 0, idx] for idx, rng_lst in enumerate(rngs)]
    heapq.heapify(heap)

    res = []
    i1, neg_i2, j, idx = heapq.heappop(heap)
    if i1: res.append(s[:i1])
    res.append("<b>")
    bs_i = i1 # index for start of current bold
    be_i = -neg_i2 # index for current end of current bold
    if j + 1 < len(rngs[idx]):
        heapq.heappush(heap, [rngs[idx][j + 1][0], -rngs[idx][j + 1][1], j + 1, idx])
    while heap:
        i1, neg_i2, j, idx = heapq.heappop(heap)
        i2 = -neg_i2
        if i1 <= be_i:
            be_i = max(be_i, i2)
            if be_i == n: break
        else:
            res.append(s[bs_i: be_i])
            res.append("</b>")
            res.append(s[be_i: i1])
            res.append("<b>")
            bs_i = i1
            be_i = i2
            if be_i == n: break
        if j + 1 < len(rngs[idx]):
            heapq.heappush(heap, [rngs[idx][j + 1][0], -rngs[idx][j + 1][1], j + 1, idx])
    res.append(s[bs_i: be_i])
    res.append("</b>")
    if be_i < n: res.append(s[be_i:])
    return "".join(res)

def manacherAlgorithm(s: Iterable) -> List[int]:
    """
    Implementation of Manacher's algorithm to find the 1D
    array or iterable (e.g. string) with the same size as s whose
    value for each index is half the length (rounded down) of the
    longest odd-length palindromic contiguous subsequence centred
    on the corresponding element of s.

    Args:
        Required positional:
        s (iterable): An ordered array to be processed

    Returns:
    A list of integers (int) with length equal to that of s, whose
    element at index i (0-indexed) gives half the length rounded
    down of the longest odd-length contiguous palindromic subsequence
    of s centred on that index.

    Examples:
        >>> manacherAlgorithm("ebabad")
        [0, 0, 1, 1, 0, 0]

        This signifies for instance that the longest odd-length
        palindromic contiguous subsequence centred on the character
        at index 2 (zero-indexed, so the character "a") has a rounded
        down half length of 1, i.e. a full length of 3, which
        corresponds to the substring from indices 1 to 3 inclusive,
        "bab".

        >>> manacherAlgorithm(['#', 'e', '#', 'b', '#', 'a', '#', 'b', '#', 'a', '#', 'a', '#', 'b', '#', 'd', '#'])
        [0, 1, 0, 1, 0, 3, 0, 3, 0, 1, 4, 1, 0, 1, 0, 1, 0]

        This signifies for instance that the longest odd-length
        palindromic contiguous subsequence centred on the character
        at index 5 (zero-indexed, so the element 'a') has a rounded
        down half length of 3, i.e. a full length of 7, which
        corresponds to the contiguous subsequence from indices 2 to
        8 inclusive, ['#', 'b', '#', 'a', '#', 'b', '#'], and the
        longest odd-length palindromic contiguous subsequence centred
        on the character at index 10 (zero-indexed, so the element '#'
        between the two 'a' elements) has a rounded down half length
        of 4, i.e. a full length of 9, which corresponds to the
        contiguous subsequence from indices 6 to 14 inclusive,
        ['#', 'b', '#', 'a', '#', 'a', '#', 'b', '#'].
        This example demonstrates how by preprocessing the original
        array with identical wild characters between each element
        and at each end, Manacher's algorithm can find the lengths
        of any palindromic contiguous subsequences (i.e. both odd
        and even length), with those centred on the wild characters
        being the even length palindromes. Indeed, the value actually
        gives the exact length of the corresponding palindrome in the
        original array.
    """
    n = len(s)
    curr_centre = 0
    curr_right = 0
    max_val = 0
    max_i = 0
    res = [0] * n
    for i in range(n):
        if i < curr_right:
            mirror = (curr_centre << 1) - i
            res[i] = min(res[mirror], curr_right - i)
        while i - res[i] - 1 >= 0 and i + res[i] + 1 < len(s) and\
                s[i + res[i] + 1] == s[i - res[i] - 1]:
            res[i] += 1
        if res[i] > max_val:
            max_val = res[i]
            max_i = i
        if i + res[i] > curr_right:
            curr_right = i + res[i]
            curr_centre = i
    return res

def longestPalindromicSubstrings(s: str) -> Tuple[str]:
    """
    Uses Manacher's algorithm to find all palindromic
    substrings of s for which there are no longer
    palindromic substrings in s

    
    """
    if not s: return [""]
    n = len(s)
    s2 = ["#"] * ((n << 1) + 1)
    for i, l in enumerate(s):
        s2[(i << 1) + 1] = l
    manacher_arr = manacherAlgorithm(s2)
    mx_len = -1
    mx_i = []
    for i, num in enumerate(manacher_arr):
        if num < mx_len: continue
        elif num > mx_len:
            mx_len = num
            mx_i = []
        mx_i.append(i)
    res = []
    for i in mx_i:
        j1 = (i - mx_len) >> 1
        res.append(s[j1:j1 + mx_len])
    return tuple(res)

def longestPalindrome(self, s: str) -> str:
    """
    Uses Manacher's algorithm to find the unique palindromic
    substring of s for which there are no longer palindromic
    substrings in s and there are no palindromic substrings
    of s with the same length and a smaller starting index
    in s.

    Example:
        >>> longestPalindrome("ebabad")
        "bab"

    Solution to Leetcode #5- Longest Palindromic Substring
    
    Original problem description:
    
    Given a string s, return the longest palindromic substring in s.
    """
    return longestPalindromicSubstrings(s)[0]

def countPalindromicSubstrings(self, s: str) -> int:
    """
    
    Solution to Leetcode #647- Palindromic Substrings
    
    Original problem description:
    
    Given a string s, return the number of palindromic substrings in
    it.

    A string is a palindrome when it reads the same backward as
    forward.

    A substring is a contiguous sequence of characters within the
    string.
    """
    n = len(s)
    s2 = ["#"] * ((n << 1) + 1)
    for i, l in enumerate(s):
        s2[(i << 1) + 1] = l
    manacher_arr = manacherAlgorithm(s2)
    return sum((x + 1) >> 1 for x in manacher_arr)