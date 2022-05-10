#!/usr/bin/env python3
from asyncio import run
from argparse import ArgumentParser
from dataclasses import dataclass
from os import SEEK_END

from aiofiles import open as aio_open

CLI = ArgumentParser()
CLI.add_argument('file', nargs=1)
CLI.add_argument('-n', default=2, type=int)
CLI.add_argument('--chunk-size', default=256, type=int)


@dataclass
class Conf:
    filename: str
    chunk_size: int = 256
    lines_count: int = 2
    encoding: str = 'utf8'


async def seek_backwards(conf: Conf):
    async with aio_open(conf.filename, mode='r', encoding=conf.encoding) as f:
        index = 0
        cursor = 0
        offset = 0
        lines_count = conf.lines_count

        await f.seek(0, SEEK_END)  # Move to the end.
        file_size = remaining_size = await f.tell()

        first_line = True
        while remaining_size > 0 and lines_count > 0:
            offset = min(file_size, offset + conf.chunk_size)
            cursor = file_size - offset

            await f.seek(cursor)
            buffer = await f.read(min(remaining_size, conf.chunk_size))

            remaining_size -= conf.chunk_size

            while buffer and lines_count > 0:
                try:
                    index = buffer.rindex('\n') + 1
                except ValueError:
                    index = None

                if index is None:
                    buffer = ''
                    continue

                if not first_line:
                    lines_count -= 1

                first_line = False
                buffer = buffer[:index - 1]

    return cursor + (index or 0)


async def readfile(conf: Conf, start):
    async with aio_open(conf.filename, mode='r', encoding=conf.encoding) as f:
        await f.seek(start)
        async for line in f:
            print(line.strip())


async def main(args):
    if args.n <= 0:
        raise RuntimeError('-n should be greater than 0.')

    conf = Conf(args.file[0], args.chunk_size, args.n)
    start = await seek_backwards(conf)
    await readfile(conf, start)


if __name__ == '__main__':
    run(main(CLI.parse_args()))
