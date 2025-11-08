# استخدام صورة Python رسمية كقاعدة
FROM python:3.12-slim

# تعيين معلومات الصانع (اختياري)
LABEL maintainer="Video Splitter Bot"
LABEL description="Telegram bot to split videos into 90-second parts"

# تثبيت ffmpeg والمكتبات المطلوبة
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملف requirements أولاً (لتحسين cache)
COPY requirements.txt .

# تثبيت المكتبات Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات
COPY . .

# إنشاء مجلد للبيانات المؤقتة والسجلات
RUN mkdir -p /app/temp /app/logs

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# التحقق من أن ffmpeg يعمل
RUN ffmpeg -version

# تشغيل البوت
CMD ["python", "bot.py"]

