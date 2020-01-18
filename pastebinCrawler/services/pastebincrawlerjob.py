from lxml import html
from model.pastebinconsts import PastebinConsts
from services.file_html_downloader import FileHtmlDownloader, HtmlPageService
from services.normalizers.normalizer import DataNormalizerRunner
from services.pastebindbservice import PastebinDBService
from services.pastebinhtmldataparser import PastebinHtmlDataParser


class JobHandler(object):
    def do_job(self):
        pass


class PastebinCrawlerJob(JobHandler):
    def __init__(self, html_page_service: HtmlPageService,
                 pastebin_html_data_parser: PastebinHtmlDataParser,
                 pastebin_db_service: PastebinDBService,
                 pastebin_data_normalizer_runner: DataNormalizerRunner
                 ):
        self.pastebin_data_normalizer_runner = pastebin_data_normalizer_runner
        self.pastebin_db_service = pastebin_db_service
        self.pastebin_html_data_parser = pastebin_html_data_parser
        self.html_page_service = html_page_service
        self.file_downloader = FileHtmlDownloader()

    def do_job(self):
        self._analyze_pastebin_data()

    def _analyze_pastebin_data(self):
        # 1. read last pastebin data from start page
        latest_pastebin_links = self._analyze_archive_page()
        # latest_pastebin_links = ['/aSsWCpWY']

        latest_pastebin_links = \
            self.remove_existing_pastes(latest_pastebin_links)

        # 2. download and analyze each paste_bin page
        # Download data
        url_per_html_map = \
            self.file_downloader \
                .download_pastebin_pages_parallel(latest_pastebin_links)

        # Analyze data
        pastebins = self._analyze_pastebin_page(url_per_html_map)

        # 3. save paste bin data in db
        self.pastebin_db_service.add_bulk(pastebin_data_list=pastebins)

    def remove_existing_pastes(self, latest_pastebin_links):
        existing_data = \
            self.pastebin_db_service.get_existing_ids(latest_pastebin_links)
        if len(existing_data) > 0:
            ids = {x['id'] for x in existing_data}
            found_data = set(latest_pastebin_links)
            found_data = found_data - ids
            latest_pastebin_links = list(found_data)

        return latest_pastebin_links

    def _analyze_pastebin_page(self, url_per_html_map):
        pastebins = list()
        for url, pastebin_page_html in url_per_html_map.items():
            pastebin_data = \
                self._analyze_pastebin_content(pastebin_page_html)
            self.pastebin_data_normalizer_runner.normalize_data(pastebin_data)
            pastebins.append({"id": url, "data": pastebin_data})

            print(
                f"url: {url }"
                f" title:{pastebin_data['title']} "
                f" author:{pastebin_data['author']}"
                f" date:{pastebin_data['date']}"
            )

        return pastebins

    def _analyze_archive_page(self):
        """
        gets all the links in the archive page
        :return:
        """
        main_page_data: str = \
            self.html_page_service.get_page_data(url=PastebinConsts.start_page)
        latest_pastebin_links: [str] \
            = self.pastebin_html_data_parser.get_archive_page_links(
            archive_pastebin_page=main_page_data)
        return latest_pastebin_links

    def _analyze_pastebin_content(self, page_data):
        """
        gets paste bin html page and returns its content
        :param page_data:
        :return:
        """

        html_data = html.fromstring(page_data)

        # 1. getting title
        title = self.pastebin_html_data_parser.get_title(html_data)

        # 2. getting author
        author = self.pastebin_html_data_parser.get_author(html_data)

        # 3. getting date
        date = self.pastebin_html_data_parser.get_date(html_data)

        # 4. getting content
        content = self.pastebin_html_data_parser.get_content(html_data)

        return self._pastebin_data_to_dict(author, content, date, title)

    def _pastebin_data_to_dict(self, author, content, date, title):
        return {"author": author,
                "title": title,
                "date": date,
                "content": content}
