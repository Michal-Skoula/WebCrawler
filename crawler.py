import requests
from bs4 import BeautifulSoup

class Crawler():
    def __init__(self, root_url: str):
        # Root url
        if not root_url.startswith(("http://","https://")): 
            raise Exception("The root url is invalid. Please use an absolute path, e.g. https://google.com.")
        
        self.root_url = root_url

        # Domain
        start = root_url.find("//")
        end = root_url.find("/", start + 2)

        if start == -1:
            raise Exception("There was an issue parsing the domain from the provided root_url. Please use an absolute path")
        if end == -1:
            end = len(root_url)
            
        self.domain = root_url[0:end]
    
    @staticmethod
    def toAbsoluteUrl(root_url: str, link: str):
        root_url_array = root_url.rstrip("/").split("/")
        link_array = link.lstrip("/").split("/")

        levels_up_count = link_array.count("..")

        new_root_url = "/".join(root_url_array[0 : len(root_url_array) - levels_up_count])
        new_link = "/".join(link_array[levels_up_count : len(link_array)])

        return new_root_url + "/" + new_link

    def isValidUrl(self, url: str):
        if url == "/" or not url:
            return False
        
        if self.root_url.rstrip("/") == url.rstrip("/"):
            return False

        for invalid in ("mailto:","tel:","#"): 
            if invalid in url: return False
        
        return True
        

    def findLinks(self, page_url: str, crawled_urls: list = []) -> list[]:
        response = requests.get(page_url)
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
                    
                elif href.startswith("/"): # Is Relative URL starting from root of filesystem
                    updated_link = self.root_url + href

                else: # Is relative url
                    updated_link = self.toAbsoluteUrl(page_url, href)

                is_domain_match = updated_link.startswith(self.domain)
                is_not_crawled = updated_link not in crawled_urls
                is_not_duplicate = updated_link not in urls

                if is_domain_match and is_not_crawled and is_not_duplicate:
                    urls.append(updated_link)

        return urls
    
    def crawl(self, queue: list[str] = [], crawled_urls: list[str] = []) -> list[str]:
        sitemap = []
        
        queue = self.findLinks(self.root_url)
        
        for url in queue:
            if url not in crawled_urls:
                print(f"Crawling: {url}")
                crawl_results = self.findLinks(url, crawled_urls)
                sitemap += crawl_results

                crawled_urls.append(url)
                queue += crawl_results
                queue.remove(url)

        return sitemap
    
root = "https://zs34.plzen.eu"
print(Crawler(root).domain)

# print(Crawler(root).crawl())

for i in Crawler(root).crawl():
    print(i)



# Crawler(root).findLinks(root)
