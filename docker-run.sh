#!/bin/bash
# سكريبت سريع لتشغيل البوت باستخدام Docker

echo "🚀 بدء تشغيل Video Splitter Bot..."

# التحقق من وجود ملف .env
if [ ! -f .env ]; then
    echo "❌ ملف .env غير موجود!"
    echo "📝 انسخ env.example إلى .env وضع التوكن"
    exit 1
fi

# التحقق من وجود Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker غير مثبت!"
    exit 1
fi

# التحقق من وجود docker-compose
if command -v docker-compose &> /dev/null; then
    echo "✅ استخدام docker-compose..."
    docker-compose up -d
    echo "✅ البوت يعمل الآن!"
    echo "📋 لعرض السجلات: docker-compose logs -f"
else
    echo "✅ استخدام Docker مباشرة..."
    docker build -t video-splitter-bot .
    docker run -d \
        --name video_splitter_bot \
        --restart unless-stopped \
        --env-file .env \
        video-splitter-bot
    echo "✅ البوت يعمل الآن!"
    echo "📋 لعرض السجلات: docker logs -f video_splitter_bot"
fi

