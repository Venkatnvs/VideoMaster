from django.shortcuts import render, redirect,get_object_or_404
from .forms import VideoUploadForm
from .tasks2 import process_video
from .models import Subtitles,VideoUpload
from django.http import HttpResponse

def video_list(request):
    videos = VideoUpload.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            a = process_video(video.id)
            return redirect('video_list')
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})

def search_videos(request):
    keyword = request.GET.get('keyword')
    results = []

    if keyword:
        subtitles = Subtitles.objects.filter(subtitle_text__icontains=keyword)

        for subtitle in subtitles:
            results.append({
                'video_id': subtitle.video.file.url,
                'start_time': subtitle.start_time,
                'end_time': subtitle.end_time
            })

    return render(request, 'search.html', {'results': results, 'keyword': keyword})


def play_video(request, video_id):
    video = get_object_or_404(VideoUpload, uuid=video_id)
    video_path = video.file.path

    with open(video_path, 'rb') as video_file:
        response = HttpResponse(video_file.read(), content_type='video/mp4')
        return response
