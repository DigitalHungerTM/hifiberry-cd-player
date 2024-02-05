from mfrc522 import SimpleMFRC522
import sys
from time import sleep
from RPi import GPIO
import json

# relative path
DATABASE_FILENAME = "uuid_to_album_name.json"

def write_to_db(uuid, album_name):
    """
    writes a map of uuid to album name to the database file
    
    :param `uuid`: uuid of the tag
    :param `album_name`: name of the album
    """
    # open database file to read
    with open(DATABASE_FILENAME, "r") as f:
        data = json.load(f)
    data[uuid] = album_name
    # write to database file
    with open(DATABASE_FILENAME, "w") as f:
        json.dump(data, f)


def main():
    # set up RFID reader
    reader = SimpleMFRC522()

    try:
        while True:
            # scan rfid tag
            print("Hold a tag near the reader")
            uuid, _ = reader.read()
            print("ID: ", uuid)
            album_name = input("Enter the album name:\n")
            write_to_db(uuid, album_name)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("exiting")
        raise


if __name__ == "__main__":
    main()
