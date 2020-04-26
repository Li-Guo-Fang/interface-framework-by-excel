import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from Config import ProjConfigVar
from Util.Log import logger
from Util.Log import logger


def send_mail(attach_file_path):
    mail_host = ProjConfigVar.mail_host
    mail_user = ProjConfigVar.mail_user
    mail_pass = ProjConfigVar.mail_pass
    sender = ProjConfigVar.sender
    receivers = ProjConfigVar.receivers

    #创建一个带附件类型的MIMEMultipart()实例
    message = MIMEMultipart()

    #对邮件属性赋值
    message['From'] = formataddr(['李国芳','1317872262@qq.com'])
    message['To'] = ''.join(receivers)
    subject = '接口自动化执行测试报告'
    message['Subject'] = Header(subject,'utf-8')

    #邮件正文内容
    message.attach(MIMEText('最新执行的接口自动化测试报告，请参阅附件内容！','plain','utf-8'))

    #构造附件1，传送测试结果的exce文件
    #print("os.path.exists(attach_file_path):%s" % os.path.exists(attach_file_path))
    logger.info("os.path.exists(attach_file_path):%s" % os.path.exists(attach_file_path))

    logger.info(os.path.exists(attach_file_path))

    #构建附件对象，添加html文件
    att = MIMEBase('application','octet-stream')
    att.set_payload(open(attach_file_path,'rb').read())
    att.add_header('Content-Disposition','attachment',filename=('utf-8','','接口自动化测试报告.html'))
    encoders.encode_base64(att)
    message.attach(att)

    try:
        #创建一个SMTP对象
        smtpObj = smtplib.SMTP(mail_host)

        #传入用户名和密码登录邮箱
        smtpObj.login(mail_user,mail_pass)

        #发送传参数包括发件人地址，收件人地址和邮件内容
        smtpObj.sendmail(sender,receivers,message.as_string())
        #print("邮件发送成功")
        logger.info("邮件发送成功")

    except smtplib.SMTPException as e:
        #print("Error:无法发送邮件",e)
        logger.debug(e)
