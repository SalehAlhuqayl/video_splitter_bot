#!/bin/bash
# سكريبت للتحقق من أن Docker يعمل بشكل صحيح

echo "🔍 التحقق من إعداد Docker..."

# التحقق من وجود Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker غير مثبت!"
    exit 1
fi
echo "✅ Docker مثبت"

# التحقق من أن Docker يعمل
if ! docker ps &> /dev/null; then
    echo "❌ Docker لا يعمل. حاول: sudo systemctl start docker"
    exit 1
fi
echo "✅ Docker يعمل"

# التحقق من وجود docker-compose
if command -v docker-compose &> /dev/null; then
    echo "✅ docker-compose مثبت"
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    echo "✅ docker compose (V2) متاح"
    COMPOSE_CMD="docker compose"
else
    echo "⚠️  docker-compose غير مثبت (اختياري)"
    COMPOSE_CMD=""
fi

# التحقق من وجود ملف .env
if [ ! -f .env ]; then
    echo "❌ ملف .env غير موجود!"
    echo "📝 انسخ env.example إلى .env وضع التوكن"
    exit 1
fi
echo "✅ ملف .env موجود"

# التحقق من وجود التوكن في .env
if ! grep -q "TELEGRAM_BOT_TOKEN=" .env || grep -q "your_bot_token_here" .env; then
    echo "⚠️  تحذير: تأكد من وضع التوكن الصحيح في ملف .env"
fi

# التحقق من وجود Dockerfile
if [ ! -f Dockerfile ]; then
    echo "❌ Dockerfile غير موجود!"
    exit 1
fi
echo "✅ Dockerfile موجود"

# محاولة بناء الصورة (اختياري)
echo ""
read -p "هل تريد بناء الصورة الآن للتحقق؟ (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔨 بناء الصورة..."
    docker build -t video-splitter-bot-test .
    if [ $? -eq 0 ]; then
        echo "✅ الصورة بُنيت بنجاح!"
        
        # التحقق من أن ffmpeg يعمل في الصورة
        echo "🔍 التحقق من ffmpeg..."
        docker run --rm video-splitter-bot-test ffmpeg -version | head -n 1
        if [ $? -eq 0 ]; then
            echo "✅ ffmpeg يعمل في الصورة"
        else
            echo "❌ مشكلة في ffmpeg"
        fi
        
        # التحقق من Python
        echo "🔍 التحقق من Python..."
        docker run --rm video-splitter-bot-test python --version
        if [ $? -eq 0 ]; then
            echo "✅ Python يعمل"
        else
            echo "❌ مشكلة في Python"
        fi
    else
        echo "❌ فشل بناء الصورة"
        exit 1
    fi
fi

echo ""
echo "✅ كل شيء جاهز!"
echo ""
echo "للتشغيل:"
if [ -n "$COMPOSE_CMD" ]; then
    echo "  $COMPOSE_CMD up -d"
else
    echo "  docker build -t video-splitter-bot ."
    echo "  docker run -d --name video_splitter_bot --restart unless-stopped --env-file .env video-splitter-bot"
fi


