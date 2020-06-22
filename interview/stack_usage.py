from . import stack
import sys


def main(input_str):
    brackets = {')': '(', ']': '[', '}': '{'}
    bracket_stack = stack.Stack('')

    for bracket in input_str:
        if bracket in brackets.values():
            bracket_stack.push(bracket)
        elif bracket in brackets.keys():
            if bracket_stack.pop() != brackets[bracket]:
                return 'Несбалансированно'
        else:
            return 'Несбалансированно'

    return 'Сбалансированно'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: using_stack.py <string_with_brackets>')
        exit(1)

    input_str = sys.argv[1]
    main(input_str)
