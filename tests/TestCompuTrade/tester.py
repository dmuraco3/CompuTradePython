import requests
r = requests.get("https://test.pypi.org/pypi/CompuTrade/json").json()
version = str(r['info']['version'])

version = version.split('.')
print(version)