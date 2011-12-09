#!/usr/bin/python
# -*- coding: utf-8 -*-


import paramiko
from threading import Thread
import subprocess
from Queue import Queue
import sys, os, os.path, socket

num_threads = 4
queue = Queue()
#ips = ["olololdddd", "google.com", "mail.ru", "yandex.ru"]
ips = ["mail.ru"]
def pinger(i, q):
# ping server
    while True:
        ip = q.get()
        print "Thread %s: Pinging %s" % (i, ip)
        ret = subprocess.call("ping -c 5 %s" % ip,
                        shell=True,
                        stdout=open('/dev/null', 'w'),
                        stderr=subprocess.STDOUT)
        if ret == 0:
            print "%s: working fine." % ip
	else:
	    print "%s: не отвечает" % ip
	    print "How about slap your shit, %s" % ip
	    ssh=paramiko.SSHClient()
	    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	    ssh.connect("note2",username="root",password="rosa", port=22)
	    stdin, stdout, stderr = ssh.exec_command("cat /var/log/pm-powersave.log")
	    result = stdout.read().splitlines()
	    print result
	    ssh.close()
	q.task_done()

#Spawn thread pool
for i in range(num_threads):

	worker = Thread(target=pinger, args=(i, queue))
	worker.setDaemon(True)
	worker.start()

#Place work in queue
for ip in ips:
	queue.put(ip)

#Wait until worker threads are done to exit    
queue.join()
