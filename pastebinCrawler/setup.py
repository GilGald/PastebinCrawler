from services.normalizers.normalizer import TitleNormalizer, \
    AuthorNormalizer, \
    DateNormalizer, \
    ContentNormalizer
from services.pastebincrawlerjob import PastebinCrawlerJob, \
    HtmlPageService, DataNormalizerRunner
from services.pastebindbservice import PastebinDBService
from services.pastebinhtmldataparser import PastebinHtmlDataParser
import schedule
import time

if __name__ == "__main__":
    normalizers = [TitleNormalizer(),
                   AuthorNormalizer(),
                   DateNormalizer(),
                   ContentNormalizer()]
    db_service = PastebinDBService()

    pastebin_crawler = PastebinCrawlerJob(HtmlPageService(),
                                          PastebinHtmlDataParser(),
                                          db_service,
                                          DataNormalizerRunner(normalizers))

    pastebin_crawler.do_job()

    #
    schedule.every(2).minutes.do(pastebin_crawler.do_job)
    # schedule.every(20).seconds.do(pastebin_crawler.do_job)

    while 1:
        schedule.run_pending()
        time.sleep(1)
