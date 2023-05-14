import time
import base64
from io import BytesIO
import re
import os
from datetime import datetime as dt

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from PIL import Image

cwd = os.getcwd()
IMAGE_FOLDER = 'download'
os.makedirs(
    name=f'{cwd}/{IMAGE_FOLDER}',
    exist_ok=True
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service
)

SLEEP_TIME = 1

def scroll_to_bottom():
    '''Scroll to the bottom of the page
    '''
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(SLEEP_TIME)

        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            element = driver.find_element(
                by=By.CSS_SELECTOR,
                value='.YstHxe input'
            )
            element.click()
            time.sleep(SLEEP_TIME)
        except:
            pass

        if new_height == last_height:
            break

        last_height = new_height

# def download_google_images(search_query: str, number_of_images: int) -> str:
#     '''Download google images with this function\n
#        Takes -> search_query, number_of_images\n
#        Returns -> None
#     '''
#     url = 'https://images.google.com/'

#     driver.get(
#         url=url
#     )

#     box = driver.find_element(
#         by=By.XPATH,
#         value="//textarea[contains(@class,'gLFyf')]"
#     )

#     box.send_keys(search_query)
#     box.send_keys(Keys.ENTER)
#     time.sleep(SLEEP_TIME)

#     scroll_to_bottom()
#     time.sleep(SLEEP_TIME)

#     img_results = driver.find_elements(
#         by=By.XPATH,
#         value="//img[contains(@class,'rg_i Q4LuWd')]"
#     )

#     total_images = len(img_results)

#     print(total_images)

#     counter = 0

#     for image in img_results:
#         if image.get_attribute('src') is not None:
#             my_image = image.get_attribute('src').split('data:image/jpeg;base64,')
#             image_name = str.lower(search_query.split()[-1])
#             file_path = f'{IMAGE_FOLDER}/{tag}/{counter}_{image_name}.jpeg'
#             try:
#                 img = Image.open(BytesIO(base64.b64decode(my_image[1])))
#                 img = img.convert('RGB')
#                 img.save(file_path, 'JPEG')
#                 print('Image saved from Base64.')
#                 counter += 1
#                 time.sleep(SLEEP_TIME)
#             except:
#                 continue

#         if counter == number_of_images:  # Move the condition here
#             break

#     if counter < number_of_images:
#         print('Only', counter, 'images downloaded.')
#     else:
#         print('All', number_of_images, 'images downloaded.')

def get_images_from_google(tag, max_images):
    url = 'https://images.google.com/'

    driver.get(
        url=url
    )

    box = driver.find_element(
        by=By.XPATH,
        value="//textarea[contains(@class,'gLFyf')]"
    )

    box.send_keys(tag)
    box.send_keys(Keys.ENTER)
    time.sleep(SLEEP_TIME)

    scroll_to_bottom()
    time.sleep(SLEEP_TIME)

    img_results = driver.find_elements(
        by=By.XPATH,
        value="//img[contains(@class,'rg_i Q4LuWd')]"
    )

    print(len(img_results))

    image_urls = set()
    counter = 0

    for image in img_results:
        if image.get_attribute('src') is not None:
            try:
                image.click()
                time.sleep(SLEEP_TIME)
            except:
                continue

            # r48jcc pT0Scc iPVvYb
            images = driver.find_elements(
                by=By.XPATH,
                value="//img[contains(@class,'r48jcc pT0Scc iPVvYb')]"
            )
            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(len(image_urls))
                    counter += 1

        if counter == max_images:  # Move the condition here
            break

    if counter < max_images:
        print('Only', counter, 'images downloaded.')
    else:
        print('All', max_images, 'images downloaded.')

    return image_urls

def download_image(tag, url, file_path, image_type='JPEG', verbose=True):
    success = False
    try:
        time = dt.now()
        curr_time = time.strftime('%H:%M:%S')
        #Content of the image will be a url
        img_content = requests.get(url).content
        #Get the bytes IO of the image
        img_file = BytesIO(img_content)
        #Stores the file in memory and convert to image file using Pillow
        image = Image.open(img_file)

        with open(file_path, 'wb') as file:
            image.save(file, image_type)

        if verbose == True:
            print(f'The image: {file_path} downloaded successfully at {curr_time}.')
        success = True
    except Exception as e:
        print(f'Unable to download image from Google Images due to\n: {str(e)}')
    return success

tags = [
    # 'Alat Musik Bonang',
    # 'Alat Musik Rebab',
    # 'Alat Musik Saluang',
    # 'Alat Musik Burdah',
    # 'Alat Musik Sasando',
    # 'Alat Musik Sape',
    # 'Alat Musik Talindo',
    # 'Alat Musik Kolintang',
    # 'Alat Musik Tifa',
    # 'Alat Musik Yi'
]

for tag in tags:
    IMAGE_SUBFOLDER = tag.split()[-1]
    cwd = os.getcwd()
    os.makedirs(
        name=f'{cwd}/{IMAGE_FOLDER}/{IMAGE_SUBFOLDER}',
        exist_ok=True
    )

    urls = get_images_from_google(
        tag=tag,
        max_images=200
    )

    counter = 0
    for url in urls:
        image_name = str.lower(IMAGE_SUBFOLDER)
        file_path = f'{IMAGE_FOLDER}/{IMAGE_SUBFOLDER}/{counter}_{image_name}.jpg'
        success = download_image(
            tag=tag,
            url=url,
            file_path=file_path,
            verbose=True
        )
        if success:
            counter += 1

driver.quit()