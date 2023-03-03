#!/bin/zsh
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chatgpt.proto
protoc chatgpt.proto --go_out=.. --go-grpc_out=..
go mod tidy