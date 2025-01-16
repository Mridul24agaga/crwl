from flask import Flask, jsonify, request
from crawler_scraper import WebCrawlerScraper

app = Flask(__name__)

@app.route('/crawl', methods=['POST'])
def crawl():
    data = request.json
    start_url = data.get('url')
    max_pages = data.get('max_pages', 10)

    if not start_url:
        return jsonify({"error": "No URL provided"}), 400

    crawler = WebCrawlerScraper(start_url, max_pages)
    crawler.crawl_and_scrape()
    return jsonify(crawler.get_data())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)