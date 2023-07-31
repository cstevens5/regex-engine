# This project will be a regex engine.
# The user will enter a regular expression and the expression will
# be converted to the corresponding finite automata.
# The user can then input strings to see if the regular expression
# matches with that string.

# I will create a class to represent a finite state machine
class Fsm:
    def __init__(self, alphabet: list, states: list, start: int, \
                 final_states: list, transitions: list) -> None:
        self.alphabet = alphabet
        self.states = states
        self.start = start
        self.final_states = final_states
        self.transitions = transitions
    # creates a string representation of the current fsm
    def to_str(self):
        sigma = "Alphabet: " + str(self.alphabet) + "\n"
        states = "States: " + str(self.states) + "\n"
        start = "Start: " + str(self.start) + "\n"
        final = "Final: " + str(self.final_states) + "\n"
        trans_header = "Transitions: [\n"
        thlen = len(trans_header)
        translist = ""
        for t in self.transitions:
            translist += " " * thlen + str(t)+ "\n"
        translist += " " * thlen + "]"
        transitions = trans_header + translist
        ret = sigma + states + start + final + transitions
        return ret

# creates an nfa for a single character
# will be useful when converting from regex to an nfa
def char(c: str) -> Fsm:
    return Fsm([c], [0, 1], 0, [1], [(0, c, 1)])

# concatenates two nfa's
def concat(nfa1, nfa2):
    new_states = []
    new_states.extend(nfa1.states)
    # renaming all the nfa2 states
    for i in range(len(new_states), len(new_states) + len(nfa2.states)):
        new_states.append(i)
    transitions = []
    transitions.extend(nfa1.transitions)
    # now rename the nfa2 transitions
    for s1, symbol, s2 in nfa2.transitions:
        transitions.append((s1 + len(nfa1.states), symbol, \
                            s2 + len(nfa1.states)))
    # now add epsilon transtions from each final state in nfa1 to
    # the start state of nfa2
    for state in nfa1.final_states:
        transitions.append((state, 'epsilon', \
                            nfa2.start + len(nfa1.states)))
    # merge the alphabets
    sigma = []
    sigma.extend(nfa1.alphabet)
    sigma.extend(nfa2.alphabet)
    sigma = list(set(sigma))
    # create the final states list - this will just be all of the
    # final states from nfa2
    final = []
    for state in nfa2.final_states:
        final.append(state + len(nfa1.states))
    # finally we can return the concatenated nfa
    return Fsm(sigma, new_states, 0, final, transitions)

# returns an nfa that is the union of the two nfa parameters
def union(nfa1, nfa2):
    new_states = [0]
    # rename all the nfa1 and nfa2 states
    for i in range(1, len(nfa1.states) + len(nfa2.states) + 1):
        new_states.append(i)
    transitions = []
    # now rename all the nfa1 transitions
    # the new state names will be the previous name + 1
    for s1, symbol, s2 in nfa1.transitions:
        transitions.append((s1 + 1, symbol, s2 + 1))
    # renaming all nfa2 transitions
    # new state names will be the previous name + len(nfa1.states) + 1
    for s1, symbol, s2 in nfa2.transitions:
        transitions.append((s1 + len(nfa1.states) + 1, symbol, \
                            s2 + len(nfa1.states) + 1))
    # now we can add transitions from the new start state the 
    # start state of nfa1 and the start state of nfa2 over epsilon
    transitions.append((0, 'epsilon', nfa1.start + 1))
    transitions.append((0, 'epsilon', nfa2.start + len(nfa1.states) + 1))
    # the end states for the new nfa will be the list of nfa1.final_states
    # merged with nfa2.final_states
    end_states = []
    for state in nfa1.final_states:
        end_states.append(state + 1)
    for state in nfa2.final_states:
        end_states.append(state + len(nfa1.states) + 1)
    # now we merge the alphabets
    sigma = []
    sigma.extend(nfa1.alphabet)
    sigma.extend(nfa2.alphabet)
    sigma = list(set(sigma))
    # now we can return the union of the two nfa parameters
    return Fsm(sigma, new_states, 0, end_states, transitions)

# function that applies the plus operation to the passed in nfa
def plus(nfa):
    # epsilon transitions will be added from each end state to
    # the start state
    transitions = nfa.transitions
    for state in nfa.final_states:
        transitions.append((state, 'epsilon', nfa.start))
    return Fsm(nfa.alphabet, nfa.states, nfa.start, nfa.final_states, \
               transitions)

