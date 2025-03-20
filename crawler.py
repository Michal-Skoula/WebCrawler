import requests
from bs4 import BeautifulSoup

class Crawler():
    def __init__(self, root_url: str):
        self.index_url = root_url

        root_url_array = self.index_url.split(".")
        self.domain = ".".join(root_url_array[len(root_url_array) - 2 : len(root_url_array)])
    
    def getDomain(self):
        return self.domain

    def setDomain(self, domain: str):
        self.domain = domain

    @staticmethod
    def absoluteUrl(root_url: str, link: str):
       root_url_array = root_url.rstrip("/").split("/")
       link_array = link.lstrip("/").split("/")

       levels_up_count = link_array.count("..")

       new_root_url = "/".join(root_url_array[0 : len(root_url_array) - levels_up_count])
       new_link = "/".join(link_array[levels_up_count : len(link_array)])

       return new_root_url + "/" + new_link

    def isValidUrl(self, url: str):
        if url == "/":
            return False

        if not url:
            return False
        
        if self.index_url == url:
            return False

        for check in ("mailto:","tel:","#"): 
            if check in url: return False
        
        # for check in ()
        return True
        
        
        

    def findLinks(self, root_url: str, crawled_urls: list = []):
        response = requests.get(root_url)
        response.raise_for_status
        if "text/html" not in response.headers["Content-Type"]: return []

        soup = BeautifulSoup(response.text, "html.parser")
        crawled_links = soup.select("a[href]")

        urls = []
        for link in crawled_links:    
            href = str(link.attrs.get("href"))

            updated_link = ""
            if self.isValidUrl(href):
                if href.startswith(("http://", "https://")): # Is absolute url
                    updated_link = href
                    
                elif href.startswith("/"): # Relative URL starting from root of filesystem
                    updated_link = self.index_url + href

                else: # Is relative url
                    updated_link = self.absoluteUrl(root_url, href)

                is_domain_match = self.domain in updated_link
                is_not_crawled = updated_link not in crawled_urls
                is_not_duplicate = updated_link not in urls

                # print(f"Link {updated_link} notExternal: {is_domain_match}, crawled: {is_not_crawled}, notDuplicate: {is_not_duplicate}")


                if is_domain_match and is_not_crawled and is_not_duplicate:
                    urls.append(updated_link)

        return urls
                        
        
        
                    
        

    def crawl():
        
        pass


# print(Crawler("test.app.youtube.com").getDomain())
# print(Crawler.absoluteUrl("youtube.com/videos/v/34d4/","/kebab"))

# print(Crawler.isValidUrl("https://kebab.com/mailto:about"))
for i in Crawler("https://zs34.plzen.eu/").findLinks("https://zs34.plzen.eu/"):
    print(i)