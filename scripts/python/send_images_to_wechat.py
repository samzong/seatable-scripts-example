"""
This script is read current row image and wecom webhook_url, then send as message.
It requires the `seatable-api` package to be installed.
"""

__author__ = "Samzong Lu"
__version__ = "1.0.0"

import requests
import base64
from seatable import context

# 图片 URL 列表
image_urls = [
    context.current_row['png_01'],
    context.current_row['png_02'],
    context.current_row['png_03']
]

# 企业微信 webhook URL
webhook_url = context.current_row['webhook_url']

# 检查 URL 是否为空
def validate_urls(image_urls, webhook_url):
    if not webhook_url:
        raise ValueError("Webhook URL 为空")
    for url in image_urls:
        if not url:
            raise ValueError("图片 URL 为空")
        if not url.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValueError(f"URL {url} 不是有效的图片链接")

# 发送文本消息
def send_text_message(content):
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    requests.post(webhook_url, json=data)

# 发送图片消息
def send_image_message(base64_content):
    data = {
        "msgtype": "image",
        "image": {
            "base64": base64_content,
            "md5": base64.b64decode(base64_content).hex()
        }
    }
    requests.post(webhook_url, json=data)

# 下载图片并转换为 base64，检查大小
def download_and_convert_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_content = response.content
        if len(image_content) <= 2 * 1024 * 1024:  # 检查图片大小是否小于等于2MB
            return base64.b64encode(image_content).decode('utf-8')
        else:
            raise ValueError(f"图片 {url} 大于2MB，无法发送")
    else:
        raise ValueError(f"无法下载图片 {url}")

# 主函数
def main():
    try:
        validate_urls(image_urls, webhook_url)
    except ValueError as e:
        print(f"错误: {e}")
        return

    send_text_message("开始发送消息")
    
    for url in image_urls:
        try:
            base64_image = download_and_convert_image(url)
            if base64_image:
                send_image_message(base64_image)
        except ValueError as e:
            print(f"错误: {e}")
            return
    
    send_text_message("结束发送消息")

if __name__ == "__main__":
    main()
