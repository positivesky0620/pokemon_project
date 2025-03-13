import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from modules.translator import translator
from modules.pokeapi_helper import get_move_details  # ✅ 기술 정보 가져오기


def setup_selenium():
    """불필요한 로그 없이 Selenium WebDriver 설정"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ✅ GUI 없이 실행
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # ✅ DevTools 메시지 및 불필요한 로그 제거
    options.add_argument("--remote-debugging-port=0")  # ✅ 디버깅 포트 사용 안 함 (DevTools 제거)
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])  # ✅ 내부 로깅 비활성화
    options.add_argument("--disable-blink-features=AutomationControlled")  # ✅ 자동화 감지 차단
    options.add_argument("--disable-infobars")  # ✅ 'Chrome is being controlled by automated software' 메시지 제거
    options.add_argument("--disable-software-rasterizer")  # ✅ WebGL 관련 메시지 방지
    options.add_argument("--log-level=3")  # ✅ WARNING 이상 로그만 표시

    # ✅ Windows에서 DevTools 메시지 완전 차단
    service = Service(ChromeDriverManager().install())

    if os.name == "nt":  # Windows 환경에서 추가 처리
        from subprocess import CREATE_NO_WINDOW
        service.creationflags = CREATE_NO_WINDOW  # ✅ 백그라운드에서 실행되도록 설정

    # ✅ Chrome 실행 시 모든 출력 차단
    driver = webdriver.Chrome(service=service, options=options)

    return driver  # ✅ WebDriver 객체 반환


def get_smogon_moves(pokemon_name):
    """Smogon에서 특정 포켓몬의 추천 기술 4개를 가져오는 함수"""

    driver = setup_selenium()  # ✅ 수정: WebDriver 객체를 가져옴

    try:
        url = f"https://www.smogon.com/dex/sv/pokemon/{pokemon_name.lower()}/"
        
        # ✅ Chrome 실행 시 모든 출력 차단 (Windows & Linux 호환)
        with open(os.devnull, "wb") as fnull:
            subprocess.Popen(
                [driver.service.path, "--remote-debugging-port=0"],
                stdout=fnull, stderr=fnull
            )

        driver.get(url)

        # ✅ 기술 목록이 로드될 때까지 대기 (최대 10초)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "MoveList"))
        )

        # ✅ HTML 가져오기
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # ✅ "PokemonPage-StrategySelector" 클래스 찾기 (포맷 확인)
        format_section = soup.find("div", class_="PokemonPage-StrategySelector")
        if not format_section:
            return {"error": "포맷 섹션을 찾을 수 없습니다."}

        # ✅ OU 포맷 찾기 (없으면 Doubles 찾기)
        format_link = format_section.find("a", string="OU") or format_section.find("a", string="Doubles")
        if not format_link:
            return {"error": "OU 또는 Doubles 포맷을 찾을 수 없습니다."}

        # ✅ 해당 포맷의 첫 번째 기술 목록 찾기
        move_list_sections = format_link.find_all_next("ul", class_="MoveList")
        if not move_list_sections:
            return {"error": "추천 기술을 찾을 수 없습니다."}

        # ✅ 기술 목록 추출 (최대 4개, 첫 번째 `li` 요소만 선택)
        moves = []
        for move_list in move_list_sections:
            first_li = move_list.find("li")  # ✅ 첫 번째 `li` 요소만 가져옴
            if first_li:
                move_link = first_li.find("a", class_="MoveLink")  # ✅ `MoveLink` 클래스에서 기술 가져오기
                if move_link:
                    move_name = move_link.text.strip()

                    # ✅ 중복되지 않도록 저장 & 한글 변환
                    if move_name and move_name not in moves:
                        moves.append(translator.translate_move_name(move_name))  

                    if len(moves) >= 4:  # ✅ 최대 4개까지만 저장
                        break
            if len(moves) >= 4:
                break

        return moves if moves else {"error": "추천 기술이 없습니다."}

    finally:
        driver.quit()
