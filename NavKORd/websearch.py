from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Makes the driver run in headless mode
options = FirefoxOptions()
options.add_argument("--headless")

search = input("What is your word: ")

service = Service("D:\\Projects and other Prodution\\Python Projects\\navkord\\geckodriver.exe")
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://en.dict.naver.com/#/search?query=" + search)
# Waits for website to load fully
driver.implicitly_wait(3)


idiom = driver.find_element(By.ID, "searchPage_entry")
first_row = idiom.find_element(By.CLASS_NAME, "row")
words = first_row.find_elements(By.CLASS_NAME, "mean_list")
results = []
final = []
count = 1

# splits the results into a list
for value in words:
    results += (value.text.split("\n"))

# removes the numbers from the list to reformat them into one item
for num in results:
    if num[:-1].isnumeric():
        pass
    else:
        final.append(str(count) + ". " + num)
        count += 1

print(final)

driver.quit()
