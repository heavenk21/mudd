from .scanner import MuddScanner

from mudd import *


class ParseTree():
    """Parse Tree Node.

    """
    def __init__(self, kind, line_number):
        self.kind = kind
        self.line_number = line_number
        self.children = []

    def __str__(self, level=0):
        ret = '  '*level+'%d\n' % (self.kind)
        for child in self.children:
            ret += child.__str__(level+1)
        return ret


def program(scanner):
    parse_tree = ParseTree(N_PROGRAM, MuddScanner.line_number)

    # N_DECLARATION_LIST
    parse_tree.children.append(declaration_list(scanner))

    return parse_tree


def declaration_list(scanner):
    parse_tree = ParseTree(N_DECLARATION_LIST, MuddScanner.line_number)

    # N_DECLARATION (minimum 1 declaration required)
    parse_tree.children.append(declaration(scanner))
    while not _is_end_of_declaration_list(scanner.next_token):
        parse_tree_top = ParseTree(N_DECLARATION_LIST, MuddScanner.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        parse_tree.children.append(declaration(scanner))

    return parse_tree


def _is_end_of_declaration_list(token):
    end_of_declaration_list_tokens = [T_EOF]
    return token.kind in end_of_declaration_list_tokens


def declaration(scanner):
    parse_tree = ParseTree(N_DECLARATION, MuddScanner.line_number)

    # N_VAR_DEC OR N_FUN_DEC
    parse_tree.children.append(var_fun_dec(scanner))

    return parse_tree


def var_fun_dec(scanner):
    parse_tree = ParseTree(N_VAR_DEC, MuddScanner.line_number)

    # N_TYPE_SPECIFIER
    parse_tree.children.append(type_specifier(scanner))

    if scanner.next_token.kind == T_MUL:
        # T_MUL (pointer)
        parse_tree.children.append(is_token_kind(scanner.next_token, T_MUL))
        scanner.get_next_token()
        # T_ID
        parse_tree.children.append(is_token_kind(scanner.next_token, T_ID))
        scanner.get_next_token()
    else:
        # T_ID
        parse_tree.children.append(is_token_kind(scanner.next_token, T_ID))
        scanner.get_next_token()
        if scanner.next_token.kind == T_LBRACK:
            # T_LBRACK
            parse_tree.children.append(
                is_token_kind(scanner.next_token, T_LBRACK)
                )
            scanner.get_next_token()
            # T_NUM
            parse_tree.children.append(
                is_token_kind(scanner.next_token, T_NUM)
                )
            scanner.get_next_token()
            # T_RBRACK
            parse_tree.children.append(
                is_token_kind(scanner.next_token, T_RBRACK)
                )
            scanner.get_next_token()
        elif scanner.next_token.kind == T_LPAREN:
            parse_tree.kind = N_FUN_DEC
            # T_LPAREN
            parse_tree.children.append(
                is_token_kind(scanner.next_token, T_LPAREN)
                )
            scanner.get_next_token()
            # N_PARAMS
            parse_tree.children.append(
                params(scanner)
                )
            # T_RPAREN
            parse_tree.children.append(
                is_token_kind(scanner.next_token, T_RPAREN)
                )
            scanner.get_next_token()
            # N_COMPOUND_STMT
            parse_tree.children.append(compound_stmt(scanner))

    # TODO: if no T_SEMICOL at the end of all var_dec, shift tab for this chunk
    if parse_tree.kind == N_VAR_DEC:
        # T_SEMICOL
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )
        scanner.get_next_token()

    return parse_tree


def type_specifier(scanner):
    parse_tree = ParseTree(N_TYPE_SPECIFIER, MuddScanner.line_number)

    if scanner.next_token.kind == T_INT:
        parse_tree.children.append(is_token_kind(scanner.next_token, T_INT))
    elif scanner.next_token.kind == T_VOID:
        parse_tree.children.append(is_token_kind(scanner.next_token, T_VOID))
    else:
        parse_tree.children.append(is_token_kind(scanner.next_token, T_STRING))
    scanner.get_next_token()

    return parse_tree


