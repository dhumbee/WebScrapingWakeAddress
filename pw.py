#! python3
#pw.py - An insecure password locker program

import sys, pyperclip

PASSWORD = {'email': 'life123',
			'blog': 'hoseup',
			'luggage': '12345'}

if len(sys.argv) < 2:
	print('Usage: python pw.py [account] - copy account password')
	sys.exit()

account = sys.argv[1] 

if account in PASSWORD:
	pyperclip.copy(PASSWORD[account])
	print('Password for' + account + ' copied to clipboard.')
else:
	print("There is no account name " + account)