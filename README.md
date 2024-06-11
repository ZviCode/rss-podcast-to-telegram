# בוט פודקאסטים ל-Telegram באמצעות RSS

פרויקט זה מאפשר שליחה אוטומטית של עדכונים על פרקי פודקאסטים מערוצי RSS לערוץ Telegram. הוא כולל אפשרויות לניהול פודקאסטים בבסיס נתונים, הורדת קבצי פרקים ושליחת התראות ל-Telegram.

## תוכן העניינים

1. [סקירה כללית](#סקירה-כללית)
2. [תכונות](#תכונות)
3. [דרישות](#דרישות)
4. [התקנה](#התקנה)
5. [הגדרה](#הגדרה)
6. [שימוש](#שימוש)
7. [הוספת ערוצי RSS](#הוספת-ערוצי-rss)
8. [הרצה עם Docker](#הרצה-עם-docker)
9. [מבנה הפרויקט](#מבנה-הפרויקט)

## סקירה כללית

בוט הפודקאסטים ל-Telegram מאפשר קבלת פרקים מערוצי RSS שונים ושליחת עדכונים, כולל קישורים ותיאורים, לערוץ Telegram ייעודי. זהו כלי שימושי להפצת פודקאסטים לקהילה באופן אוטומטי.

## תכונות

- קבלת פרקי פודקאסטים מערוצי RSS.
- סינון ועיבוד נתוני פודקאסטים.
- הורדת קבצי פודקאסטים.
- שליחת עדכונים מעוצבים לערוץ Telegram.
- ניהול ערוצי פודקאסטים בבסיס נתונים.
- תמיכה בהרצה בסביבת Docker.

## דרישות

- Python 3.7+ (אם לא משתמשים ב-Docker)
- Token של בוט Telegram
- Docker (לסביבת הרצה במכולה)

## התקנה

### ללא Docker

1. יש לשכפל את המאגר:

    ```bash
    git clone https://github.com/ZviCode/rss-podcast-to-telegram.git
    cd rss-podcast-to-telegram
    ```

2. יצירת סביבה וירטואלית והפעלתה:

    ```bash
    python -m venv venv
    source venv/bin/activate  # ב-Windows יש להשתמש ב `venv\Scripts\activate`
    ```

3. התקנת התלויות הנדרשות:

    ```bash
    pip install -r requirements.txt
    ```

4. הגדרת בסיס הנתונים PostgreSQL והטבלאות כפי שמתואר בקובץ `tables.py`.

5. יצירת קובץ `.env` בספריית השורש עם ההגדרות שלך (ראה [הגדרה](#הגדרה)).

### עם Docker

1. ודא כי Docker מותקן ורץ על המחשב שלך.

2. בניית התמונה של Docker:

    ```bash
    docker build -t rss-podcast-bot .
    ```

3. יצירת קובץ `.env` בספריית השורש עם ההגדרות שלך (ראה [הגדרה](#הגדרה)).

## הגדרה

יש ליצור קובץ `.env` בספריית השורש ולהוסיף את המשתנים הבאים:

```
START_PATH=/app/downloads
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=-1001995413878
DATABASE_URL=your-database-url
```

- `START_PATH`: נתיב הספריה לאחסון קבצי הפודקאסטים שהורדו.
- `TELEGRAM_BOT_TOKEN`: Token של בוט Telegram לשליחת הודעות.
- `TELEGRAM_CHAT_ID`: מזהה הערוץ ב-Telegram אליו יש לשלוח את העדכונים.
- `DATABASE_URL`: מחרוזת ההתחברות לבסיס הנתונים שלך PostgreSQL.

## שימוש

### ללא Docker

1. הפעלת הסביבה הווירטואלית:

    ```bash
    source venv/bin/activate  # ב-Windows יש להשתמש ב `venv\Scripts\activate`
    ```

2. הרצת הסקריפט `app.py` להתחלת קבלת הפרקים ועיבודם:

    ```bash
    python app.py
    ```

### עם Docker

1. הרצת המכולה של Docker:

    ```bash
    docker run -d --name rss-podcast-bot --env-file .env rss-podcast-bot
    ```

    פקודה זו תתחיל את המכולה במצב נפרד ותהריץ את הסקריפט כל שעה כפי שצוין בקובץ `crontab`.

## הוספת ערוצי RSS

להוספת ערוץ RSS חדש לבסיס הנתונים, יש לפעול על פי ההנחיות הבאות:

1. ודא כי בסיס הנתונים מוגדר וזמין עם ה- `DATABASE_URL` שצוין בקובץ `.env`.

2. השתמש בפונקציה `add_podcast` מתוך הקובץ `repo.py` להוספת ערוץ RSS חדש.

    ```python
    import repo

    podcast_name = 'שם הפודקאסט שלך'
    rss_link = 'https://your-podcast.com/rss'
    chat_id = '-1001234567890'  # החלף במזהה הערוץ שלך ב-Telegram

    repo.add_podcast(podcast_name, rss_link, chat_id)
    ```

3. ניתן להריץ את הסקריפט הנ"ל או להוסיף אותו לסקריפט הראשי להוספת ערוצי RSS באופן דינמי.

## הרצה עם Docker

להרצת הפרויקט באמצעות Docker, פעל לפי ההוראות הבאות:

1. ודא כי הקבצים הבאים נמצאים בספריית השורש בנוסף לקבצים הרגילים:

    - `Dockerfile`: מגדיר את תמונת Docker.
    - `crontab`: מגדיר את עבודת ה-cron להרצת הסקריפט כל שעה.
    - `requirements.txt`: מפרט את התלויות הנדרשות לפרויקט.

2. בניית תמונת Docker:

    ```bash
    docker build -t rss-podcast-bot .
    ```

3. הרצת מכולת Docker:

    ```bash
    docker run -d --name rss-podcast-bot --env-file .env rss-podcast-bot
    ```

4. בדיקת יומנים כדי לוודא שהסקריפט פועל כראוי:

    ```bash
    docker logs rss-podcast-bot
    ```

## מבנה הפרויקט

- `app.py`: הסקריפט הראשי לקבלה, עיבוד ושליחת עדכונים על הפודקאסטים.
- `repo.py`: פעולות בסיס הנתונים והורדת הקבצים.
- `utils.py`: פונקציות עזר להודעות ופעולות על קבצים.
- `config.py`: ניהול הגדרות באמצעות משתני סביבה.
- `.env`: קובץ ההגדרות של הסביבה.
- `requirements.txt`: רשימת התלויות של הפרויקט.
- `Dockerfile`: קובץ Docker ליצירת תמונה של Docker.
- `crontab`: קובץ crontab להגדרת עבודת cron.
- `README.md`: קובץ זה.
- `.gitignore`: קבצים שלא ישמרו במאגר.


## קרדיטים
- chatgpt (readme file)
- my_telegram_group(idea)


#
#