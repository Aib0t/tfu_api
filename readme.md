# Transformers Universe API, bundles generator and stuff

## How to use it

- put `./client_config/config.xml` into `%user%/AppData/Local/Jagex Ltd/Transformers Universe/tuclient_Data/config.xml`
- Clone Api repo
- Download cdn files from mega
- Put cdn files into `%api_cloned_dir%/gamecdn
- Launch API
- Launch game

## Info

### Transformers Universe API

"""API""" is a dummy API to pass initial data requests for both standalone client, Web client and to serve gamecdn files.

Code located in `main.py` and is using FastAPI. It servers files from `./gamecnd` directory, it answers to requests I've encountered while getting the game to get to login screen and that's pretty much it.

### Bundles generator

The most important script here is `data_packer.py`. It can rebuild server side bundle files from client cache, by automating `disunity`, which you can grab at https://github.com/ata4/disunity

### Gamecnd rebuilder

Second usefull script is `./gamecdn_rebuilder/gamecnd_rebuilder.py`, which can rebuild proper gamecdn folder structure, by using data from `CAB-_Index`. 

### Client redirection

In order to redirect client to our local server simply put `./client_config/config.xml` into `%user%/AppData/Local/Jagex Ltd/Transformers Universe/tuclient_Data/config.xml`. This will redirect client without any need for additional patching.

### Bundles and Clients

You can grab my rebuilded gamecdn files from https://mega.nz/folder/cYIGmaZD#H4G4FMBUHTgu8dgjLG3F0A, plus unmodified caches I currently have. Additionally, I added a bunch of clients .msi files and a rare .dmg installer for Mac.

### Additional info

- `CAB-_Index` file contains info about each and every file client uses, as well as those files CRC32 hash, versions (gamecdn folder) and so and so. Game won't (50% of time) load files with incorrect CRC32 hash, so in order to force it to load wrong file some editing of Index file is required. Or you can patch hash verification in the binary.
- Game is using uLobby and uLink - 2 deprecated Unity multiplayer libs for actually online portion of the game, starting from login.
- Game is easy to research, thanks to being build with Unity and a lot of symbols left over.

