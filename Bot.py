BOT_TOKEN = "6424192155:AAFqRm_qlTbCdSZlP-3TmoQoAnqc0Fy_f1k"


from features.commands import bin_lookup_handler, card_check_handler, hello_handler
from telegram.ext import ApplicationBuilder, CommandHandler, filters

from utils.db_connection import conn


if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("hello", hello_handler))
    app.add_handler(CommandHandler("chk", card_check_handler))
    app.add_handler(CommandHandler("bin", bin_lookup_handler))
    print('CC Checker 🤠 running...')

    app.run_polling()

conn.close()