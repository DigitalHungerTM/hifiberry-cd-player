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
    list audio files in a folder
    path: path of folder
    return: list of song names
    """
    songs = sorted(
        [f for f in listdir(path)
            if isfile(join(path, f))
            and f.split(".")[-1] in AUDIO_FILE_TYPES]
    )
    return songs


def play_album(album: str, client):
    """
    uses the mpd socket to play specified `album`
    album: the album to be played
    client: an MPDClient object
    return: 0 for fail, 1 for succes
    """
    # connect the client
    client.connect(LOCAL_MPD_SOCKET) # defaults to port 6600 if none is provided
    client.clear() # clear current queue
    # add songs to queue
    album_path = ALBUMS_PATH + album + "/"
    songs = get_songs_in_folder(album_path)
    for song in songs:
        client.add(album_path + song)

    # turn on play
    client.play()

    # disconnect client
    client.close()
    client.disconnect()


def main():
    print("not meant to be run directly")
    print("please import the functions in this file to another script")
    exit(-1)


if __name__ == "__main__":
    main()
