import os
import pandas as pd

# ✅ 상대 경로를 절대 경로로 변환하여 동적으로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # modules 폴더의 상위 디렉토리
DATA_DIR = os.path.join(BASE_DIR, "data")  # "data/" 폴더 경로 설정

class NameTranslator:
    def __init__(self):
        """포켓몬, 기술, 특성, 타입 데이터를 불러와 한글-영어 변환을 지원하는 클래스"""
        self.pokemon_dict = self.load_csv("pokemon_names.csv")
        self.move_dict = self.load_csv("moves.csv")
        self.ability_dict = self.load_csv("abilities.csv")
        
        # ✅ 타입 변환 딕셔너리 (영어 → 한글)
        self.type_dict = {
            "normal": "노말", "fire": "불꽃", "water": "물", "electric": "전기", "grass": "풀", "ice": "얼음",
            "fighting": "격투", "poison": "독", "ground": "땅", "flying": "비행", "psychic": "에스퍼", "bug": "벌레",
            "rock": "바위", "ghost": "고스트", "dragon": "드래곤", "dark": "악", "steel": "강철", "fairy": "페어리"
        }

    def load_csv(self, filename):
        """CSV 파일을 불러와 한글-영어 매핑 딕셔너리 생성"""
        file_path = os.path.join(DATA_DIR, filename)  # ✅ data 폴더에서 파일 로드
        if not os.path.exists(file_path):
            print(f"⚠️ {filename} 파일이 존재하지 않습니다. 먼저 데이터를 크롤링하세요!")
            return {}

        df = pd.read_csv(file_path)  # ✅ 상대 경로에서 파일을 읽어옴
        return {row["Korean"]: row["English"] for _, row in df.iterrows()}  # ✅ 한글 → 영어 변환 딕셔너리 생성

    def translate_pokemon_name(self, korean_name):
        """포켓몬 한글 → 영어 변환"""
        return self.pokemon_dict.get(korean_name, korean_name)

    def translate_move_name(self, korean_move):
        """기술 한글 → 영어 변환"""
        return self.move_dict.get(korean_move, korean_move)

    def translate_ability_name(self, korean_ability):
        """특성 한글 → 영어 변환"""
        return self.ability_dict.get(korean_ability, korean_ability)

    def translate_type(self, type_name):
        """타입 영어 → 한글 변환"""
        return self.type_dict.get(type_name.lower(), type_name)

# ✅ 변환기 객체 생성
translator = NameTranslator()
