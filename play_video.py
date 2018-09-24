import av
import cv2

camera_path = "rtsp://path_to_rts_stream"
container = av.open(camera_path, "r")
video_stream = container.streams.video[0]

for packet in container.demux(video_stream):
    for frame in packet.decode():
        image = frame.to_nd_array(format="bgr24")
        cv2.imshow("Test", image)
        if cv2.waitKey(20) & 0xFF == 27:
            break

cv2.destroyAllWindows()