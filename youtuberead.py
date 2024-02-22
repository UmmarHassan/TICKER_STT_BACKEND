# import required libraries
# from vidgear.gears import CamGear
# import cv2
# def streamer(source):
#     # Add YouTube Video URL as input source (for e.g https://youtu.be/uCy5OuSQnyA)
#     # and enable Stream Mode (`stream_mode = True`)
#     stream = CamGear(
#         source="https://www.youtube.com/watch?v=O3DPVlynUM0", 
#         stream_mode=True,
#         logging=True
#     ).start()

#     # loop over
#     while True:

#         # read frames from stream
#         frame = stream.read()

#         # check for frame if Nonetype
#         if frame is None:
#             break

#         # {do something with the frame here}

#         # Show output window
#         cv2.imshow("Output", frame)

#         # check for 'q' key if pressed
#         key = cv2.waitKey(1) & 0xFF
#         if key == ord("q"):
#             break

#     # close output window
#     cv2.destroyAllWindows()

#     # safely close video stream
#     stream.stop()


# importing vlc module
# import vlc
  
# # importing pafy module
# import pafy
  
# # url of the video
# url = "https://www.youtube.com/watch?v=il_t1WVLNxk&list=PLqM7alHXFySGqCvcwfqqMrteqWukz9ZoE"
  
# # creating pafy object of the video
# video = pafy.new(url)
  
# # getting stream at index 0
# best = video.streams[0]
  
# # creating vlc media player object
# media = vlc.MediaPlayer(best.url)
  
# # start playing video
# media.play()
import cv2
import pafy

def get_youtube_frame(url):
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")

    # Open the video stream
    cap = cv2.VideoCapture(best.url)
    success, frame = cap.read()
    if success:
        # Process the frame as needed
        cv2.imwrite("frame.jpg", frame)
    cap.release()

# Usage example
url = "https://www.youtube.com/watch?v=sUKwTVAc0Vo"
get_youtube_frame(url)

# Usage example
