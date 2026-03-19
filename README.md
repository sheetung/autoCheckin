# 科研通 & NewAPI 青龙签到脚本

一个基于青龙面板的自动签到工具，支持科研通和NewAPI站点的自动签到，支持多账号/多站点管理、推送通知和异常处理。

![image](https://img.shields.io/github/stars/sheetung/autoCheckin) | ![image](https://img.shields.io/github/forks/sheetung/autoCheckin) | ![image](https://img.shields.io/github/issues/sheetung/autoCheckin)

## 🌟 功能特性

1. **多账号/多站点管理**：
   - 科研通：支持多个账号同时签到
   - NewAPI：支持多个站点同时签到
2. **智能识别状态**：自动判断签到结果（成功 / 失败 / 已签到）
3. **详细签到信息**：
   - 科研通：显示签到状态
   - NewAPI：显示签到状态、累计天数、获得金额和历史记录
4. **多推送通知**：
   - 钉钉机器人消息提醒（支持 Markdown 格式）
   - Bark 消息推送（iOS 专属，未测试）
5. **异常处理机制**：自动捕获网络错误、Cookie 失效等问题
6. **日志记录**：控制台输出详细的签到过程和结果

## 🚀 使用方法

### 1. 订阅配置

在青龙面板「订阅管理」中添加：

- **名称**：签到脚本
- **链接**：`https://github.com/sheetung/autoCheckin.git`
- **分支**：`master`
- **定时规则**：根据需求设置（例如 `0 0 * * *` 每天凌晨执行）
- **文件后缀**：`py`

### 2. 环境变量配置

#### 科研通
在青龙面板「环境变量」中设置：

```bash
# 多个Cookie用&分隔
export ABLESCI_COOKIES="cookie1&cookie2&cookie3"
```

#### NewAPI
在青龙面板「环境变量」中设置：

```bash
# 多个站点用&分隔，每个站点格式为 url@cookie
export NEWAPI_ACCOUNTS="http://127.0.0.1:3333/@session=your_cookie_here&http://example.com/@session=another_cookie"
```

### 3. 推送配置（可选）

在青龙面板「配置文件」中设置：

```bash
# 钉钉推送配置（可选）
export DD_BOT_TOKEN="your_dingtalk_token"
export DD_BOT_SECRET="your_dingtalk_secret"

# Bark推送配置（可选，未测试）
export BARK_PUSH="your_bark_key"
```

## 📦 部署说明

1. 确保青龙面板已安装 Python 环境
2. 通过 Git 或手动上传方式部署脚本
3. 首次运行前检查环境变量是否正确配置

## 📝 运行示例

### 科研通

```bash
正在签到第 1 个账号...
正在使用 Cookie 签到: abcdefghijklmnopqr...
签到结果: {'status': 'error', 'message': '签到失败，您今天已于 [07:00:01] 签到'}
第 1 个账号签到完成

签到结果汇总：
{'status': 'error', 'message': '签到失败，您今天已于 [07:00:01] 签到'}
✅ bark推送成功
✅ 钉钉推送成功
```

### NewAPI

```bash
正在签到第 1 个站点...
正在签到站点: http://49.233.13.104:3333
使用 Cookie: session=MTc3MzcyNTk5...
签到结果: 今日已签到
累计签到: 2 天
累计获得: ¥0.0300
最近签到记录:
  - 2026-03-19: ¥0.02
  - 2026-03-16: ¥0.01
第 1 个站点签到完成

签到结果汇总：
站点: http://49.233.13.104:3333/
结果: {'status': 'success', 'message': '签到成功', 'data': {'message': '今日已签到', 'success': False, 'detail': {'data': {'enabled': True, 'max_quota': 10, 'min_quota': 1, 'stats': {'checked_in_today': True, 'checkin_count': 2, 'records': [{'checkin_date': '2026-03-19', 'quota_awarded': 2}, {'checkin_date': '2026-03-16', 'quota_awarded': 1}], 'total_checkins': 2, 'total_quota': 3}}, 'success': True}}

✅ bark推送成功
✅ 钉钉推送成功
```

## ⚠️ 注意事项

1. 钉钉推送功能需要正确配置机器人权限，例如关键词和`DD_BOT_SECRET`
2. NewAPI站点的Cookie需要包含session信息，格式为`session=your_session_id`
3. 本工具仅用于学习交流，禁止用于商业用途

## 📜 声明

```plaintext
本项目所有代码仅用于学习和研究目的，严禁用于商业用途。
用户需遵守相关网站的用户协议及相关法律法规。
下载后请在24小时内删除，否则一切法律后果自负。
```

## 📢 反馈与贡献

- 提交问题：[GitHub Issues](https://github.com/sheetung/ablesciCheck/issues)
- 代码贡献：[Fork & Pull Request](https://github.com/sheetung/ablesciCheck/pulls)

> 开源协议：MIT License