# function that applies the kleene star operation to the passed
# in nfa parameter
def star(nfa):
    new_states = [0]
    # rename the nfa states to the previous name + 1 to account for 
    # the new start state
    for i in range(1, len(nfa.states) + 1):
        new_states.append(i)
    # now we will rename all the nfa transitions using the new state
    # names
    transitions = []
    for s1, symbol, s2 in nfa.transitions:
        transitions.append((s1 + 1, symbol, s2 + 1))
    # now we must add an epsilon transition from the new start
    # state to the previous start state
    transitions.append((0, 'epsilon', nfa.start + 1))
    # add epsilon transitions from each final state in the nfa to the
    # new start state
    for state in nfa.final_states:
        transitions.append((state + 1, 'epsilon', 1))
    # we also must add the new start state to the list of
    # accepting states
    end_states = [0]
    # add the appropriate end states from the nfa to the new list
    # of end states
    for state in nfa.final_states:
        end_states.append(state + 1)
    # finally, we can return the new nfa
    return Fsm(nfa.alphabet, new_states, 0, end_states, transitions)

# returns true if the character parameter is an operand in a regular
# expression, false if it is an operator
def is_operand(character):
    if character >= 'a' and character <= 'z':
        return True
    elif character >= 'A' and character <= 'Z':
        return True
    elif character >= '0' and character <= '9':
        return True
    return False

# This function takes in a regulare expression and puts the expression
# in infix form. Returns a new string containing the infix form of
# regular expression parameter.
def to_infix_form(regex: str) -> str:
    indices = []
    new_str = regex[:]
    for i in range(len(regex) - 1):
        c1 = regex[i]
        c2 = regex[i + 1]
        if is_operand(c1) or c1 == ')' or c1 == '*' or c1 == '+':
            if is_operand(c2) or c2 == '(':
                indices.append(i)
    
    for i in range(len(indices)):
        index = indices[i]
        new_str = new_str[:index + i + 1] + "." + new_str[index + i + 1:]

    return new_str

# This function takes in a regular expression in infix form and converts
# it to postfix form. This function is necessary because Thompson's 
# construction (used in create_nfa) only works if the given regular
# expression is in postfix form. A new string containing the postfix
# form will be returned.
def infix_to_postfix(infix_regex: str) -> str:
    # we will use a stack to convert between forms
    stack = []
    postfix = ''
    precedence = {'*' : 3, '+' : 3, '.' : 2, '|' : 1}

    # loop through all charcters in infix_regex
    for ch in infix_regex:
        # if the char is an operand or is the '*' operator, we will
        # add it to the postfix string
        if is_operand(ch) or ch == '*' or ch == '+':
            postfix += ch
        # opening parenthesis will be added to the stack
        elif ch == '(':
            stack.append(ch)
        # if closing parenthesis, we will pop elements from the stack
        # and add them to postfix until an opening parenthesis is reached
        elif ch == ')':
            while len(stack) > 0 and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        else:
            while len(stack) > 0 and (stack[-1] == '*' or \
                stack[-1] == '.') and precedence[ch] <= \
                precedence[stack[-1]]:
                postfix += stack.pop()
            stack.append(ch)
    
    # now flush out the rest of the stack
    while len(stack) > 0:
        postfix += stack.pop()
    
    # finally we can return the regular expression in postfix form
    return postfix


