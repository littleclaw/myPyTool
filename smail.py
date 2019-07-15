import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from_addr = 'someuser@qq.com'
password = 'smtp_password'
to_addr = ['123456789@qq.com', 'abcdef@qq.com']
cc_addr = 'cc@qq.com'
smtp_server = 'smtp.qq.com'


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def build_msg(content, origin_name, to_name, subject):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('%s <%s>' % (origin_name, from_addr))
    msg['To'] = ", ".join(to_addr)
    msg['Cc'] = _format_addr('%s <%s>' % ('有关部门', cc_addr))
    msg['Subject'] = Header(subject, 'utf-8').encode()
    return msg


def send_msg(msg):
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


if __name__ == '__main__':
    fr = "lttclaw"
    to = "开发人员"
    sub = "执行日志"
    text = "Hello, there"
    mail_msg = build_msg(text, fr, to, sub)
    send_msg(mail_msg)




