import inspect

"""
    类似于pytest将某种前缀mcp的函数 或者 mcp前缀的类及其mcp开头的类函数识别并注册到 mcpserver中去
"""

# def mcptool_list_open_prs(repo_name: str, github_client) -> list[str]:
#     """列出 GitHub 仓库的 open PR"""
#     repo = github_client.get_repo(repo_name)
#     return [pr.title for pr in repo.get_pulls(state="open")]

# def mcptool_repo_info(repo_name: str, github_client) -> dict:
#     """返回 GitHub 仓库的一些基本信息"""
#     repo = github_client.get_repo(repo_name)
#     return {"full_name": repo.full_name, "stars": repo.stargazers_count}

# def register(mcp, github_client):
#     # 获取当前模块中所有以 mcptool_ 开头的函数
#     for name, func in inspect.getmembers(__import__(__name__), inspect.isfunction):
#         if name.startswith("mcptool_"):
#             # 构造包装器，使得 github_client 成为隐藏参数注入
#             def make_wrapped(f):
#                 return lambda *args, **kwargs: f(*args, github_client=github_client, **kwargs)

#             tool_func = make_wrapped(func)
#             tool_func.__name__ = name  # 保留函数名以避免冲突
#             tool_func.__doc__ = func.__doc__  # 保留文档
#             mcp.tool()(tool_func)  # 注册