def params(scanner):
    parse_tree = ParseTree(N_PARAMS, MuddScanner.line_number)

    if scanner.next_token.kind == T_VOID:
        parse_tree.children.append(is_token_kind(scanner.next_token, T_VOID))
        scanner.get_next_token()
    else:
        parse_tree.children.append(param_list(scanner))

    return parse_tree


def param_list(scanner):
    parse_tree = ParseTree(N_PARAM_LIST, MuddScanner.line_number)

    # N_PARAM (minimum 1 parameter required)
    parse_tree.children.append(param(scanner))
    while not _is_end_of_param_list(scanner.next_token):
        parse_tree_top = ParseTree(N_PARAM_LIST, MuddScanner.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        parse_tree.children.append(is_token_kind(scanner.next_token, T_COMMA))
        scanner.get_next_token()
        parse_tree.children.append(param(scanner))

    return parse_tree


def _is_end_of_param_list(token):
    end_of_param_list_tokens = [T_RPAREN]
    return token.kind in end_of_param_list_tokens


def param(scanner):
    parse_tree = ParseTree(N_PARAM, MuddScanner.line_number)

    # N_TYPE_SPECIFIER
    parse_tree.children.append(type_specifier(scanner))

    if scanner.next_token.kind == T_MUL:
        # T_MUL (pointer)
        parse_tree.children.append(is_token_kind(scanner.next_token, T_MUL))
        scanner.get_next_token()
        # T_ID
        parse_tree.children.append(is_token_kind(scanner.next_token, T_ID))
        scanner.get_next_token()
    else:
        # T_ID
        parse_tree.children.append(is_token_kind(scanner.next_token, T_ID))
        scanner.get_next_token()
        if scanner.next_token.kind == T_LBRACK:
            # T_LBRACK
            parse_tree.children.append(
                is_token_kind(scanner.next_token, T_LBRACK)
                )
            scanner.get_next_token()
            # T_RBRACK
            parse_tree.children.append(
                is_token_kind(scanner.next_token, T_RBRACK)
                )
            scanner.get_next_token()
        # else:
        #     is_token_kind(scanner.next_token, T_COMMA, T_RPAREN)

    return parse_tree


def statement(scanner):
    parse_tree = ParseTree(N_STATEMENT, MuddScanner.line_number)

    token = scanner.next_token
    if token.kind == T_LCURLY:
        parse_tree.children.append(compound_stmt(scanner))
    elif token.kind == T_IF:
        parse_tree.children.append(if_stmt(scanner))
    elif token.kind == T_WHILE:
        parse_tree.children.append(while_stmt(scanner))
    elif token.kind == T_RETURN:
        parse_tree.children.append(return_stmt(scanner))
    elif token.kind == T_WRITE or token.kind == T_WRITELN:
        parse_tree.children.append(write_stmt(scanner))
    else:
        parse_tree.children.append(expression_stmt(scanner))
    return parse_tree


def expression_stmt(scanner):
    parse_tree = ParseTree(N_EXPRESSION_STMT, MuddScanner.line_number)

    if scanner.next_token.kind == T_SEMICOL:
        parse_tree.children.append(scanner.next_token)
    else:
        # N_EXPRESSION
        parse_tree.children.append(expression(scanner))

        # T_SEMICOL
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )

    scanner.get_next_token()

    return parse_tree


def expression(scanner):
    parse_tree = ParseTree(N_EXPRESSION, MuddScanner.line_number)

    scanner.set_backtrack_index()
    # N_VAR
    parse_tree_var = var(scanner, parse_error=False)
    # T_ASSIGN
    parse_tree_assign = expression_assign(scanner, parse_error=False)

    if parse_tree_var and parse_tree_assign:
        parse_tree.children.extend([parse_tree_var, parse_tree_assign])
        # N_EXPRESSION
        parse_tree.children.append(expression(scanner))
        scanner.unset_backtrack_index()
    else:
        scanner.backtrack()
        # N_EXPRESSION
        parse_tree.children.append(
            comp_exp(scanner)
            )

    return parse_tree


