import webbrowser, os, sys
import pyperclip

command = 'start python manage.py runserver'
os.system(command)

arg = ''


if len(sys.argv) >= 2:
    arg = sys.argv[1]
else:
    arg = pyperclip.paste()


url = 'http://localhost:8000/'
url = url + arg

webbrowser.open(url)
