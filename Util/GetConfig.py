import configparser
import os

class Config(object):

    def __init__(self,config_file_path):
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()   #创建ConfigParser类的对象
        self.config.read(self.config_file_path)

    def get_all_sections(self):    #获取所有的section信息，列表返回
        return self.config.sections()

    def get_option(self,section_name,option_name):    #返回该section下的对应配置项的值
        value = self.config.get(section_name,option_name)
        return value

    def all_section_items(self,section_name):    #返回该section下的所有配置项的信息，以字典的形式返回
        items = self.config.items(section_name)
        #print(items)
        return dict(items)

if __name__=="__main__":
    proj_path = os.path.dirname(os.path.dirname(__file__))
    print("proj_path:%s"%proj_path)
    data_file = os.path.join(proj_path,"Config\\interace_server_info.ini")
    print("data_file:%s"%data_file)
    config = Config(data_file)
    print("all sections in config:",config.get_all_sections())
    for section in config.get_all_sections():
        print("items in section [%s]:%s" %(section,config.all_section_items(section)))
    ip = config.get_option("interface_server","ip")
    port = config.get_option("interface_server","port")
    print("ip:%s" %ip)
    print("port:%s" %port)

