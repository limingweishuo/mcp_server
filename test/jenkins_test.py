import requests, time
from requests.auth import HTTPBasicAuth


# 轮询 queue item 直到获得 build number
def wait_for_build_number(queue_url, auth, max_wait=60):
    for i in range(max_wait):
        r = requests.get(f"{queue_url}api/json", auth=auth)
        if r.status_code == 200:
            data = r.json()
            if 'executable' in data:
                return data['executable']['number']
        time.sleep(1)
    return None


# 无参数触发 newportal release/cosv3_1.16
def trigger_cosv3_noparams():
    # Jenkins 账号信息
    USERNAME = 'lim2'
    API_TOKEN = '11dfa16e653e865bddd27a8b0c19daff46'

    # Jenkins Job 的完整路径（注意：必须是 multibranch 的子 job）
    JENKINS_URL = 'https://master-2.jenkins.autodesk.com'
    JOB_PATH = 'job/raas/job/raas.portal/job/release%252Fcosv3_1.16/'
    TRIGGER_URL = f'{JENKINS_URL}/{JOB_PATH}/build'  # 如果是参数化构建则用 buildWithParameters

    auth = HTTPBasicAuth(USERNAME, API_TOKEN)

    # 触发构建
    resp = requests.post(TRIGGER_URL, auth=auth)

    if resp.status_code == 201:
        print("✅ 构建已触发")
        queue_url = resp.headers.get('Location') # 获取队列信息
    else:
        print(f"❌ 触发失败，状态码: {resp.status_code}")
        print(resp.text)

    """
        Jenkins 确实返回了 queue URL，但Jenkins还没有开始构建queue item只是排队中，等Jenkins分配executor之后，才会关联一个构建编号（如 #517）
    """
    build_number = wait_for_build_number(queue_url, auth)
    if build_number:
        print(f"🎉 构建编号：#{build_number}")
    else:
        print("⌛ 构建编号获取超时")
    

# 获取某个分支的最新的构建信息，而非日志
def fetch_lastbuild_info():
    JENKINS_URL = 'https://master-2.jenkins.autodesk.com'
    JOB_PATH = 'job/raas/job/APITest/job/master'
    auth = HTTPBasicAuth('lim2', '11dfa16e653e865bddd27a8b0c19daff46')
    url = f"{JENKINS_URL}/{JOB_PATH}/lastBuild/api/json"
    resp = requests.get(url, auth=auth)
    if resp.status_code == 200:
        data = resp.json()
        print(data)
        print(f"✅ 构建编号: #{data['number']}")
        print(f"📊 状态: {data['result']}")
        print(f"⏱️ 耗时: {data['duration'] / 1000:.2f} 秒")
    else:
        print("❌ 查询失败:", resp.status_code)


# 获取某个流水线执行需不需要参数
JENKINS_URL = 'https://master-2.jenkins.autodesk.com'
JOB_PATH = 'job/raas/job/APITest/job/master'
auth = HTTPBasicAuth('lim2', '11dfa16e653e865bddd27a8b0c19daff46')

url = f'{JENKINS_URL}/{JOB_PATH}/api/json'
resp = requests.get(url, auth=auth)
data = resp.json()

# 查找参数定义
for p in data.get("property", []):
    if p.get("_class") == "hudson.model.ParametersDefinitionProperty":
        print("✅ 该 Job 需要参数")
        for param in p.get("parameterDefinitions", []):
            print(f"- {param['name']} (type: {param['type']}, default: {param.get('defaultParameterValue', {}).get('value')})")
    else:
        print("✅ 此 Job 不需要参数，可直接触发 /build 接口")


