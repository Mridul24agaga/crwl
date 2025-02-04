import json
from crawler_scraper import WebCrawlerScraper

def handler(event, context):
    print("Received event:", json.dumps(event))
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }
    
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    # Check if the path is /api/crawl
    if event['path'] != '/api/crawl':
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'error': 'Not Found'})
        }

    try:
        body = json.loads(event['body'] if event['body'] else '{}')
        print("Parsed body:", json.dumps(body))
        
        start_url = body.get('url')
        max_pages = body.get('max_pages', 10)

        if not start_url:
            print("No URL provided")
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'No URL provided'})
            }

        print(f"Starting crawler with URL: {start_url}, max_pages: {max_pages}")
        crawler = WebCrawlerScraper(start_url, max_pages)
        crawler.crawl_and_scrape()
        
        result = crawler.get_data()
        print("Crawler result:", json.dumps(result))
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        }
    except Exception as e:
        print("Error occurred:", str(e))
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }