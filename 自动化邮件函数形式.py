from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import email as eml
import smtplib as smp

def  _format_addr(s):
    name, addr = eml.utils.parseaddr(s)
    return eml.utils.formataddr((eml.header.Header(name, 'utf-8').encode(), addr))


# s_mail='吴智强<wuzhiqiang@mylike.com>'
# r_mail = ['吴智强<wuzhiqiang@mylike.com>', '陈曦<127807675@qq.com>']
# text_ = """\t本周资产报告如下：\n\t新增资产量稳步上升中，主要是东南区域进件量较多，件均在1W8左右，众数区间在(25000,30000]，目前整体业务稳步上升中。"""
# title = """颐尔信贷后资产监控周报"""
# _path = r'E:\python\美莱集团全国商户通过率.html'
# _attachment_type1 = 'html'
# _attachment_type2 = 'html'
# _attachment_name = '美莱集团全国商户通过率.html'


def sendemail(s_mail, r_mail, title, text_, _path, _attachment_type1, _attachment_type2, _attachment_name):
    msg = MIMEMultipart()
    msg['From'] = _format_addr(s_mail)
    msg['To'] = ','.join(r_mail)
    msg['Subject'] = eml.header.Header(title, 'utf-8').encode()
    msg.attach(MIMEText(text_, 'plain', 'utf-8'))

    with open(_path, 'rb') as f:
        mime = MIMEBase(_attachment_type1, _attachment_type2, filename=_attachment_name)
        mime.add_header('Content-Disposition', 'attachment', filename=_attachment_name)
        mime.add_header("Content-ID", "<0>")
        mime.add_header("X-Attachment-Id", "0")
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)

    recevermail = [eml.utils.parseaddr(i)[1] for i in r_mail]

    server = smp.SMTP_SSL('smtp.qiye.163.com', '994')
    server.set_debuglevel(1)
    server.login('wuzhiqiang@mylike.com', 'python@139547')
    server.sendmail('wuzhiqiang@mylike.com', recevermail, msg.as_string())
    server.quit()

s_mail='吴智强<wuzhiqiang@mylike.com>'
r_mail = [_format_addr('吴智强<wuzhiqiang@mylike.com>'), _format_addr('汪昊<wang.hao@yexfintech.com>')]
text_ = """\t本周资产报告如下：\n\t新增资产量稳步上升中，主要是东南区域进件量较多，件均在1W8左右，众数区间在(25000,30000]，目前整体业务稳步上升中。"""
title = """颐尔信贷后资产监控周报"""
_path = r'E:\python\美莱集团全国商户通过率.html'
_attachment_type1 = 'html'
_attachment_type2 = 'html'
_attachment_name = '美莱集团全国商户通过率.html'

sendemail(s_mail, r_mail, title, text_, _path, _attachment_type1, _attachment_type2, _attachment_name)


