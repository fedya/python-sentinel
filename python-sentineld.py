#!/usr/bin/env python

import sys, time
import daemon
import paramiko
from threading import Thread
import subprocess
from Queue import Queue
import sys, os, os.path, socket


class MyDaemon(daemon.Daemon):
    def __init__(self):
    	daemon.Daemon.pidfile = "/tmp/python-sentd.pid"


    def run(self):
	num_threads = 1
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
            			print "server %s: not respond" % ip
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

my_daemon = MyDaemon()

if len(sys.argv) >= 2:
    if 'start' == sys.argv[1]:
        my_daemon.start()
    #	my_daemon.start(interactive=True)
    elif 'stop' == sys.argv[1]:
        my_daemon.stop()
    elif 'restart' == sys.argv[1]:
        my_daemon.restart()
    elif 'status' == sys.argv[1]:
        my_daemon.status()
    else:
        print "Unknown command"
        sys.exit(2)
    sys.exit(0)
