import websocket, requests, json, random

BASE_URL = "https://apiv3.fansly.com/api/v1"

class Chatbot:
    def __init__(self, chatRoom):
        """
        Initialize the class.
        Required params: chatRoom id (type: str)

        Required flow to run client: Init -> Login -> Run

        I will eventually change the chatroom id to be 
        automatically found, sorry for the inconvenience!
        """
        self.token = ""
        self.headers = ""
        self.session = requests.session()
        self.chatRoomId = chatRoom
    
    def login(self, username, password):
        """
        Copied and pasted login code from client.py

        Usage: Chatbot.login(username, password)
        Returns: None (token is stored in class)
        """
        deviceID = ''.join([str(random.randint(0, 9)) for i in range(32)])
        headers = {"Referer": "https://fansly.com","Content-Type": "application/json","Accept": "application/json","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}

        r = self.session.post(BASE_URL+"/login", headers=headers, json={"deviceId": deviceID, "password": password, "username": username})
        token = ""
        try:
            if list(r.json()['response'].keys()).index("twofa") != -1:
                code = input("What is the emailed code?")
                r = self.session.post(BASE_URL+"/login/twofa", headers=headers, json={"token": r.json()['response']['twofa']['token'], "code": code})
                token = r.json()['response']['token']
        except:
            if r != 500:
                token = r.json()['response']['session']['token']
            else:
                return False
        self.token = token
        self.headers = {
                "Referer": "https://fansly.com",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": self.token,
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }

    def on_message(self, ws, message):
        """
        Usage: None (sub-method of self.ws)
        Returns: (MessageContent, MessageAuthor)
        """

        ## Parsing this event was a pain in the ass lol
        raw = json.loads(json.loads(json.loads(message)["d"])["event"]) 

        message = raw["chatRoomMessage"]["content"]
        messageAuthor = raw["chatRoomMessage"]["username"]

        print(message)

        ## Use your logic here. Example ping command has been provided

        if message[0] == "!": # Or whatever your prefix is
            message = message[1:]
            print(message)
            messageSplit = message.split(" ")

            match messageSplit[0]:
                case "ping":
                    self.sendMessage(f"@{messageAuthor} pong!")



            



    def on_open(self, ws):
        ## Ping every 20 seconds.
        print("Opened connection")
        d = "{\"token\":"+f"\"{self.token}\""+"}"
        d2 = "{\"chatRoomId\":\""+self.chatRoomId+"\"}"
        ws.send(json.dumps({"t":1,"d":d}))
        ws.send(json.dumps({"t":46001,"d":d2}))   

    def sendMessage(self, content):
        """
        Post chat message in specified room with content

        Usage: Fansly.postChatMessage(<content:str>)
        Returns: Response Object
        """

        r = self.session.post(BASE_URL+f"/chatroom/message?chatRoomId=chatRoom", headers=self.headers, json={"chatRoomId": str(self.chatRoomId), "content": content})
        return r.json()
    
    def on_error(self, ws, e):
        print(f"Error: {e}")

    def on_close(self, ws, close_status_code, close_msg):
        print("conn closed")

    def run(self):
        """
        Run the client.
        Usage: Chatbot.run()
        """
        ws = websocket.WebSocketApp("wss://chatws.fansly.com/",
                                on_open=self.on_open,
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close)

        ws.run_forever()