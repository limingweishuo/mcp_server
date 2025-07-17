import random
import requests, time
from requests.auth import HTTPBasicAuth
from fastmcp import FastMCP

import modules.github_tools as github_tools
import modules.jenkins_tools as jenkins_tools
import modules.aws_tools as aws_tools
import modules.spinnaker_tools as spinnaker_tools

from config.aws_config import *
from config.github_config import *
from config.jenkins_config import *
from config.spinnaker_config import *

mcp = FastMCP(name="Devops Mcp")

class Devop_MCP():
    def __init__(self, mcp):
        self.mcp = mcp
        self.github_client = None
        self.jenkins_client = None
        self.jenkins_auth = None
        self.boto_session = None
        self.spinnaker_api = None

    def init_client(self):
        self.jenkins_auth = HTTPBasicAuth(JENKINS_USERNAME, JENKINS_API_TOKEN)

    def tool_register(self):
        # github_tools.register(self.mcp, github_client)
        jenkins_tools.register_local_mcp_class_methods(self.mcp.tool, jenkins_auth = self.jenkins_auth)
        # aws_tools.register(mcp, boto_session)
        # spinnaker_tools.register(mcp, spinnaker_api)

if __name__ == "__main__":
    # 注册各模块
    dcp = Devop_MCP(mcp=mcp)
    dcp.init_client()
    dcp.tool_register()

    mcp.run()