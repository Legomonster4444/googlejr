from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <form action="/fetch" method="get">
        <input type="text" name="url" placeholder="Enter URL" required>
        <button type="submit">Go</button>
    </form>
    '''

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not url.startswith('http'):
        url = 'http://' + url
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error: {e}"

    content = response.text

    # Modify links to open within the browser
    content = content.replace('href="http', 'href="/fetch?url=http')
    content = content.replace("href=\'http', "href=\'/fetch?url=http")
    content = content.replace('src="http', 'src="/fetch?url=http')

    return render_template_string(content)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
