# Regular Expression Engine

A regular expression engine written in python

## Overview

The main purpose of this project is to test what strings are accepted by a particular regular expression. This is done by converting the regular expression to it's equivalent finite state machine, and then using the finite state machine to determine if a string is accepted. Thompson's construction is used to convert the regular expression to an equivalent nfa (nondeterministic finite automaton). From there, the nfa can then be converted to an equivalent dfa (deterministic finite automaton) using the subset construction conversion method. The new dfa can then be traversed to determine whether or not the string is accepted. In order to use this engine, a regular expression string must be passed to the re_to_nfa() function, which creates and returns the equivalent nfa. Then the created nfa can be passed to the accept() function along with whatever string is being tested. The accept() function will return True if the string is accepted by the nfa, and false if the string is not accepted.

## Examples

Say you are trying to see what strings are matched by the regular expression "(abc)\*".
You would create the nfa and then test strings in the following way:

```python
nfa = re_to_nfa("(abc)*")
assert(accept("abc", nfa))
assert(accept("", nfa))
assert(accept("abcabcabc", nfa))
assert(not accept("abcccc", nfa))
assert(not accept("ab", nfa))
```

All of the above assertions should pass.

## Installation

First you should copy the github repository by entering the following command in the terminal or command prompt:

```
git clone https://github.com/cstevens5/regex-engine
```

Once you have copied the repository you can create your own files to test the code, or you can run the existing tests that I have created.
To run the existing tests, simply enter the following command while in the project directory:

```
pytest
```
