from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO, emit
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from zipfile import ZipFile
from urllib.parse import urlparse, urljoin

app = Flask(__name__)
socketio = SocketIO(app)

currently_crawling_pages = set()

def crawl_web(url, depth=2):
    visited_pages = set()
    base_url = urlparse(url).scheme + '://' + urlparse(url).hostname
    website_name = urlparse(url).hostname.split('.')[0]  # Extract website name from the URL
    zip_buffer = BytesIO()

    with ZipFile(zip_buffer, 'a') as zip_file:
        def recursive_crawl(current_url, current_depth):
            if current_url in visited_pages or current_url in currently_crawling_pages or current_depth > depth:
                return

            currently_crawling_pages.add(current_url)

            try:
                with requests.get(current_url, stream=True) as response:
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    for link in soup.find_all('a'):
                        next_url = link.get('href')
                        if next_url:
                            absolute_url = urljoin(base_url, next_url)
                            if absolute_url.startswith(base_url):
                                recursive_crawl(absolute_url, current_depth + 1)

                    content = response.content
                    file_name = current_url.rsplit('/', 1)[-1].replace('/', '_') + ".html"
                    zip_file.writestr(file_name, content)

            except requests.exceptions.RequestException:
                pass

            finally:
                currently_crawling_pages.remove(current_url)
                visited_pages.add(current_url)
                socketio.emit('update_pages', list(currently_crawling_pages))

        recursive_crawl(url, 1)

    return zip_buffer.getvalue(), website_name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    url_to_crawl = request.form['url']
    depth = int(request.form['depth'])
    zip_data, website_name = crawl_web(url_to_crawl, depth)

    return send_file(BytesIO(zip_data), download_name=f'{website_name}_crawled_data.zip', as_attachment=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
