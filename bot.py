import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد السجلات (Logging) لمراقبة الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# استبدل هذا التوكن بالتوكن الخاص بـ بوتك من BotFather
TOKEN = "8800928973:AAEObKKrJ2jC4jsocySfIZjdggt8IN7uhu0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """أمر البداية عند تشغيل البوت"""
    await update.message.reply_text(
        "أهلاً بك! أرسل لي قائمة بالأسماء والمبالغ (كل اسم ومبلغ في سطر، مثل:\nأحمد 100\nمحمد 250)\n"
        "وسأقوم بحساب المجموع الكلي وترتيبهم من الأصغر للأكبر تلقائياً."
    )

async def process_calculation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالجة الرسالة وحساب المجموع والترتيب"""
    text = update.message.text
    if not text:
        return

    lines = text.strip().split('\n')
    items = []
    
    # نمط للبحث عن الأرقام والمبالغ في السطر (يدعم الأرقام مع علامة $ أو بدونها)
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # استخراج الأرقام من السطر
        numbers = re.findall(r'\d+(?:\.\d+)?', line)
        if numbers:
            # نأخذ آخر رقم مذكر في السطر كقيمة للمبلغ
            amount = float(numbers[-1])
            # إزالة المبلغ وعلامات العملة من السطر للحصول على الاسم فقط
            name = line
            for num in numbers:
                name = name.replace(num, "")
            name = name.replace("$", "").replace("¥", "").replace("€", "").strip()
            
            # إذا بقي الاسم فارغاً، نضع اسم افتراضي أو نترك القيمة
            if not name:
                name = "حساب"
                
            items.append((name, amount))

    if not items:
        await update.message.reply_text("عذراً، لم أتمكن من قراءة أي مبالغ أو أسماء من رسالتك. الرجاء التأكد من التنسيق.")
        return

    # ترتيب القائمة من الأصغر إلى الأكبر بناءً على المبلغ
    items_sorted = sorted(items, key=lambda x: x[1])
    
    # حساب المجموع الكلي
    total_sum = sum(x[1] for x in items)
    
    # بناء نص الإجابة بنفس التنسيق المطلوب في الصورة تماماً
    response_lines = ["📋 القائمة مرتبة من الأصغر للأكبر:"]
    for name, amount in items_sorted:
        # إذا كان المبلغ صحيح بدون فواصل نطبعه كعدد صحيح، وإلا ككسر
        if amount.is_integer():
            response_lines.append(f"{name} {int(amount)}$")
        else:
            response_lines.append(f"{name} {amount}$")
            
    response_lines.append("") # سطر فارغ
    if total_sum.is_integer():
        response_lines.append(f"💰 المجموع الكلي = {int(total_sum)}.00 دولار")
    else:
        response_lines.append(f"💰 المجموع الكلي = {total_sum:.2f} دولار")

    response_text = "\n".join(response_lines)
    
    # إرسال النتيجة للمستخدم
    await update.message.reply_text(response_text)

def main() -> None:
    """تشغيل البوت"""
    # إنشاء التطبيق وتمرير التوكن الخاص بالبوت
    application = Application.builder().token(TOKEN).build()

    # تسجيل الأوامر والرسائل
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_calculation))

    # بدء تشغيل البوت واستقبال البيانات (Polling)
    print("البوت يعمل الآن بنجاح على السيرفر...")
    application.run_polling()

if __name__ == '__main__':
    main()
