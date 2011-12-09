#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("note2",username="fdkit",password="rosa", port=22)
stdin, stdout, stderr = ssh.exec_command("cat /var/log/syslog")
result = stdout.read().splitlines()
print result
#ssh.close()
