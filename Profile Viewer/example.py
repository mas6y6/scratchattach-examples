import scratchattach as scratch3 #Import the scratchattach module

#Logins to your scratch account using sessionid
session = scratch3.Session(".eJxVkEtPwzAQhP9LzjTEdvzqrZU4IYGIkApcIsdeNyaNXcWuykP8d2wpl15nZr_Z3d_qEmHxaoZqW80qsm9W3VUpTOCzYIRAjFFMKOYtQc1gueCCMo0ZGMTF9qv7GHfp7cW-glvU8-Ghe3Rs08oDjxlzCkfnN-6cSUTUqCE1JrJGCGevV5c09qW8dyYHOBW4lYRky3wqfwx9cjP8BF8W282wOK3un-Dav4dlup0fVRxzCEklDVKSSI6ZUQYjqxWxzaCJQLTF0oLhtLHlPohJhzC5Ar9mIJhb5KB0_kDZq2jgU25PLvh6NWLdwfm0ivs1_PcPuABqDw:1qUtFi:qT1j73gwy-ix2YANcvjHE80ptk4", username="Python")

#Replace "session_id" with your session id 
#Use https://github.com/TimMcCool/scratchattach/wiki/Get-your-session-id to get session id of your account
conn = session.connect_cloud("885272042") #replace the text with your project id
client = scratch3.CloudRequests(conn,ignore_exceptions=True) #The "ignore_exceptions" input does not let the server go down when a error occurs

# When a request is send from the scratch project it will be detected with this line of code below
# and the "@" symbol before "client.request" means that it will execute the function below the "@client.request" line.
@client.request
def get_profile(username):
    user = scratch3.get_user(username) # Creates a class with the user info

    returndata = []

    returndata.append(user.username)
    returndata.append(user.follower_count())
    returndata.append(user.message_count())
    returndata.append(user.join_date)
    returndata.append(user.id)

    return returndata # Returns the list back to scratch

client.run() #Starts the server