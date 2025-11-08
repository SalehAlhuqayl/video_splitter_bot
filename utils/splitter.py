from moviepy.editor import VideoFileClip
import ffmpeg
from pathlib import Path


def split_fast_copy(in_path, out_dir="cuts"):
    """
    in_path: مسار الفيديو
    out_dir: مجلد الإخراج
    """
    # تحويل Path إلى string إذا لزم الأمر
    in_path_str = str(in_path) if isinstance(in_path, Path) else in_path
    cuts = get_cuts(get_duration(in_path_str))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    part_coutier = 0
    parts = []
    for c in cuts:
        part_coutier += 1
        out_path = out / f"Part_{part_coutier}.mp4"
        (
            ffmpeg
            .input(in_path_str, ss=c["start"], to=c["end"])  # seek تقريبي سريع
            .output(str(out_path), c="copy")             # دون إعادة ترميز
            .overwrite_output()
            .run(quiet=True)
        )
        parts.append(out_path)
    return parts

def get_cuts(duration):
    """يقسم الفيديو إلى أجزاء كل جزء 90 ثانية"""
    new_time = 0
    times = [0]

    while new_time <= duration:
        new_time += 90
        if new_time > duration:
            times.append(duration)
            break
        times.append(new_time)

    cuts = []
    for i in range(len(times) - 1):
        cuts.append({"start": times[i], "end": times[i + 1]})
    return cuts

def get_duration(video_path):
    # تحويل Path إلى string إذا لزم الأمر
    video_path_str = str(video_path) if isinstance(video_path, Path) else video_path
    clip = VideoFileClip(video_path_str)
    duration = clip.duration
    clip.close()
    return duration