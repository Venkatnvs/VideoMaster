from celery import shared_task
import subprocess
from .models import VideoUpload, Subtitles
import os
from django.conf import settings

# @shared_task

def process_video(video_id):
    video = VideoUpload.objects.get(id=video_id)
    input_path = video.file.path
    output_path = os.path.join(settings.MEDIA_ROOT,"subtitles",f'subtitles_{video_id}.srt')

    ccextractor_command = f'ccextractorwinfull {input_path} -o {output_path}'
    subprocess.run(ccextractor_command, shell=True)
    
    with open(output_path, 'r') as subtitle_file:
        for line in subtitle_file:
            parts = line.strip().split('\n')
            print(parts)
            start_end = parts[0].split(' --> ')
            start_time = start_end[0].strip()
            end_time = start_end[1].strip()
            subtitle_text = parts[1]

            subtitle = Subtitles(video=video, start_time=start_time, end_time=end_time, subtitle_text=subtitle_text)
            subtitle.save()

    return "done"