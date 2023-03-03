from concurrent import futures
from typing import List

import grpc

import pb.chatgpt_pb2 as chatgpt__pb2
import pb.chatgpt_pb2_grpc as chatgpt_pb2__grpc
from tool import chatgpt


class ChatGptService(chatgpt_pb2__grpc.ChatGptServiceServicer):
    def Answer(self, request: chatgpt__pb2.AnswerReq, context) -> chatgpt__pb2.AnswerResp:
        messages: List[chatgpt.ChatGptMessage] = []
        for message in request.messages:
            messages.append(chatgpt.ChatGptMessage(message.text, chatgpt.RoleEnum.fromPb(message.role)))
        cg: chatgpt.ChatGpt = chatgpt.ChatGpt(max_input_length=request.maxTokens, preset_messages=messages)
        try:
            openAIResp = cg.request()
        except Exception as e:
            response = chatgpt__pb2.AnswerResp()
            response.errorInfo = e.__str__()
            return response
        else:
            response = chatgpt__pb2.AnswerResp()
            response.errorInfo = ""
            '''
            message AnswerResp {
              message Choice {
                ChatGptMessage message = 1;
                string finishReason = 2;
                int64 index = 3;
              }
              repeated Choice choices = 1;
              string errorInfo = 2;
            }
            '''
            choices = []
            for choice in openAIResp.choices:
                role = chatgpt.RoleEnum.get(choice.message.role)
                roleInt = chatgpt.RoleEnum.toPb(role)
                choices.append(chatgpt__pb2.AnswerResp.Choice(
                    finishReason=choice.finish_reason,
                    index=choice.index,
                    message=chatgpt__pb2.ChatGptMessage(
                        text=choice.message.content,
                        role=roleInt,
                    ),
                ))
            response.choices.extend(choices)
            return response


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chatgpt_pb2__grpc.add_ChatGptServiceServicer_to_server(ChatGptService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"server started at port {port}")
    server.wait_for_termination()
