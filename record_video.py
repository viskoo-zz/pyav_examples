import av

#If you are recording video in the same codec as the one received from rtsp stream
#you can just copy packets (no need to decode them) to the output container
#This way reduces load on processor because there is no need for decoding/encoding frames

camera_path = "rtsp://path_to_rts_stream"
container = av.open(camera_path, "r")
video_stream = container.streams.video[0]

out_container = av.open("test.mp4", "w", format='mp4')
outstream = out_container.add_stream(template=video_stream)
outstream.options = {}

first_packet = True
for packet in container.demux(video_stream):
    if first_packet:
        #There is a bug in pyav where first frame has the decoding/presentation timestamps set to some high value.
        #This is causing pyav recording to crash so we manualy set the first frame dts and pts to 0
        packet.dts = 0
        packet.pts = 0
        first_packet = False

    out_container.mux(packet)