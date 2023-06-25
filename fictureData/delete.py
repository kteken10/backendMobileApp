import requests

# Désactiver le support du proxy
requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()
table=[ "http://localhost:5000/visiteurs","http://localhost:5000/fournisseurs","http://localhost:5000/automobiles"]

for url in table:
    
    response = requests.delete(url, proxies={'http': None, 'https': None})



if response.status_code == 200:
    data = response.json()
    print(data['message'])
else:
    print("Une erreur s'est produite lors de la suppression ")
