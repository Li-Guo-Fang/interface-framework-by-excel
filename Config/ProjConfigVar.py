import os

proj_path = os.path.dirname(os.path.dirname(__file__))
test_data_file = os.path.join(proj_path,"TestData","接口测试数据.xlsx")

#excel中测试用例数据管理
test_data_row_no_col_no = 0
test_data_interface_name_col_no = 1
test_data_request_data_col_no = 2
test_data_response_data_col_no = 3
test_data_assert_word_col_no = 4
test_data_test_result_col_no = 5
test_data_correlate_regx_col_no = 6
test_data_test_elapse_time_col_no = 7
test_data_is_executed_col_no = 8
test_data_executed_time_col_no = 9


#测试用例的管理
test_case_row_no_col_no = 0
test_case_test_step_sheet_name_col_no = 2
test_case_is_executed_dol_no = 3
test_case_executed_result_col_no = 7
test_case_executed_time_col_no = 8

#邮件参数
mail_host = "smtp.qq.com"    #服务器
mail_user = "1317872262@qq.com"    #用户名
mail_pass = "gzayzlyjmwgriaee"    #口令

sender = "1317872262@qq.com"
receivers = "18301991450@163.com"

#日志配置路径
conf_path = os.path.join(proj_path + u"\Config\Logger.conf")

#统计
total_cases = 0
success_cases = 0
falses_cases = 0