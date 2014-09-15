import sys
import imaplib
import getpass
import email
import datetime
import time
import commands

#connect to the email address
M = imaplib.IMAP4_SSL('imap.gmail.com')
try:
	M.login('ikarambelas@gmail.com', getpass.getpass())
except imaplib.IMAP4.error:
	print 'LOGIN FAILED'
	exit()

while 1:
	time.sleep(60 * 5)
	rv, data = M.select("INBOX")
	if rv == 'OK':
		#collect only emails addressed to notify
		rv, searchdata = M.search(None, 'TO', '"ian.karambelas@gmail.com"')
		if searchdata == ['']:
			print "No messages found!"
			continue
		for num in reversed(searchdata[0].split()):
			rv, fetchdata = M.fetch(num, '(RFC822)')
			if rv != 'OK':
				print "ERROR getting message", num
				continue
			msg = email.message_from_string(fetchdata[0][1])
			for part in msg.walk():
				if part.get_content_type() == 'text/plain':
					#overwrite data.txt for a new report
					f = open('data.txt', 'w')
					f.write('#time\tvalue\n')
					f.close()
					#make mysql query and write to the data file
					if commands.gen_data(part.get_payload().split(), msg['Return-Path'][1:-1]):
						#generate a gnuplot program text file and execute it
						commands.gen_report(part.get_payload().split())
						#generate a mime-formated email with the report attached and send it
						commands.gen_email(msg['Return-Path'][1:-1])

			#get message uid for deletion
			rv, uiddata = M.fetch(num, '(UID)')
			if rv == 'OK':
				#delete the email by copying, gmail handles purging
				msg_uid = uiddata[0][uiddata[0].rfind(' ') + 1:-1]
				result = M.uid('COPY', msg_uid, '[Gmail]/Trash')
