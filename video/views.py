from django.shortcuts import render, redirect,get_object_or_404
from .forms import VideoUploadForm
from .tasks import process_video
from .models import Subtitles,VideoUpload
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import boto3
from boto3.dynamodb.conditions import Key, Attr

def video_list(request):
    videos = VideoUpload.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            video_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(f'uploads/video_{video.uuid}.mp4', video_file)
            process_video.delay(video.uuid)
            messages.info(request,"The video is processing")
            return redirect('video_list')
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})

def search_videos(request,video_id):
    keyword = request.GET.get('keyword')
    results = []
    context = None
    if keyword:
        subtitles = Subtitles.objects.filter(subtitle_text__icontains=keyword,video__uuid=video_id)

        for subtitle in subtitles:
            results.append({
                'video_id': subtitle.video.file.url,
                'start_time': subtitle.start_time,
                'end_time': subtitle.end_time
            })
        context = {'results': results, 'keyword': keyword}

    return render(request, 'search.html',context)


def play_video(request, video_id):
    video = get_object_or_404(VideoUpload, uuid=video_id)
    video_path = video.file.path

    with open(video_path, 'rb') as video_file:
        response = HttpResponse(video_file.read(), content_type='video/mp4')
        return response
    

def search_videos2(request, video_id):
    keyword = request.GET.get('keyword')
    results = []
    context = None

    if keyword:
        dynamodb = boto3.client('dynamodb',region_name='ap-south-1')
        table_name = 'nvstable_nosql'
        expression_attribute_values = {
            ':keyword': {'S': keyword},
            ':video': {'S': video_id}
        }
        filter_expression = 'VideoId = :video AND contains(Subtitle, :keyword)'
        response = dynamodb.scan(
            TableName=table_name,
            FilterExpression=filter_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        # results = response.get('Items', [])
        # filter_expression = Attr('video').contains(keyword) & Attr('VideoId').eq(str(video_id))

        # # Perform the scan operation
        # response = dynamodb.scan(
        #     TableName=table_name,
        #     FilterExpression=str(filter_expression)
        # )

        # Extract the items from the response
        results = response.get('Items', [])
        print(results)
        context = {'results': results, 'keyword': keyword}
    return render(request, 'search2.html', context)
