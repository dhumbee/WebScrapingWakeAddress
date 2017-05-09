import requests
import bs4

resp = requests.get('http://localhost:8000/golfer/8')
#print(resp.status_code)
golfer8 = bs4.BeautifulSoup(resp.text, "html.parser")
#print(golfer8)
td_list = golfer8.select('td')

full_list = []
index = 0
for el in td_list:
	td_text = el.getText()
	td_text = td_text.strip()
	if index % 2 == 0:
		inner_list = []
		inner_list.append(td_text)
	else:
		inner_list.append(td_text)
			
		full_list.append(inner_list)
	index += 1

full_list.insert(1, ["----------", "----------"])


for inner in full_list:
	row = inner[0].ljust(21) + "  " + inner[1].ljust(21)
	print(row)