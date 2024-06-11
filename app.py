import feedparser
import os
import time
from datetime import datetime

import config
import repo
import utils


def main():
    all_podcasts = repo.get_all_podcasts()
    exception = False

    for podcast in all_podcasts:
        if exception:
            break

        rss_link = podcast['rss_link']
        feed = feedparser.parse(rss_link)

        for entry in reversed(feed['entries']):
            title = entry['title'].replace('/', ' ')[:50]
            description = utils.replace_text(entry.get('description', ''))
            pub_date = entry.get('published')
            links = entry.get('links', [])

            if pub_date:
                pub_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
            
            if not links:
                continue

            link_mp3, link_to_podcast = utils.extract_links(links)

            if not repo.if_exists(link_to_podcast):
                if any(link_mp3.endswith(ext) for ext in config.ENDEF_FILES):
                    file_name = repo.download_file(link_mp3, f"{config.START_PATH}/{title}.mp3")
                    repo.add_uploader(podcast['name'], title, description, link_to_podcast, pub_date, link_mp3)
                    stt = utils.send_to_telegram(podcast['chat_id'], title, file_name)
                    if stt.get('error_code') == 429:
                        time_to_sleep = int(stt.get('parameters', {}).get('retry_after', 5))
                        time.sleep(time_to_sleep)
                        utils.send_to_telegram(podcast['chat_id'], title, file_name)
                    os.remove(file_name)
                else:
                    exception = True
                    break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        utils.log_error(e)
