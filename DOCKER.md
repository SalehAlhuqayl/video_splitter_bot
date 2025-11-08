# دليل Docker

هذا الدليل يشرح كيفية تشغيل البوت باستخدام Docker على سيرفر Linux.

## المتطلبات

- Docker مثبت على السيرفر
- Docker Compose (اختياري لكن موصى به)
- توكن بوت تيليجرام

## التثبيت السريع

### 1. استنساخ المشروع

```bash
git clone https://github.com/yourusername/video_splitter_bot.git
cd video_splitter_bot
```

### 2. إعداد متغيرات البيئة

انسخ ملف `env.example` إلى `.env`:

```bash
cp env.example .env
```

عدّل ملف `.env` وضع التوكن:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 3. بناء وتشغيل باستخدام Docker Compose (موصى به)

```bash
docker-compose up -d
```

### 4. أو بناء وتشغيل باستخدام Docker مباشرة

```bash
# بناء الصورة
docker build -t video-splitter-bot .

# تشغيل الحاوية
docker run -d \
  --name video_splitter_bot \
  --restart unless-stopped \
  --env-file .env \
  video-splitter-bot
```

## الأوامر المفيدة

### عرض السجلات

```bash
# مع Docker Compose
docker-compose logs -f

# مع Docker مباشرة
docker logs -f video_splitter_bot
```

### إيقاف البوت

```bash
# مع Docker Compose
docker-compose down

# مع Docker مباشرة
docker stop video_splitter_bot
docker rm video_splitter_bot
```

### إعادة تشغيل البوت

```bash
# مع Docker Compose
docker-compose restart

# مع Docker مباشرة
docker restart video_splitter_bot
```

### تحديث البوت

```bash
# 1. سحب التحديثات
git pull

# 2. إعادة بناء الصورة
docker-compose build --no-cache

# 3. إعادة التشغيل
docker-compose up -d
```

### عرض حالة البوت

```bash
# مع Docker Compose
docker-compose ps

# مع Docker مباشرة
docker ps | grep video_splitter_bot
```

## استكشاف الأخطاء

### البوت لا يعمل

1. تحقق من السجلات:
```bash
docker-compose logs bot
```

2. تحقق من أن التوكن صحيح:
```bash
cat .env
```

3. تحقق من أن الحاوية تعمل:
```bash
docker-compose ps
```

### خطأ في تحميل الفيديو

- تأكد من أن ffmpeg مثبت في الحاوية (يجب أن يكون تلقائياً)
- تحقق من السجلات للأخطاء

### مشاكل الذاكرة

إذا كان السيرفر ضعيف، عدّل `docker-compose.yml` وقلل حد الذاكرة:

```yaml
deploy:
  resources:
    limits:
      memory: 1G
```

## التكوين المتقدم

### إضافة متغيرات بيئة إضافية

عدّل `docker-compose.yml`:

```yaml
environment:
  - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
  - LOG_LEVEL=INFO
```

### تغيير مسار السجلات

عدّل `docker-compose.yml`:

```yaml
volumes:
  - /path/to/logs:/app/logs
```

### تشغيل في الخلفية مع systemd

أنشئ ملف `/etc/systemd/system/video-splitter-bot.service`:

```ini
[Unit]
Description=Video Splitter Bot
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/video_splitter_bot
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down

[Install]
WantedBy=multi-user.target
```

ثم فعّل الخدمة:

```bash
sudo systemctl enable video-splitter-bot
sudo systemctl start video-splitter-bot
```

## الأمان

- **لا ترفع ملف `.env` إلى Git** - يحتوي على التوكن السري
- استخدم Docker secrets في الإنتاج
- راجع أذونات الملفات

## الأداء

- البوت يستخدم ذاكرة قليلة نسبياً
- استخدم `docker stats` لمراقبة الاستخدام
- يمكن تشغيل عدة نسخ على نفس السيرفر (مع توكنات مختلفة)

## الدعم

إذا واجهت مشاكل:
1. راجع السجلات
2. افتح Issue على GitHub
3. راجع [README.md](README.md) للمزيد من المعلومات

