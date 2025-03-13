import requests
from modules.translator import translator  # ✅ 번역기 추가


def get_pokemon_info(pokemon_name):
    """PokéAPI에서 특정 포켓몬의 정보를 가져오는 함수"""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"].capitalize(),
            "height": data["height"] / 10,  # 미터 단위 변환
            "weight": data["weight"] / 10,  # kg 단위 변환
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "base_stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
            "moves": [move["move"]["name"] for move in data["moves"][:10]]  # 기술 10개만 가져오기
        }
    else:
        return {"error": "포켓몬을 찾을 수 없습니다."}

def get_type_effectiveness(type_name):
    """PokéAPI에서 특정 타입의 상성 정보를 가져오는 함수"""
    url = f"https://pokeapi.co/api/v2/type/{type_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "double_damage_from": [t["name"] for t in data["damage_relations"]["double_damage_from"]],
            "half_damage_from": [t["name"] for t in data["damage_relations"]["half_damage_from"]],
            "no_damage_from": [t["name"] for t in data["damage_relations"]["no_damage_from"]],
        }
    else:
        return {"error": "타입 정보를 찾을 수 없습니다."}


def get_move_details(move_name):
    """PokéAPI에서 특정 기술의 정보를 가져오고, 한글 이름으로 변환"""
    url = f"https://pokeapi.co/api/v2/move/{move_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        move_name_kor = translator.translate_move_name(data["name"])  # ✅ 한글 변환 적용
        return {
            "name": move_name_kor,  # ✅ 한글 이름으로 저장
            "power": data["power"] if data["power"] is not None else 0,
            "accuracy": data["accuracy"] if data["accuracy"] is not None else 100,
            "pp": data["pp"],
            "type": translator.translate_type(data["type"]["name"]),  # ✅ 타입도 한글로 변환
            "damage_class": data["damage_class"]["name"],  # 물리/특수/보조 구분
            "effect": data["effect_entries"][0]["effect"] if data["effect_entries"] else "효과 없음"
        }
    else:
        return {"error": "기술 정보를 찾을 수 없습니다."}