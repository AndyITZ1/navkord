import datetime
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


# https://en.dict.naver.com/#/search?range=all&query=%EC%97%B4
# https://en.dict.naver.com/#/search?range=all&query=%ED%99%95%EC%9D%B8%ED%95%98%EB%8B%A4
# https://en.dict.naver.com/#/search?range=all&query=%EA%B2%B0%EC%A0%95%ED%95%98%EB%8B%A4
# https://en.dict.naver.com/#/search?query=%EC%9D%BC&range=all


def ktoe(word):
    # try:
        dic = {"word": word, "count": 1, "date": datetime.datetime.now().isoformat()}
        driver.get("https://en.dict.naver.com/#/search?query=" + word)
        # Waits for website to load fully
        driver.implicitly_wait(3)

        component_keyword = driver.find_element(By.ID, "searchPage_entry").find_elements(By.CLASS_NAME, "row")
        suggestion = driver.find_element(By.ID, "container").find_elements(By.CLASS_NAME, "suggestion")
        suggestion_word = ""
        if suggestion:
            act_suggest = suggestion[0].text.split("\n")
            if act_suggest[1].find("Would you like to search") >= 0:
                return "This word does not exist."
            else:
                suggestion_word = act_suggest[1].split("'")
                word = suggestion_word[1]
                dic["conj"] = "This is word is a conjugated version of " + word

        if not component_keyword:
            return "No definitions were found for this word!"
        for l in component_keyword:
            result = []
            source = l.find_element(By.CLASS_NAME, "source").text  # the korean dictionary source
            key = l.find_element(By.CLASS_NAME, "link").text  # the highlighted blue wor
            if key.startswith(word) and (key == word or key.startswith(word + ' ')):
                if source not in dic:
                    dic[source] = []
                result += l.find_element(By.CLASS_NAME, "mean_list").text.split("\n")
                for num in result:
                    if num[:-1].isnumeric():
                        pass
                    else:
                        dic[source].append(num)


        add_ktoe(dic)
        return dic
    # except Exception:
    #     return "Error: Invalid word or website down"


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

        ret_dic = {"Word": "", "count": 1, "date": datetime.datetime.now().isoformat(), "Adjective": [], "Noun": [],
                   "Verb": [], "Interjection": [], "Other": []}
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
    except Exception:
        return "Error: Invalid word or website down"
