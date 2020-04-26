from bottle import template

def report_html(data,html_name):

    #定义变量保存模板字符串
   template_demo = """
   <!-- CSS goes in the document HEAD or added to your external stylesheet -->
<style type="text/css">
table.hovertable {
    font-family: verdana,arial,sans-serif;
    font-size:11px;
    color:#333333;
    border-width: 1px;
    border-color: #999999;
    border-collapse: collapse;
}
table.hovertable th {
    background-color:#ff6347;
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #a9c6c9;
}
table.hovertable tr {
    background-color:#d4e3e5;
}
table.hovertable td {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #a9c6c9;
}
</style>

<!-- Table goes in the document BODY -->

<head>

<meta http-equiv="content-type" content="txt/html; charset=utf-8" />

</head>

<table class="hovertable">
<tr>
    <th>接口 URL</th><th>请求数据</th><th>接口响应数据</th><th>接口调用耗时(单位：ms)</th><th>断言词</th><th>测试结果</th>
</tr>
% for url,request_data,response_data,test_time,assert_word,result in items:
<tr onmouseover="this.style.backgroundColor='#ffff66';" onmouseout="this.style.backgroundColor='#d4e3e5';">

    <td>{{url}}</td><td>{{request_data}}</td><td>{{response_data}}</td><td>{{test_time}}</td><td>{{assert_word}}</td><td>
    % if result == '失败':
    <font color=red>
    % end
    {{result}}</td>
</tr>
% end
</table>
   """

    #渲染该模板字符串，template()函数的第一个参数是要渲染的模板名称，第二个参数是模板中需要用到的对象
    # 此处传入的是保存测试结果的列表对象，返回的结果是渲染之后的模板（字符串对象）
   html = template(template_demo, items=data)
   with open(html_name+".html", 'wb') as f:
      f.write(html.encode('utf-8'))