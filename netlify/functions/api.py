from flask import Flask, jsonify, request
from crawler_scraper import WebCrawlerScraper
from flask.cli import load_dotenv
import json

app = Flask(__name__)
load_dotenv()

def handler(event, context):
    with app.test_request_context(
        path=event['path'],
        method=event['httpMethod'],
        headers=event['headers'],
        data=event['body']
    ):
        try:
            response = app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': str(e)
            }

@app.route('/api/crawl', methods=['POST'])
def crawl():
    data = json.loads(request.data)
    start_url = data.get('url')
    max_pages = data.get('max_pages', 10)

    if not start_url:
        return jsonify({"error": "No URL provided"}), 400

    crawler = WebCrawlerScraper(start_url, max_pages)
    crawler.crawl_and_scrape()
    return jsonify(crawler.get_data())

# This is required for local testing
if __name__ == '__main__':
    app.run(debug=True)