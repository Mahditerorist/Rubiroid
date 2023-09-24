from encryption import encryption
import asyncio
import aiohttp
import random
from json import loads, dumps
from re import findall
from json import loads, dumps
from base64 import b64decode


      
class rubika:
    def __init__(self, auth: str, private_key: str) -> None:
        self.auth          = auth
        self.key           = private_key
        self.encryption    = encryption(auth, f"-----BEGIN RSA PRIVATE KEY-----\n{self.key}\n-----END RSA PRIVATE KEY-----")
        self.auth_send     = self.encryption.changeAuthType(auth)
        self.__app_version = "3.3.2"
        self.__api_version = "6"
        self.__url         = "https://messengerg2c58.iranlms.ir/"


    async def makeRequests(self, method: str, temp_code: str, data: str):
        createData = lambda method, data, temp_code: {
            "input": data,
            "client": {
                "app_name": "Main",
                "app_version": self.__app_version,
                "lang_code": "fa",
                "package": "app.rbmain.a",
                "temp_code": temp_code,
                "platform": "Android"
            },
            "method": method
        }
        async with aiohttp.ClientSession() as CipherX:
            async with CipherX.post(self.__url, headers={
                    'Origin': 'https://web.rubika.ir',
					'Referer': 'https://web.rubika.ir/',
					'Host':self.__url.replace("https://","").replace("/",""),
					'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"}, data=dumps({
                "api_version": self.__api_version,
                "auth": self.auth_send,
                "data_enc": self.encryption.encrypt(dumps(createData(method, data, temp_code))),
                "sign": self.encryption.makeSignFromData(self.encryption.encrypt(dumps(createData(method, data, temp_code))))
            })) as response:
                Cipher = await response.text()
                return loads(self.encryption.decrypt(loads(Cipher)['data_enc']))
            
    def send_post(self, method: str, temp_code: str, data):
        try:
            return asyncio.run(self.makeRequests(method=method, temp_code=temp_code, data=data))
        except:
            pass

    def sendMessage(self, guid: str, text: str):
        rnd = lambda min_val, max_val: str(random.randint(min_val, max_val))
        method, temp_code, input_data = "sendMessage", "2", {"is_mute":False,"object_guid":guid,"rnd": int(rnd(100000, 999999)),"text": text}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
    
    def joinChannelAction(self, guid: str):
        method, temp_code, input_data = "joinChannelAction", "2", {"action": "Join", "channel_guid": guid}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
    
    def joinGroupByLink(self, hash_link: str):
        method, temp_code, input_data = "groupPreviewByJoinLink", "2", {"hash_link": hash_link}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
    
    def leaveGroup(self, guid: str):
        method, temp_code, input_data = "leaveGroup", "2", {"group_guid": guid}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
        
    def searchGlobalObject(self, text: str, filter_type: list = ['Bot', 'Channel', 'User']):
        '''
            Max Search Channel | 14
        '''
        method, temp_code, input_data = "searchGlobalObjects", "2", {"filter_types": filter_type, "search_text": text}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
    
    def getLinkFromAppUrl(self, app_link: str):
        method, temp_code, input_data = "getLinkFromAppUrl", "2", {"app_url": app_link}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
    
    def forwardMessages(self, from_guid: str, send_guid: str, message_ids: list):
        rnd = lambda min_val, max_val: str(random.randint(min_val, max_val))
        method, temp_code, input_data = "forwardMessages", "2", {"from_object_guid": from_guid, "to_object_guid": send_guid, "message_ids":message_ids, "rnd": int(rnd(100000, 999999))}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
    
    def getChats(self):
        method, temp_code, input_data = "getChats", "2", {}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
     
    def getMessages(self, object_guid: str, max_id: str, sort: str = "FromMax"):
        method, temp_code, input_data = "getMessages", "2", {"object_guid": object_guid, "sort": sort, "max_id": max_id}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
    
    def getMessagesByID(self, message_ids: list, object_guid: str):
        method, temp_code, input_data = "getMessagesByID", "2", {"message_ids": message_ids, "object_guid": object_guid}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
    
    def seenChats(self, seen_list: dict = {'object_guid':"message_id"}):
        method, temp_code, input_data = "seenChats", "2", {"seen_list": seen_list}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)
    
    def getChannelInfo(self, guid_channel: str):
        method, temp_code, input_data = "getChannelInfo", "2", {"channel_guid": guid_channel}
        return self.send_post(method=method, temp_code=temp_code, data=input_data)