def expression_assign(scanner, parse_error=True):
    assign = None
    try:
        # T_ASSIGN
        assign = is_token_kind(
            scanner.next_token, T_ASSIGN, parse_error=parse_error
            )
        scanner.get_next_token()
    except BackTrackError:
        assign = None
    finally:
        return assign


def var(scanner, parse_error=True):
    parse_tree = None
    try:
        parse_tree = ParseTree(N_VAR, MuddScanner.line_number)

        if scanner.next_token.kind == T_MUL:
            # T_MUL
            parse_tree.children.append(
                is_token_kind(
                    scanner.next_token, T_MUL, parse_error=parse_error
                    )
                )
            scanner.get_next_token()

        # T_ID
        parse_tree.children.append(
            is_token_kind(
                scanner.next_token, T_ID, parse_error=parse_error
                )
            )
        scanner.get_next_token()

        # T_LBRACK N_EXPRESSION T_RBRACK
        if scanner.next_token.kind == T_LBRACK:
            # T_LBRACK
            parse_tree.children.append(
                is_token_kind(
                    scanner.next_token, T_LBRACK, parse_error=parse_error
                    )
                )
            scanner.get_next_token()
            # N_EXPRESSION
            parse_tree.children.append(
                expression(scanner)
                )
            # T_RBRACK
            parse_tree.children.append(
                is_token_kind(
                    scanner.next_token, T_RBRACK, parse_error=parse_error
                    )
                )
            scanner.get_next_token()
    except BackTrackError:
        parse_tree = None

    finally:
        return parse_tree


def comp_exp(scanner):
    parse_tree = ParseTree(N_COMP_EXP, MuddScanner.line_number)

    # N_E
    parse_tree.children.append(e(scanner))
    if _is_relop(scanner.next_token):
        # N_RELOP
        parse_tree.children.append(relop(scanner))
        # N_E
        parse_tree.children.append(e(scanner))

    return parse_tree


def _is_relop(token):
    is_relop_tokens = [T_LEQ, T_LES, T_EQU, T_NEQ, T_GRE, T_GEQ]
    return token.kind in is_relop_tokens


def relop(scanner):
    parse_tree = ParseTree(N_RELOP, MuddScanner.line_number)

    # T_LEQ, T_LES, T_EQU, T_NEQ, T_GRE, T_GEQ
    parse_tree.children.append(
        is_token_kind(
            scanner.next_token,
            T_LEQ, T_LES, T_EQU, T_NEQ, T_GRE, T_GEQ
            )
        )
    scanner.get_next_token()

    return parse_tree


