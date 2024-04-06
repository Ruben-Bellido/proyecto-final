import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import random
import csv

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

bucket_list = ['https://www.amazon.es/HP-15-fd0042ns-Ordenador-port%C3%A1til-Graphics/dp/B0CFBGWVQD/ref=sr_1_4?dib=eyJ2IjoiMSJ9.aoMhGcee8VYmgN3D0U2sTAqtFmpV83m0jdH6lkzhsI6oPWLraNdPXElQ1tFkt8lard6Fj0KKREb4PzAtGwtXQJNRfN9oNldoc6N1mjYSHDWIVcA3RVW-X7JIG49CmXXsetu4R-RZw-4Ds8_vJ5VLLErHwRSxLzZMs4qkUIV7W-6h432NypNPo6cWpcaaUxum9c6-uSKtsPxbB8wX1eUB2Wq2WstpRLjoXu2YWVCUMf0v-01oAbVDA1bQKgqlN4PfBQ88kfLecQieqlcPEmLpgRdqr0IxGtHDlxA608kr6Zk.DPLrA6WevfsiJ3BGsxTOnyC4w8H1-nO2TJ-DMu2dVYY&dib_tag=se&qid=1712414913&s=computers&sr=1-4&ufe=app_do%3Aamzn1.fos.0fd54328-1d46-4534-bd0f-16141b40bb5b',
               'https://www.amazon.es/Rii-Mini-i8-ergon%C3%B3mico-touchpad/dp/B00YDSSB6A?pf_rd_r=84P3B8YYS15RGM67DHNR&pf_rd_t=Events&pf_rd_i=deals&pf_rd_p=c2fe896f-6544-4e82-9c0f-79dcf8a574c4&pf_rd_s=slot-14&ref=dlx_deals_gd_dcl_img_11_19b3468c_dt_sl14_c4'
               ]


def get_amazon_price(dom):

    try:
        price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
        #price = price.replace(',', '').replace('€', '').replace('.00', '')
        #return int(price)
        price = price.replace(',', '.').replace('€', '').replace('.00', '')
        return float(price)
    except Exception as e:
        price = 'Not Available'
        return None


def get_product_name(dom):
    try:
        name = dom.xpath('//span[@id="productTitle"]/text()')
        [name.strip() for name in name]
        return name[0]
    except Exception as e:
        name = 'Not Available'
        return None

# write data into a csv file

with open('master_data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['product name', 'price', 'url'])

    for url in bucket_list:
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')
        amazon_dom = et.HTML(str(soup))

        product_name = get_product_name(amazon_dom)
        product_price = get_amazon_price(amazon_dom)

        time.sleep(random.randint(2, 10))

        writer.writerow([product_name, product_price, url])
        print(product_name, product_price)
