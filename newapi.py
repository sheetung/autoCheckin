# -*- coding: utf-8 -*-
"""
new Env('NewAPI签到');
"""
import os
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse

# 添加bark推送
bark_push = "https://api.day.app/{key}" #(自建推送的自行替换整段url，非自建只需替换key即可)
bark_group = "NewAPI"
bark_icon = "https://staticres.ablesci.com/apple-touch-icon.png"
bark_sound = os.environ.get("BARK_SOUND", "")

# 添加钉钉推送
dingtalk_token = os.environ.get("DD_BOT_TOKEN", "")
dingtalk_secret = os.environ.get("DD_BOT_SECRET", "")

class NewAPI:
    name = "NewAPI签到"

    def __init__(self, url, cookie, user_id="2"):
        self.url = url.rstrip('/')
        self.cookie = cookie
        self.user_id = user_id

    def sign(self):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": self.cookie,
            "DNT": "1",
            "Referer": f"{self.url}/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "New-Api-User": self.user_id  # 使用传入的用户ID
        }
        # 签到URL，根据NewAPI站点的实际签到接口调整
        # 从测试结果看，正确的接口路径是 /api/user/checkin
        sign_url = f"{self.url}/api/user/checkin"
        try:
            # 尝试使用POST请求进行签到
            response = requests.post(sign_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            # 获取详细的签到信息
            detail_response = requests.get(sign_url, headers=headers)
            detail_response.raise_for_status()
            detail_result = detail_response.json()
            
            # 合并结果
            result['detail'] = detail_result
            return {"status": "success", "message": "签到成功", "data": result}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"签到失败: {str(e)}"}

    def main(self):
        print(f"正在签到站点: {self.url}")
        print(f"使用 Cookie: {self.cookie[:20]}...")
        result = self.sign()
        
        # 解析并显示详细的签到信息
        if result.get('data'):
            签到状态 = result['data'].get('message', '未知')
            详细信息 = result['data'].get('detail', {})
            
            if 详细信息.get('data'):
                数据 = 详细信息['data']
                统计信息 = 数据.get('stats', {})
                总签到次数 = 统计信息.get('total_checkins', 0)
                总获得金额 = 统计信息.get('total_quota', 0) * 0.01  # 假设1配额=0.01元
                
                print(f"签到结果: {签到状态}")
                print(f"累计签到: {总签到次数} 天")
                print(f"累计获得: ¥{总获得金额:.4f}")
                
                # 显示最近的签到记录
                记录 = 统计信息.get('records', [])
                if 记录:
                    print("最近签到记录:")
                    for 一条记录 in 记录:
                        日期 = 一条记录.get('checkin_date', '未知')
                        获得金额 = 一条记录.get('quota_awarded', 0) * 0.01
                        print(f"  - {日期}: ¥{获得金额:.2f}")
            else:
                print(f"签到结果: {result}")
        else:
            print(f"签到结果: {result}")
        
        return result

def send_bark_notification(results):
    if not bark_push:
        print("未配置Bark推送，跳过通知")
        return

    title = "NewAPI签到"
    body_lines = []

    for idx, (url, result) in enumerate(results, 1):
        if result.get('status') == 'success':
            msg = result.get('data', {}).get('msg', '签到成功（无详细信息）')
            body_lines.append(f"站点{idx} ({url}): {msg}")
        else:
            error = result.get('message', '未知错误')
            body_lines.append(f"站点{idx} ({url}): ❌签到失败 - {error}")

    body = "\n".join(body_lines)

    # 构造Bark请求参数
    params = {
        'title': title,
        'body': body,
        'icon': bark_icon,
        'sound': bark_sound,
        'group': bark_group
    }

    # 发送POST请求（JSON格式）
    bark_url = f"{bark_push}"
    try:
        resp = requests.post(bark_url, json=params)
        resp.raise_for_status()
        print("✅ Bark推送成功")
    except Exception as e:
        print(f"❌ Bark推送失败: {str(e)}")

def send_dingtalk_notification(results):
    if not dingtalk_token:
        print("未配置钉钉推送，跳过通知")
        return

    title = "NewAPI签到"
    text_lines = []
    text_lines.append(f"# {title}")
    for idx, (url, result) in enumerate(results, 1):
        if result.get('status') == 'success':
            msg = result.get('data', {}).get('msg', '签到成功（无详细信息）')
            text_lines.append(f"站点{idx} ({url}): {msg}\n")
        else:
            error = result.get('message', '未知错误')
            text_lines.append(f"站点{idx} ({url}): ❌签到失败 - {error}\n")

    text = "\n".join(text_lines)

    # 构造钉钉消息体
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        }
    }

    # 签名验证
    if dingtalk_secret:
        timestamp = str(round(time.time() * 1000))
        secret_enc = dingtalk_secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, dingtalk_secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        dingtalk_url = f"https://oapi.dingtalk.com/robot/send?access_token={dingtalk_token}&timestamp={timestamp}&sign={sign}"
    else:
        dingtalk_url = f"https://oapi.dingtalk.com/robot/send?access_token={dingtalk_token}"

    headers = {"Content-Type": "application/json; charset=utf-8"}
    try:
        resp = requests.post(dingtalk_url, json=data, headers=headers)
        print(f"钉钉响应：{resp.text}")
        resp.raise_for_status()
        print("✅ 钉钉推送成功")
    except requests.exceptions.HTTPError as e:
        print(f"❌ 钉钉推送失败: {e}")
        print(f"错误详情: {resp.text}")
    except Exception as e:
        print(f"❌ 钉钉推送失败: {str(e)}")

def main():
    # 读取环境变量 NEWAPI_ACCOUNTS，格式为 url@cookie&url@cookie
    accounts = os.getenv("NEWAPI_ACCOUNTS")
    if not accounts:
        print("未找到环境变量 NEWAPI_ACCOUNTS，请检查配置")
        return

    # 解析账号列表
    account_list = accounts.split("&")
    results = []
    
    for i, account in enumerate(account_list):
        print(f"正在签到第 {i + 1} 个站点...")
        try:
            # 解析 url@cookie 格式
            url, cookie = account.split("@")
            
            # 从URL中提取用户ID（如果需要）
            # 这里假设用户ID是固定的，实际使用时可能需要从cookie或URL中提取
            user_id = "2"  # 默认为用户ID 2
            
            # 使用正确的路径进行签到
            result = NewAPI(url, cookie, user_id).main()
            results.append((url, result))
        except Exception as e:
            results.append(("", {"status": "error", "message": f"第 {i + 1} 个站点签到失败: {str(e)}"}))
        print(f"第 {i + 1} 个站点签到完成\n")

    print("\n签到结果汇总：")
    for url, result in results:
        print(f"站点: {url}")
        print(f"结果: {result}")
        print()

    # 发送Bark通知
    send_bark_notification(results)

    # 发送钉钉通知
    send_dingtalk_notification(results)

if __name__ == "__main__":
    main()