import requests

class Parser():
    def __init__(self, root_url:str):
        self.url = root_url

        self.html = requests.get(self.url).text

    def title(self):
        start = self.html.find('<title>')
        end = self.html.find('</title>')

        if start == -1 or end == -1:
            return None
        else:
            return self.html[start+7:end]
        
    


s = Crawler('https://www.skoula.com')

print(s.title())
