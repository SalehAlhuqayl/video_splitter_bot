"""
دوال تحميل الفيديوهات من الروابط
"""
import yt_dlp
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def download_tiktok_video(url: str, output_path: Path) -> Path:
    """
    تحميل فيديو من رابط تيك توك
    
    Args:
        url: رابط تيك توك
        output_path: مسار حفظ الفيديو
        
    Returns:
        مسار الفيديو المحمّل
    """
    # إنشاء اسم ملف بسيط
    output_file = output_path / "tiktok_video.%(ext)s"
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',  # أفضل جودة mp4
        'outtmpl': str(output_file),
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # الحصول على معلومات الفيديو
            info = ydl.extract_info(url, download=True)
            
            # الحصول على اسم الملف المحمّل
            filename = ydl.prepare_filename(info)
            video_path = Path(filename)
            
            # إذا لم يكن الملف موجوداً، ابحث في المجلد
            if not video_path.exists():
                # البحث عن أي ملف فيديو في المجلد
                video_extensions = ['.mp4', '.webm', '.mkv', '.mov', '.avi']
                for ext in video_extensions:
                    potential_files = list(output_path.glob(f"*{ext}"))
                    if potential_files:
                        return potential_files[0]
                
                # إذا لم نجد، استخدم الاسم المتوقع
                logger.warning(f"الملف المتوقع {filename} غير موجود، البحث في {output_path}")
                all_files = list(output_path.glob("*"))
                if all_files:
                    return all_files[0]
                
                raise FileNotFoundError(f"لم يتم العثور على الملف المحمّل في {output_path}")
            
            return video_path
            
    except Exception as e:
        logger.error(f"خطأ في تحميل الفيديو من {url}: {e}")
        raise


def is_tiktok_url(url: str) -> bool:
    """
    التحقق من أن الرابط هو رابط تيك توك
    
    Args:
        url: الرابط للتحقق
        
    Returns:
        True إذا كان رابط تيك توك
    """
    tiktok_domains = [
        'tiktok.com',
        'vm.tiktok.com',
        'vt.tiktok.com',
        'www.tiktok.com',
    ]
    
    url_lower = url.lower()
    return any(domain in url_lower for domain in tiktok_domains)

