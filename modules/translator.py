import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DATA_DIR = os.path.join(BASE_DIR, "data")  

class NameTranslator:
    def __init__(self):
        """포켓몬, 기술, 특성 데이터를 불러와 한글-영어 및 영어-한글 변환을 지원하는 클래스"""
        self.pokemon_dict, self.pokemon_dict_reverse = self.load_csv("pokemon_names.csv")  # ✅ 영어-한글 변환 추가
        self.move_dict, self.move_dict_reverse = self.load_csv("moves.csv")  # ✅ 기술 변환
        self.ability_dict, _ = self.load_csv("abilities.csv")  # ✅ 특성 변환
        # ✅ 타입 변환 딕셔너리 (영어 → 한글)
        self.type_dict = {
            "normal": "노말", "fire": "불꽃", "water": "물", "electric": "전기", "grass": "풀", "ice": "얼음",
            "fighting": "격투", "poison": "독", "ground": "땅", "flying": "비행", "psychic": "에스퍼", "bug": "벌레",
            "rock": "바위", "ghost": "고스트", "dragon": "드래곤", "dark": "악", "steel": "강철", "fairy": "페어리"
        }

    def load_csv(self, filename):
        """CSV 파일을 불러와 한글-영어 및 영어-한글 매핑 딕셔너리 생성"""
        file_path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(file_path):
            print(f"⚠️ {filename} 파일이 존재하지 않습니다. 먼저 데이터를 크롤링하세요!")
            return {}, {}

        df = pd.read_csv(file_path)

        # ✅ 한글 → 영어 변환 딕셔너리
        kor_to_eng = {row["Korean"]: row["English"] for _, row in df.iterrows()}

        # ✅ 영어 → 한글 변환 딕셔너리 (대소문자 무시)
        eng_to_kor = {row["English"].lower(): row["Korean"] for _, row in df.iterrows()}

        return kor_to_eng, eng_to_kor

    def translate_pokemon_name(self, name):
        """포켓몬 한글 ↔ 영어 변환 (대소문자 무시)"""
        name_lower = name.lower()

        # ✅ 영어 → 한글 변환
        if name_lower in self.pokemon_dict_reverse:
            return self.pokemon_dict_reverse[name_lower]

        # ✅ 한글 → 영어 변환 추가
        if name in self.pokemon_dict:
            return self.pokemon_dict[name]

        return name  # ✅ 변환되지 않는 경우 원래 이름 유지

    def translate_move_name(self, move_name, for_pokeapi=False):
        """기술 한글 ↔ 영어 변환 (PokéAPI 요청 여부에 따라 다르게 변환)"""
        move_name_lower = move_name.lower()

        # ✅ moves.csv의 영어 기술명을 소문자로 변환하여 변환 딕셔너리 생성
        move_dict_lower = {k.lower(): v for k, v in self.move_dict.items()}  # 한글 → 영어 변환
        move_dict_reverse_lower = {k.lower(): v for k, v in self.move_dict_reverse.items()}  # 영어 → 한글 변환

        # ✅ 한글 → 영어 변환
        if move_name_lower in move_dict_lower:
            move_name_eng = move_dict_lower[move_name_lower]
        else:
            move_name_eng = move_name

        # ✅ PokéAPI 요청용 변환 (공백 → 하이픈 변환 추가)
        if for_pokeapi:
            move_name_eng = move_name_eng.replace(" ", "-")  # ✅ PokéAPI에서는 공백 대신 하이픈 사용

        # ✅ 영어 → 한글 변환 (moves.csv 기반)
        if not for_pokeapi and move_name_eng.lower() in move_dict_reverse_lower:
            return move_dict_reverse_lower[move_name_eng.lower()]  # ✅ 한글로 변환

        return move_name_eng  # ✅ 변환된 영어 이름 반환




    def translate_ability_name(self, ability_name):
        """특성 한글 → 영어 변환"""
        return self.ability_dict.get(ability_name, ability_name)
    
    def translate_type(self, type_name):
        """타입 영어 → 한글 변환"""
        return self.type_dict.get(type_name.lower(), type_name)

# ✅ 변환기 객체 생성
translator = NameTranslator()

# ✅ 디버깅: 변환 딕셔너리 확인
print("🔹 self.pokemon_dict_reverse 샘플:", list(translator.pokemon_dict_reverse.items())[:10])  # ✅ 첫 10개 확인
