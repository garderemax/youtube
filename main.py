import sys
import json
import requests
from bs4 import BeautifulSoup


def scrap(videoId):
    url = "https://www.youtube.com/watch?v=" + videoId + "&format=json"
    embedUrl = "http://www.youtube.com/oembed?url=" + url + "&format=json"
    response = requests.get(url)
    if (response.status_code != 200):
        return {"error": response.status_code}
    soup = BeautifulSoup(response.content,'html.parser')

    result = {}

    result["title"] = soup.find("meta", itemprop="name")["content"]
    result["authorName"] = soup.find("span", itemprop="author").next.next["content"]
    result["viewCount"] = soup.find("meta", itemprop="interactionCount")["content"]
    result["description"] = soup.find("meta", itemprop="description")["content"]
    result["descriptionLinks"] = []
    result["id"] = videoId
    result["comments"] = []

    return result

def main():
    if len(sys.argv) != 5:
        print("main.py -i <inputfile> -o <outputfile>")
        return
    inputFilePath = sys.argv[2]
    outputFilePath = sys.argv[4]

    input = json.load(open(inputFilePath))
    output = [scrap(videoId) for videoId in input["videos_id"]]
    outputFile = open(outputFilePath, "w")
    outputFile.write(json.dumps(output, indent=4))
    outputFile.close()

if __name__ == "__main__":
    main()