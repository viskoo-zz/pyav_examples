import av
from av.logging import Capture

#Catchin errors either on the stream opening or on stream handling(decoding)

try:
    camera_path = "rtsp://path_to_rts_stream"
    in_container = av.open(camera_path, "r")
    video_stream = in_container.streams.video[0]
except av.utils.AVError as e:
    print(e)

def handle_errors(logs):
    while len(logs) > 0:
        log = logs.pop()
        print log

with Capture(local=True) as logs:
    for packet in in_container.demux(video_stream):
        for frame in packet.decode():
            #Do something with frame
            handle_errors(logs)
