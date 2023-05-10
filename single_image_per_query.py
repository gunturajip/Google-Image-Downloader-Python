import time
import base64
from io import BytesIO
import re
import os

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

SLEEP_TIME = 0.2

def download_google_images(search_query: str, number_of_images: int) -> str:
    '''Download google images with this function\n
       Takes -> search_query, number_of_images\n
       Returns -> None
    '''
    url = 'https://images.google.com/'

    driver.get(
        url=url
    )

    box = driver.find_element(
        by=By.XPATH,
        value="//textarea[contains(@class,'gLFyf')]"
    )

    box.send_keys(search_query)
    box.send_keys(Keys.ENTER)
    time.sleep(SLEEP_TIME)

    img_results = driver.find_elements(
        by=By.XPATH,
        value="//img[contains(@class,'rg_i Q4LuWd')]"
    )

    total_images = len(img_results)

    print(total_images)

    counter = 0
    # scroll_to_end()
    for image in img_results: 
        if (image.get_attribute('src') is not None):
            my_image = image.get_attribute('src').split('data:image/jpeg;base64,')
            image_name = '_'.join(str.lower(search_query).split())
            file_path = f'{IMAGE_FOLDER}/{tag}/{counter}_{image_name}.jpeg'
            img = Image.open(BytesIO(base64.b64decode(my_image[1])))
            img = img.convert('RGB')
            img.save(file_path, 'JPEG')
            print('Image saved from Base64.')
            return file_path

            # filename = SAVE_FOLDER + 'helmet'+str(counter)+'.jpeg'
            # if(len(my_image) >1): 
            #     with open(filename, 'wb') as f: 
            #         f.write(base64.b64decode(my_image[1]))
            # else: 
            #     print(image.get_attribute('src'))
            #     urllib.request.urlretrieve(image.get_attribute('src'), SAVE_FOLDER + 'helmet'+ str(counter)+'.jpeg')
            counter += 1
        if counter >= total_images:
            print('No more images to download.')
            break
        if counter == number_of_images:
            break


    # count = 0

    # for img_result in img_results:
    #     try:
    #         WebDriverWait(
    #             driver,
    #             15
    #         ).until(
    #             EC.element_to_be_clickable(
    #                 img_result
    #             )
    #         )
    #         img_result.click()
    #         time.sleep(SLEEP_TIME)

    #         actual_img = driver.find_element(
    #             by=By.XPATH,
    #             value="//img[contains(@class,'r48jcc pT0Scc iPVvYb')]"
    #         )

    #         src = ''

    #         print(actual_img)

            # for actual_img in actual_imgs:
            #     if 'https://encrypted' in actual_img.get_attribute('src'):
            #         pass
            #     elif 'http' in actual_img.get_attribute('src'):
            #         src += actual_img.get_attribute('src')
            #         break
            #     else:
            #         pass

            # for actual_img in actual_imgs:
            #     if src == '' and 'base' in actual_img.get_attribute('src'):
            #         src += actual_img.get_attribute('src')

            # if 'https://' in src:
            #     image_name = search_query.replace('/', ' ')
            #     image_name = re.sub(pattern=" ", repl="_", string=image_name)
            #     file_path = f'{IMAGE_FOLDER}/{count}_{image_name}.jpeg'
            #     try:
            #         result = requests.get(src, allow_redirects=True, timeout=10)
            #         open(file_path, 'wb').write(result.content)
            #         img = Image.open(file_path)
            #         img = img.convert('RGB')
            #         img.save(file_path, 'JPEG')
            #         print('Image saved from https.')
            #         return file_path
            #     except:
            #         print('Bad image.')
            #         try:
            #             os.unlink(file_path)
            #         except:
            #             pass
            #         count -= 1
            # else:
            #     img_data = src.split(',')
            #     image_name = search_query.replace('/', ' ')
            #     image_name = re.sub(pattern=" ", repl="_", string=image_name)
            #     file_path = f'{IMAGE_FOLDER}/{count}_{image_name}.jpeg'
            #     try:
            #         img = Image.open(BytesIO(base64.b64decode(img_data[1])))
            #         img = img.convert('RGB')
            #         img.save(file_path, 'JPEG')
            #         print('Image saved from Base64.')
            #         return file_path
            #     except:
            #         print('Bad image.')
            #         count -= 1
        # except ElementClickInterceptedException as e:
        #     count -= 1
        #     print(e)
        #     print('Image is not clickable.')
        #     driver.quit()

        # count += 1
        # if count >= total_images:
        #     print('No more images to download.')
        #     break
        # if count == number_of_images:
        #     break

tags = [
    'Elon Musk',
    'Tim Cook',
    'Sundar Pichai',
    'Steve Jobs'
]

for tag in tags:
    cwd = os.getcwd()
    IMAGE_SUBFOLDER = tag
    os.makedirs(
        name=f'{cwd}/{IMAGE_FOLDER}/{IMAGE_SUBFOLDER}',
        exist_ok=True
    )
    file_path = download_google_images(
        tag,
        1
    )
    print(file_path)

driver.quit()