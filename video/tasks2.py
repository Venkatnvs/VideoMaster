from celery import shared_task
import subprocess
from .models import VideoUpload, Subtitles
import os
from django.conf import settings
import re

# @shared_task

def parse_time_range(time_range):
    start, end = time_range.split(' --> ')
    return start, end

def process_video(video_id):
    video = VideoUpload.objects.get(id=video_id)
    input_path = video.file.path
    output_path = os.path.join(settings.MEDIA_ROOT,"subtitles",f'subtitles_{video_id}.srt')

    # Run ccextractor command
    ccextractor_command = f'ccextractorwinfull {input_path} -o {output_path}'
    subprocess.run(ccextractor_command, shell=True)

    with open(output_path, 'r') as subtitle_file:
        subtitle_text = subtitle_file.read()
        subtitle_entries = subtitle_text.split('\n\n')
        j=0
        for i in subtitle_entries:
            lines = i.split('\n')
            if len(lines) >= 3:
                sequence = lines[0]
                time_range = lines[1]
                start_time, end_time = parse_time_range(time_range)
                content = '\n'.join(lines[2:])
                # print({'sequence': sequence.strip(), 'start_time': start_time.strip(),"end_time":end_time.strip(), 'content': content.strip()})
                # print("-----------")
                subtitle = Subtitles(video=video, start_time=start_time, end_time=end_time, subtitle_text=content)
                subtitle.save()




    return "done"