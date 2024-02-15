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
        opcode = []
        for param in params:
            # Depending on the type of param, we generate appropriate opcode.
            if param.type == TokenType.STRING_LITERAL:
                # String literals are UTF-8 encoded
                opcode.extend(param.value.encode('utf-8'))
            elif param.type == TokenType.BYTE_LITERAL:
                opcode.extend(param.value)
                # Else, it is a Word Literal
            else:
                opcode.extend(utils.word_to_binary(param.value)) # Assuming there is a method to convert words to binary, we have to confirm.
        return opcode


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
        # Same as DAT, but this is multiplied N times
        opcodeN = []
        # Depending on the type of param, we generate appropriate opcode and multiply it with N
        if params[1].type == TokenType.STRING_LITERAL:
            # String literals are UTF-8 encoded
            opcodeN = list(params[1].value.encode('utf-8'))
        elif params[1].type == TokenType.BYTE_LITERAL:
            opcodeN = list(params[1].value)
            # Else, it is a Word Literal
        else:
            opcodeN = list(utils.word_to_binary(params[1].value)) # Assuming there is a method to convert words to binary, we have to confirm.
        return opcodeN * params[0].value


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
        # In assembly language, variable declaration in this context doesn't translate into actual
        # machine code but rather informs the assembler how to substitute the variable in the code.
        const_name, const_value = params[0], params[1]
        if const_name.type != TokenType.VARIABLE:
            self._raise_macro_error(const_name.pos, f"Expected a variable, got {const_name.type}")
        # Register the constant in the assembler and return an empty opcode since CONST doesn't translate directly to machine code
        self.assembler.register_constant(const_name.value, const_value) # Assuming assembler has a registration system like this, we have to explore and confirm this one.
        return []


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
