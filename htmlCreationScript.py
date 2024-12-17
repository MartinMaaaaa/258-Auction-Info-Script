from dataFetcher import fetch_data  # 导入 fetch_data 函数

# 获取目标网址
url = input("请输入目标网址 (e.g: https://ccpowerdeals.hibid.com/catalog/594888/high-value-online-returns-and-unclaimed-freight--264-): ")
id_of_img = input("请输入第一个开始爬取的图片id（e.g：221669508）：")
container = ".bid_container_" + str(input("输入container#（e.g: 1)： "))
detail = url.replace("/catalog/", "/auction/")
# 调用 fetch_data 函数来获取数据
title_text, start_date, end_date, lot_count,img_url1,img_url2,img_url3,img_url4,img_url5 = fetch_data(url,id_of_img)

# 定义 HTML 内容并替换占位符
html_content = f"""
<!-- CSS 样式 -->
<style>
    /* 添加 Total Lots、Start Time、Close Time 的值 */
    {container} .total-lots::after {{
        content: "{lot_count}"; /* 替换为实际的总数值 */
    }}

    {container} .start-time::after {{
        content: "{start_date.replace("-","/")}"; /* 替换为实际的开始时间 */
    }}

    {container} .close-time::after {{
        content: "{end_date.replace("-","/")} 08:00 PM"; /* 替换为实际的结束时间 */
    }}
    
    {container} .lot-info p{{
        margin-bottom: 10px;
    }}
</style>

<!-- JavaScript 代码 -->
<script>
document.addEventListener("DOMContentLoaded", function() {{
  
    // 预定义每张图片的背景图片 URL
    const imageUrls = [
        "{img_url1}",
        "{img_url2}",
        "{img_url3}",
        "{img_url4}",
        "{img_url5}"
    ];

    // 获取所有轮播项中的图片容器
    const imageContainers = document.querySelectorAll('{container} .elementor-carousel-image');
    const titleElement = document.querySelector('{container} .bid-title h2'); // 获取标题元素
    const openingStatusElement = document.querySelector('{container} .opening-status h3'); // 获取 Opening in Hibid 部分
    const clickElement = document.querySelector('{container} .elementor-main-swiper'); // 
    const viewMore = document.querySelector('{container} .view_more'); // 
    const auctionDetail = document.querySelector('{container} .auction_detail'); // 
    
    clickElement.addEventListener("click", () => {{
    window.open("{url}", "_blank");  // 在新窗口打开链接
   }});
   
   viewMore.addEventListener("click", () => {{
    window.open("{url}", "_blank");  // 在新窗口打开链接
   }});
   auctionDetail.addEventListener("click", () => {{
    window.open("{detail}", "_blank");  // 在新窗口打开链接
   }});
    // 计算当前时间
    const currentTime = new Date();

    // 解析 start-time 和 close-time
    const startDate = new Date('{start_date}T10:00:00');
    const closeDate = new Date('{end_date}T23:59:59');
    
    // 获取需要隐藏的容器元素
    const bidContainer = document.querySelector('{container}'); 
    // 更新标题内容
    if (titleElement) {{
        titleElement.textContent = "{title_text}"; // 根据需要设置标题内容
    }}

    // 判断是否在开场时间段内
    if (currentTime < startDate || currentTime > closeDate) {{ // 不在开场时间段内，隐藏整个元素
        if (bidContainer) {{
            bidContainer.style.display = "none";
        }}
    }} 

    // 检查是否找到 .elementor-carousel-image 元素
    if (imageContainers.length > 0) {{
        // 为每个容器设置 background-image 和点击链接
        imageContainers.forEach((container, index) => {{
            // 确保容器存在，并且当前索引在数组范围内
            if (index < imageUrls.length ) {{
                // 设置 background-image
                container.style.backgroundImage = `url(${{imageUrls[index]}})`;

                // 添加点击事件，将页面重定向到对应链接地址
                container.style.cursor = "pointer";  // 设置鼠标样式为手指形状
            }}
        }});
    }}
}});
</script>
"""

# 将 HTML 内容写入文本文件
with open("output.html.txt", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML 文件已生成：output.html.txt")
