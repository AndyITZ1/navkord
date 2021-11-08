from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from navdata import add_etok, add_ktoe

# Makes the driver run in headless mode
options = FirefoxOptions()
options.add_argument("--headless")

service = Service("./geckodriver.exe")
driver = webdriver.Firefox(service=service, options=options)


def ktoe(word):
    try:
        dic = {"word": word}
        driver.get("https://en.dict.naver.com/#/search?query=" + word)
        # Waits for website to load fully
        driver.implicitly_wait(3)
        results = []

        component_keyword = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[3]/div").find_elements(
            By.CLASS_NAME, "row")
        # for m in component_keyword:
        #     if m.find_element(By.CLASS_NAME, "highlight").text == word:
        #         print(m.find_element(By.CLASS_NAME, "highlight").text)
        for l in component_keyword:
            if l.find_element(By.CLASS_NAME, "source").text == "ET-house Neungyule Korean-English Dictionary" and l.find_element(By.CLASS_NAME, "link").text.startswith(word):
                print(l.find_element(By.CLASS_NAME, "mean_list").text)
                results += l.find_element(By.CLASS_NAME, "mean_list").text.split("\n")
                #break
        print(results)
        for num in results:
            if num[:-1].isnumeric():
                pass
            else:
                dic[str(count)] = num
                count += 1
        add(dic)
        return dic
    except:
        return "Error: Invalid word or website down"

def etok(word):
    try:
        dic = {"word": word}
        driver.get("https://en.dict.naver.com/#/search?query=" + word)
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
                # final.append(str(count) + ". " + num)
                dic[str(count)] = num
                count += 1

        # print(final)
        dic_to_str = ""
        for key, value in dic.items():
            dic_to_str += key + ": " + value + "\n"

        ret_dic = {"Word": "", "Adjective": [], "Noun": [], "Verb": [], "Interjection": [], "Other": []}
        for line in dic_to_str.splitlines():
            if line.find("word") >= 0:
                ret_dic["Word"] = line.split(": ")[1]
            elif line.find("Adjective") >= 0:
                ret_dic["Adjective"].append(line.split("Adjective ")[1] + "\n")
            elif line.find("Noun") >= 0:
                ret_dic["Noun"].append(line.split("Noun ")[1] + "\n")
            elif line.find("Verb") >= 0:
                ret_dic["Verb"].append(line.split("Verb ")[1] + "\n")
            elif line.find("Interjection") >= 0:
                ret_dic["Interjection"].append(line.split("Interjection ")[1] + "\n")
            else:
                ret_dic["Other"].append(line.split(": ")[1] + "\n")

        add_etok(ret_dic)
        return ret_dic
        driver.quit()
    except:
        return "Error: Invalid word or website down"
