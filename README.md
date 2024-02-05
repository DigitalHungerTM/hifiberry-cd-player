# HiFiBerry cd player

Scan RFID tag in a cd case to play its album, that is stored on a network share.

## TODO

- buy hifiberry dac
- make case
- add run at boot entry

## Installation

```bash
# install / update pip
python3 -m pip install --upgrade pip

# install packages
pip3 install setuptools wheel spidev

# clone the repo
git clone https://github.com/DigitalHungerTM/hifiberry-cd-player.git

# run the rfid reader
cd hifiberry-cd-player
python3 main.py

# run the rfid database writer
python3 writer.py

# add run at boot entry
```
