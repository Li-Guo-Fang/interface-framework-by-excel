from Util.GetConfig import Config
import os
from Config.ProjConfigVar import proj_path


#读取工程的配置文件
data_path = os.path.join(proj_path,"Config\\interace_server_info.ini")
config = Config(data_path)

#读取配置文件中的ip信息
ip = config.get_option("interface_server","ip")

#读取配置文件中的端口信息
port = config.get_option("interface_server","port")


#根据读取的ip和端口信息，生成不同接口的请求url
#将接口请求的url和接口文档中定义的请求方法封装在元组中，供框架中的其他代码使用
register = ("post","http://%s:%s/register/" %(ip,port))
login =  ("post","http://%s:%s/login/" %(ip,port))
create =("post","http://%s:%s/create/" %(ip,port))
getblogsofuser = ("post","http://%s:%s/getBlogsOfUser/" %(ip,port))
getblogcontent = ("get","http://%s:%s/getBlogContent/" %(ip,port))
update = ("put","http://%s:%s/update/" %(ip,port))
delete = ("post","http://%s:%s/delete/" %(ip,port))