# This function takes in a regular expression in postfix form and 
# returns a corresponding epsilon nfa. Thompson's construction is 
# used here to easily convert the regular expression to an nfa.
def create_nfa(postfix_regex: str) -> Fsm:
    stack = []
    # for this algorithm, we will loop through each character in the
    # regex parameter and perform operations based on the character
    for ch in postfix_regex:
        # if the current character is an operand, then we will create
        # a single character nfa and push it to the stack
        if is_operand(ch):
            stack.append(char(ch))
        # '.' means concatenation, so we will pop two nfa's from the 
        # stack, concatenate them, and then push the new nfa onto
        # the stack. Since the regex is in postfix form, there should
        # always be at least 2 elements in the stack when this case
        # evaluates to true.
        elif ch == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concat(nfa1, nfa2))
        # The next case will be union. In this case we will
        # again pop two nfa's from the stack, union them, and then
        # push the resulting nfa onto the stack.
        elif ch == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(union(nfa1, nfa2))
        # Another case is when the '+' operator is used. This operator
        # specifies that the previous item on the stack must occur
        # one or more times.
        elif ch == '+':
            stack.append(plus(stack.pop()))
        # The last case will be applying the Kleene star operation
        # to an nfa. We will pop an nfa from the stack, apply the
        # star operation, and then push the new nfa onto the stack.
        elif ch == '*':
            stack.append(star(stack.pop()))
        # if none of the if clauses are true, then some error has 
        # occurred or the expression is not valid
        else:
            print("Something went wrong. Please try again.")
            quit()

    # Now there should only be one nfa left in the stack and this
    # is our final nfa. We can just return this.
    return stack.pop()

# takes a regular expression and returns an nfa that represents
# the given expression
def re_to_nfa(regex: str) -> Fsm:
    return create_nfa(infix_to_postfix(to_infix_form(regex)))

# Returns a list of states that are reachable when moving on the 
# specified symbol. The returned states must be reachable by moving
# from some state in states on the given symbol.
def move(symbol, states: list, nfa: Fsm) -> list:
    # if symbol is not in the alphabet, we will return an empty list
    ret = set()
    if symbol != 'epsilon' and symbol not in nfa.alphabet:
        return []
    # now we loop through the transitions in the nfa and add the 
    # correct states to the return list
    for s1, sym, s2 in nfa.transitions:
        if sym == symbol and s1 in states:
            ret.add(s2)
    # cast ret to a list and then return
    return list(ret)

    

# Returns a list of states that are the result of performing an
# epsilon closure on the given states. The returned list will
# contain all of the original states, and all states reachable by
# moving on epsilon from the orignal states.
def e_closure(states: list, nfa: Fsm) -> list:
    # first create a set and add all states in the states list
    # to the set
    ret = []
    ret.extend(states)
    for s in ret:
        lst = move('epsilon', [s], nfa)
        for state in lst:
            if state not in ret:
                ret.append(state)
    return ret


# Converts the nfa parameter to it's corresponding dfa.
# The newly created dfa will be returned.
def nfa_to_dfa(nfa):
    states = []
    start_state = e_closure([nfa.start], nfa)
    # add the first state to the list
    states.append(start_state)

    sigma = nfa.alphabet
    sigma.sort()
    transitions = []
    # now we will loop through each state in states and move on each
    # character in the alphabet for each state
    for s in states:
        for letter in sigma:
            temp = e_closure(move(letter, s, nfa), nfa)
            # if temp is not empty, then we need to add a transition
            # from states[i] to the returned state
            if temp != []:
                if temp not in states:
                    states.append(temp)
                j = states.index(temp)
                # now we need to add a transition from states[i] to 
                # states[j] over letter. The transition will use i
                # and j as the new state names
                transitions.append((states.index(s), letter, j))
    
    # The start state of the new dfa will be 0, the state at 
    # states[0]
    # Now we must loop through states again to determine which
    # states will be end states in the new dfa
    end_states = []
    for i in range(0, len(states)):
        for elt in states[i]:
            if elt in nfa.final_states:
                end_states.append(i)
    
    new_states = [0] * len(states)
    for i in range(0, len(states)):
        new_states[i] = i
    
    # now we can just return the new dfa
    return Fsm(sigma, new_states, 0, end_states, transitions)



# Function to check whether the string parameter is accepted by
# the nfa parameter. Returns true if so, false otherwise
def accept(s: str, nfa):
    # First we will convert the nfa parameter to it's corresponding 
    # dfa. This is done because dfa's have unique transitions, which
    # makes them easier to represent as a string.
    dfa = nfa_to_dfa(nfa)

    new_str = ''
    current_state = dfa.start

    # now we loop through each letter in s and check if a transition
    # from the current state over the letter exists
    for letter in s:
        # check for a transition
        for state1, symbol, state2 in dfa.transitions:
            if state1 == current_state and symbol == letter:
                new_str += letter
                current_state = state2
                break
    
    # now we can return true if new_str is the same as s and 
    # current state is in the dfa's list of end states
    return new_str == s and current_state in dfa.final_states
