from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

# Configure Firefox options for headless mode
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('-headless')

#driver = webdriver.Firefox()
driver = webdriver.Firefox(options=firefox_options)
driver.get("https://topmovies.actor/")

def search_movie(movie_name):
    search_field = driver.find_element(By.ID, 's')
    search_field.clear()
    search_field.send_keys(movie_name)
    search_field.send_keys(Keys.RETURN)

def print_movie_list(link_elements):
    i = 1
    for link_element in link_elements:
        print(i,link_element.text)
        i = i + 1
    movie_index = int(input("Select Index"))
    return movie_index

def select_movie():
    link_elements = driver.find_elements(By.CSS_SELECTOR, '#content_box article a')
    i  = print_movie_list(link_elements)
    time.sleep(2)
    driver.get(link_elements[i].get_attribute('href'))

def download_movie():
    article_element = driver.find_element(By.CSS_SELECTOR, 'article.article')

    download_links = article_element.find_elements(By.CSS_SELECTOR, 'a.maxbutton-1.maxbutton.maxbutton-download-links')

    if download_links:
        first_link = download_links[0]
        driver.get(first_link.get_attribute('href'))
    else:
        print("No download links found.")

def bypass():
    #Fast Server
    try:
        link_element = driver.find_element(By.CLASS_NAME,"maxbutton-5")
        driver.get(link_element.get_attribute('href'))
    except Exception as e:
        print("An error occurred:", e)

    #Start Verfication
    try:
        js_script = "document.querySelector('a[onclick*=\"document.getElementById(\\'landing\\').submit()\"]').click();"
        driver.execute_script(js_script)

    except Exception as e:
        print("An error occurred:", e)

    time.sleep(5)

    try:
        js_script = """
                        var linkElement = document.querySelector('a[onclick*="document.getElementById"]');
                        linkElement.click();
                    """

        driver.execute_script(js_script)

    except Exception as e:
        print("An error occurred:", e)

    time.sleep(10)

    try:
        js_script = "document.getElementById('verify_button').click();"
        driver.execute_script(js_script)

    except Exception as e:
        print("An error occurred:", e)

    time.sleep(10)

    try:
        js_script = "return document.getElementById('two_steps_btn').getAttribute('href');"
        href = driver.execute_script(js_script)
        driver.get(href)

    except Exception as e:
        print("An error occurred:", e)


def get_link():
    try:
        button_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'drc')))
        driver.execute_script("arguments[0].click();", button_element)
    except Exception as e:
        print("An error occurred while clicking the button:", e)
    time.sleep(2)

    try:
        input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'form-control')))
        input_text = input_element.get_attribute('value')

        print("Input Text:", input_text)

    except Exception as e:
        print("An error occurred while retrieving input text:", e)

    return input_text


def play_in_vlc(media_link):
    command = f'vlc "{media_link}"'

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def cleanup():
    driver.quit()

try:
    movie_name = input("Enter Movie Name:")
    search_movie(movie_name)
    time.sleep(2)
    select_movie()
    time.sleep(2)
    download_movie()
    time.sleep(6)
    bypass()
    time.sleep(15)
    media_link = get_link()
    time.sleep(15)
    play_in_vlc(media_link)
finally:
    cleanup()
