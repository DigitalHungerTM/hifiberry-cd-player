from mpd import MPDClient
from os import listdir
from os.path import isfile, join

# set constants
LOCAL_MPD_SOCKET = "/var/run/mpd/socket"

NAS_FOLDER = "undefined-vault-K70iu/"
ALBUMS_PATH = "/data/library/" + NAS_FOLDER
ALBUM_NAME = "Hyperspace"
FINAL_ALBUM_PATH = ALBUMS_PATH + ALBUM_NAME + "/"

AUDIO_FILE_TYPES = ["m4a", "wav", "flac", "mp3", "mp4", "wma", "aac", "ogg", "alac", "pcm", "aiff"]


def get_songs_in_folder(path: str) -> list[str]:
    """
    list files ending in .flac in a folder
    path: path of folder
    return: list of song names
    """
    songs = sorted(
        [f for f in listdir(path)
            if isfile(join(path, f))
            and f.split(".")[-1] in AUDIO_FILE_TYPES]
    )
    return songs

def main():
    # set up connection with mpd socket
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None
    client.connect(LOCAL_MPD_SOCKET) # defaults to port 6600 if none is provided
    client.clear() # clear current queue
    # print(client.mpd_version)
    # print(client.find("album", "Hyperspace")) # find example
    
    # add songs to queue
    songs = get_songs_in_folder(FINAL_ALBUM_PATH)
    for song in songs:
        client.add(FINAL_ALBUM_PATH + song)

    # turn on play
    client.play()
    
    # disconnect the client
    client.close()
    client.disconnect()


if __name__ == "__main__":
    main()
