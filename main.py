from mpd import MPDClient
import mpd_funcs
from mfrc522 import SimpleMFRC522
import sys
from time import sleep
from RPi import GPIO
import json

INTERVAL = 1


def main():
    # set up MPD client
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None

    # set up RFID reader
    reader = SimpleMFRC522()

    # load database
    with open("uuid_to_album_name.json", "r") as f:
        database = json.load(f)

    # main loop
    try:
        old_uuid = ""
        while True:
            # scan rfid tag
            print("Hold a tag near the reader")
            uuid, _ = reader.read()
            print("ID: ", uuid)

            # check if tag is new
            if uuid == old_uuid:
                sleep(INTERVAL)
            else: # play new album
                old_uuid = uuid
                album_name = database[str(uuid)]
                if mpd_funcs.play_album(album_name, client):
                    print("playing album", album_name)
                else:
                    print("something went wrong")
                sleep(INTERVAL)

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("exiting")
        raise


if __name__ == "__main__":
    main()
