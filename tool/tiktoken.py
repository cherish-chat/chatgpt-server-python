import tiktoken

# 使用 tiktoken 判断 token 数量 是否超过 n 个，如果超过，截断后面的 token

enc = tiktoken.get_encoding("gpt2")


class TokenInfo:
    def __init__(self):
        # 原始文本
        self.text: str = ""
        # 截断后的文本
        self.text_truncated: str = ""
        # 原始文本的 token 数量
        self.length: int = 0
        # 截断后的文本的 token 数量
        self.length_truncated: int = 0

    def __str__(self):
        return f"TokenInfo(text={self.text}, text_truncated={self.text_truncated}, length={self.length}, length_truncated={self.length_truncated})"


def get_token_info(text: str, n: int = 2048, is_split: bool = True) -> TokenInfo:
    token_info = TokenInfo()
    token_info.text = text
    token_info.length = len(enc.encode(text))
    if is_split:
        if token_info.length > n:
            token_info.text_truncated = enc.decode(enc.encode(text)[:n])
            token_info.length_truncated = len(enc.encode(token_info.text_truncated))
    else:
        token_info.text_truncated = token_info.text
        token_info.length_truncated = token_info.length
    return token_info
