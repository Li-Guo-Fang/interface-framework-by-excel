import json
import re
import hashlib
import requests
from Util.api_request import api_request
from Config.interfaceInfo import *
from Config.ProjConfigVar import *
from Util.Excel import Excel
from Config.ProjConfigVar import *
from Util.DataHandler import *
import time
from html_report import report_html
from Util.Mail import send_mail
from Util.Log import *

#获取测试数据文件的绝对路径
test_data_excel_path = os.path.join(proj_path,"TestData\\接口测试数据.xlsx")
#test_data_sheet_name = "注册登录"
test_cases_wb = Excel(test_data_excel_path)
#test_cases_wb.get_sheet_by_name(test_data_sheet_name)

test_results_for_html_report = []


#读取所有的接口测试用例
#test_cases = test_case_from_test_data_sheet(test_data_excel_path,test_data_sheet_name)


#遍历执行所有sheet中的测试用例
for test_sheet_name in get_test_case_sheet_names(test_data_excel_path):
    flag = True
    test_cases_wb.get_sheet_by_name(test_sheet_name[1])
    test_cases = test_cases_from_test_data_sheet(test_data_excel_path,test_sheet_name[1])
    #print('test_cases:',test_cases)

    for case in test_cases:
        start_time = time.time()
        interfaceName = case[1]
        logging.info("接口名称: %s" % interfaceName)
        requestBody = case[2]
        logging.info("请求body: %s" % str(requestBody))

        #print("接口名称: %s, eval()执行后值为: %s" % (interfaceName, eval(interfaceName)))      #eval的用法是去掉“”号
        assertKey = case[3]
        #print("断言关键字：%s" %assertKey)
        logger.info("断言关键字：%s" %assertKey)
        requestUrl = eval(interfaceName)
        #print("requestUrl: %s" % requestUrl)


        #requestBody = data_handler(requestBody)

        # 发送注册接口请求，请求方式为post
        responseObj,send_data = send_request(interfaceName,requestBody)
        total_cases+=1
        end_time = time.time()
        #print("请求结果(responseObj.text):", responseObj.text)
        logger.info(responseObj.text)

        #写入请求结果
        test_cases_wb.write_cell_value(int(case[0]+1),test_data_response_data_col_no+1,responseObj.text)

        #写入用例执行当前时间
        test_cases_wb.write_current_time(int(case[0]+1),test_data_executed_time_col_no+1)


        #处理断言并写入结果
        try:
            if not assert_result(responseObj,assertKey):
                raise AssertionError
            test_cases_wb.write_cell_value(int(case[0]+1),test_data_test_result_col_no+1,"成功")
            test_results_for_html_report.append((responseObj.url,send_data,responseObj.text,int(end_time - start_time)*1000,assertKey,"成功"))
            success_cases+=1
        except AssertionError:
            test_cases_wb.write_cell_value(int(case[0])+1,test_data_test_result_col_no+1,"失败")
            test_results_for_html_report.append((responseObj.url,send_data,responseObj.text,int(end_time - start_time)*1000,assertKey,"失败"))
            flag = False
            falses_cases+=1
        except:
            test_cases_wb.write_cell_value(int(case[0]) + 1, test_data_test_result_col_no + 1, "失败")
            test_results_for_html_report.append(
                (responseObj.url, send_data, responseObj.text, int(end_time - start_time) * 1000, assertKey, "失败"))
            flag = False
            falses_cases+=1

        #print("接口请求的耗时为 %d 毫秒"%((end_time - start_time)*1000))
        logger.info((end_time - start_time)*1000)

        #写入用例执行的耗时
        test_cases_wb.write_cell_value(int(case[0] + 1),test_data_test_elapse_time_col_no + 1,str(int(end_time - start_time)*1000))

        test_cases_wb.write_cell_value(5,1,"总用例执行条数：%s，成功用例条数：%s,失败用例条数：%s" %(total_cases,success_cases,falses_cases))


        correlate_regx = case[4]

        if correlate_regx:
            #print("关系表达式：%s" %str(correlate_regx))
            logger.info(str(correlate_regx))
            var_name = correlate_regx.split("||")[0]
            regx = correlate_regx.split("||")[1]

            if re.search(regx,responseObj.text).group(1):
                var_value = re.search(regx,responseObj.text).group(1)
                global_vars[var_name] = var_value
                #print("从响应中提取的变量名：%s，变量值为%s"%(var_name,var_value))
                logger.info(var_name)
                logger.info(var_value)
                #print("生成的全局变量名：globe_vars[%s]=%s" %(var_name,global_vars[var_name]))
                logger.info(var_name)
                logger.info(global_vars[var_name])


    test_cases_wb.get_sheet_by_index(1)

    if flag:
        test_cases_wb.write_cell_value(int(test_sheet_name[0]) + 1,test_case_executed_result_col_no,"成功")
    else:
        test_cases_wb.write_cell_value(int(test_sheet_name[0]) + 1,test_case_executed_result_col_no,"失败")

    test_cases_wb.write_current_time(int(test_sheet_name[0])+1,test_case_executed_time_col_no)

    #print("#"*50)


#html_name = "接口自动化测试报告"
#report_html(test_results_for_html_report,html_name)


#发送邮件报告
html_name = '接口自动化测试报告'
report_html(test_results_for_html_report,html_name)
send_mail(html_name + '.html')


