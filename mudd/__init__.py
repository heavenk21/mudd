# BPL Tokens

# End-of-file
T_EOF = 100
# Keywords
T_INT = 101
T_VOID = 102
T_STRING = 103
T_IF = 104
T_ELSE = 105
T_WHILE = 106
T_RETURN = 107
T_WRITE = 108
T_WRITELN = 109
T_READ = 110
# Symbols
T_SEMICOL = 111
T_COMMA = 112
T_LBRACK = 113
T_RBRACK = 114
T_LCURLY = 115
T_RCURLY = 116
T_LPAREN = 117
T_RPAREN = 118
T_LES = 119
T_LEQ = 120
T_EQU = 121
T_NEQ = 122
T_GEQ = 123
T_GRE = 124
T_PLU = 125
T_MIN = 126
T_MUL = 127
T_DIV = 128
T_MOD = 129
T_AND = 130
# Assignment sign
T_ASSIGN = 195
# Comments
T_LCOM = 196
T_RCOM = 197
# Identifiers
T_ID = 198
# Numbers
T_NUM = 199
# Strings
T_STRLIT = 194

# BPL Non-terminals
N_PROGRAM = 200
N_STATEMENT = 201
N_EXPRESSION_STMT = 202
N_EXPRESSION = 203
N_COMPOUND_STMT = 204
N_STATEMENT_LIST = 205
N_WHILE_STMT = 206
N_IF_STMT = 207
N_RETURN_STMT = 208
N_WRITE_STMT = 209
N_DECLARATION_LIST = 210
N_DECLARATION = 211
N_VAR_DEC = 212
N_TYPE_SPECIFIER = 213
N_FUN_DEC = 214
N_PARAMS = 215
N_PARAM_LIST = 216
N_PARAM = 217
N_VAR = 218
N_COMP_EXP = 219
N_RELOP = 220
N_E = 221
N_ADDOP = 222
N_T = 223
N_MULOP = 224
N_F = 225
N_FACTOR = 226
N_FUN_CALL = 227
N_ARGS = 228
N_ARG_LIST = 229
N_LOCAL_DECS = 230

KIND_NAME = {
    100 : 'T_EOF',
    101 : 'T_INT',
    102 : 'T_VOID',
    103 : 'T_STRING',
    104 : 'T_IF',
    105 : 'T_ELSE',
    106 : 'T_WHILE',
    107 : 'T_RETURN',
    108 : 'T_WRITE',
    109 : 'T_WRITELN',
    110 : 'T_READ',
    111 : 'T_SEMICOL',
    112 : 'T_COMMA',
    113 : 'T_LBRACK',
    114 : 'T_RBRACK',
    115 : 'T_LCURLY',
    116 : 'T_RCURLY',
    117 : 'T_LPAREN',
    118 : 'T_RPAREN',
    119 : 'T_LES',
    120 : 'T_LEQ',
    121 : 'T_EQU',
    122 : 'T_NEQ',
    123 : 'T_GEQ',
    124 : 'T_GRE',
    125 : 'T_PLU',
    126 : 'T_MIN',
    127 : 'T_MUL',
    128 : 'T_DIV',
    129 : 'T_MOD',
    130 : 'T_AND',
    195 : 'T_ASSIGN',
    196 : 'T_LCOM',
    197 : 'T_RCOM',
    198 : 'T_ID',
    199 : 'T_NUM',
    194 : 'T_STRLIT',
    200 : 'N_PROGRAM',
    201 : 'N_STATEMENT',
    202 : 'N_EXPRESSION_STMT',
    203 : 'N_EXPRESSION',
    204 : 'N_COMPOUND_STMT',
    205 : 'N_STATEMENT_LIST',
    206 : 'N_WHILE_STMT',
    207 : 'N_IF_STMT',
    208 : 'N_RETURN_STMT',
    209 : 'N_WRITE_STMT',
    210 : 'N_DECLARATION_LIST',
    211 : 'N_DECLARATION',
    212 : 'N_VAR_DEC',
    213 : 'N_TYPE_SPECIFIER',
    214 : 'N_FUN_DEC',
    215 : 'N_PARAMS',
    216 : 'N_PARAM_LIST',
    217 : 'N_PARAM',
    218 : 'N_VAR',
    219 : 'N_COMP_EXP',
    220 : 'N_RELOP',
    221 : 'N_E',
    222 : 'N_ADDOP',
    223 : 'N_T',
    224 : 'N_MULOP',
    225 : 'N_F',
    226 : 'N_FACTOR',
    227 : 'N_FUN_CALL',
    228 : 'N_ARGS',
    229 : 'N_ARG_LIST',
    230 : 'N_LOCAL_DECS',
}
