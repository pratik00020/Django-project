from django.shortcuts import render, redirect
from .forms import VideoForm
from .tasks import procoess_video
import boto3
from django.conf import settings
from django.shortcuts import render

def upload_video(request):
    if request.method == 'POST' :
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video =form.save()
            procoess_video.delay(video.id)
            return redirct('video_list')
        
        else: 
            form = VideoForm()
            return render(request, 'upload_video.html', {'form': form})
        
def video_list(request):
    videos = video.objects.all()
    return render(request, 'video_list.html', {'videos' : videos})     


def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(settings.DYNAMO_TABLE_NAME)
        response  = table.scan(
            FilterExpression="contains(Text, :query)",
            ExpressionAttributeValues={":query":query}
        )
        results = response['Items']
        return render(request, 'search.html',{'query': query, 'results' : results})