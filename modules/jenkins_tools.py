import inspect
import sys

class MCP_JobManager():
    def __init__(self, jenkins_auth):
        self.jenkins_auth = jenkins_auth
    
    def mcp_fetchjobinfo(self):
        return "hello fetch job info"


def _register_class_methods_from_module(module, register_func, **init_kwargs):
    for name, cls in inspect.getmembers(module, inspect.isclass):
        if name.startswith("MCP_"):
            try:
                instance = cls(**init_kwargs)  # 传入参数
            except TypeError:
                continue  # 构造函数不接受这些参数就跳过
            for method_name, method in inspect.getmembers(instance, inspect.ismethod):
                print(method_name, method)
                if method_name.startswith("mcp_"):
                    register_func(method)

def register_local_mcp_class_methods(register_func, **init_kwargs):
    """注册当前文件中的 MCP_ 类的 mcp_ 方法"""
    current_module = sys.modules[__name__]
    _register_class_methods_from_module(current_module, register_func, **init_kwargs)

def register_external_mcp_class_methods(module, register_func, **init_kwargs):
    """注册外部模块中的 MCP_ 类的 mcp_ 方法"""
    _register_class_methods_from_module(module, register_func, **init_kwargs)
