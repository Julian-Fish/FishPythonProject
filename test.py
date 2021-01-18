import urllib.request
import urllib.parse
data = {}
data['name'] = 'Somebody Here'
data['location'] = 'Northampton'
data['language'] = 'Python'
url_values = urllib.parse.urlencode(data)
print(url_values)  # The order may differ from below.  

url = 'https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/maya%20script/py/Construct.py'
full_url = url + '?' + url_values
data = urllib.request.urlopen(full_url)
text = data.read()

print(text)