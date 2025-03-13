from modules.pokeapi_helper import get_pokemon_info, get_type_effectiveness, get_move_details
from modules.smogon_scraper import get_smogon_moves
from modules.translator import translator

def recommend_battle_strategy(pokemon, opponent):
    # ✅ 포켓몬 정보 가져오기
    my_pokemon = get_pokemon_info(pokemon)
    enemy_pokemon = get_pokemon_info(opponent)

    if "error" in my_pokemon or "error" in enemy_pokemon:
        return "포켓몬 정보를 가져오는 데 실패했습니다."

    # ✅ 포켓몬 타입을 한글로 변환
    my_pokemon_types = [translator.translate_type(t) for t in my_pokemon["types"]]
    enemy_pokemon_types = [translator.translate_type(t) for t in enemy_pokemon["types"]]

    # ✅ Smogon 추천 기술 가져오기 (한글 변환 포함)
    smogon_moves = get_smogon_moves(pokemon)

    # ✅ 배틀 전략 추천 메시지 생성
    strategy = f"🔹 {translator.translate_pokemon_name(pokemon)} ({pokemon})의 추천 기술: {', '.join(smogon_moves)}\n\n"
    strategy += f"🛡 배틀 전략 추천:\n"
    strategy += f"{translator.translate_pokemon_name(pokemon)} vs {translator.translate_pokemon_name(opponent)}\n"
    strategy += f"상대 타입: {', '.join(enemy_pokemon_types)}\n"

    # ✅ Smogon 추천 기술 중 가장 강한 기술 찾기
    best_move = None
    best_power = 0
    for move in smogon_moves:
        move_details = get_move_details(move)  # ✅ 기술 정보 가져오기
        move_power = move_details.get("power", 0)  # ✅ 기술의 파워 가져오기
        if move_power > best_power:
            best_power = move_power
            best_move = move  # ✅ 변환된 한글 기술명 저장

    if best_move:
        strategy += f"✅ 추천 공격 기술: {best_move} (최대 피해 가능)\n"
    else:
        strategy += "강력한 기술이 부족합니다. 교체를 고려하세요.\n"

    return strategy
