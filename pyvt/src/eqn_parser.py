import re
import numpy as np

class DataTabular():

    symblist  = []
    arraylist = []

    def __init__(self):
        pass

    def add_name(self, varname):
        self.symblist.append(varname)

    def add_array(self, array):
        self.arraylist.append(array)

# Functions
def parentheses_enclosed(s):
    paren_order = re.findall(r'[\(\)]', s)
    
    if paren_order.count('(') != paren_order.count(')'):
        return False
    
    curr_levels = []
    nest_lv = 0
    for p in paren_order:
        if p == '(':
            nest_lv += 1
        else:
            nest_lv -= 1
        curr_levels.append(nest_lv)
    if 0 in curr_levels[:-1]:
        return False
    else:
        return True

def remove_matched_parentheses(s):
    if ')' in s:
        # find the first ')'
        end = s.find(')')
        # find the last '(' before the first ')'
        start = max([i for i, char in enumerate(s[:end]) if char == '(' ])
        # remove the parentheses
        return remove_matched_parentheses(s[:start] + s[end+1:])
    else:
        return s

def interpret(f, dt):

    for index in range(len(dt.symblist)):
        if dt.symblist[index] == f:
            return dt.arraylist[index]
   
    if re.match(r'\A\(.+\)\Z', f) and parentheses_enclosed(f): 
        return interpret(f[1:-1], dt) 

    if f.replace('.', '', 1).isdigit():
        return float(f)

    rest_f = remove_matched_parentheses(f)

    if '+' in rest_f: 
        comps = re.compile(r'[\+]').split(f)
    elif '-' in rest_f:
        comps = re.compile(r'[\-]').split(f)
    elif '*' in rest_f:
        comps = re.compile(r'[\*]').split(f)
    else:
        comps = re.compile(r'[\/]').split(f)
    
    if comps[0].count('(') != comps[0].count(')'):
        nested_level = comps[0].count('(') - comps[0].count(')')
        pos = len(comps[0])
        for comp in comps[1:]:
            if '(' in comp:
                nested_level += comp.count('(')
            if ')' in comp:
                nested_level -= comp.count(')')
            pos += len(comp) + 1  # +1 because of the operator inside parenthesis
            if nested_level == 0:
                break
    else:
        pos = len(comps[0])

    left = f[:pos]  # left component
    right = f[pos+1:]  # right component
    operator = f[pos]  # the operator
    
    if operator == '+':
        return interpret(left, dt) + interpret(right, dt)
    elif operator == '-':
        return interpret(left, dt) - interpret(right, dt)
    elif operator == '*':
        return interpret(left, dt) * interpret(right, dt)
    elif operator == '/':
        denominator = interpret(right, dt)
        #if denominator == 0 or denominator is np.nan:
        if 0 in denominator: 
            return np.nan
        else:
            return interpret(left, dt) / interpret(right, dt)

    return np.nan


#print(interpret(f, dt))

