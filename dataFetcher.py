from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re


def format_date_to_iso(date_str):
    """
    :param date_str: 输入的日期字符串
    :return: 转换后的日期字符串，格式为 YYYY-MM-DD
    """
    # 尝试的日期格式列表
    date_formats = [
        "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y", "%Y-%m-%d",
        "%d/%m/%Y", "%m-%d-%Y", "%Y.%m.%d", "%d.%m.%Y"
    ]

    for date_format in date_formats:
        try:
            # 尝试解析日期
            parsed_date = datetime.strptime(date_str, date_format)
            # 格式化为 ISO 8601 格式
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # 如果所有格式都不匹配，抛出异常
    raise ValueError(f"无法解析日期字符串: {date_str}")

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
        date_text = date_element.text.replace("Date(s) ", "")  # 假设 date_text 格式是 "2024/11/5 - 2024/11/18"
        start_date_raw, end_date_raw = date_text.split(" - ")  # 拆分 start 和 end 日期

        # 使用日期解析函数
        start_date = format_date_to_iso(start_date_raw)
        end_date = format_date_to_iso(end_date_raw)

        img_urls = []
        id_of_img = int(id_of_img)  # 确保 id_of_img 是整数
        i = 0  # 偏移量初始值
        while len(img_urls) < 5:  # 确保收集到 5 个有效链接
            try:
                xpath = f'//*[@id="lot-{id_of_img + i}"]/div/div/div[2]/div[2]/a/div/app-thumbnail/div/img'
                print(xpath)
                img_src = driver.find_element(By.XPATH, xpath).get_attribute('src')
                img_src = simplify_url(img_src)


                if img_src:  # 检查链接是否非空
                    img_urls.append(img_src)  # 如果有效，加入列表
            except Exception:
                pass  # 如果发生异常，直接跳过
            finally:
                i += 1  # 无论是否成功处理，偏移量递增

        # 将列表中的链接分配给 img_url1 到 img_url5
        img_url1, img_url2, img_url3, img_url4, img_url5 = img_urls

        # 获取 lot 数字

        lot_count_match = re.search(r"of ([\d,]+) lots", lot_count_text)
        if lot_count_match:
            lot_count = int(lot_count_match.group(1).replace(",", ""))  # 移除逗号并转换为整数
        else:
            lot_count = 0  # 如果无法匹配到数字，则设为 0

        driver.quit()

        return str(title_text), str(start_date), str(end_date), str(lot_count), str(img_url1), str(img_url2), str(img_url3), str(img_url4), str(img_url5)

    except Exception as e:
        print(f"Error fetching data: {e}")
        driver.quit()
        return None, None, None, None, None, None, None, None, None