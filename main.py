from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import re

async def start(update, context):
    await update.message.reply_text(
        "اهلاً! ابعتلي قائمة فيها مبالغ مثل:\n"
        "محمد 300$\nميار 400$\n"
        "وأنا بجمعهم لك ✅ وبارتبهم كمان 💸"
    )

async def handle_message(update, context):
    text = update.message.text

    # استخدام تعبير منتظم لاستخراج الأرقام يلي بتنتهي بـ $ (أو بدون)
    numbers = re.findall(r'\b\d+(?:\.\d+)?(?=\$?)', text)

    if numbers:
        float_numbers = list(map(float, numbers))
        float_numbers.sort()
        total = sum(float_numbers)

        # إنشاء نص الأرقام المرتبة
        sorted_text = ", ".join(f"{n:.2f}" for n in float_numbers)

        reply = (
            f"🔢 تم العثور على {len(numbers)} مبلغ.\n"
            f"📈 الأرقام مرتبة تصاعديًا: {sorted_text}\n"
            f"💰 المجموع الكلي = {total:.2f} دولار"
        )
    else:
        reply = "❗ ما لقيتش أي أرقام في الرسالة. حاول تبعتني صيغة زي:\nمحمد 300$\nميار 250$"

    await update.message.reply_text(reply)

app = ApplicationBuilder().token("ضع_التوكن_تبعك_هنا").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
