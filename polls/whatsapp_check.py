# # import pywhatkit as pw
# # import time

# # def send_media(number, media_path):
# #     try:
# #         # Wait for 10 seconds before sending the message
# #         time.sleep(3)
        
# #         # Send media using pywhatkit
# #         pw.send_media(phone_no=number, media_file=media_path)
        
# #         print("Media sent successfully!")
# #     except Exception as e:
# #         print("Error sending media:", str(e))
# # number = "+923155503675"  # Replace with the desired phone number
# # media_path = "ticker.jpg"  # Replace with the actual media file path

# # send_media(number, media_path)
# import pywhatkit
# import time
# # Send a WhatsApp Message to a Contact at 1:30 PM
# # pywhatkit.sendwhatmsg("+910123456789", "Hi", 13, 30)

# # Same as above but Closes the Tab in 2 Seconds after Sending the Message
# # pywhatkit.sendwhatmsg("+910123456789", "Hi", 13, 30, 15, True, 2)

# # Send an Image to a Group with the Caption as Hello
# # pywhatkit.sendwhats_image("AB123CDEFGHijklmn", "ticker.jpg", "Hello")

# # Send an Image to a Contact with the no Caption
# pywhatkit.sendwhats_image("+923119633700", "ticker.jpg",tab_close=True)
# time.sleep(5)
# # Send a WhatsApp Message to a Group at 12:00 AM
# # pywhatkit.sendwhatmsg_to_group("AB123CDEFGHijklmn", "Hey All!", 0, 0)

# # Send a WhatsApp Message to a Group instantly
# # pywhatkit.sendwhatmsg_to_group_instantly("AB123CDEFGHijklmn", "Hey All!")

# # Play a Video on YouTubefrom alright import WhatsApp

# from alright import WhatsApp
# # import time
# def send_whatsapp_message(number):
#     whatsapp = WhatsApp()
#     whatsapp.find_user(number)
#     whatsapp.send_picture('ticker.jpg',"Text to accompany image")
#     # time.sleep(4)
#     whatsapp.close()

# # Usage example
# number = "+923119633700"  # Recipient's phone number
# message = "Hello, this is a test message!"  # Message content

# send_whatsapp_message(number)
# import pyautogui
import pywhatkit
# import keyboard
import time
# try:
#         pywhatkit.sendwhats_image(
#             "++923086715563", 
#             'ticker.jpg',
#             tab_close=True
#         )
        
     
#         print("Message sent!")
# except Exception as e:
#         print(str(e)) 
# from infobip_channels.whatsapp.channel import WhatsAppChannel
# channel = WhatsApp Channel.from_auth_params({
#     "base_url": "5vryyd.api.infobip.com",
#     "api_key": "••••••••••••••••••••••••••••"
# })
# response = channel.send_image_message({
#   "from": "+923155503675",
#   "to": "+923119633700",
#   "messageId": "a28dd97c-1ffb-4fcf-99f1-0b557ed381da",
#   "content": {
#     "mediaUrl": "https://seekvectorlogo.com/wp-content/uploads/2019/06/infobip-vector-logo-small.png",
#     "caption": "Check out our logo!"
#   }
# })
# from whatsapp import Client

# phone_to = '31641371199'

# client = Client(login='3161516888', password='secretpasswordbase64')
# client.send_message(phone_to, 'Hello Lola')
# client.send_media(phone_to, path='/Users/tax/Desktop/logo.jpg')
import asyncio


from AsyncPywhatKit.src import sendimg_or_video_immediately




async def main():
    await sendimg_or_video_immediately("+923119633700", "ticker.jpg",tab_close=True)
asyncio.run(main())