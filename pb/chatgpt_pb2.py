# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chatgpt.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rchatgpt.proto\x12\x02pb\":\n\x0e\x43hatGptMessage\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x1a\n\x04role\x18\x02 \x01(\x0e\x32\x0c.pb.RoleEnum\"D\n\tAnswerReq\x12$\n\x08messages\x18\x01 \x03(\x0b\x32\x12.pb.ChatGptMessage\x12\x11\n\tmaxTokens\x18\x02 \x01(\x05\"\x9b\x01\n\nAnswerResp\x12&\n\x07\x63hoices\x18\x01 \x03(\x0b\x32\x15.pb.AnswerResp.Choice\x12\x11\n\terrorInfo\x18\x02 \x01(\t\x1aR\n\x06\x43hoice\x12#\n\x07message\x18\x01 \x01(\x0b\x32\x12.pb.ChatGptMessage\x12\x14\n\x0c\x66inishReason\x18\x02 \x01(\t\x12\r\n\x05index\x18\x03 \x01(\x03*/\n\x08RoleEnum\x12\n\n\x06System\x10\x00\x12\r\n\tAssistant\x10\x01\x12\x08\n\x04User\x10\x02\x32;\n\x0e\x43hatGptService\x12)\n\x06\x41nswer\x12\r.pb.AnswerReq\x1a\x0e.pb.AnswerResp\"\x00\x42\x06Z\x04./pbb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chatgpt_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\004./pb'
  _ROLEENUM._serialized_start=309
  _ROLEENUM._serialized_end=356
  _CHATGPTMESSAGE._serialized_start=21
  _CHATGPTMESSAGE._serialized_end=79
  _ANSWERREQ._serialized_start=81
  _ANSWERREQ._serialized_end=149
  _ANSWERRESP._serialized_start=152
  _ANSWERRESP._serialized_end=307
  _ANSWERRESP_CHOICE._serialized_start=225
  _ANSWERRESP_CHOICE._serialized_end=307
  _CHATGPTSERVICE._serialized_start=358
  _CHATGPTSERVICE._serialized_end=417
# @@protoc_insertion_point(module_scope)