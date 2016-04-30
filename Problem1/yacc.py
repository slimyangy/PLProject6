import ply.yacc as yacc

# Get the token map from the lexer.  This is required.

from lex import tokens

DEBUG = True

# Namespace & built-in functions

#############
name = {}
variables = {}

def cons(l):
    return [l[0]] + l[1]

name['cons'] = cons

def concat(l):
    return l[0] + l[1]

name['concat'] = concat

def listar(l):
    return l

name['list'] = listar

def car(l):
    return l[0][0]

name['car'] = car

def cdr(l):
    return l[0][1:]

name['cdr'] = cdr

def eq(l):
    return l[0] == l[1]

name['eq'] = eq
name['='] = eq

def _and(l):
    return not False in l

name['and'] = _and

def _or(l):
    return True in l

name['or'] = _or

def cond(l):
    if l[0]:
        return l[1]

name['cond'] = cond

def add(l):
    return sum(l)

name['+'] = add

def minus(l):
    '''Unary minus'''
    return l[0] - l[1]

name['-'] = minus

# added a multiplication function
def mult(l):
    return l[0] * l[1]

name['*'] = mult

# added a division function
def div(l):
    if l[1] == 0:
        print "0 in denominator you noob"
    else:
        return l[0] / float(l[1])

name['/'] = div

def _print(l):
    print lisp_str(l[0])

name['print'] = _print

#  Evaluation functions

def lisp_eval(simb, items):
    if simb in name:
        return call(name[simb], eval_lists(items))
    else:
       return [simb] + items

# function caller

def call(f, l):
    try:
        return f(eval_lists(l))  
    except TypeError:
        return f

# list evaluator

def eval_lists(l):
    r = []
    for i in l:
        if is_list(i):
            if i:
                r.append(lisp_eval(i[0], i[1:]))
            else:
                r.append(i)
        else:
            r.append(i)
    return r

# Utilities functions

def is_list(l):
    return type(l) == type([])

def lisp_str(l):
    if type(l) == type([]):
        if not l:
            return "()"
        r = "("
        for i in l[:-1]:
            r += lisp_str(i) + " "
        r += lisp_str(l[-1]) + ")"
        return r
    elif l is True:
        return "#t"
    elif l is False:
        return "#f"
    elif l is None:
        return 'nil'
    else:
        return str(l)

# BNF
# Backus-Naur Format

def p_exp_atom(p):
    'exp : atom'
    p[0] = p[1]

def p_exp_qlist(p):
    'exp : quoted_list'
    p[0] = p[1]

# doublecall allows to clear the variable 'a'

def p_exp_doublecall(p):
    'exp : LPAREN call call RPAREN'
    p[0] = p[3]
    # clear the variable as per instructions when this type of call is used
    variables.clear()

def p_exp_call(p):
    'exp : call'
    p[0] = p[1]

def p_quoted_list(p):
    'quoted_list : QUOTE list'
    p[0] = p[2]

def p_list(p):
    'list : LPAREN items RPAREN'
    p[0] = p[2]

def p_items(p):
    'items : item items'
    p[0] = [p[1]] + p[2]

def p_items_empty(p):
    'items : empty'
    p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_item_atom(p):
    'item : atom'
    p[0] = p[1]

def p_item_list(p):
    'item : list'
    p[0] = p[1]

def p_item_list(p):
    'item : quoted_list'
    p[0] = p[1]
        
def p_item_call(p):
    'item : call'
    p[0] = p[1]

def p_item_empty(p):
    'item : empty'
    p[0] = p[1]

# easiest way is to allow call to recognize let and if
# refer back to the lexer

def p_let(p):
    'call : LPAREN LET LPAREN SIMB NUM RPAREN RPAREN'
    variables[p[4]] = p[5]
    print p[4], "->", p[5]

def p_let2(p):
    'call : LET LPAREN SIMB NUM RPAREN'
    variables[p[3]] = p[4]
    print p[3], "->", p[4]

def p_if(p):
    '''call : LPAREN IF bool NUM NUM RPAREN'''
    if p[3]:
        p[0] = p[4]
    else:
        p[0] = p[5]

def p_call(p):
    'call : LPAREN SIMB items RPAREN'
    if DEBUG: print "Calling", p[2], "with", p[3]
    p[0] = lisp_eval(p[2], p[3])   

# alter simbol
def p_atom_simbol(p):
    'atom : SIMB'
    try:
        p[0] = variables[p[1]]
    except LookupError:
        p[0] = p[1]

def p_atom_bool(p):
    'atom : bool'
    p[0] = p[1]

def p_atom_num(p):
    'atom : NUM'
    p[0] = p[1]

def p_atom_word(p):
    'atom : TEXT'
    p[0] = p[1]

def p_atom_empty(p): 
    'atom :'
    pass

def p_true(p):
    'bool : TRUE'
    p[0] = True

def p_false(p):
    'bool : FALSE'
    p[0] = False

def p_nil(p):
    'atom : NIL'
    p[0] = None

# Error rule for syntax errors
def p_error(p):
    print "Syntax error!! ",p

# Build the parser
# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")
yacc.yacc()


