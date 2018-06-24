from bs4 import BeautifulSoup
import requests
import time,html5lib,xlwt
import os

class lp_inf():
    name = ''
    loction = ''
    area = ''
    lp_type = ''
    avg_price = ''
    total_price=''
    sale_status = ''

def str_wipe(string):
    return string.replace(' ','').replace('\n','')
    
def get_loupan(loupans,worksheet,row):
    lp  = lp_inf()
    for loupan in loupans:
        lp.name = str_wipe(loupan.select('.name')[0].text.split('/')[0] )  #解析出楼盘名称
        lp.location = str_wipe(loupan.select('.resblock-location')[0].text.split('/')[0])    #解析出楼盘地址
      
        lp.area = str_wipe(loupan.select('.resblock-area')[0].text)
        lp.lp_type = str_wipe(loupan.select('.resblock-type')[0].text)
        lp.avg_price = str_wipe(loupan.select('.main-price')[0].text.split('/')[0])  #获取价格，去除字符串中的空格和换行符
        if(len(loupan.select('.second')) > 0):
            lp.total_price = str_wipe(loupan.select('.second')[0].text)
        
        lp.sale_status = str_wipe(loupan.select('.sale-status')[0].text)

        worksheet.write(row,0,lp.name)
        worksheet.write(row,1,lp.avg_price)
        worksheet.write(row,2,lp.total_price)
        worksheet.write(row,3,lp.area)
        worksheet.write(row,4,lp.lp_type)
        worksheet.write(row,5,lp.sale_status)
        worksheet.write(row,6,lp.location)
        row = row +1 
        
def jiexi_loupans(url,worksheet,row): #解析楼盘的网页位置
    wb_data = requests.get(url) #获取网页数据
    soup = BeautifulSoup(wb_data.content,'html5lib')  #解析
    loupans = soup.select('.resblock-list') #解析出楼盘的div块
    get_loupan(loupans,worksheet,row)

if __name__ == '__main__':
    url = 'https://cd.fang.lianjia.com/loupan/pg'
    title = ['楼盘名称','均价','总价','面积','属性','是否在售','地址']
    row = 1
    nowtime = time.time()
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet0',cell_overwrite_ok=True)
    for t in range(len(title)):
        worksheet.write(0,t,title[t])
    for i in range(1):
        print(i+1)
        jiexi_loupans(url+str(i+1),worksheet,row)
        print('done!')
    workbook.save(os.path.abspath('.')+str(int(nowtime))+'.xls')    


