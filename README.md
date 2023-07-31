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

## FSM Class

This project uses a class to represent finite state machine objects. An FSM class allows the project to adhere to object oriented design principles. It also allows for cleaner and easier to read code. The FSM class contains 5 fields, a constructor (**init**() method), and a to_str() method. The to_str() method was created for testing purposes and doesn't have any applications to the actual project. The 5 fields are:

    1. alphabet - a finite list of characters
    2. states - a list of the states in the current FSM
    3. start - the starting state of the FSM
    4. final_states - a list of accepting states in the FSM
    5. transitions - a list of tuples that contains all of the transitions in the current FSM

The states of the FSM will always be integers, so the states field is a list of integers, the start field is a single integer, and the final_states field is also a list of integers.

The transitions field is a list of tuples that represent the FSM's transitions. Each tuple contains 3 elements. The first element is the state being transitioned from, the second element is the character of the transition, and the third element is the state that is being transitioned to.
Examples:

```python
(1, 'a', 2)  # transition from state 1 to state 2 over the character 'a'
(0, 'epsilon', 1)  # transition from state 0 to state 1 over epsilon (an empty charcter)
```

## Infix and Postfix Notation

Infix and postfix notations are ways of representing regular expressions. Infix form is a representation where the operators are placed between the operands. When converting a regular expression to an nfa, the regular expression will first be converted to infix form. This is done because it is easy to convert from infix form to postfix form.

Once in infix form, the regular expression will then be converted to postfix form. Postfix form is a notation where the operators appear after the operands. It is necessary to convert the expression to postfix form in order for Thompson's construction to work properly.

## Thompson's Construction

Thompson's construction is an algorithm for converting a regular expression to an nfa. The algorithm creates nfa's for subexpressions of the regular expression and stores these nfa's in a stack. The regular expression is traversed left to right, and by the end of the regular expression the final nfa will be the only object left in the stack. The rules for the algorithm are as follows:

    - If the current character is an operand, then a single character nfa is created and pushed onto the stack.
    - If the current character represents concatenation ('.'), two nfa's are popped from the stack and concatenated together. The concatenated nfa is then pushed to the stack.
    - If the current character represents a union ('|'), two nfa's are popped from the stack and unioned together. The unioned nfa is then pushed to the stack.
    - If the curerent character represents a closure/kleene star expression, one nfa is popped from the stack and the closure is applied to it. The new nfa is then pushed onto the stack.

When the algorithm finishes running, the final nfa in the stack is popped and Thompson's construction is complete.

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
