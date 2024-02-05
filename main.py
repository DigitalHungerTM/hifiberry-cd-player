from mpd import MPDClient
import mpd_funcs

INTERVAL = 5


def main():
    # set up MPD client
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None

    # main loop
    try:
        while True:
            # if album name is set and album name is not last album name
            #     play new album
            # else
            #     sleep for a certain interval
            pass
    
    except KeyboardInterrupt:
        print("exiting")
        raise


if __name__ == "__main__":
    main()
