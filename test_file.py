from main import char, concat, union, plus, star, to_infix_form, \
    infix_to_postfix, create_nfa, re_to_nfa, move, e_closure, \
    nfa_to_dfa, accept
from main import Fsm


# tests that the to_infix_form() function works as intended
def test_infix_form():
    assert(to_infix_form('abc') == 'a.b.c')
    assert(to_infix_form('a*') == 'a*')
    assert(to_infix_form('a*b(c|d)') == 'a*.b.(c|d)')

# tests that the infix_to_postfix() function works as intended
def test_infix_to_postfix():
    nfa = create_nfa(infix_to_postfix(to_infix_form('a*b(c|d)')))
    print(nfa.to_str())
    assert(accept('abc', nfa))
    assert(accept('abd', nfa))

# tests that the char() function creates the correct nfa
def test_char():
    nfa = char('a')
    assert(nfa.alphabet == ['a'])
    assert(nfa.states == [0, 1])
    assert(nfa.start == 0)
    assert(nfa.final_states == [1])
    assert(nfa.transitions == [(0, 'a', 1)])

# tests that the concat() function correctly concatenates the nfa
# parameters
def test_concat():
    nfa = concat(char('a'), char('b'))
    print(nfa.to_str())
    assert(set(nfa.alphabet) == set(['a', 'b']))
    assert(set(nfa.states) == set([0, 1, 2, 3]))
    assert(nfa.start == 0)
    assert(nfa.final_states == [3])
    assert(set(nfa.transitions) == set([(0, 'a', 1), (1, 'epsilon', 2), \
                                        (2, 'b', 3)]))

# tests that the union() function correctly unions the nfa parameters
def test_union():
    nfa = union(char('a'), char('b'))
    assert(set(nfa.alphabet) == set(['a', 'b']))
    assert(set(nfa.states) == set([0, 1, 2, 3, 4]))
    assert(nfa.start == 0)
    assert(set(nfa.final_states) == set([2, 4]))
    assert(set(nfa.transitions) == set([(0,'epsilon',1), (0,'epsilon',3), \
                                (1,'a',2), (3,'b',4)]))

# tests that the plus() function works as intended
def test_plus():
    nfa = plus(char('a'))
    assert(nfa.alphabet == ['a'])
    assert(set(nfa.states) == set([0, 1]))
    assert(nfa.start == 0)
    assert(nfa.final_states == [1])
    assert(set(nfa.transitions) == set([(0,'a',1), (1,'epsilon',0)]))

# tests that the star() function works as intended
def test_star():
    nfa = star(char('a'))
    assert(nfa.alphabet == ['a'])
    assert(set(nfa.states) == set([0, 1, 2]))
    assert(nfa.start == 0)
    assert(set(nfa.final_states) == set([0, 2]))
    assert(set(nfa.transitions) == set([(0,'epsilon',1), (1,'a',2), \
                                        (2,'epsilon',1)]))

# tests that the nfa to dfa conversion works as intended
def test_nfa_to_dfa():
    # testing dfa conversion of a union
    dfa1 = nfa_to_dfa(union(char('a'), char('b')))
    assert(set(dfa1.alphabet) == set(['a', 'b']))
    assert(set(dfa1.states) == set([0, 1, 2]))
    assert(dfa1.start == 0)
    assert(set(dfa1.final_states) == set([1, 2]))
    assert(set(dfa1.transitions) == set([(0,'a',1), (0,'b',2)]))

    # dfa conversion of a concatenation
    dfa2 = nfa_to_dfa(concat(char('a'), char('b')))
    assert(set(dfa2.alphabet) == set(['a', 'b']))
    assert(set(dfa2.states) == set([0, 1, 2]))
    assert(dfa2.start == 0)
    assert(dfa2.final_states == [2])
    assert(set(dfa2.transitions) == set([(0,'a',1), (1,'b',2)]))
    
    # dfa conversion for the kleene star operation
    dfa3 = nfa_to_dfa(star(char('a')))
    assert(dfa3.alphabet == ['a'])
    assert(set(dfa3.states) == set([0, 1]))
    assert(dfa3.start == 0)
    assert(set(dfa3.final_states) == set([0, 1]))
    assert(set(dfa3.transitions) == set([(0,'a',1), (1,'a',1)]))
    
# tests a very basic case of creating an nfa from a regular expression
# and testing the strings it accepts
def test_accept1():
    nfa = re_to_nfa('a*')
    print(nfa.to_str())
    assert(accept('', nfa))
    assert(accept('a', nfa))
    assert(accept('aaaa', nfa))
    assert(accept('aaaaaaaaaaa', nfa))
    assert(not accept('aaaabbb', nfa))
    assert(not accept('aaad', nfa))

def test_accept2():
    nfa = re_to_nfa('a+b')
    assert(accept('ab', nfa))
    assert(accept('aaaaaaab', nfa))
    assert(not accept('', nfa))
    assert(not accept('aaaaaaa', nfa))
    assert(not accept('b', nfa))


def test_accept3():
    nfa = re_to_nfa('(ab)*cd(x|y)*')
    assert(accept('cd', nfa))
    assert(accept('abcdxy', nfa))
    assert(accept('abababcdxxxxyyxxyx', nfa))
    assert(not accept('', nfa))

    nfa2 = re_to_nfa('(ab)*cd(x|y)+')
    assert(accept('cdx', nfa2))
    assert(not accept('cd', nfa2))

def test_accept4():
    nfa = re_to_nfa('(ab)+')
    assert(accept('ab', nfa))
    assert(accept('abababab', nfa))
    assert(not accept('', nfa))
    assert(not accept('abababa', nfa))
    assert(not accept('aba', nfa))