import os
import pickle
import hashlib
from Util.Excel import *
import re
from Util.api_request import api_request
from Config.interfaceInfo import *
from Config.ProjConfigVar import *
from Util.Log import logger


global_vars = {}
proj_path = os.path.dirname(os.path.dirname(__file__))
data_file = os.path.join(proj_path,"Config\\StaticDataFile")

#初始化框架工程中的全局变量global_vars，以字典形式存储测试数据中的唯一值数据。
#框架工程中若要使用字典中的任意一个变量，则每次使用后，均需要将字典中的value值进行加1操作。
#如：global_vars ={"unique_num1":100,"unique_num2":1000}

def get_unique_number_value(unique_number):
    global global_vars
    try:
        with open(data_file,"rb") as fp:
            var = pickle.load(fp) # 读取pickle序列化字节流文件中内容，反序列化成python的字典对象：{"unique_num1":100,"unique_num2":1000}
            data= var[unique_number] # 获取字典对象中key为unique_number的值
            #print("全局唯一数当前生成的值是：%s" %data)
            logger.info("全局唯一数当前生成的值是：%s" %data)
            global_vars[unique_number]=str(data)
            var[unique_number] +=1 # 把字典对象中key为unique_number的值进行加一操作，以便下提取时保持唯一
        with open(data_file,"wb") as fp:
            pickle.dump(var,fp) # 修改后的字典对象，序列化到字节流文件中
    except Exception as e:
        #print("获取测试框架的全局唯一数变量值失败，请求的全局唯一数变量是%s,异常原因如下：%s" %(unique_number,e))
        logger.debug(e)
        data = None
    finally:
        return data

def md5(s):
    m5 = hashlib.md5()
    m5.update(s.encode("utf-8"))
    md5_value = m5.hexdigest()
    return md5_value

def assert_result(respons,key_word):
    """验证数据的正确性"""
    try:
        assert key_word in respons.text
        #print("断言成功")
        logger.info("断言成功")
        return True
    except AssertionError as e:
        #print("断言失败")
        logger.info("断言失败")
        return False


#读取excel文件中某个sheet，获取测试用例
def test_cases_from_test_data_sheet(test_data_excel_path,test_data_sheet_name):
    #print(test_data_excel_path)
    logger.info(test_data_excel_path)
    test_cases_wb = Excel(test_data_excel_path)
    test_cases_wb.get_sheet_by_name(test_data_sheet_name)
    #print("设定的测试用例sheet名称是：%s" % test_data_sheet_name)
    logger.info("设定的测试用例sheet名称是：%s" % test_data_sheet_name)
    #读取所有的接口测试用例
    #print("test_cases_wb_row_values():%s" % test_cases_wb.get_all_row_values())
    logger.info("test_cases_wb_row_values():%s" % test_cases_wb.get_all_row_values())
    #print("*"*50)
    test_cases = []
    for row in test_cases_wb.get_all_row_values():
        if row[test_data_is_executed_col_no] and row[test_data_is_executed_col_no].lower() == "y":
            test_case = row[test_data_row_no_col_no],row[test_data_interface_name_col_no],row[test_data_request_data_col_no],\
                        row[test_data_assert_word_col_no],row[test_data_correlate_regx_col_no]
            test_cases.append(test_case)
    #print("test_cases:",test_cases)
    logger.info("test_cases:%s"% test_cases)

    return test_cases



