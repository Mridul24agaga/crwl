import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json

class WebCrawlerScraper:
    def __init__(self, start_url, max_pages=10):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.data = []
        # Removed base_domain restriction

    def is_valid(self, url):
        parsed = urlparse(url)
        # Removed domain restriction, now accepts any valid URL
        return bool(parsed.netloc) and bool(parsed.scheme)

    def extract_section_content(self, soup):
        try:
            # Get all text content
            all_text = soup.get_text(separator=' ', strip=True)
            
            # Get all links
            links = [{'text': a.get_text(strip=True), 'href': a.get('href')} 
                    for a in soup.find_all('a', href=True)]
            
            # Get all images
            images = [{'src': img.get('src'), 'alt': img.get('alt')} 
                     for img in soup.find_all('img')]
            
            # Get all headings
            headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
            
            # Get meta tags
            meta_tags = {
                meta.get('name', meta.get('property', '')): meta.get('content')
                for meta in soup.find_all('meta')
                if meta.get('content')
            }

            return {
                'text_content': all_text,
                'links': links,
                'images': images,
                'headings': headings,
                'meta_tags': meta_tags
            }
        except Exception as e:
            print(f"Error extracting content: {str(e)}")
            return {}

    def crawl_and_scrape(self):
        try:
            response = requests.get(
                self.start_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0'
                },
                timeout=30,
                verify=False  # Ignore SSL certificate verification
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data
            page_data = {
                'url': self.start_url,
                'title': soup.title.string if soup.title else '',
                'content': self.extract_section_content(soup)
            }
            
            self.data.append(page_data)
            
        except Exception as e:
            print(f"Error crawling {self.start_url}: {str(e)}")
            self.data.append({
                'url': self.start_url,
                'error': str(e)
            })
    
    def get_data(self):
        return self.data