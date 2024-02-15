'''
Assembler macros
'''

import logging

from instructions.operands import get_operand_opcode
from utils import utils
from utils.errors import AldebaranError
from .tokenizer import Token, TokenType, Reference


logger = logging.getLogger(__name__)


class Macro:
    '''
    Macro base class
    '''

    param_count = (None, None)
    substitute_variables_in_params = None
    param_types = None
    param_type_list = None

    def __init__(self, assembler, source_line, line_number):
        self.assembler = assembler
        self.source_line = source_line
        self.line_number = line_number
        self.name = self.__class__.__name__

    def run(self, params):
        '''
        Validate parameters, run macro, return generated opcode
        '''
        # validate parameter count
        pass

    def do(self, params):
        '''
        Run macro, return generated opcode
        '''
        pass

    def _validate_parameter(self, param, param_type_list, param_number=None):
        pass

    def _raise_macro_error(self, pos, error_message):
        pass

    def _raise_error(self, pos, error_message, exception):
        pass


class DAT(Macro):
    '''
    .DAT <param>+

    Insert byte, word and string literals
    '''

    param_count = (1, None)
    substitute_variables_in_params = 'all'
    param_type_list = [TokenType.BYTE_LITERAL, TokenType.WORD_LITERAL, TokenType.STRING_LITERAL]

    def do(self, params):
        pass


class DATN(Macro):
    '''
    .DATN <repeat> <value>

    Insert byte, word and string literal multiple times
    '''

    param_count = (2, 2)
    substitute_variables_in_params = 'all'
    param_types = [
        [TokenType.BYTE_LITERAL, TokenType.WORD_LITERAL],
        [TokenType.BYTE_LITERAL, TokenType.WORD_LITERAL, TokenType.STRING_LITERAL],
    ]

    def do(self, params):
        pass


class CONST(Macro):
    '''
    .CONST <name> <value>

    Define variable
    '''

    param_count = (2, 2)
    substitute_variables_in_params = [2]
    param_types = [
        [TokenType.VARIABLE],
        [TokenType.BYTE_LITERAL, TokenType.WORD_LITERAL, TokenType.STRING_LITERAL],
    ]

    def do(self, params):
        pass


class PARAM(Macro):
    '''
    .PARAM <name>

    Define word parameter in a scope
    '''

    param_count = (1, 1)
    length = 2
    param_types = [
        [TokenType.VARIABLE],
    ]

    def do(self, params):
        pass


class PARAMB(PARAM):
    '''
    .PARAMB <name>

    Define byte parameter in a scope
    '''

    param_count = (1, 1)
    length = 1


class VAR(Macro):
    '''
    .VAR <name> [default_value]

    Define local word variable in a scope (with optional default value)
    '''

    param_count = (1, 2)
    length = 2
    param_types = [
        [TokenType.VARIABLE],
    ]

    def do(self, params):
        pass


class VARB(VAR):
    '''
    .VARB <name> [default_value]

    Define local byte variable in a scope (with optional default value)
    '''

    param_count = (1, 2)
    length = 1


MACRO_SET = {
    'DAT': DAT,
    'DATN': DATN,
    'CONST': CONST,
    'PARAM': PARAM,
    'PARAMB': PARAMB,
    'VAR': VAR,
    'VARB': VARB,
}


def _raise_error(code, line_number, pos, error_message, exception):
    pass


def _param_count_string(cnt):
    pass


# pylint: disable=missing-docstring

class MacroError(AldebaranError):
    pass


class VariableError(MacroError):
    pass


class ScopeError(MacroError):
    pass
