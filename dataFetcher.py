from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def simplify_url(url: str) -> str:
    # 从 URL 中提取 base_url
    base_url = url.split('?')[0]

    # 获取 '?' 后面的参数部分
    params = url.split('?')[1]

    # 保留 id 和 checksum 参数，去掉其他无关的部分
    new_params = "&".join([param for param in params.split('&') if 'id=' in param or 'checksum=' in param])

    # 拼接成新的 URL
    new_url = base_url + '?' + new_params

    return new_url



def fetch_data(url, id_of_img):
    # 设置 ChromeOptions
    options = Options()
    options.add_argument('--headless')  # 如果你不想显示浏览器，可以加上这行

    # 启动 ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    try:
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '/html/body/app-root/div[1]/main/div/div/app-catalog/app-auction-header/div/div/div/div[1]/a/div'))
        )
        date_element = driver.find_element(By.XPATH, '/html/body/app-root/div[1]/main/div/div/app-catalog/app-auction-header/div/div/div/div[2]/div/div[2]/p[1]')  # 替换为实际日期元素的 XPath
        # 获取总 lot 数
        lot_count_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="lot-list_info"]/span'))
        )
        lot_count_text = lot_count_element.text

        title_text = title_element.text

        # 获取 date_text 并拆分为 start_date 和 end_date
        date_text = date_element.text  # 假设 date_text 格式是 "2024/11/5 - 2024/11/18"
        date_text = date_text.replace("Date(s) ", "")
        start_date, end_date = date_text.split(" - ")  # 拆分 start 和 end 日期
        start_date = start_date.replace("/","-")
        end_date = end_date.replace("/", "-")

        img_url1 = simplify_url(driver.find_element(By.XPATH, '//*[@id="'+str(int(id_of_img)) +'"]').get_attribute('src'))
        img_url2 = simplify_url(driver.find_element(By.XPATH, '//*[@id="' + str(int(id_of_img)+1) + '"]').get_attribute('src'))
        img_url3 = simplify_url(driver.find_element(By.XPATH, '//*[@id="' + str(int(id_of_img)+2) + '"]').get_attribute('src'))
        img_url4 = simplify_url(driver.find_element(By.XPATH, '//*[@id="' + str(int(id_of_img)+3) + '"]').get_attribute('src'))
        img_url5 = simplify_url(driver.find_element(By.XPATH, '//*[@id="' + str(int(id_of_img)+4) + '"]').get_attribute('src'))

        # 获取 lot 数字

        lot_count_match = re.search(r"of ([\d,]+) lots", lot_count_text)
        if lot_count_match:
            lot_count = int(lot_count_match.group(1).replace(",", ""))  # 移除逗号并转换为整数
        else:
            lot_count = 0  # 如果无法匹配到数字，则设为 0

        driver.quit()

        return title_text, start_date, end_date, lot_count,img_url1, img_url2, img_url3, img_url4, img_url5

    except Exception as e:
        print(f"Error fetching data: {e}")
        driver.quit()
        return None, None, None, None, None, None, None, None, None