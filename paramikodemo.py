import paramiko

host = "174.137.54.228"
ssh_port = 27599
ssh_user = "root"
ssh_pwd = "your_root_password"


if __name__ == '__main__':
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy)
    ssh.connect(host, ssh_port, ssh_user, ssh_pwd)

    stdin, stdout, stderr = ssh.exec_command("ls /home/lttclaw")
    print(stdout.read().decode('utf-8'))
    ssh.close()


def pullFile():
    transport = paramiko.Transport((host, ssh_port))
    sftp = paramiko.SFTP.from_transport(transport)
    sftp.get('/home/lttclaw/index.html', 'index.html')
    sftp.close()
    transport.close()
