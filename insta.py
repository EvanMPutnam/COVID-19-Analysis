import os
import time
import shutil

location = "212928653"

def delete_images(delete_items = True):
    if not os.path.exists('json_files/'):
        os.mkdir('json_files/')
    for root, dirs, files in os.walk(location):
        for fle in files:
            if '.json' in fle:
                seconds = str(time.time())
                shutil.copy2(os.path.join(root, fle), 'json_files/' + seconds + '.json')
            try:
                if delete_items:
                    os.remove(os.path.join(root, fle))
            except Exception as e:
                print (e)


def scrape():
    os.system('instagram-scraper --location ' + location + ' --maximum 1 --retry-forever --media-metadata --latest-stamps time')
    delete_images(delete_items = True)
    while True:
        os.system('instagram-scraper --location ' + location + ' --maximum 100 --retry-forever --media-metadata --latest-stamps time')
        print ('Deleting')
        delete_images(delete_items = True)


if __name__ == "__main__":
    scrape()

