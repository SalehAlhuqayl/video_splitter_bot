# bot.py
import os
import asyncio
import tempfile
import shutil
import logging
from pathlib import Path
from telegram.constants import ChatAction
from telegram import Update
from telegram.error import Conflict
from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters

# استيراد دالتك
from utils.splitter import split_fast_copy

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message or update.edited_message
    if not msg:
        return

    tg_file = None
    file_name = "video.mp4"

    if msg.video:
        tg_file = await context.bot.get_file(msg.video.file_id)
        file_name = msg.video.file_name or "video.mp4"
    elif msg.document and (msg.document.mime_type or "").startswith("video/"):
        tg_file = await context.bot.get_file(msg.document.file_id)
        file_name = msg.document.file_name or "video.mp4"
    else:
        await msg.reply_text("أرسل فيديو كـ Video أو كـ Document (mp4 مثلًا).")
        return

    await context.bot.send_chat_action(chat_id=msg.chat_id, action=ChatAction.TYPING)

    work_dir = Path(tempfile.mkdtemp(prefix="tg_split_"))
    in_path = work_dir / file_name
    out_dir = work_dir / "chunks"
    out_dir.mkdir(exist_ok=True)

    try:
        # 1) تنزيل الفيديو
        await tg_file.download_to_drive(custom_path=str(in_path))
        await msg.reply_text("استلمت الملف. جاري المعالجة الآن …")

        # 2) تشغيل معالجك في thread حتى ما يحبس الـ event loop
        def _run_processing():
            return split_fast_copy(in_path, out_dir)

        parts: list[Path] = await asyncio.to_thread(_run_processing)

        if not parts:
            await msg.reply_text("تأكد من كود المعالجة.")
            return

        # 3) إرسال النتائج بالترتيب
        for idx, p in enumerate(sorted(parts), start=1):
            await context.bot.send_chat_action(chat_id=msg.chat_id, action=ChatAction.UPLOAD_VIDEO)
            caption = f"الجزء {idx} / {len(parts)}"
            try:
                with open(p, "rb") as f:
                    await msg.reply_video(video=f, caption=caption)
            except Exception as e:
                await msg.reply_text(f"تعذّر إرسال جزء {idx}: {e}")

        await msg.reply_text("انتهيت ✅")

    except Exception as e:
        await msg.reply_text(f"خطأ أثناء المعالجة: {e}")
    finally:
        try:
            shutil.rmtree(work_dir, ignore_errors=True)
        except Exception:
            pass

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرسل فيديو وسأقوم بتقسيمه إلى أجزاء مدتها 90 ثانية.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """معالج الأخطاء العام"""
    error = context.error
    
    # تجاهل خطأ Conflict - يعني أن هناك نسخة أخرى تعمل
    if isinstance(error, Conflict):
        logger.warning("تحذير: يبدو أن هناك نسخة أخرى من البوت تعمل. تأكد من إيقاف جميع النسخ الأخرى.")
        return
    
    logger.error(f"حدث خطأ: {error}", exc_info=error)
    if isinstance(update, Update) and update.message:
        try:
            await update.message.reply_text("حدث خطأ أثناء المعالجة. حاول مرة أخرى.")
        except Exception:
            pass

async def setup_bot(app: Application):
    """إعداد البوت قبل البدء"""
    try:
        # محاولة إيقاف أي webhook نشط
        await app.bot.delete_webhook(drop_pending_updates=True)
        logger.info("تم تنظيف webhook إن وجد")
    except Exception as e:
        logger.warning(f"لم يتم إيقاف webhook: {e}")

def main():
    # احصل على التوكن من متغير البيئة أو ضعه هنا مباشرة
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("خطأ: يجب تعيين متغير البيئة TELEGRAM_BOT_TOKEN")
        print("أو عدّل الكود وضَع التوكن مباشرة")
        return

    # إنشاء التطبيق
    app = Application.builder().token(token).post_init(setup_bot).build()

    # إضافة معالج الأخطاء
    app.add_error_handler(error_handler)

    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

    # بدء البوت مع حذف التحديثات القديمة
    print("البوت يعمل الآن...")
    print("ملاحظة: إذا ظهر خطأ Conflict، تأكد من إيقاف جميع النسخ الأخرى من البوت")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
