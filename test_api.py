import requests
import json

url = "http://127.0.0.1:5000/crawl"
data = {
    "url": "https://www.getmorebacklinks.org/",
    "max_pages": 5  # Increased to get more pages
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Crawl successful!")
    crawled_data = response.json()
    
    # Pretty print the first page's data as an example
    print("\nFirst page data structure:")
    print(json.dumps(crawled_data[0], indent=2))
    
    # Print summary of all crawled pages
    print("\nCrawled pages summary:")
    for page in crawled_data:
        print(f"\nURL: {page['metadata']['url']}")
        print(f"Title: {page['metadata']['title']}")
        print("Sections found:", list(page['sections'].keys()))
else:
    print(f"Error: {response.status_code}")
    print(response.text)