import requests, random, atexit

BASE_URL = "https://apiv3.fansly.com/api/v1"

class Fansly:
    def __init__(self, autoExit=True):
        self.token = ""
        self.username = ""
        self.deviceID = ""
        self.sessionID = ""
        self.autoExit = autoExit
        self.session = requests.session()
        self.headers = {}
        atexit.register(self.handleExit)
    
    def logout(self):
        """
        Logs out current client session.
        Usage: logout() 
        """

        if self.sessionID != "" and self.autoExit:
            self.session.post(BASE_URL+"/session/close", headers=self.headers, json={"id": self.sessionID})
    
    def handleExit(self):
        """
        Handles program exist to automatically log out session so 
        you don't have a million sessions every time you look at "active sessions"
        """

        if self.sessionID != "":
            print("Logging out client...")
            self.logout()
    
    def login(self, username, password):
        """
        Endpoint: /login
        What it do? Logs you into the service, returns new token for randomized device id
        Usage: Fansly.login(<username>, <password>)
        Returns: Account Token, Session ID
        """

        # Save username for later
        self.username = username

        deviceID = ''.join([str(random.randint(0, 9)) for i in range(32)])
        sessionID = ""
        headers = {"Referer": "https://fansly.com","Content-Type": "application/json","Accept": "application/json","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}

        r = self.session.post(BASE_URL+"/login", headers=headers, json={"deviceId": deviceID, "password": password, "username": username})
        token = ""
        try:
            if list(r.json()['response'].keys()).index("twofa") != -1:
                code = input("What is the emailed code?")
                r = self.session.post(BASE_URL+"/login/twofa", headers=headers, json={"token": r.json()['response']['twofa']['token'], "code": code})
                token = r.json()['response']['token']
                sessionID = r.json()['response']['id']
        except:
            if r != 500:
                token = r.json()['response']['session']['token']
                sessionID = r.json()['response']['session']['id']
            else:
                return False
        self.token = token
        self.sessionID = sessionID
        self.headers = {
                "Referer": "https://fansly.com",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": self.token,
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        return token, sessionID
    
    def getAccount(self, username=None):
        """
        Gets account data for account with specified username (optional),,
        or the user's data

        Usage: Fansly.getAccount(<username>)
        Returns: Fansly user object
        """
        if username == None:
            username = self.username

        r = self.session.get(BASE_URL+f"/account?usernames={username}", headers=self.headers)
        return r.json()