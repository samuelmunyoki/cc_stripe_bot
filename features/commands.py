from telegram import Update
from telegram.ext import  ContextTypes
from utils.group_check import group_check_middleware
from utils.rate_limit import rate_limit_middleware

async def hello_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if group_check_middleware(update):
        if await rate_limit_middleware(update, context):
            await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    else:
        if await rate_limit_middleware(update, context):
            await update.message.reply_text(f'Hey {update.effective_user.first_name}, I only work in group chats.')