# Code by Simon Monk https://github.com/simonmonk/
# Edited by Mathijs Afman https://github.com/DigitalHungerTM

from . import MFRC522
import RPi.GPIO as GPIO
from time import sleep
  
class SimpleMFRC522:
  
    READER = None
    
    KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
    BLOCK_ADDRS = [8, 9, 10]
    
    def __init__(self):
        self.READER = MFRC522.MFRC522()
    
    def read(self, timeout=300):
        """
        read rfid tag
        :param `timeout`: seconds after which the reader stops trying, defaults to 300
        :return: id and text if found, else None
        """
        id, text = self.read_no_block()
        i = 0
        while not id and i < timeout:
            id, text = self.read_no_block()
            sleep(1)
            i += 1
        return id, text if id else None
  
    def read_id(self, timeout=300):
        """
        read id from rfid tag
        :param `timeout`: seconds after which the reader stops trying, defaults to 300 (5 minutes)
        :return: id if found, else None
        """
        id = self.read_id_no_block()
        i = 0
        while not id and i < timeout:
          id = self.read_id_no_block()
          sleep(1)
          i += 1
        return id if id else None
  
    def read_id_no_block(self):
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None
        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
            return None
        return self.uid_to_num(uid)
    
    def read_no_block(self):
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None, None
        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
            return None, None
        id = self.uid_to_num(uid)
        self.READER.MFRC522_SelectTag(uid)
        status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
        data = []
        text_read = ''
        if status == self.READER.MI_OK:
            for block_num in self.BLOCK_ADDRS:
                block = self.READER.MFRC522_Read(block_num) 
                if block:
                        data += block
            if data:
                 text_read = ''.join(chr(i) for i in data)
        self.READER.MFRC522_StopCrypto1()
        return id, text_read
      
    def write(self, text):
        id, text_in = self.write_no_block(text)
        while not id:
            id, text_in = self.write_no_block(text)
        return id, text_in
  
    def write_no_block(self, text):
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None, None
        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
            return None, None
        id = self.uid_to_num(uid)
        self.READER.MFRC522_SelectTag(uid)
        status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
        self.READER.MFRC522_Read(11)
        if status == self.READER.MI_OK:
            data = bytearray()
            data.extend(bytearray(text.ljust(len(self.BLOCK_ADDRS) * 16).encode('ascii')))
            i = 0
            for block_num in self.BLOCK_ADDRS:
              self.READER.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
              i += 1
        self.READER.MFRC522_StopCrypto1()
        return id, text[0:(len(self.BLOCK_ADDRS) * 16)]
        
    def uid_to_num(self, uid):
        n = 0
        for i in range(0, 5):
            n = n * 256 + uid[i]
        return n
