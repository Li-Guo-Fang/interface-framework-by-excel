import requests
import json
import hashlib
import re
from Util.Log import logger

def api_request(url,request_method,request_content):
    if request_method =="get":
        try:
            if isinstance(request_content,dict):
                #print("请求的接口地址是：%s" %url)
                logger.info("请求的接口地址是：%s" %url)
                #print("请求的数据是：%s" %request_content)
                logger.info("请求的数据是：%s" %request_content)
                r = requests.get(url,params=json.dumps(request_content))
            else:
                r = requests.get(url+str(request_content))
                #print("请求的接口地址是：%s" %r.url)
                logger.warning("请求的接口地址是：%s" %r.url)
                #print("请求的数据是：%s" %request_content)
                logger.warning("请求的数据是：%s" %request_content)
        except BaseException as e:
            #print("get 方法请求发生异常：请求的url是：%s,请求的内容是：%s\n发生的异常信息如下：%s"%(url,request_content,e))
            logger.debug(e)
            r = None
        return r
    elif request_method == "post":
        try:
            if isinstance(request_content,dict):
                #print("请求的接口地址是:%s" %url)
                logger.info("请求的接口地址是:%s" %url)
                #print("请求的数据是;%s" %json.dumps(request_content))
                logger.info(json.dumps("请求的数据是;%s" %json.dumps(request_content)))
                r = requests.post(url,data=json.dumps(request_content))
            else:
                raise ValueError
        except ValueError as e:
            #print("post方法请求发生异常：请求的url是%s,请求的内容是%s\n发生的异常信息如下：%s" %(url,request_content,e))
            logger.debug(e)
            r = None
        return r
    elif request_method == "put":
        try:
            if isinstance(request_content,dict):
                #print("请求的接口地址是：%s"%url)
                logger.info("请求的接口地址是：%s"%url)
                #print("请求的数据是：%s"%json.dumps(request_content))
                logger.info("请求的数据是：%s"%json.dumps(request_content))
                r = requests.put(url,data = json.dumps(request_content))
            else:
                raise ValueError
        except ValueError as e:
            #print("put 方法请求发生异常：请求的url是%s,请求的内容是%s\n发生异常信息如下："%(url,request_content,e))
            logger.debug(e)
            r = None
        return r