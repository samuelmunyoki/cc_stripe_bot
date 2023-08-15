from features.stripe import send_card
import string
import requests
import json

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

async def card_check_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if group_check_middleware(update):
        
        if await rate_limit_middleware(update, context):
            try:
                args = update.message.text.split()[1:]  # Remove the command itself ("/check")
                if len(args) != 1:
                    await update.message.reply_text("Invalid arguments.\n\nUsage: /check cc_number|cvv|month|year")
                    return
                await update.message.reply_text(f'♻ Please wait checking...\n\nIt might take a few seconds.')
                await send_card(update, args)
            except:
                await update.message.reply_text(f'Please try again.')
            
    else:
        if await rate_limit_middleware(update, context):
            await update.message.reply_text(f'Hey {update.effective_user.first_name}, I only work in group chats.')

async def bin_lookup_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if group_check_middleware(update):
        if await rate_limit_middleware(update, context):
            args = update.message.text.split()[1:]
            
            if len(args) != 1:
                await update.message.reply_text("Invalid arguments.\n\nUsage: /bin BIN_Number")
                return

            url = f"https://lookup.binlist.net/{args[0]}"

            try:
                res = requests.request("GET", url)
                response_text = res.text
                status_code = res.status_code

                if status_code == 200:
                    try:
                        response = json.loads(response_text) 
                        card_details = (
                            f"Valid BIN -  ✅\n\n"
                            f"📌 Scheme: {response.get('scheme', 'N/A')}\n"
                            f"📌 Card Type: {response.get('type', 'N/A')}\n"
                            f"📌 Brand: {response.get('brand', 'N/A')}\n"
                            f"📌 Country: {response['country'].get('name', 'N/A')}\n"
                            f"📌 Currency: {response['country'].get('currency', 'N/A')}\n"
                            f"📌 Prepaid: {response.get('prepaid', 'N/A')}"
                        )
                        await update.message.reply_text(card_details)
                    except json.JSONDecodeError:
                        await update.message.reply_text("Invalid JSON response format.")
                elif status_code == 429:
                    await update.message.reply_text('We are experiencing high traffic.')
                else:
                    await update.message.reply_text('❌ Invalid BIN ❌')
            except Exception as e:
                await update.message.reply_text(f'Internal error: {e}')
    else:
        await update.message.reply_text(f'Hey {update.effective_user.first_name}, I only work in group chats.')
