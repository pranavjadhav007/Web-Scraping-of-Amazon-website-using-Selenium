import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

s=Service("D:\Codes\Web_Scrapping\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe")
driver=webdriver.Chrome(service=s)

time.sleep(3)

reviews=[]
customer_review_summaries=[]
book_names=[]
author_names=[]
prices=[]
rated_bys=[]
book_summaries=[]
pages=[]


url='https://www.amazon.in/s?k=books&crid=3AAQT12P4QQ3L&sprefix=books%2Caps%2C268&ref=nb_sb_noss_1'
for i in range(4):
    driver.get(url)

    book_links=driver.find_elements(By.XPATH,"//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
    book_urls=[i.get_attribute("href") for i in book_links]
    print(len(book_urls))

    for link in book_urls:
        print(link)
        driver.get(link)
        try:
            check_book=driver.find_element(By.XPATH,"//span[contains(@class, 'a-size-medium a-color-secondary celwidget') and contains(text(), 'Paperback')]")

            book_name=driver.find_element(By.XPATH,'//div[@class="a-section a-spacing-none"]//span[@class="a-size-large celwidget"]')
            book_names.append(book_name.text)

            author_name=driver.find_element(By.XPATH,"//span[@class='author notFaded']//a[@class='a-link-normal']")
            author_names.append(author_name.text)

            price=driver.find_element(By.XPATH,"//span[@class='a-price-whole']")
            prices.append(price.text)

            try:
                book_summary = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,"//div[@class='a-expander-content a-expander-partial-collapse-content']//span"))
                )
                book_summaries.append(book_summary.text)
            except:
                book_summaries.append("No summary present")

            try:
                num_pages = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,"//span[contains(text(), 'pages')]"))
                )
                pages.append(num_pages.text)
            except:
                pages.append("No info present")
            try:
                rated_by = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,"//span[@id='acrCustomerReviewText']"))
                )
                rated_bys.append(rated_by.text)
            except:
                rated_bys.append("No one yet rated")

            try:
                customer_review_summary = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//p[@class='a-spacing-small']//span"))
                )
                customer_review_summaries.append(customer_review_summary.text)
            except:
                customer_review_summaries.append("No reviews")

            try:
                review = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@class='a-popover-trigger a-declarative']//span[@class='a-size-base a-color-base']"))
                )
                # review=driver.find_element(By.XPATH,"//a[@class='a-popover-trigger a-declarative']//span[@class='a-size-base a-color-base']")
                reviews.append(review.text)
            except:
                reviews.append("Not yet reviewed")
            time.sleep(2)
        except:
            print("not a book")
    driver.get(url)
    print("\n\n\n\nNext page is going to render\n\n\n\n")
    url_a=driver.find_element(By.XPATH,'//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
    url=url_a.get_attribute("href")
    time.sleep(1)

print(len(book_names),len(author_names),len(prices),len(rated_bys),len(reviews),len(customer_review_summaries),len(book_summaries))

df=pd.DataFrame({'Book_name':book_names,"Author_name":author_names,"price":prices,"rated_bys":rated_bys,"reviews":reviews,"customer_review_summaries":customer_review_summaries,"book_summaries":book_summaries})

df.to_csv("books_dataset.csv",index=False)

