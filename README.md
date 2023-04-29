# Python C-to-Java Compiler

This project is a C-to-Java compiler developed in Python. It is divided into several parts, including the Lexer, Parser, Type Checking, and Code Generation. Below are the instructions and notes for each part of the project.

## Part 1: Lexer

1. Copy `mycc.py` and `lexer1.py` to the Pyrite directory.
2. Run the command: `python3 ./mycc.py -1 testfile` (e.g., `tricky.c`)

_Note_: Initially, the regular expression method was used, but it was difficult to handle multiple lines of comments and strings. The alternative approach reads character by character.

## Part 3: Parser

1. Copy `parser1.py` and `lexer2.py` to the Pyrite directory.
2. Run the command: `python3 ./parser1.py -3 testfile` (e.g., `test1.c`)

_Notes_:

- The LL(1) method was initially used, but due to conflicts in the grammar, the LL(K) method was adopted.
- The parser uses a recursive descent method to match the grammar.
- The implementation does not support `const struct` (test3.c, line 17).

## Part 4: Type Checking

1. Copy `typechecking.py` to the existing directory containing `lexer2.py` and `parser1.py`.
2. Run the command: `python3 ./typechecking.py -4 testfile` (e.g., `test1.c`)

_Notes_:

- Bugs fixed in Part 3:
  - Allow `const` parameters.
  - Allow `struct` list in `strucdef`.
  - Allow `structdec` in function body, but not in parameters.
  - Allow multiple `vardec`.
  - Fixed bugs in `parse_lval` function to work with `A[]`.

## Part 5: Code Generation

1. Copy `codegen.py` and `lexer2.py` to the Pyrite directory.
2. Run the command: `python3 ./codegen.py -5 testfile`

## Part 6: Code Generation 2 - Flow Control

1. Copy `codegen.py` and `lexer2.py` to the Pyrite directory.
2. Run the command: `python3 ./codegen.py -6 testfile`

_Note_: Parts 5 and 6 are not completed. Partial credit is requested to check if the grade is sufficient for graduation. Thank you for your understanding.

## Part 2: Include, Define, and Ifdef for Lexer1

1. Copy `part2` to the Pyrite directory.
2. Run the command: `python3 ./part2.py -2 testfile`

_Notes_:

- The implementation works well for `include`, but there are still bugs in `define` and nested `ifdef`.
