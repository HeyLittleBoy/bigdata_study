import asyncio  # 导入异步IO模块
from playwright.async_api import async_playwright  # 导入playwright的异步API
import pandas as pd  # 导入pandas库

async def scroll_page(page):
    previous_height = await page.evaluate('document.body.scrollHeight')  # 获取页面初始高度
    print("滚动页面中......")
    while True:  # 无限循环，直到页面高度不再变化
        await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')  # 向下滚动页面
        await page.wait_for_timeout(2000)  # 等待2秒以加载内容

        new_height = await page.evaluate('document.body.scrollHeight')  # 获取新的页面高度
        if new_height == previous_height:  # 如果页面高度没有变化，跳出循环
            break
        previous_height = new_height  # 更新页面高度
    print("滚动页面结束")

async def scrape_page():
    async with async_playwright() as p:  # 使用playwright进行异步操作
        browser = await p.chromium.launch(headless=False)  # 启动Chromium浏览器
        page = await browser.new_page()  # 打开一个新页面
        url = "https://cht.1688.com/index.html?spm=a260k.dacugeneral.home2019scene.d0.6aef35e4SvQAR5"  # 目标URL
        await page.goto(url)  # 访问目标URL
        await page.wait_for_timeout(3000)  # 等待2秒以加载内容

        my_list = []

        # 切换类目并爬取链接
        tab_base_basenav = await page.query_selector('.mainBox .navBox .tabNav .tabBaseNav')  # 获取包含类目标签的父元素
        tab_base_exrnav = await page.query_selector('.mainBox .navBox .tabNav .tabExrNav')  # 获取包含类目标签的父元素
        base_nav_items = await tab_base_basenav.query_selector_all('.baseNavItem')  # 获取所有符合选择器的类目标签
        exr_nav_items = [item for item in await tab_base_exrnav.query_selector_all('.exrNavItem') ]
        nav_items = base_nav_items 
        print(nav_items)
        try:
            for item in nav_items:
                base_nav_moreButton = (await tab_base_basenav.query_selector_all('.moreButton'))[0]  # 获取符合选择器的类目标签

                await base_nav_moreButton.click()
                print("已经点击更多1")
                
                item_text = await item.inner_text()  # 获取类目标签的文本
                print(item_text)

                await item.click()  # 点击类目标签
                # await page.wait_for_timeout(1000)  # 等待2秒以加载内容
            
                # await scroll_page(page)  # 切换类目后滚动页面以加载内容
                # await page.wait_for_timeout(3000)  # 等待2秒以加载内容

                print(item_text)
                
                filtered_links = await page.eval_on_selector_all('.mainBox .listBox .cardListItem a',
                                                                '(elements) => elements.map(element => element.href)')  # 获取所有符合选择器的链接
                
                my_list.append(filtered_links)
                

        except Exception as e:
            print(f"Failed to click on the specified category: {e}")  # 打印错误信息

        await browser.close()  # 关闭浏览器

        return my_list  # Return the list of filtered links
    
async def scrape_detial():
    async with async_playwright() as p:  # 使用playwright进行异步操作
        filtered_links = await scrape_page()  # Await the coroutine to get the result

        for url_list in filtered_links:  # Iterate over the list of lists
            for url in url_list:  # Iterate over each URL in the inner list
                browser = await p.chromium.launch(headless=False)  # 启动Chromium浏览器
                page = await browser.new_page()  # 打开一个新页面
                await page.wait_for_timeout(9000)  # 等待2秒以加载内容
                await page.goto(url)  # 访问目标URL
                await page.wait_for_timeout(3000)  # 等待2秒以加载内容
                await browser.close()  # 关闭浏览器 after processing each URL


async def main():
    data = await scrape_detial()  # 调用scrape_detial函数并获取返回的数据
    
asyncio.run(main())  # 运行main函数
