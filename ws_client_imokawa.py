import asyncio
import websockets
​
is_input_valu =0
​
async def ph(websocket, path):
    while True:
        data = await websocket.recv()
        print(data)
​
        # if is_input_valu ==1:
        input_value = input()
        await websocket.send(input_value)
​
# async def get_input():
    # input_value = input()
    # is_input_valu =1
​
start_server = websockets.serve(ph, '0.0.0.0', 60000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
