from celery import shared_task
import subprocess
from .models import VideoUpload, Subtitles
import os
from django.conf import settings
import boto3
import requests

def parse_time_range(time_range):
    start, end = time_range.split(' --> ')
    return start, end

@shared_task
def process_video(video_id):
    video = VideoUpload.objects.get(uuid=video_id)
    # video_url = video.file.url
    # print(video_url)
    # s3 = boto3.client('s3',region_name='ap-south-1')
    input_path = os.path.join(settings.MEDIA_ROOT,"uploads",f'video_{video_id}.mp4')
    # s3.download_file('nvsvenakt', video_url, input_path)
    # response = requests.get(video_url, stream=True)
    # with open(input_path, 'wb') as file:
    #     for chunk in response.iter_content(chunk_size=128):
    #         file.write(chunk)
    output_path = os.path.join(settings.MEDIA_ROOT,"subtitles",f'subtitles_{video_id}.srt')

    ccextractor_command = f'ccextractorwinfull {input_path} -o {output_path}'
    subprocess.run(ccextractor_command, shell=True)
    
    with open(output_path, 'r') as subtitle_file:
        subtitle_text = subtitle_file.read()
        subtitle_entries = subtitle_text.split('\n\n')
        for i in subtitle_entries:
            lines = i.split('\n')
            if len(lines) >= 3:
                sequence = lines[0]
                time_range = lines[1]
                start_time, end_time = parse_time_range(time_range)
                content = '\n'.join(lines[2:])
                content = content.strip()
                store_subtitle_in_dynamodb(video_id, start_time, content,end_time)
                # subtitle = Subtitles(video=video, start_time=start_time, end_time=end_time, subtitle_text=content)
                # subtitle.save()

    return "done"

def store_subtitle_in_dynamodb(video_id, timestamp, subtitle,end_time):
    dynamodb = boto3.client('dynamodb',region_name='ap-south-1')
    table_name = 'nvstable_nosql'
    item = {
        'video':{'S': end_time},
        'VideoId': {'S': str(video_id)},
        'Timestamp': {'S': timestamp},
        'Subtitle': {'S': subtitle},
    }
    dynamodb.put_item(TableName=table_name, Item=item)