# chatgpt-server-python

python写的chatgpt grpc server

## 环境变量

```bash
export OPENAI_API_KEY=your_openai_api_key
export GRPC_SERVER_PORT=50051 # default=50051
```

## docker部署

### 1. 编译二进制

```bash
pip freeze > requirements.txt
tar -czvf chatgpt-server-python.tar.gz requirements.txt main.py pb/* server/* tool/*
pyinstaller --onefile --clean --name=chatgpt-server-python main.py
```

### 2. 构建镜像

```bash
docker build --platform linux/amd64  -t registry.cn-shanghai.aliyuncs.com/xxim-dev/chatgpt-server-python:202303031900 .
```

```bash
docker run --name chatgpt-server-python \
-d -p 50051:50051 \
-e OPENAI_API_KEY=your_openai_api_key \
registry.cn-shanghai.aliyuncs.com/xxim-dev/chatgpt-server-python:202303031900
```

## go sdk 调用示例

```go
package main

import (
	"context"
	chatgptpb "github.com/cherish-chat/chatgpt-server-python/pb"
	"github.com/zeromicro/go-zero/zrpc"
	"log"
)

func main() {
	conf := zrpc.RpcClientConf{
		Endpoints: []string{"127.0.0.1:50051"},
		NonBlock:  true,
		Timeout:   60000,
	}
	chatgptpb.InitClient(conf)
	reply, err := chatgptpb.Answer(context.Background(), &chatgptpb.AnswerReq{
		Messages: []*chatgptpb.ChatGptMessage{{
			Text: "我现在很无聊，我要一直复读你的话，请你不要生气",
			Role: chatgptpb.RoleEnum_User,
		}},
		MaxTokens: 500,
	})
	if err != nil {
		log.Fatalf("error: %v", err)
	} else {
		for _, choice := range reply.Choices {
			log.Printf("choice: %v", choice.Message.Text)
		}
	}
}

```