# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywidl/grammar.py
# Compiled at: 2012-03-31 09:52:20
from lexis import *
import model, helper, ply.yacc as yacc, os

def p_Definitions(p):
    """Definitions : Definitions ExtendedAttributeList Definition"""
    p[3].extended_attributes = p[2]
    p[0] = p[1] + [p[3]]


def p_Definitions_empty(p):
    """Definitions : """
    p[0] = []


def p_Definition(p):
    """Definition : CallbackOrInterface
                | PartialInterface
                | Dictionary
                | Exception
                | Enum
                | Typedef
                | ImplementsStatement
  """
    p[0] = p[1]


def p_CallbackOrInterface_callback(p):
    """CallbackOrInterface : callback CallbackRestOrInterface"""
    p[0] = p[2]


def p_CallbackOrInterface_interface(p):
    """CallbackOrInterface : Interface"""
    p[0] = p[1]


def p_CallbackRestOrInterface(p):
    """CallbackRestOrInterface : CallbackRest"""
    p[0] = p[1]


def p_CallbackRestOrInterface_interface(p):
    """CallbackRestOrInterface : Interface"""
    p[0] = p[1]
    p[0].callback = True


def p_Interface(p):
    """Interface : interface IDENTIFIER Inheritance "{" InterfaceMembers "}" ";"
  """
    p[0] = model.Interface(name=p[2], parent=p[3], members=p[5])


def p_PartialInterface(p):
    """PartialInterface : partial interface IDENTIFIER "{" InterfaceMembers "}" ";"
  """
    p[0] = model.PartialInterface(name=p[3], members=p[5])


def p_InterfaceMembers(p):
    """InterfaceMembers : InterfaceMembers ExtendedAttributeList InterfaceMember"""
    p[3].extended_attributes = p[2]
    p[0] = p[1] + [p[3]]


def p_InterfaceMembers_empty(p):
    """InterfaceMembers : """
    p[0] = []


def p_InterfaceMember(p):
    """InterfaceMember : Const
                     | AttributeOrOperation
  """
    p[0] = p[1]


def p_Dictionary(p):
    """Dictionary : dictionary IDENTIFIER Inheritance "{" DictionaryMembers "}" ";"
  """
    p[0] = model.Dictionary(name=p[2], parent=p[3], members=p[5])


def p_DictionaryMembers(p):
    """DictionaryMembers : ExtendedAttributeList DictionaryMember DictionaryMembers"""
    p[2].extended_attributes = p[1]
    p[0] = [p[2]] + p[3]


def p_DictionaryMembers_empty(p):
    """DictionaryMembers : """
    p[0] = []


def p_DictionaryMember(p):
    """DictionaryMember : Type IDENTIFIER Default ";"
  """
    p[0] = model.DictionaryMember(type=p[1], name=p[2], default=p[3])


def p_Default(p):
    """Default : "=" DefaultValue"""
    p[0] = p[2]


def p_Default_empty(p):
    """Default : """
    p[0] = None
    return


def p_DefaultValue(p):
    """DefaultValue : ConstValue"""
    p[0] = p[1]


def p_DefaultValue_string(p):
    """DefaultValue : STRING"""
    p[0] = model.Value(type=model.Value.STRING, value=p[1])


def p_DefaultValue_empty(p):
    """DefaultValue : """
    p[0] = None
    return


def p_Exception(p):
    """Exception : exception IDENTIFIER Inheritance "{" ExceptionMembers "}" ";"
  """
    p[0] = model.Exception(name=p[2], parent=p[3], members=p[5])


def p_ExceptionMembers(p):
    """ExceptionMembers : ExtendedAttributeList ExceptionMember ExceptionMembers"""
    p[2].extended_attributes = p[1]
    p[0] = [p[2]] + p[3]


def p_ExceptionMembers_empty(p):
    """ExceptionMembers : """
    p[0] = []


def p_Inheritance(p):
    """Inheritance : ":" IDENTIFIER"""
    p[0] = p[2]


def p_Inheritance_empty(p):
    """Inheritance : """
    p[0] = None
    return


def p_Enum(p):
    """Enum : enum IDENTIFIER "{" EnumValueList "}" ";"
  """
    p[0] = model.Enum(name=p[2], values=p[4])


def p_EnumValueList(p):
    """EnumValueList : STRING EnumValues"""
    p[0] = [
     p[1]] + p[2]


def p_EnumValues(p):
    """EnumValues : "," STRING EnumValues"""
    p[0] = [
     p[2]] + p[3]


def p_EnumValues_empty(p):
    """EnumValues : """
    p[0] = []


