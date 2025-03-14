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
    translated_moves = [translator.translate_move_name(move) for move in smogon_moves]

    # ✅ 배틀 전략 추천 메시지 생성
    strategy = f"🔹 {translator.translate_pokemon_name(pokemon)} ({pokemon})의 추천 기술: {', '.join(translated_moves)}\n\n"
    strategy += f"🛡 배틀 전략 추천:\n"
    strategy += f"{translator.translate_pokemon_name(pokemon)} vs {translator.translate_pokemon_name(opponent)}\n"
    strategy += f"상대 타입: {', '.join(enemy_pokemon_types)}\n"

    # ✅ 가장 강한 기술 찾기 로직 수정
    best_move = None
    best_power = 0

    print("🔹 추천 기술 목록:", smogon_moves)  # ✅ 추천 기술 목록 출력

    for move in smogon_moves:
        move_details = get_move_details(move)  # ✅ 기술 정보 가져오기
        move_power = move_details.get("power", 0) if move_details.get("power") is not None else 0

        print(f"🔹 기술: {move}, 파워: {move_power}")  # ✅ 각 기술의 파워 출력

        if move_power > best_power:
            best_power = move_power
            best_move = move  # ✅ 가장 강한 기술 업데이트

    # ✅ 가장 강한 기술 추천 메시지 추가
    if best_move:
        strategy += f"✅ 추천 공격 기술: {best_move} (최대 피해 가능, 파워: {best_power})\n"
    else:
        strategy += "⚠️ 강력한 기술이 부족합니다. 교체를 고려하세요.\n"

    test_moves = ["용의춤", "지진", "신속", "Ice Spinner"]
    for move in test_moves:
        move_info = get_move_details(move)
        print(f"🔹 '{move}' 기술 정보: {move_info}")

    return strategy
