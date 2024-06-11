import requests
from tqdm import tqdm
import re
import logging

import config



def download_file(link: str, filename: str) -> str:
    'Download a file from a link and save it with a filename'
    response = requests.get(link, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    with open(filename, 'wb') as file, tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:
        for data in response.iter_content(block_size):
            file.write(data)
            progress_bar.update(len(data))

    return filename


def send_to_telegram(chat_id: str, title: str, file_name: str) -> dict:
    'Send a message to a Telegram chat with a title and a file name'
    bot_token = config.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendAudio" if file_name else f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'title': title, 'caption': title, 'parse_mode': 'HTML', 'disable_notification': True}
    files = {'audio': open(file_name, 'rb')} if file_name else {}
    response = requests.post(url, data=data, files=files).json()
    if not response['ok']:
        logging.error(f"Failed to send message: {response}")
    return response


def log_error(error: Exception) -> None:
    'Log an error message to the console and a file'
    logging.error(f"Error: {error}")    
    

def extract_links(links: list[dict]) -> tuple[str, str]:
    'Extract the links to the mp3 file and the podcast from a list of links'
    link_mp3 = ""
    link_to_podcast = ""
    for link in links:
        href = link.get('href', '').split('?')[0]
        if any(href.endswith(ext) for ext in config.ENDEF_FILES):
            link_mp3 = href
        else:
            link_to_podcast = href
    return link_mp3, link_to_podcast


def replace_text(text):
    'Replace text with HTML tags for bold, italic, and links'
    text = re.sub(r"(https?://[^\s]+)", r"<a href='\1'>\1</a>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    text = f"<p>{text}</p>"
    return text