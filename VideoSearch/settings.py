CELERY_BROKE_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

AWS_ACCESS_KEY_ID = 'AKIA2UC27VLUHEW4SA6B'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'video-storage-bucket-pratik'
DYNAMODB_TABLE_NAME = 'VideoSubtitle'



# Static and media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')