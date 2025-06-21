import re
import os
import sys
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text(
        "أرسل لي قائمة فيها أسماء ومبالغ مثل:\n"
        "محمد 100$\nسارة 2500$\nوأنا برتبهم وبحسبلك المجموع ✅"
    )

async def stopbot(update, context):
    await update.message.reply_text("📴 جاري إيقاف البوت... إلى اللقاء 👋")
    await asyncio.sleep(1)
    await context.application.stop()
    sys.exit()  # ← هذا هو المفتاح اللي يخلي Railway يوقف الخدمة

async def handle_message(update, context):
    text = update.message.text
    lines = text.strip().split("\n")
    entries = []

    for line in lines:
        match = re.search(r'(.+?)\s+(\d+(?:\.\d+)?)\$?', line)
        if match:
            name = match.group(1).strip()
            amount = float(match.group(2))
            entries.append((name, amount))

    if not entries:
        await update.message.reply_text(
            "ما لقيتش ولا مبلغ. تأكد إنك كاتب كل سطر بهالصيغة:\nالاسم 200$"
        )
        return

    sorted_entries = sorted(entries, key=lambda x: x[1])
    total = sum(amount for _, amount in sorted_entries)
    count = len(sorted_entries)

    formatted = "\n".join([
        f"{name} {int(amount) if amount.is_integer() else amount}$"
        for name, amount in sorted_entries
    ])

    reply = (
        f"📋 تم العثور على {count} مبلغ.\n\n"
        f"{formatted}\n\n"
        f"💰 المجموع الكلي: {int(total) if total.is_integer() else total}$"
    )

    await update.message.reply_text(reply)

# التوكن الوهمي – للتجربة فقط
app = ApplicationBuilder().token("7909729072:AAHurHOhrdm5Q117Mi4UHbQP0DE_2wARxww").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stopbot", stopbot))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