#将请求数据中包含的${变量名}的字符串部分，替换为唯一数或者全局变量字典中对应的全局变量
def data_handler(requestData):
    if re.search(r"\$\{unique_num\d+\}", requestData):  # 匹配用户名参数，即"${www}"的格式
        var_name = re.search(r"\$\{(unique_num\d+)\}", requestData).group(1)  # 获取用户名参数

        #print("var_name:%s" % var_name)
        logger.info("var_name:%s" % var_name)
        var_value = get_unique_number_value(var_name)
        #print("var_value: %s" % var_value)
        logger.info("var_value: %s" % var_value)
        requestBody = re.sub(r"\$\{unique_num\d+\}", str(var_value), requestData)
        var_name = var_name.split("_")[1]
        #print("var_name: %s" % var_name)
        logger.info("var_name: %s" % var_name)
        global_vars[var_name] = var_value
        #print("global_vars: %s" % str(global_vars))
        logger.info("global_vars: %s" % str(global_vars))

    if re.search(r"\$\{\w+\(.+\)\}", requestData):  # 匹配密码参数,即"${xxx()}"的格式
        var_pass = re.search(r"\$\{(\w+\(.+\))\}", requestData).group(1)  # 获取密码参数
        #print("var_pass: %s" % var_pass)
        logger.info("var_pass: %s" % var_pass)
        #print("eval(var_pass): %s" % eval(var_pass))
        logger.info("eval(var_pass): %s" % eval(var_pass))
        requestData = re.sub(r"\$\{\w+\(.+\)\}", eval(var_pass), requestData)  # 将requestBody里面的参数内容通过eval修改为实际变量值
        #print("requestBody after replace: %s" % requestData)  # requestBody是拿到的请求时发送的数据
        logger.info("requestBody after replace: %s" % requestData)

    if re.search(r"\$\{(\w+)\}", requestData):
        #print("all mached data: ", re.findall(r"\$\{(\w+)\}", requestData))
        for var_name in re.findall(r"\$\{(\w+)\}", requestData):
            #print("替换前 data: ", requestData)
            requestData = re.sub(r"\$\{%s\}" % var_name, str(global_vars[var_name]), requestData)
            #print("替换后 data:", requestData )

    return requestData


#发送接口请求数据到接口的服务器url地址
def send_request(interface_name,data):
    #data_handler主要用于数据处理，因为excel读取的数据都是字符串，需要转换为对应的格式，比如字典，列表，元组等格式，
    # 因为授权信息为元组格式，body是json格式，在转换格式之前先进行变量处理，因此会调用data_handler函数处理
    data = data_handler(data)
    try:
        responseObj = api_request(eval(interface_name)[1],eval(interface_name)[0],eval(data))
        #返回请求对象和请求数据
        return responseObj,data
    except Exception as e:
        #print("调用接口的函数参数出错，调用的参数为%s"%interface_name,"\n错误信息是：",e)
        logger.debug("调用接口的函数参数出错，调用的参数为%s"%interface_name,"\n错误信息是：",e)
        return None,data


def get_test_case_sheet_names(test_data_excel_path):
    #读取行号和需要执行的测试用例sheet名称
    test_cases_wb = Excel(test_data_excel_path)
    test_cases_wb.get_sheet_by_index(1)
    test_case_to_run_sheet_names = []
    for row in test_cases_wb.get_all_row_values():
        #1个需要和1个测试用例sheet名称组成一个元祖
        #多个元祖放入列表中，组成一个测试用例sheet的集合列表
        if row[test_case_test_step_sheet_name_col_no] and row[test_case_is_executed_dol_no].lower() == 'y':
            test_case_to_run_sheet_names.append((row[test_case_row_no_col_no], row[test_case_test_step_sheet_name_col_no]))
            #print("test_case_to_run_sheet_names: %s" % test_case_to_run_sheet_names)
            logger.info("test_case_to_run_sheet_names: %s" % test_case_to_run_sheet_names)
    return test_case_to_run_sheet_names



# 测试代码
if __name__ =="__main__":
    #print("proj_path: ", proj_path)
    #print("data_file: ", data_file)
    #初始化2个唯一书变量，初始值可以根据数据的使用情况进行自定义

    data={"unique_num1":100,"unique_num2":1000}
    with open(data_file,"wb") as fp:
        pickle.dump(data,fp) # 把data对象用pickle.dump()方法序列化到文件中存储
    with open(data_file,"rb") as fp:
        data=pickle.load(fp) # 把文件中的内容用pickle.load()方法反序列化成python中的对象
    #print("data: ", data)
    #print('data["unique_num1"]: ', data["unique_num1"])
    #print('data["unique_num2"]: ', data["unique_num2"])

    #print(get_unique_number_value("unique_num1"))
    #print(get_unique_number_value("unique_num2"))

#    get_test_case_sheet_names(test_data_file)