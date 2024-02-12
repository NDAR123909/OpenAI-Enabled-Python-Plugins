# UniScraper

UniScraper is an OpenAI scraping plugin that allows users to scrape data from websites. It is designed to be run solely on Python and utilizes a Flask app running on localhost port 7250.

## Getting Started

Before running UniScraper, make sure you have Python installed on your machine. Additionally, you will need to install the following libraries:

- requests
- Flask
- beautifulsoup4
- selenium
- openai

To run UniScraper, follow these steps:

1. Open the main.py file on your code editor
2. Run the script

## Usage

To use UniScraper, follow these instructions:

1. Open another command prompt and run the following command:
```
curl -X POST -H "Content-Type: application/json" -d "{\"url\": \"{url here}\", \"loop_time\": \"{MM/DD/YYYY}, {HH:MM} {AM/PM}\"}" http://127.0.0.1:7250/scrape
```
Replace `{url here}` with the URL of the website you want to scrape and `{MM/DD/YYYY}, {HH:MM} {AM/PM}` with the desired date and time for the scraping to occur.

For example:
```
curl -X POST -H "Content-Type: application/json" -d "{\"url\": \"https://edition.cnn.com/world/asia\", \"loop_time\": \"01/29/2024, 02:34 PM\"}" http://127.0.0.1:7250/scrape
```

2. Wait until the designated time and date for the scraping to occur.
3. Once the scraping is triggered successfully, the scraped information will appear in a JSON output in the code editor, and the command terminal will display the message "message: scraping triggered successfully".

Please note that UniScraper is particularly effective at scraping websites with heavy anti-scraping measures.

## License

UniScraper is an open-source project.

Good! If you would like to generate a new README.txt file, please provide the new file information.
