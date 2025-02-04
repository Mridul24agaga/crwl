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
        self.base_domain = urlparse(start_url).netloc

    def is_valid(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme) and parsed.netloc == self.base_domain

    def extract_section_content(self, soup):
        sections = {}
        
        # Extract header content
        header = soup.find('header') or soup.find(class_=['header', 'nav', 'navbar'])
        if header:
            sections['header'] = {
                'navigation': [{'text': link.get_text(strip=True), 'href': link.get('href')} 
                             for link in header.find_all('a')],
                'text': header.get_text(strip=True)
            }

        # Extract hero/main section
        hero = soup.find(class_=['hero', 'main-content', 'hero-section']) or soup.find('main')
        if hero:
            sections['hero'] = {
                'title': hero.find(['h1', 'h2']).get_text(strip=True) if hero.find(['h1', 'h2']) else '',
                'description': hero.find('p').get_text(strip=True) if hero.find('p') else '',
                'buttons': [{'text': btn.get_text(strip=True), 'href': btn.get('href')} 
                          for btn in hero.find_all('a', class_=['button', 'btn'])]
            }

        # Extract all sections with headings
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            section = heading.find_parent('section') or heading.find_parent('div')
            if section:
                section_id = heading.get_text(strip=True)
                sections[f'section_{section_id}'] = {
                    'heading': section_id,
                    'content': section.get_text(strip=True),
                    'links': [{'text': link.get_text(strip=True), 'href': link.get('href')} 
                             for link in section.find_all('a')]
                }

        # Extract forms
        forms = soup.find_all('form')
        if forms:
            sections['forms'] = [{
                'action': form.get('action'),
                'method': form.get('method'),
                'inputs': [{'type': input.get('type'), 'name': input.get('name')} 
                          for input in form.find_all('input')]
            } for form in forms]

        # Extract footer content
        footer = soup.find('footer')
        if footer:
            sections['footer'] = {
                'text': footer.get_text(strip=True),
                'links': [{'text': link.get_text(strip=True), 'href': link.get('href')} 
                         for link in footer.find_all('a')]
            }

        return sections

    def crawl_and_scrape(self):
        queue = [self.start_url]
        
        while queue and len(self.visited_urls) < self.max_pages:
            url = queue.pop(0)
            
            if url not in self.visited_urls:
                try:
                    print(f"Crawling: {url}")
                    response = requests.get(url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    
                    if response.status_code == 200:
                        self.visited_urls.add(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Extract metadata
                        metadata = {
                            'url': url,
                            'title': soup.title.string if soup.title else "No title",
                            'meta_description': soup.find('meta', {'name': 'description'})['content'] 
                                if soup.find('meta', {'name': 'description'}) else "",
                        }
                        
                        # Extract all sections
                        sections = self.extract_section_content(soup)
                        
                        # Combine metadata and sections
                        page_data = {
                            'metadata': metadata,
                            'sections': sections
                        }
                        
                        self.data.append(page_data)
                        
                        # Find all internal links
                        for link in soup.find_all('a', href=True):
                            new_url = urljoin(url, link['href'])
                            if self.is_valid(new_url) and new_url not in self.visited_urls:
                                queue.append(new_url)
                        
                        time.sleep(2)  # Respectful delay between requests
                        
                except Exception as e:
                    print(f"Error crawling {url}: {str(e)}")
            
    def get_data(self):
        return self.data

    def save_to_json(self, filename='crawled_data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)