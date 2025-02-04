import json
from crawler_scraper import WebCrawlerScraper
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def handler(event, context):
    # Allow all origins and methods
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': '*'
    }
    
    # Handle preflight requests
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    try:
        # Parse request body
        body = json.loads(event['body'] if event['body'] else '{}')
        url = body.get('url', '')
        
        # Basic URL validation
        if not url:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'URL is required'})
            }

        # Add http:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        # Initialize crawler with more permissive settings
        crawler = WebCrawlerScraper(url, max_pages=1)
        crawler.crawl_and_scrape()
        
        # Return results
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(crawler.get_data())
        }
        
    except Exception as e:
        return {
            'statusCode': 200,  # Return 200 even for errors
            'headers': headers,
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to scrape the URL, but request was processed'
            })
        }