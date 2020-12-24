# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\AST_ext.py
# Compiled at: 2009-07-07 11:29:42
import pprint, parser, symbol, token, tokenize, sys
name_sequence = [
 292, 293, 294, 295, 297, 298, 299, 300, 301, 302,
 303, 304, 305]

def gen_assign_val_subtree(assign_val, assign_val_type):
    name_sequence.reverse()
    sublist = []
    if assign_val_type == 2:
        sublist = [
         2, '%(assign_val)d' % vars()]
    elif assign_val_type == 1:
        sublist = [
         2, '%(assign_val)f' % vars()]
    elif assign_val_type == 3:
        sublist = [
         3, '"%(assign_val)s"' % vars()]
    for val in name_sequence[0:len(name_sequence) - 1]:
        sublist = [
         val, sublist]

    name_sequence.reverse()
    return sublist


class AST_Visitor:

    def __init__(self, modifying_AST):
        self.checking_assign_name = 0
        self.setting_assign_val = 0
        self.name_seq_index = 0
        self.expecting_equals = 0
        self.extracting_assign_val = 0
        self.extracted_val = 'not found'
        self.modifying_AST = modifying_AST

    def traverse(self, AST_sublist, assign_name, assign_val_subtree):
        if type(AST_sublist) != list:
            return AST_sublist
        elif len(AST_sublist) == 2:
            if self.name_seq_index > 0:
                if self.name_seq_index == len(name_sequence) - 1 and AST_sublist[0] == name_sequence[self.name_seq_index]:
                    if len(AST_sublist[1]) == 3:
                        if self.extracting_assign_val == 1:
                            extracted_val = AST_sublist[1][1]
                            self.extracted_val = extracted_val
                            self.extracting_assign_val = 0
                        else:
                            self.checking_assign_name = 1
                    self.name_seq_index = 0
                else:
                    expected_val = name_sequence[self.name_seq_index]
                    if AST_sublist[0] == expected_val:
                        self.name_seq_index = self.name_seq_index + 1
                    else:
                        self.name_seq_index = 0
                return AST_sublist[0:1] + [self.traverse(AST_sublist[1], assign_name, assign_val_subtree)]
            elif AST_sublist[0] == 292:
                if self.setting_assign_val == 1:
                    AST_sublist[1] = assign_val_subtree
                    self.setting_assign_val = 0
                else:
                    self.name_seq_index = 1
                return AST_sublist[0:1] + [self.traverse(AST_sublist[1], assign_name, assign_val_subtree)]
            else:
                return AST_sublist[0:1] + [self.traverse(AST_sublist[1], assign_name, assign_val_subtree)]
        elif len(AST_sublist) == 3:
            if type(AST_sublist[1]) != list:
                if self.checking_assign_name == 1:
                    if AST_sublist[1] == assign_name:
                        self.expecting_equals = 1
                    self.checking_assign_name = 0
                elif self.expecting_equals == 1:
                    if AST_sublist[1] == '=':
                        if self.modifying_AST == 1:
                            self.setting_assign_val = 1
                        elif self.modifying_AST == 0:
                            self.extracting_assign_val = 1
                    self.expecting_equals = 0
                return AST_sublist[0:2]
        if self.name_seq_index > 0 or self.name_seq_index < len(name_sequence) - 1:
            if self.extracting_assign_val == 1:
                self.extracted_val = 'compound'
                self.extracting_assign_val = 0
        sub_list = []
        for x in AST_sublist:
            sub_list = sub_list + [self.traverse(x, assign_name, assign_val_subtree)]

        return sub_list


def modify_AST(myAST, assign_name, assign_val):
    myAST_Visitor = AST_Visitor(1)
    old_AST_list = myAST.tolist(1)
    assign_val_type = 0
    if isinstance(assign_val, int):
        assign_val_type = 2
    elif isinstance(assign_val, float):
        assign_val_type = 1
    elif type(assign_val) == str:
        assign_val_type = 3
    new_AST_list = myAST_Visitor.traverse(old_AST_list, assign_name, gen_assign_val_subtree(assign_val, assign_val_type))
    myNewAST = parser.sequence2ast(new_AST_list)
    return myNewAST


def extract_from_AST(myAST, assign_name):
    myAST_Visitor = AST_Visitor(0)
    old_AST_list = myAST.tolist(1)
    new_AST_list = myAST_Visitor.traverse(old_AST_list, assign_name, 0)
    return myAST_Visitor.extracted_val