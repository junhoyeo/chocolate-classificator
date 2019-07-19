import multiprocessing
from google_images_download import google_images_download


def download(keyword):
    response = google_images_download.googleimagesdownload()
    response.download({
        'keywords': keyword,
        'limit': 10000,
        'chromedriver': './chromedriver'
    })


if __name__ == '__main__':
    keywords = ['dark chocolate', 'white chocolate']
    pool = multiprocessing.Pool(processes=2)
    pool.map(download, keywords)
    pool.close()
    pool.join()
