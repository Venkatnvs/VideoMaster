from django.shortcuts import render, redirect,get_object_or_404
from .forms import VideoUploadForm
from .tasks import process_video
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
            process_video.delay(video.id)
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
