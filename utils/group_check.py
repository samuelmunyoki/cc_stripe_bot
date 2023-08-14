from telegram import Update
def group_check_middleware(update: Update):
    if update.message.chat.type == "group" or update.message.chat.type == "supergroup":
        return True
    else:
        return False