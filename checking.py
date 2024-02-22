import cv2
ticker_video=f'../video-169.mp4'

vidcap = cv2.VideoCapture(ticker_video)
total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
value= int(vidcap.get(cv2.CAP_PROP_FPS))
print('val',value)
# val.append(value)
success,image = vidcap.read()
print('total',total)
print('valllllllll',value)
width = 640 # keep original width
height = 360
dim = (width, height)
count = 0
lst=[]
ticker_idx=0
# all_tickers_remove=glob.glob('extract/*.jpg')
# for i in all_tickers_remove:
#     os.remove(i)

while success:
    print('count',count)
    # image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    # color = (255, 0, 0)
    # thickness = 2
    # image = cv2.rectangle(resized,  (250,526),(295,345), color, thickness)  
    if count % 50== 0: 
        
            cv2.imwrite(f"checking/{count}.jpg", image)  
            cv2.imwrite(f"checking/{count}.jpg", image)  

           
    success,image = vidcap.read()
    # print('Read a new frame: ', success)
    if not success:
        break
    # else:
    #      resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    count+=1
    # count += 1
        # cv2.imwrite("frames/%d.jpg" % count, image)     # save frame as JPEG file  
        # image = cv2.imread(f'{resized}')
        # face = image[306:344, 1:516]
        # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
        # compare=Character_Comparison.objects.create(characters_comparing=characters)
        # if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
            