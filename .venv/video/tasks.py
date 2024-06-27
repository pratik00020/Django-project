import os 
from celery import shared_task
from .models import Video
import subprocess
import boto3
from django.conf import settings 
import json
from datetime import datetime

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video_path = video.file.path

    #Extract subtitles using CCextractor
    subtitle_path = f"{video_path}.srt"
    command = f"ccextractor {video_path} -o {subtitle_path}"
    subprocess.run(command, shell=True, check=True)

    #Parse subtitles
    subtitles = pasre_subtitles(subtitle_path)
    
    #store subtitle in DynamoDB
    store_subtitles(video_id, subtitles)

    #Upload video to S3
    s3 = boto3.client('s3')
    s3.upload_file(video_path, settings.AWS_STORAGE_BUCKET_NAME, f"videos/{os.path.basename(video_path)}")


    def parse_subtitles(subtitle_path):
        subtitles = []
        with open(subtitle_path, 'r') as file:
            for line in file: 
                if line.strip().isdigit():
                    timesstamp = file.readline().strip()
                    text = file.readline().strip()
                    start, end = timesstamp.split('-->')
                    start_time = convert_to_seconds(start)
                    end_time = convert_to_seconds(end)
                    subtitles.apppend({
                        'start' : start_time,
                        'end' : end_time,
                        'text' : text
                    })

            return subtitles


        def convert_to_seconds(timestamp):
            h,m,s = map(float, timesstamp.repalce(',', '.').split(':'))
            return h * 3600 + m * 60 + s

        def store_subtitles(video_id, subtitles):
            dynamodb = boto3.resource('dynamodb') 
            table = dynamodb.Table(settings.DYNAMODB_TABLE_NAME)
            with table.batch_writer() as batch:
                for subtitle in subtitles: 
                    batch.put_item(Item={
                        'VideoId': str(video_id),
                        'Start': subtitle['start'],
                        'End' : subtitle['end'],
                        'Text' : subtitle['text']
                    })
                     
