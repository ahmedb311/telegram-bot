from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import re

async def start(update, context):
    await update.message.reply_text("اهلاً! ابعتلي قائمة فيها مبالغ مثل:\nمحمد 300$\nميار 400$\nوأنا بجمعهم لك ✅")

async def handle_message(update, context):
    text = update.message.text

    # استخدام تعبير منتظم لاستخراج الأرقام يلي بتنتهي بـ $ (أو بدون)
    numbers = re.findall(r'\b\d+(?:\.\d+)?(?=\$?)', text)

    # تحويلهم لأرقام وجمعهم
    total = sum(map(float, numbers))

    await update.message.reply_text(f"🔢 تم العثور على {len(numbers)} مبلغ.\n💰 المجموع الكلي = {total:.2f} دولار")

app = ApplicationBuilder().token("7909729072:AAHurHOhrdm5Q117Mi4UHbQP0DE_2wARxww").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()