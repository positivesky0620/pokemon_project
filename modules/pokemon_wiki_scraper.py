import requests
from bs4 import BeautifulSoup
import pandas as pd

# ✅ 포켓몬 위키 URL (포켓몬, 기술, 특성)
POKEMON_URL = "https://pokemon.fandom.com/ko/wiki/국가별_포켓몬_이름_목록"
MOVES_URL = "https://pokemon.fandom.com/ko/wiki/국가별_기술_이름_목록"
ABILITIES_URL = "https://pokemon.fandom.com/ko/wiki/국가별_특성_이름_목록"

def fetch_pokemon_names():
    """포켓몬 이름 (한글, 영어, 일본어) 크롤링 후 CSV로 저장"""
    response = requests.get(POKEMON_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")  # 첫 번째 표 찾기
    rows = table.find_all("tr")[1:]  # 헤더 제외

    data = []
    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 3:
            korean_name = columns[1].text.strip()
            english_name = columns[3].text.strip()
            japanese_name = columns[2].text.strip()
            data.append([korean_name, english_name, japanese_name])

    df = pd.DataFrame(data, columns=["Korean", "English", "Japanese"])
    df.to_csv("pokemon_names.csv", index=False, encoding="utf-8-sig")
    print("✅ 포켓몬 이름 데이터 저장 완료!")

def fetch_moves():
    """기술 이름 (한글, 영어, 일본어) 크롤링 후 CSV로 저장"""
    response = requests.get(MOVES_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")  
    rows = table.find_all("tr")[1:]

    data = []
    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 3:
            korean_name = columns[1].text.strip()
            english_name = columns[3].text.strip()
            japanese_name = columns[2].text.strip()
            data.append([korean_name, english_name, japanese_name])

    df = pd.DataFrame(data, columns=["Korean", "English", "Japanese"])
    df.to_csv("moves.csv", index=False, encoding="utf-8-sig")
    print("✅ 기술 데이터 저장 완료!")

def fetch_abilities():
    """특성 이름 (한글, 영어, 일본어) 크롤링 후 CSV로 저장"""
    response = requests.get(ABILITIES_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")  
    rows = table.find_all("tr")[1:]

    data = []
    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 3:
            korean_name = columns[1].text.strip()
            english_name = columns[3].text.strip()
            japanese_name = columns[2].text.strip()
            data.append([korean_name, english_name, japanese_name])

    df = pd.DataFrame(data, columns=["Korean", "English", "Japanese"])
    df.to_csv("abilities.csv", index=False, encoding="utf-8-sig")
    print("✅ 특성 데이터 저장 완료!")

if __name__ == "__main__":
    fetch_pokemon_names()
    fetch_moves()
    fetch_abilities()
