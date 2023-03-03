package pb

import (
	"context"
	"github.com/zeromicro/go-zero/zrpc"
)

var chatGptServiceClient_ ChatGptServiceClient

func InitClient(conf zrpc.RpcClientConf) {
	grpcClient := zrpc.MustNewClient(conf)
	chatGptServiceClient_ = NewChatGptServiceClient(grpcClient.Conn())
}

func Answer(ctx context.Context, req *AnswerReq) (*AnswerResp, error) {
	return chatGptServiceClient_.Answer(ctx, req)
}
