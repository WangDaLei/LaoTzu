import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from bank_spider.items import OpenMarkOperationUrlItem, \
                                OpenMarkOperationMLFItem, \
                                OpenMarkOperationReverseRepoItem
from bank_operation.models import OpenMarkOperationUrl

bank_url = "http://www.pbc.gov.cn"

class UrlSpider(scrapy.Spider):
    name = "url_spider"
    all_url = []

    def start_requests(self):
        url_objs = OpenMarkOperationUrl.objects.all()
        for url_obj in url_objs:
            self.all_url.append(url_obj.url)
        for i in range(3):
            url = "http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125431/125475/17081/index%s.html"%(i+1)
            yield SplashRequest(url, self.parse, args={'wait': 3})

    def parse(self, response):
        sel = Selector(response)
        urls_list = sel.xpath('//a[re:test(@href, "125475/\d")]/@href').extract()
        for url_line in urls_list:
            if bank_url + url_line not in self.all_url:
                item = OpenMarkOperationUrlItem()
                item['url'] = bank_url + url_line
                yield item

class OperationSpider(scrapy.Spider):
    name = "operation_spider"
    all_url = []

    def start_requests(self):
        url_objs = OpenMarkOperationUrl.objects.filter(processed=False)
        for url_obj in url_objs:
            self.all_url.append(url_obj.url)
            url_obj.processed = True
            url_obj.save()
        for url in self.all_url:
            yield SplashRequest(url.strip(), self.parse, args={'wait': 3})

    def parse(self, response):
        sel = Selector(response)
        dates = sel.xpath(u'//tbody/tr/td/span[re:test(@id, "shijian")]//text()').extract()
        orders = sel.xpath(u'//title[contains(./text(), "公开市场")]/text()').extract()
        out_rerepo = ""
        out_mlf = ""
        for bankorder in orders:
            year = str(bankorder).strip().split(']')[0].split('[')[-1]
            order = str(bankorder).strip().split(u'号')[0].split(u'第')[-1]
            out_rerepo = (str(year)+" "+str(order)+" "+str(dates[0]).strip().split(' ')[0]+" ")
            out_mlf = (str(year)+" "+str(order)+" "+str(dates[0]).strip().split(' ')[0]+" ")

        urls_list = sel.xpath(u'//table/tbody/tr/td/div/p[re:test(.//text(), "逆回购操作情况")]/following-sibling::*[2]/tbody/tr/td[re:test(.//text(), "期限")]/parent::*/following-sibling::*//text()').extract()
        # urls_list = sel.xpath(u'//table/tbody/tr/td/div/p[re:test(.//b/span/text(), "逆回购操作情况")]//following-sibling::*[1]/table/tbody/tr/td[re:test(.//span//text(), "期限")]/parent::*/following-sibling::*//text()').extract()
        for url_line in urls_list:
            out_rerepo += str(url_line).strip()

        MLFStr = ""
        urls_list = sel.xpath(u'//table/tbody/tr/td/div/p[re:test(.//text(), "MLF")]//text()').extract()
        for url_line in urls_list:
            MLFStr += str(url_line).strip()

        if "MLF操作情况" in MLFStr:
            urls_list = sel.xpath(u'//table/tbody/tr/td/div/p[re:test(.//text(), "MLF")]/following-sibling::*[2]/tbody/tr/td[re:test(.//text(), "期限")]/parent::*/following-sibling::*//text()').extract()
            for url_line in urls_list:
                out_mlf += str(url_line).strip()
        for item in self.process_rerepo(out_rerepo):
            yield item
        for item in  self.process_mlf(out_mlf):
            yield item

    def process_rerepo(self, string):
        if len(string.strip().split(' ')) == 3:
            return
        else:
            temp_str = ""
            for i in range(len(string)):
                temp_str += string[i]
                if string[i] == '%':
                    temp_str += " "
            temp_set = temp_str.strip().split(' ')
            year = temp_set[0]
            order = temp_set[1]
            date = temp_set[2]
            count = (len(temp_set)-3)
            for i in range(count):
                ut = temp_set[(i+3)]
                unit = ''
                if ut.find("天") != -1:
                    num = ut.split(u'天')[0]
                    temp = ut.split(u'天')[1]
                    unit = "天"
                elif ut.find("月") != -1:
                    if ut.find("个月") != -1:                       
                        num = ut.split(u'个月')[0]
                        temp = ut.split(u'个月')[1]
                        unit = "月"
                    else:
                        num = ut.split(u'月')[0]
                        temp = ut.split(u'月')[1]
                        unit = "月"
                elif ut.find("年") != -1:
                    num = ut.split(u'年')[0]
                    temp = ut.split(u'年')[1]
                    unit = "年"
                else:
                    print("error")
                    return
                print(unit)
                money = temp.split(u"亿元")[0]
                inter = temp.split(u"亿元")[1].split("%")[0]
                item = OpenMarkOperationReverseRepoItem()
                item['date'] = date
                item['order'] = order
                item['money'] = money
                item['intereset'] = inter
                item['duration'] = num
                item['duration_unit'] = unit
                yield item

    def process_mlf(self, string):
        if len(string.strip().split(' ')) == 3:
            return
        else:
            temp_str = ""
            for i in range(len(string)):
                temp_str += string[i]
                if string[i] == '%':
                    temp_str += " "
            temp_set = temp_str.strip().split(' ')
            year = temp_set[0]
            order = temp_set[1]
            date = temp_set[2]
            count = (len(temp_set)-3)
            for i in range(count):
                ut = temp_set[(i+3)]
                unit = ''
                if ut.find("天") != -1:
                    num = ut.split(u'天')[0]
                    temp = ut.split(u'天')[1]
                    unit = "天"
                elif ut.find("月") != -1:
                    if ut.find("个月") != -1:                       
                        num = ut.split(u'个月')[0]
                        temp = ut.split(u'个月')[1]
                        unit = "月"
                    else:
                        num = ut.split(u'月')[0]
                        temp = ut.split(u'月')[1]
                        unit = "月"
                elif ut.find("年") != -1:
                    num = ut.split(u'年')[0]
                    temp = ut.split(u'年')[1]
                    unit = "年"
                else:
                    print("error")
                    return
                money = temp.split(u"亿元")[0]
                inter = temp.split(u"亿元")[1].split("%")[0]
                item = OpenMarkOperationMLFItem()
                item['date'] = date
                item['order'] = order
                item['money'] = money
                item['intereset'] = inter
                item['duration'] = num
                item['duration_unit'] = unit
                yield item

