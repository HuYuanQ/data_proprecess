# coding:utf-8
import datetime
import pandas as pd
import requests
from lxml import etree


class CarSalesInfo:
    def __init__(self,current_date):
        self.basic_url = 'https://xl.16888.com/style-201101-' + current_date + '-'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}
        self.rank_total_num = 0

    # 发送url请求，timeout为15秒
    def parse_url(self,url):
        response = requests.get(url,headers=self.headers,timeout=15) # 发送请求
        content = response.text  # 获取html内容
        html = etree.HTML(content)  # 分析html内容，返回DOM根节点
        return html


    def get_data(self,page_num):
        url = self.basic_url + str(page_num) +'.html'
        html = self.parse_url(url)
        if page_num == 1:
            html = self.parse_url(url)
            self.rank_total_num = html.xpath('/html/body/div[5]/div[3]/div[2]/div/div[2]/div[2]/div[1]/div/a[6]//text()')
        result_list = html.xpath('/html/body/div[5]/div[3]/div[2]/div/div[2]/div[1]/table/tr')
        for i in result_list[0:1]:  # 遍历tr列表
            title1 = i.xpath(".//th[1]//text()")
            title2 = i.xpath(".//th[2]//text()")
            title3 = i.xpath(".//th[3]//text()")
            title4 = i.xpath(".//th[4]//text()")
            title5 = i.xpath(".//th[5]//text()")
        for i in enumerate(result_list[1:]):  # 遍历tr列表
            value1 = i[1].xpath(".//td[1]//text()")
            value2 = i[1].xpath(".//td[2]//text()") if len(i[1].xpath(".//td[2]//text()"))!=0 else [None]
            value3 = i[1].xpath(".//td[3]//text()") if len(i[1].xpath(".//td[2]//text()"))!=0 else [None]
            value4 = i[1].xpath(".//td[4]//text()") if len(i[1].xpath(".//td[2]//text()"))!=0 else [None]
            value5 = i[1].xpath(".//td[5]//text()") if len(i[1].xpath(".//td[2]//text()"))!=0 else [None]
            value6 = i[1].xpath(".//td[6]/div/a[1]/@href")
            car_sales_log_url = 'https://xl.16888.com' + value6[0]
            if value2 is not None:
                log_url_list = {
                    title1[0]: value1,
                    title2[0]: value2,
                    title3[0]: value3,
                    title4[0]: value4,
                    title5[0]: value5,
                    '历史销量url': [car_sales_log_url]}
                log = pd.DataFrame(log_url_list)
            if page_num == 1 and i[0] == 0:
                log.to_csv("car_sales_log_url3.csv", mode='a', header=True, encoding="utf-8", index=False)
            else:
                log.to_csv("car_sales_log_url3.csv", mode='a', header=False, encoding="utf-8", index=False)
            with open("car_rank_result.txt", "a+") as f:
                f.write(str(log_url_list))
                f.write("\n")
        if page_num < int(self.rank_total_num[0]):
            page_num += 1
            self.get_data(page_num)


    def run(self,page_num):
        self.get_data(page_num)

if __name__ == '__main__':
    current_date = datetime.datetime.now().strftime("%Y%m")
    carsales = CarSalesInfo(current_date)
    carsales.run(1)