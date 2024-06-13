from seatable_api import Base,context
import requests

server_url = context.server_url
api_token = context.api_token

base = Base(api_token, server_url)
base.auth()

current_row = context.current_row
username = context.current_username

keyword = current_row.get('过滤关键词', None)
current_url = current_row.get('seatable_share_url', None)
current_row_id = current_row.get('_id', None)

# 检查当前行的字段状态 seatable_share_url 不为空时，不执行
# 获取关键词, 关键词为空，不执行
# 调用 api 初始化项目，respone {}.app_uuid, 调用报错了，提示错误，联系 船长
# 保存 uuid 到 seatable_share_url

def alter_tips(msg,type):
    return base.send_toast_notification(username, msg, toast_type=type)

def update_share_url(app_uuid: str):
    data = {
      "seatable_share_url": app_uuid
    }
    try:
      base.update_row(table_name="BxRl",row_id=current_row_id,row_data=data)
    except Exception as e:
       alter_tips(msg="应用创建成功，但 seatable_share_url 更新失败，请自行填写。", type="danger")


if not current_url and keyword is not None:
   url = "http://172.30.120.156:8002/add_project"  # 这个 API 做了复制应用，并批量更新对应的 filter 参数
   data = {
     "project": keyword
   }
   headers = {
     "Content-Type": "application/json"
   }
   try:
       resp = requests.post(url=url,json=data,headers=headers)
       print(resp.json())
       update_share_url(app_uuid=resp.json()['app_uuid'])
       alter_tips(msg="创建成功", type="success")
   except Exception as e:
       alter_tips(msg="创建失败，稍后重试", type="danger")
   
else:
   alter_tips(msg="项目应用已创建，无需重复创建！", type="warning")



