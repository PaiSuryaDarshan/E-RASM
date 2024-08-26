import requests

CHEMICAL = "Propanol"

url = "https://www.sigmaaldrich.com/IN/en/sds/mm/6.18663?userType=anonymous"
headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1'}
file_Path = f"./storage_directory/{CHEMICAL}.pdf"

response = requests.get(url, stream =True, headers = headers)

if response.status_code == 200:
    pass
else:
    print(f"RESPONSE ERROR - BLACKLISTED - [{CHEMICAL}]")
    print(response)
    print(response.status_code)

content = response.content

with open(file_Path, "wb") as file:
    file.write(content)
    file.close()