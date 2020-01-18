import multiprocessing
import requests as req

from model.pastebinconsts import PastebinConsts


class HtmlPageService(object):
    def get_page_data(self, url):
        resp = req.get(url)
        return resp.content


class FileHtmlDownloader(object):

    def _get_paste_html_data(self, url):
        resp = req.get(url)
        data = resp.content
        return {"url": url, "data": data}

    def download_pastebin_pages_parallel(self, latest_pastebin_links):
        pool = multiprocessing.Pool()
        pastebin_download_urls = [f"{PastebinConsts.base_url}{pastebin_link}"
                                  for pastebin_link in latest_pastebin_links]
        outputs = pool.map(self._get_paste_html_data, pastebin_download_urls)
        pool.close()
        pool.join()
        url_per_html_map = {x["url"]: x["data"] for x in outputs}
        return url_per_html_map