def p_CallbackRest(p):
    """CallbackRest : IDENTIFIER "=" ReturnType "(" ArgumentList ")" ";"
  """
    p[0] = model.Callback(name=p[1], return_type=p[3], arguments=p[5])


def p_Typedef(p):
    """Typedef : typedef ExtendedAttributeList Type IDENTIFIER ";"
  """
    p[0] = model.Typedef(type_extended_attributes=p[2], type=p[3], name=p[4])


def p_ImplementsStatement(p):
    """ImplementsStatement : IDENTIFIER implements IDENTIFIER ";"
  """
    p[0] = model.ImplementsStatement(interface=p[1], functionality=p[3])


def p_Const(p):
    """Const : const ConstType IDENTIFIER "=" ConstValue ";"
  """
    p[0] = model.Const(type=p[2], name=p[3], value=p[5])


def p_ConstValue_boolean(p):
    """ConstValue : BooleanLiteral"""
    p[0] = model.Value(type=model.Value.BOOLEAN, value=p[1])


def p_ConstValue_integer(p):
    """ConstValue : INTEGER"""
    p[0] = model.Value(type=model.Value.INTEGER, value=p[1])


def p_ConstValue_float(p):
    """ConstValue : FLOAT"""
    p[0] = model.Value(type=model.Value.FLOAT, value=p[1])


def p_ConstValue_null(p):
    """ConstValue : null"""
    p[0] = model.Value(type=model.Value.NULL, value=p[1])


def p_BooleanLiteral_true(p):
    """BooleanLiteral : true"""
    p[0] = True


def p_BooleanLiteral_false(p):
    """BooleanLiteral : false"""
    p[0] = False


def p_AttributeOrOperation(p):
    """AttributeOrOperation : Attribute
                          | Operation
  """
    p[0] = p[1]


def p_AttributeOrOperation_stringifier(p):
    """AttributeOrOperation : stringifier StringifierAttributeOrOperation
  """
    p[0] = p[2]
    p[0].stringifier = True


def p_StringifierAttributeOrOperation(p):
    """StringifierAttributeOrOperation : Attribute
                                     | OperationRest
                                     | ";"
  """
    p[0] = p[1]


def p_Attribute(p):
    """Attribute : Inherit ReadOnly attribute Type IDENTIFIER ";"
  """
    p[0] = model.Attribute(inherit=p[1], readonly=p[2], type=p[4], name=p[5])


def p_Inherit_true(p):
    """Inherit : inherit"""
    p[0] = True


def p_Inherit_false(p):
    """Inherit : """
    p[0] = False


def p_ReadOnly_true(p):
    """ReadOnly : readonly"""
    p[0] = True


def p_ReadOnly_false(p):
    """ReadOnly : """
    p[0] = False


def p_Operation(p):
    """Operation : Qualifiers OperationRest"""
    p[0] = helper.applyQualifiers(p[2], p[1])


def p_Qualifiers_static(p):
    """Qualifiers : static"""
    p[0] = [
     helper.STATIC]


def p_Qualifiers_specials(p):
    """Qualifiers : Specials"""
    p[0] = p[1]


def p_Specials(p):
    """Specials : Special Specials"""
    p[0] = [
     p[1]] + p[2]


def p_Specials_empty(p):
    """Specials : """
    p[0] = []


def p_Special_getter(p):
    """Special : getter"""
    p[0] = helper.GETTER


def p_Special_setter(p):
    """Special : setter"""
    p[0] = helper.SETTER


def p_Special_creator(p):
    """Special : creator"""
    p[0] = helper.CREATOR


def p_Special_deleter(p):
    """Special : deleter"""
    p[0] = helper.DELETER


def p_Special_legacycaller(p):
    """Special : legacycaller"""
    p[0] = helper.LEGACYCALLER


def p_OperationRest(p):
    """OperationRest : ReturnType OptionalIdentifier "(" ArgumentList ")" ";"
  """
    p[0] = model.Operation(return_type=p[1], name=p[2], arguments=p[4])


def p_OptionalIdentifier(p):
    """OptionalIdentifier : IDENTIFIER"""
    p[0] = p[1]


def p_OptionalIdentifier_empty(p):
    """OptionalIdentifier : """
    p[0] = None
    return


def p_ArgumentList(p):
    """ArgumentList : Argument Arguments"""
    p[0] = [
     p[1]] + p[2]


def p_ArgumentList_empty(p):
    """ArgumentList : """
    p[0] = []


def p_Arguments(p):
    """Arguments : "," Argument Arguments"""
    p[0] = [
     p[2]] + p[3]


def p_Arguments_empty(p):
    """Arguments : """
    p[0] = []


