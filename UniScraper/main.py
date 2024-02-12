# Import the libraries we need
import requests
from flask import Flask, request, send_from_directory, jsonify
from bs4 import BeautifulSoup
import time
import selenium
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from openai import OpenAI


# Initialize the Flask app
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route('/')
def home():
    return 'What are you doing here?'

# Add these lines
@app.after_request
def add_header(response):
    response.headers['Connection'] = 'keep-alive'
    return response

# App triggers the /scrape function
@app.route('/scrape', methods=['GET', 'POST'])
def trigger_scraping():
    if request.method == 'GET':
        return "This route is for POST requests only."
    data = request.get_json()

    user_url = data.get('url')
    loop_time = data.get('loop_time')

    # Convert user input to seconds
    loop_time = convert_to_seconds(loop_time)

    # Call the scraping function
    scrape_website(user_url, loop_time)

    return jsonify({"message": "Scraping process triggered successfully."})

# ChatGPT will use this route to find our manifest file, ai-plugin.json; it will look in the ".well-known" folder
@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.',
                               'ai-plugin.json',
                               mimetype='application/json')

# ChatGPT will use this route to find our API specification, openapi.yaml
@app.route('/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')

# OPTIONAL: If you want a logo to display on your plugin in the Plugin Store, then upload a file named logo.png to the root of your project, and uncomment the code below.
@app.route('/logo.png')
def plugin_logo():
    return send_from_directory('.', 'logo.png')

def convert_to_seconds(date_time):
    specified_time = datetime.strptime(date_time, "%m/%d/%Y, %I:%M %p")
    current_time = datetime.now()
    time_difference = specified_time - current_time
    return max(time_difference.total_seconds(), 0)

# Modify the scrape_website function
def scrape_website(url, loop_time):
    chrome_options = Options()
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    start_time = datetime.now()

    while True:
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()

        if elapsed_time >= loop_time:
            break  # Break out of the loop after loop_time seconds

    # Check if the request object is present (indicating a request)
    if request:
        # Use Selenium to fetch the webpage content
        driver.get(url)
        time.sleep(5)  # Adjust this delay as needed

        # Use BeautifulSoup to parse the HTML and extract data
        soup = BeautifulSoup(driver.page_source, "html.parser")

        profile_data = {}
        profile_data["text"] = soup.get_text(separator="\n")
        print("RESPONSE FROM SCRAPER")
        print(profile_data)

    driver.quit()  # Close the browser after scraping

    # Extract information from scraped data and generate a prompt
    prompt = f"""Based on the latest information from {profile_data}, summarize the information accordingly. Before proceeding with your summary, you should be able to identify the kind of content from which the information came from, as well as the platform it came from.
REGARDING THE RECEIVED DATA:
The raw information that you will receive will contain clusters of text containing the separator (a backslash symbol followed by a lowercase 'n'). This is used to visualize a line break. 
Additionally, the textual information will oftentimes contain irrelevant or unnecessary pieces of information. Be cautious of the following as well as other redundant information potentially not included in this list:
- Repetitive navigation elements
- Redundant headings and links
- Advertisement sections 
- Repetitive content feed sections
- Repetitive video information
- Unnecessary white spaces
You must be able to discern which information is relevant or not. You must also be sure to organize your summary into bullet points. 
REGARDING THE OUTPUT FORMATTING:
When formatting your summary, it must be formatted in such a way that the user can easily distinguish what kind of sub information was listed, the date in which it was posted, and the content summary of the sub information. Be sure to list the information from most recent to least recent from top to bottom according to the date. Incorporate the following template into your summary:
- **sub_information_heading** (date): content_summary
...
Incorporate the following markdown elements into your summary:
- Bullet Points (-) or Numbered Lists: For listing each piece of information in a concise manner.
- Bold (**): For highlighting the headings of certain sub information"""

    # Send the prompt to ChatGPT
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a helpful scraping agent that specializes in organizing and summarizing information."},
            {"role": "user", "content": prompt},
        ]
    )
    print(response.choices[0].message.content)

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7250, debug=True, threaded=True, use_reloader=False)
