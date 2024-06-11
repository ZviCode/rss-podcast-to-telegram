import datetime

import utils
from tables import Podcast, Uploader, get_session


def add_podcast(name: str, rss_link: str, chat_id: str) -> None:
    'Add a new podcast to the database'
    with get_session() as session:
        new_podcast = Podcast(name=name, rss_link=rss_link, chat_id=chat_id)
        session.add(new_podcast)
        session.commit()
        

def add_uploader(name: str, title: str, description: str, link_to_podcast: str, pub_date: datetime.datetime, link_mp3: str) -> bool:
    'Add a new uploader to the database'
    with get_session() as session:
        exists = session.query(Uploader).filter(Uploader.link_to_podcast == link_to_podcast).first()
        if exists:
            session.close()
            return False
        new_uploader = Uploader(name=name, title=title, description=description, link_to_podcast=link_to_podcast, pubDate=pub_date, link_mp3=link_mp3)
        session.add(new_uploader)
        session.commit()
        return True


def download_file(link: str, filename: str) -> str:
    'Download a file from a link and save it with a filename'
    return utils.download_file(link, filename)


def get_all_podcasts() -> list[dict]:
    'Get all podcasts from the database'
    with get_session() as session:
        podcasts = session.query(Podcast).all()
        result = [{'name': p.name, 'rss_link': p.rss_link, 'chat_id': p.chat_id} for p in podcasts]
        return result


def delete_podcast(name: str) -> None:
    'Delete a podcast from the database'
    with get_session() as session:
        session.query(Podcast).filter(Podcast.name == name).delete()
        session.commit()
    

def if_exists(link_to_podcast: str) -> bool:
    'Check if a podcast exists in the database'
    with get_session() as session:
        exists = session.query(Uploader).filter(Uploader.link_to_podcast == link_to_podcast).first()
        return exists is not None
