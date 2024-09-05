import asyncio


def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print(f'reader={reader.feed_data()}')
    output = bytes(str('abcdef'))
    writer.write(output)
    print(f'writer={writer.write(output)}')
    pass


async def asyncio_1():
    '''
    exercise 1

    spin up a server
    '''

    server = asyncio.start_server(handler, host="127.0.0.1", port=8888,
                                  limit=1000)

    print(f'{server}')
    pass


asyncio.run(asyncio_1())
