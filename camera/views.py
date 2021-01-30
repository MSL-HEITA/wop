from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
from . import camera_open
from  django.http.response import StreamingHttpResponse
from django.views.decorators import gzip

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
                b'content-type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@login_required
def stream(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    @gzip.gzip_page
    def video_feed(request):
        try:
            return StreamingHttpResponse(gen(camera_open()),content_type='multipart/x-mixed-replace; boundary=frame')
        except HttpResponseServerError as e:
            print("aborted")
            
    return render(request, "api.html", {
        "rooms": rooms,

    })