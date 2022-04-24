# encoding utf-8
import smtplib
import requests
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from_addr = 'lttclaw@qq.com'
password = 'hwpzapzrkmgpgaba'
to_addr = ['543426680@qq.com', 'lttclaw@qq.com']
smtp_server = 'smtp.qq.com'


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def build_msg(content, origin_name, subject):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('%s <%s>' % (origin_name, from_addr))
    msg['To'] = ", ".join(to_addr)
    # msg['Cc'] = _format_addr('%s <%s>' % ('抄送', cc_addr))
    msg['Subject'] = Header(subject, 'utf-8').encode()
    return msg


def send_msg(msg):
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


# 这是主程序入口

if __name__ == '__main__':
    sender = "lttclaw@qq.com"
    subject = "土味情话来自程序"
    response = requests.get("https://api.lovelive.tools/api/SweetNothings")
    with open("smail.py", encoding='utf-8') as f:
        source = f.read()
    texts = "这是一句来自网络随机生成的情话：" + response.text + "\n下面是给你发邮件的源代码,最后十行你是不是也能大概读懂，怎么样，要不要学？\n" + source
    mail_msg = build_msg(texts, sender, subject)
    send_msg(mail_msg)
