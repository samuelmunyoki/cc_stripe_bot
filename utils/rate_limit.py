import time
from config.constants.rate import RATE_SECONDS
from config.responses.responses import  wait_msg
from utils.db_connection import conn, cursor
from telegram import Update
from telegram.ext import  ContextTypes


cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_timestamps (
        user_id INTEGER PRIMARY KEY,
        timestamp REAL
    )
''')

conn.commit()
async def rate_limit_middleware(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute('SELECT timestamp FROM user_timestamps WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        last_timestamp = result[0]
        current_time = time.time()
        elapsed_time = current_time - last_timestamp
        remaining_time = max(0, RATE_SECONDS - elapsed_time)
        if elapsed_time < RATE_SECONDS:
            await update.message.reply_text(f'{wait_msg(remaining_time)}')
            return False 
        
    cursor.execute('INSERT OR REPLACE INTO user_timestamps (user_id, timestamp) VALUES (?, ?)', (user_id, time.time()))
    conn.commit()

    return True
