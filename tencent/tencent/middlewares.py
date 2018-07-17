# coding=utf-8

from settings import USER_AGENTS
from settings import PROXIES
import random
import base64

#使用linkexractors无法设置随机user-agent,settings文件已有设置（疑似）
class random_user_agent(object):
    def process_requst(self,request,spider):
        #print '*'*50
        user_agent = random.choice(USER_AGENTS)
        #print user_agent
        request.headers.setdefault('User-Agent',user_agent)

class random_proxy(object):
    def process_request(self,request,spider):
        proxy=random.choice(PROXIES)
        print '-' * 50
        print proxy

        if proxy['user_passwd'] is None:
            #代理没有账户验证的使用方式
            request.meta['proxy']='https://'+proxy['ip_port']
        else:
            #代理有账户验证的使用方式

            #对账户密码进行base64编码
            user_passwd_base64=base64.b64decode(proxy['user_passwd'])
            #对应到代理服务器的信令格式
            request.headers['Proxy-Authorization']='Basic '+user_passwd_base64

            #信令格式
            # CONNECT 59.64.128.198:21 HTTP/1.1
            # Host: 59.64.128.198:21
            # Proxy-Authorization: Basic bGV2I1TU5OTIz
            # User-Agent: OpenFetion

            request.meta['proxy']='https://'+proxy['ip_port']