def e(scanner):
    parse_tree = ParseTree(N_E, MuddScanner.line_number)

    # N_T
    parse_tree.children.append(t(scanner))
    while _is_addop(scanner.next_token):
        parse_tree_top = ParseTree(N_E, MuddScanner.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        # N_ADDOP
        parse_tree.children.append(addop(scanner))
        # N_T
        parse_tree.children.append(t(scanner))

    return parse_tree


def _is_addop(token):
    is_addop_tokens = [T_PLU, T_MIN]
    return token.kind in is_addop_tokens


def addop(scanner):
    parse_tree = ParseTree(N_ADDOP, MuddScanner.line_number)

    # T_PLU, T_MIN
    parse_tree.children.append(
        is_token_kind(
            scanner.next_token,
            T_PLU, T_MIN
            )
        )
    scanner.get_next_token()

    return parse_tree


def t(scanner):
    parse_tree = ParseTree(N_T, MuddScanner.line_number)

    # N_F
    parse_tree.children.append(f(scanner))
    while _is_mulop(scanner.next_token):
        parse_tree_top = ParseTree(N_T, MuddScanner.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        # N_MULOP
        parse_tree.children.append(mulop(scanner))
        # N_F
        parse_tree.children.append(f(scanner))

    return parse_tree


def _is_mulop(token):
    is_mulop_tokens = [T_MUL, T_DIV, T_MOD]
    return token.kind in is_mulop_tokens


def mulop(scanner):
    parse_tree = ParseTree(N_MULOP, MuddScanner.line_number)

    # T_MUL, T_DIV, T_MOD
    parse_tree.children.append(
        is_token_kind(
            scanner.next_token,
            T_MUL, T_DIV, T_MOD
            )
        )
    scanner.get_next_token()

    return parse_tree


def f(scanner):
    parse_tree = ParseTree(N_F, MuddScanner.line_number)

    if scanner.next_token.kind in [T_MIN, T_AND, T_MUL]:
        # T_MIN, T_AND, T_MUL
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_MIN, T_AND, T_MUL)
            )
        scanner.get_next_token()

    parse_tree.children.append(factor(scanner))

    return parse_tree


def factor(scanner):
    parse_tree = ParseTree(N_FACTOR, MuddScanner.line_number)

    if scanner.next_token.kind == T_LPAREN:
        # T_LPAREN
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_LPAREN)
            )
        scanner.get_next_token()
        # N_EXPRESSION
        parse_tree.children.append(expression(scanner))
        # T_RPAREN
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_RPAREN)
            )
        scanner.get_next_token()
    elif scanner.next_token.kind == T_READ:
        # T_READ
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_READ)
            )
        scanner.get_next_token()
        # T_LPAREN
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_LPAREN)
            )
        scanner.get_next_token()
        # T_RPAREN
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_RPAREN)
            )
        scanner.get_next_token()
    elif scanner.next_token.kind in [T_NUM, T_STRLIT]:
        # T_NUM, T_STRLIT
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_NUM, T_STRLIT)
            )
        scanner.get_next_token()
    else:
        # T_ID
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_ID)
            )
        scanner.get_next_token()
        # TODO: add FUN_CALL with Backtracking
        if scanner.next_token.kind == T_LBRACK:
            # T_LBRACK
            parse_tree.children.append(
                is_token_kind(scanner.next_token, T_LBRACK)
                )
            scanner.get_next_token()
            # N_EXPRESSION
            parse_tree.children.append(expression(scanner))
            # T_RBRACK
            parse_tree.children.append(
                is_token_kind(scanner.next_token, T_RBRACK)
                )
            scanner.get_next_token()

    return parse_tree


def compound_stmt(scanner):
    parse_tree = ParseTree(N_COMPOUND_STMT, MuddScanner.line_number)

    # T_LCURLY
    parse_tree.children.append(is_token_kind(scanner.next_token, T_LCURLY))
    # N_STATEMENT_LIST
    parse_tree.children.append(statement_list(scanner))
    # T_RCURLY
    parse_tree.children.append(is_token_kind(scanner.next_token, T_RCURLY))
    scanner.get_next_token()

    return parse_tree