def p_Argument(p):
    """Argument : ExtendedAttributeList OptionalOrRequiredArgument"""
    p[0] = p[2]
    p[0].extended_attributes = p[1]


def p_OptionalOrRequiredArgument_optional(p):
    """OptionalOrRequiredArgument : optional Type IDENTIFIER Default"""
    p[0] = model.OperationArgument(type=p[2], name=p[3], optional=True, default=p[4])


def p_OptionalOrRequiredArgument(p):
    """OptionalOrRequiredArgument : Type Ellipsis IDENTIFIER"""
    p[0] = model.OperationArgument(type=p[1], ellipsis=p[2], name=p[3])


def p_Ellipsis_true(p):
    """Ellipsis : ELLIPSIS"""
    p[0] = True


def p_Ellipsis_false(p):
    """Ellipsis : """
    p[0] = False


def p_ExceptionMember(p):
    """ExceptionMember : Const
                     | ExceptionField
  """
    p[0] = p[1]


def p_ExceptionField(p):
    """ExceptionField : Type IDENTIFIER ";"
  """
    p[0] = model.ExceptionField(type=p[1], name=p[2])


def p_ExtendedAttributeList(p):
    """ExtendedAttributeList : "[" ExtendedAttribute ExtendedAttributes "]"
    """
    p[0] = [
     p[2]] + p[3]


def p_ExtendedAttributeList_empty(p):
    """ExtendedAttributeList : """
    p[0] = []


def p_ExtendedAttributes(p):
    """ExtendedAttributes : "," ExtendedAttribute ExtendedAttributes"""
    p[0] = [
     p[2]] + p[3]


def p_ExtendedAttributes_empty(p):
    """ExtendedAttributes : """
    p[0] = []


def p_ExtendedAttribute(p):
    """ExtendedAttribute : ExtendedAttributeNoArgs
                       | ExtendedAttributeArgList
                       | ExtendedAttributeIdent
                       | ExtendedAttributeNamedArgList
  """
    p[0] = p[1]


def p_Type_single(p):
    """Type : SingleType"""
    p[0] = p[1]


def p_Type_union(p):
    """Type : UnionType TypeSuffix"""
    p[0] = helper.unwrapTypeSuffix(p[1], p[2])


def p_SingleType(p):
    """SingleType : NonAnyType"""
    p[0] = p[1]


def p_SingleType_any(p):
    """SingleType : any TypeSuffixStartingWithArray"""
    p[0] = helper.unwrapTypeSuffix(model.SimpleType(model.SimpleType.ANY), p[2])


def p_UnionType(p):
    """UnionType : "(" UnionMemberType or UnionMemberType UnionMemberTypes ")"
  """
    t = [
     p[2]] + [p[4]] + p[5]
    p[0] = model.UnionType(t=t)


def p_UnionMemberType_nonAnyType(p):
    """UnionMemberType : NonAnyType"""
    p[0] = p[1]


def p_UnionMemberType_unionType(p):
    """UnionMemberType : UnionType TypeSuffix"""
    p[0] = helper.unwrapTypeSuffix(p[1], p[2])


def p_UnionMemberType_anyType(p):
    """UnionMemberType : any "[" "]" TypeSuffix"""
    p[0] = helper.unwrapTypeSuffix(model.Array(t=model.SimpleType(type=model.SimpleType.ANY)), p[4])


def p_UnionMemberTypes(p):
    """UnionMemberTypes : or UnionMemberType UnionMemberTypes"""
    p[0] = [
     p[2]] + p[3]


def p_UnionMemberTypes_empty(p):
    """UnionMemberTypes : """
    p[0] = []


def p_NonAnyType_primitiveType(p):
    """NonAnyType : PrimitiveType TypeSuffix"""
    p[0] = helper.unwrapTypeSuffix(p[1], p[2])


def p_NonAnyType_domString(p):
    """NonAnyType : DOMString TypeSuffix"""
    p[0] = helper.unwrapTypeSuffix(model.SimpleType(type=model.SimpleType.DOMSTRING), p[2])


def p_NonAnyType_interface(p):
    """NonAnyType : IDENTIFIER TypeSuffix"""
    p[0] = helper.unwrapTypeSuffix(model.InterfaceType(name=p[1]), p[2])


def p_NonAnyType_sequence(p):
    """NonAnyType : sequence "<" Type ">" Null"""
    p[0] = model.Sequence(t=p[3], nullable=p[5])


def p_NonAnyType_object(p):
    """NonAnyType : object TypeSuffix"""
    p[0] = helper.unwrapTypeSuffix(model.SimpleType(type=model.SimpleType.OBJECT), p[2])


