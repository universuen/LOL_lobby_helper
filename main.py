from lcu_driver import Connector

connector = Connector()


async def get_summoner_info(connection):
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    if summoner.status == 200:
        data = await summoner.json()
        print('Summoner Info:')
        print(f'\tID: {data["displayName"]}')
        print(f'\tlevel: {data["summonerLevel"]}')
    else:
        print('Please login into your account and restart the script...')


async def creat_lobby(connection):
    custom = {
        "customGameLobby": {
            "configuration": {
                "gameMode": "PRACTICETOOL",
                "gameMutator": "",
                "gameServerRegion": "",
                "mapId": 11,
                "mutators": {"id": 1},
                "spectatorPolicy": "AllAllowed",
                "teamSize": 5
            },
            "lobbyName": "TEST",
            "lobbyPassword": ""
        },
        "isCustom": True
    }

    lobby = await connection.request('post', '/lol-lobby/v2/lobby', data=custom)

    if lobby.status == 200:
        print(f'[创建5V5训练模式] 已成功创建 训练房间')


# fired when LCU API is ready to be used
@connector.ready
async def connect(connection):
    await get_summoner_info(connection)
    await creat_lobby(connection)


# fired when League Client is closed (or disconnected from websocket)
@connector.close
async def disconnect(_):
    print('The client have been closed!')


# starts the connector
connector.start()
