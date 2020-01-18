from lxml import html
from lxml.html import HtmlElement

from model.pastebinconsts import PastebinConsts


class PastebinHtmlDataParser(object):
    def get_content(self, html_data):
        content_find = html_data.find_class("paste_code")
        content = content_find[0].value
        return content

    def get_date(self, html_data):
        find_class = html_data.find_class("paste_box_line2")
        date = [x for x in find_class[0] if x.tag == "span"][0].values()[0]
        return date

    def get_author(self, html_data):
        find_class = html_data.find_class("paste_box_line2")
        author = \
            next(iter(x for x in find_class[0].iterlinks()
                      if x[0].tag == 'a'), "")
        result = ""
        if author != "" and isinstance(author[0], HtmlElement):
            result = str(author[0].text)

        return result

    def get_title(self, html_data):
        find_class = html_data.find_class("paste_box_line1")
        title = list(find_class)[0].text_content()
        return title

    def get_archive_page_links(self, archive_pastebin_page):
        main_page_data = archive_pastebin_page
        # todo make a better tree walk with some css selector if possible
        html_data = html.fromstring(main_page_data)
        find_class = html_data.find_class(PastebinConsts.main_table)
        all_rows = [x for x in find_class[0] if x.tag == "tr"]
        all_columns = [list(x) for x in all_rows]
        all_links = [list(x[0])[1] for x in all_columns if x[0].tag == "td"]
        all_pages_links = list(list(x.iterlinks())[0][2] for x in all_links)
        # todo filter out all links that are older than 2 minutes
        return all_pages_links
