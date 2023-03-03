import os

from server.server import serve

if __name__ == '__main__':
    port = os.getenv("GRPC_SERVER_PORT", 50051)
    serve(port)
