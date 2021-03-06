from bs4 import BeautifulSoup
import requests
import pickle
from pathlib import Path


def main():

    #scrape the website for raw text data
    u = "https://rankedboost.com/pokemon-go/type-chart/?fbclid=IwAR0FLnSAKpdo2PTpxvggYi8Rw-QNRpP02_v8SFOY2HKUoIbrwHWelA-rc08"
    webpage = requests.get(u).text
    soup = BeautifulSoup(webpage, features="html.parser")
    data = str(soup.findAll()).split("\n")

    strong_against = {}
    weak_against = {}

    cur_type = ""

    #save lists into data file
    for line in data:
        if line.startswith("<td class=\"column-1\"><span style=\"color: ") and "Chart" not in line:
            if "Pokemon Type" in line:
                break
            start = len("<td class=\"column-1\"><span style=\"color: #d3d3d3;\"><strong>")
            end = line.find(" TYPE", start)
            cur_type = line[start:end]
            start += len(" TYPE</strong></span></td><td class=\"column-2\"><strong>Strong Against:</strong> ") + len(cur_type)
            end = line.find("</td><td class=\"column-3\">", start)
            strong_counters = line[start:end]
            strong_against[cur_type] = strong_counters
            start += len("</td><td class=\"column-3\"><strong>Weak Against:</strong> ") + len(strong_counters)
            end = line.find("</td>", start)
            weak_counters = line[start:end]
            weak_against[cur_type] = weak_counters
            if cur_type =="NORMAL":
                weak_against[cur_type] = "None"

    strong_outfile = Path("../Info/strongtypecounters.pickle")
    weak_outfile = Path("../Info/weaktypecounters.pickle")
    if not strong_outfile.is_file():
        strong_outfile = Path("Info/strongtypecounters.pickle")
        weak_outfile = Path("Info/weaktypecounters.pickle")

    pickle.dump(strong_against, open(str(strong_outfile), "wb"))
    pickle.dump(weak_against, open(str(weak_outfile), "wb"))


if __name__ == "__main__":
    main()