def p_NonAnyType(p):
    """NonAnyType : Date TypeSuffix"""
    p[0] = helper.unwrapTypeSuffix(model.SimpleType(type=model.SimpleType.DATE), p[2])


def p_ConstType(p):
    """ConstType : PrimitiveType Null"""
    p[0] = p[1]
    p[0].nullable = p[2]


def p_PrimitiveType_integer(p):
    """PrimitiveType : UnsignedIntegerType"""
    p[0] = p[1]


def p_PrimitiveType_boolean(p):
    """PrimitiveType : boolean"""
    p[0] = model.SimpleType(type=model.SimpleType.BOOLEAN)


def p_PrimitiveType_byte(p):
    """PrimitiveType : byte"""
    p[0] = model.SimpleType(type=model.SimpleType.BYTE)


def p_PrimitiveType_octet(p):
    """PrimitiveType : octet"""
    p[0] = model.SimpleType(type=model.SimpleType.OCTET)


def p_PrimitiveType_float(p):
    """PrimitiveType : float"""
    p[0] = model.SimpleType(type=model.SimpleType.FLOAT)


def p_PrimitiveType_double(p):
    """PrimitiveType : double"""
    p[0] = model.SimpleType(type=model.SimpleType.DOUBLE)


def p_UnsignedIntegerType_unsigned(p):
    """UnsignedIntegerType : unsigned IntegerType"""
    p[0] = helper.unwrapIntegerType(True, p[2])


def p_UnsignedIntegerType(p):
    """UnsignedIntegerType : IntegerType"""
    p[0] = helper.unwrapIntegerType(False, p[1])


def p_IntegerType_short(p):
    """IntegerType : short"""
    p[0] = helper.SHORT


def p_IntegerType_long(p):
    """IntegerType : long OptionalLong"""
    if not p[2]:
        p[0] = helper.LONG
    else:
        p[0] = helper.LONGLONG


def p_OptionalLong_true(p):
    """OptionalLong : long"""
    p[0] = True


def p_OptionalLong_false(p):
    """OptionalLong : """
    p[0] = False


def p_TypeSuffix(p):
    """TypeSuffix : "[" "]" TypeSuffix"""
    p[0] = [
     helper.ARRAY] + p[3]


def p_TypeSuffix_null(p):
    """TypeSuffix : "?" TypeSuffixStartingWithArray"""
    p[0] = [
     helper.NULLABLE] + p[2]


def p_TypeSuffix_empty(p):
    """TypeSuffix : """
    p[0] = []


def p_TypeSuffixStartingWithArray(p):
    """TypeSuffixStartingWithArray : "[" "]" TypeSuffix"""
    p[0] = [
     helper.ARRAY] + p[3]


def p_TypeSuffixStartingWithArray_empty(p):
    """TypeSuffixStartingWithArray : """
    p[0] = []


def p_Null_true(p):
    """Null : "?"
  """
    p[0] = True


def p_Null_false(p):
    """Null : """
    p[0] = False


def p_ReturnType(p):
    """ReturnType : Type"""
    p[0] = p[1]


def p_ReturnType_void(p):
    """ReturnType : void"""
    p[0] = model.SimpleType(model.SimpleType.VOID)


def p_ExtendedAttributeNoArgs(p):
    """ExtendedAttributeNoArgs : IDENTIFIER"""
    p[0] = model.ExtendedAttribute(value=model.ExtendedAttributeValue(name=p[1]))


def p_ExtendedAttributeArgList(p):
    """ExtendedAttributeArgList : IDENTIFIER "(" ArgumentList ")"
  """
    p[0] = model.ExtendedAttribute(value=model.ExtendedAttributeValue(name=p[1], arguments=p[3]))


def p_ExtendedAttributeIdent(p):
    """ExtendedAttributeIdent : IDENTIFIER "=" IDENTIFIER"""
    p[0] = model.ExtendedAttribute(name=p[1], value=model.ExtendedAttributeValue(name=p[3]))


def p_ExtendedAttributeNamedArgList(p):
    """ExtendedAttributeNamedArgList : IDENTIFIER "=" IDENTIFIER "(" ArgumentList ")"
  """
    p[0] = model.ExtendedAttribute(name=p[1], value=model.ExtendedAttributeValue(name=p[3], arguments=p[5]))


def p_error(p):
    raise RuntimeError("Syntax error at '%s'" % p.value)


parsedir = os.path.dirname(__file__)
parser = yacc.yacc(tabmodule='pywidl.parsetab', outputdir=parsedir, debug=1)

def parse(source):
    return parser.parse(source)