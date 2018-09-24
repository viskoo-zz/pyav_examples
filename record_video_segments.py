import av
import time

#Below code shows how to record rtsp stream splitted into mp4 files
camera_path = "rtsp://path_to_rts_stream"
in_container = av.open(camera_path, "r")
video_stream = in_container.streams.video[0]

out_container = None

def start_container(stream, timestamp):
    global out_container
    #filename example: file_1234567123.mp4
    filename = "./file_" + str(timestamp) + ".mp4"
    out_container = av.open(filename, "w", format="mp4")
    outstream = out_container.add_stream(template=stream)
    outstream.options = {}

def stop_container():
    global out_container
    out_container.close()
    out_container = None

first_packet = True
rescaling_nr = 0
clip_duration = 1 * 60 * 1000 #10 minutes
first_frame_timestamp = int(time.time() * 1000)

for packet in in_container.demux(video_stream):
    if first_packet:
        packet.dts = 0
        packet.pts = 0
        first_packet = False

    cur_timestamp = int(time.time() * 1000)
    #clips will be splitted if the time is larger than clip duration and on next first keyframe
    if packet.is_keyframe and (cur_timestamp - first_frame_timestamp) >= clip_duration:
        stop_container()

    if out_container is None:
        rescaling_nr = packet.dts
        start_container(video_stream, cur_timestamp)
        first_frame_timestamp = cur_timestamp

    #Pyav does not rescale down pts/dts so we have to do it manually for every packet
    packet.pts -= rescaling_nr
    packet.dts -= rescaling_nr

    out_container.mux_one(packet)