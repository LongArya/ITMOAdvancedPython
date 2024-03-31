import os
import time
import click
from http import HTTPStatus
import asyncio
import aiohttp
import aiofiles
from pathlib import Path
from pydantic import FilePath, DirectoryPath
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests


IMAGES_URL_SRC = "https://www.thiswaifudoesnotexist.net/"


def download_waifu_image_without_async(output_path: FilePath):
    """Test function"""
    web_page_output = requests.get(IMAGES_URL_SRC)
    web_page_soup_object = BeautifulSoup(web_page_output.text, "html.parser")
    image_src = web_page_soup_object.find_all(name="img")[0].get("src")
    img_url = urljoin(IMAGES_URL_SRC, image_src)
    #
    img_output = requests.get(img_url)
    print(img_output.status_code)
    with open(output_path, "wb") as f:
        f.write(img_output.content)


async def download_waifu_image(output_path: FilePath, session: aiohttp.ClientSession):
    async with session.get(IMAGES_URL_SRC) as download_page_responce:
        if download_page_responce.status != HTTPStatus.OK:
            return
        page_text = await download_page_responce.text()
        download_page_soup_object = BeautifulSoup(page_text, "html.parser")
        image_src = download_page_soup_object.find_all(name="img")[0].get("src")

    img_url = urljoin(IMAGES_URL_SRC, image_src)
    async with session.get(img_url) as image_responce:
        if image_responce.status != HTTPStatus.OK:
            return
        image_bytes = await image_responce.read()
        async with aiofiles.open(output_path, "wb") as f:
            await f.write(image_bytes)


async def async_downloader(num_files: int, output_dir: DirectoryPath):
    async with aiohttp.ClientSession() as session:
        for file_num in range(num_files):
            await download_waifu_image(
                output_dir / f"async_download_{file_num}.png", session
            )


@click.command()
@click.option("--files_num", type=int)
@click.option("--output_dir", type=Path)
def run(files_num: int, output_dir: DirectoryPath):
    t1 = time.time()
    os.makedirs(output_dir, exist_ok=True)
    asyncio.run(async_downloader(files_num, output_dir))
    t2 = time.time()
    print(t2 - t1)


def time_sequential():
    t1 = time.time()
    for _ in range(5):
        download_waifu_image_without_async("download.png")
    t2 = time.time()
    print(t2 - t1)


if __name__ == "__main__":
    run()
