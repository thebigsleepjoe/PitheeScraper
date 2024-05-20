# [Pithee](pithee.com) Scraper

This is a simple terminal-based web scraper for the pithee.com website. It scrapes the website for the latest winners and posts.

It can grab the latest archive of winners without needing an API key, but for actual random posts it needs you to provide your token.

## Usage

Git clone or download this repo and have Python installed. No libraries are needed.

To run: `python3 main.py <token> <nWinners> <nPosts>`

NOTE: If you want >50 winners, you will need to wait a loooong time, as the API only allows us to fetch the last 50 winners. More on why this is can be seen below. Posts are acquired first, and it typically takes a very short amount of time to fetch this data in comparison.

## How to get your token

On Chrome/Chromium/anything with Inspect element:

1. Go to pithee.com
2. Right click and select "Inspect" (or press CTRL+SHIFT+I)
3. Go to the "Network" tab and select "Fetch/XHR"
4. Refresh the page
5. Click on the "get_posts" request
6. Go to the "Headers" tab
7. Copy the "Authorization" header value (it should start with "Bearer"). DO NOT include the word "Bearer" in the token you provide in the script.

Note: Please do not share or stream your token. It probably won't do much, but it's better to be safe than sorry.

The token naturally expires after 3600 seconds, which is about an hour from when you open the page. This shouldn't be an issue for 99% of users, but if you are running this script for a long time, you may need to refresh the page and get a new token.

## Data

### Where is the data stored?

Check the ./data/ folder for the winners and posts. Posts and winners are stored in a .yaml file separate from one another. What you do with the data is up to you.

Data is never automatically cleared by the script, so you will need to manually delete the files if you want to start fresh.

### Does this store my token?

The script will not store your token, nor should it ever leave your memory. It is sent to the Pithee API server via a POST request.

## How long does it take?

### Winners

Pithee works by selecting a winner every 10 minutes. The archive API this script uses does not reveal any more than 50 of the most recent winner posts. The script will wait for 10 minutes before fetching the next **1** winner. This makes it take a veeeery long time if you are trying to get more than 50 winners.

24 hours = 144 winners

### Posts

For posts, we can get about ~10 per fetch, but the script intentionally waits about 3 seconds between fetching the next batch. While it probably can be faster, I don't want to risk getting anyone using this tool banned from the website (by flooding it), as this uses your personal API token.

1 minute = 200 posts

1 hour = 12000 posts

## Why make this?

I wanted to train an AI to classify "funny" and "not funny" posts. Pithee had the best database I cold think of for this, without requiring me to manually curate a database. Though Pithee isn't particularly known for its quality posts, it's a very good start.

## Accreditation

CC-BY-SA: Basically, just credit me somewhere if you use my code or project. Otherwise, go crazy.