def statement_list(scanner):
    parse_tree = ParseTree(N_STATEMENT_LIST, MuddScanner.line_number)
    scanner.get_next_token()
    while not _is_end_of_statement_list(scanner.next_token):
        parse_tree_top = ParseTree(N_STATEMENT_LIST, MuddScanner.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        parse_tree.children.append(statement(scanner))

    return parse_tree


def _is_end_of_statement_list(token):
    end_of_statement_list_tokens = [T_RCURLY]
    return token.kind in end_of_statement_list_tokens


def while_stmt(scanner):
    parse_tree = ParseTree(N_WHILE_STMT, MuddScanner.line_number)

    # T_WHILE
    parse_tree.children.append(is_token_kind(scanner.next_token, T_WHILE))
    scanner.get_next_token()
    # T_LPAREN
    parse_tree.children.append(is_token_kind(scanner.next_token, T_LPAREN))
    scanner.get_next_token()
    # N_EXPRESSION
    parse_tree.children.append(expression(scanner))
    # T_RPAREN
    parse_tree.children.append(is_token_kind(scanner.next_token, T_RPAREN))
    scanner.get_next_token()
    # N_STATEMENT
    parse_tree.children.append(statement(scanner))
    # scanner.get_next_token()

    return parse_tree


def if_stmt(scanner):
    parse_tree = ParseTree(N_IF_STMT, MuddScanner.line_number)

    # T_IF
    parse_tree.children.append(is_token_kind(scanner.next_token, T_IF))
    scanner.get_next_token()
    # T_LPAREN
    parse_tree.children.append(is_token_kind(scanner.next_token, T_LPAREN))
    scanner.get_next_token()
    # N_EXPRESSION
    parse_tree.children.append(expression(scanner))
    # T_RPAREN
    parse_tree.children.append(is_token_kind(scanner.next_token, T_RPAREN))
    scanner.get_next_token()
    # N_STATEMENT
    parse_tree.children.append(statement(scanner))
    # scanner.get_next_token()

    # T_ELSE
    if scanner.next_token.kind == T_ELSE:
        parse_tree.children.append(scanner.next_token)
        scanner.get_next_token()
        # N_STATEMENT
        parse_tree.children.append(statement(scanner))

    return parse_tree


def return_stmt(scanner):
    parse_tree = ParseTree(N_RETURN_STMT, MuddScanner.line_number)

    # T_RETURN
    parse_tree.children.append(is_token_kind(scanner.next_token, T_RETURN))
    scanner.get_next_token()

    if scanner.next_token.kind == T_SEMICOL:
        # T_SEMICOL
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )
    else:
        # N_EXPRESSION
        parse_tree.children.append(expression(scanner))
        # T_SEMICOL
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )

    scanner.get_next_token()

    return parse_tree


def write_stmt(scanner):
    parse_tree = ParseTree(N_RETURN_STMT, MuddScanner.line_number)

    if scanner.next_token.kind == T_WRITE:
        # T_WRITE
        parse_tree.children.append(is_token_kind(scanner.next_token, T_WRITE))
        scanner.get_next_token()
        # T_LPAREN
        parse_tree.children.append(is_token_kind(scanner.next_token, T_LPAREN))
        scanner.get_next_token()
        # N_EXPRESSION
        parse_tree.children.append(expression(scanner))
        # T_RPAREN
        parse_tree.children.append(is_token_kind(scanner.next_token, T_RPAREN))
        scanner.get_next_token()
        # T_SEMICOL
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )
        scanner.get_next_token()

    else:
        # T_WRITELN
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_WRITELN)
            )
        scanner.get_next_token()
        # T_LPAREN
        parse_tree.children.append(is_token_kind(scanner.next_token, T_LPAREN))
        scanner.get_next_token()
        # T_RPAREN
        parse_tree.children.append(is_token_kind(scanner.next_token, T_RPAREN))
        scanner.get_next_token()
        # T_SEMICOL
        parse_tree.children.append(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )
        scanner.get_next_token()

    return parse_tree


def is_token_kind(token, *token_kind, parse_error=True):
    if token.kind in token_kind:
        return token
    elif parse_error:
        raise ParseError
    else:
        raise BackTrackError


class MuddParser():
    """Recursive Descent Parser.

    """
    def __init__(self, filename):
        self.scanner = MuddScanner(filename)
        self.parse_tree = None
        MuddScanner.line_number = 1

    def parse(self):
        self.scanner.get_next_token()
        self.parse_tree = program(self.scanner)
        self.scanner.get_next_token()
        if self.scanner.next_token.kind == T_EOF:
            print('Accept')
            return self.parse_tree
        else:
            print('Reject')
            raise ParseError


class ParseError(Exception):
    pass


class BackTrackError(Exception):
    pass
