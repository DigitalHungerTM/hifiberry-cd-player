from mpd import MPDClient
import mpd_funcs
import rfid_reader.SimpleMFRC522 as SimpleMFRC522
from rfid_reader import SimpleMFRC522
import sys
from time import sleep
from RPi import GPIO
import json

TIMEOUT = 3
INTERVAL = 1

def main():
    # set up MPD client
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None

    # set up RFID reader
    reader = SimpleMFRC522.SimpleMFRC522()

    # load database
    with open("uuid_to_album_name.json", "r") as f:
        database = json.load(f)

    # main loop
    try:
        old_uuid = ""
        playing = True
        while True:
            # scan rfid tag
            print("Hold a tag near the reader")
            uuid = reader.read_id(timeout=TIMEOUT)
            if playing and not uuid: # stop playback
                print("no tag found, stopping playback")
                if mpd_funcs.stop_playback(client):
                    old_uuid = "" # reset old uuid so that album replays when it is placed again
                    playing = False
                    print("stopped playback")
                else:
                    print("something went wrong")

            # check if tag is new
            if not uuid:
                print("no tag found, sleeping")
                sleep(INTERVAL)
            elif uuid != old_uuid: # early exit
                print("new tag detected, playing album")
                playing = True
                old_uuid = uuid
                album_name = database[str(uuid)]
                if mpd_funcs.play_album(album_name, client):
                    print("playing album", album_name)
                else:
                    print("something went wrong")
            else:
                print("same tag as before, album already playing")

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("KeyboardInterrupt")
        exit(0)
    except:
        GPIO.cleanup()
        raise


if __name__ == "__main__":
    main()
