import os
from modules.smogon_scraper import get_smogon_moves
from modules.battle_strategy import recommend_battle_strategy
from modules.translator import translator
from modules.pokemon_wiki_scraper import fetch_pokemon_names, fetch_moves, fetch_abilities

# ✅ 상대 경로 설정 (data 폴더를 상대적으로 찾도록 변경)
DATA_DIR = "data"

# ✅ 상대 경로로 CSV 파일 경로 설정
POKEMON_CSV = os.path.join(DATA_DIR, "pokemon_names.csv")
MOVES_CSV = os.path.join(DATA_DIR, "moves.csv")
ABILITIES_CSV = os.path.join(DATA_DIR, "abilities.csv")

def check_and_fetch_data():
    """CSV 파일이 없으면 크롤링을 실행하고, 있으면 한 번만 확인 메시지를 출력"""

    # ✅ data 폴더가 없으면 생성
    if not os.path.exists(DATA_DIR):
        print(f"⚠️ data 폴더가 존재하지 않습니다. 새로 생성합니다: {DATA_DIR}")
        os.makedirs(DATA_DIR)

    # ✅ 먼저 없는 파일을 확인하고 크롤링해야 하는 파일만 저장
    files_to_check = [
        (POKEMON_CSV, "pokemon_names.csv", fetch_pokemon_names),
        (MOVES_CSV, "moves.csv", fetch_moves),
        (ABILITIES_CSV, "abilities.csv", fetch_abilities)
    ]

    missing_files = []

    # ✅ 첫 번째 체크: 존재하지 않는 파일만 리스트에 추가
    for file_path, file_name, fetch_function in files_to_check:
        if not os.path.exists(file_path):  # ✅ 상대 경로로 파일 확인
            print(f"⚠️ {file_name} 파일이 존재하지 않습니다. 데이터를 크롤링합니다...")
            missing_files.append((file_path, file_name, fetch_function))

    # ✅ 크롤링 실행 (필요한 경우만)
    for file_path, file_name, fetch_function in missing_files:
        fetch_function()  # ✅ 크롤링 실행
        print(f"✅ {file_name} 크롤링 완료!")

    # ✅ 최종 확인
    all_files_exist = True
    for file_path, file_name, _ in files_to_check:
        if not os.path.exists(file_path):  # ✅ 크롤링 후에도 없는 파일이 있으면 오류
            print(f"⚠️ {file_name} 파일이 여전히 존재하지 않습니다. 오류가 발생한 것 같습니다!")
            all_files_exist = False
        else:
            print(f"✅ {file_name} 파일이 존재합니다.")

    if all_files_exist:
        print("✅ 모든 필수 CSV 파일이 존재합니다. 크롤링을 건너뜁니다.")

def main():
    print("🔹 포켓몬 배틀 전략 추천 시스템 🔹")

    # ✅ 포켓몬 이름 입력 (한글 가능)
    pokemon_kor = input("포켓몬 이름을 입력하세요 (한글 가능): ").strip()
    opponent_kor = input("상대 포켓몬 이름을 입력하세요 (한글 가능): ").strip()

    # ✅ 한글 → 영어 변환
    pokemon_name = translator.translate_pokemon_name(pokemon_kor)
    opponent_name = translator.translate_pokemon_name(opponent_kor)

    # ✅ Smogon 추천 기술 가져오기
    smogon_moves = get_smogon_moves(pokemon_name)
    if "error" in smogon_moves:
        print(f"⚠️ 오류 발생: {smogon_moves['error']}")
    else:
        print(f"🔹 {pokemon_kor} ({pokemon_name})의 추천 기술: {', '.join(smogon_moves)}")

    # ✅ 배틀 전략 추천
    strategy = recommend_battle_strategy(pokemon_name, opponent_name)
    print(f"\n🛡 배틀 전략 추천:\n{strategy}")

if __name__ == "__main__":
    # ✅ CSV 파일이 없으면 크롤링 실행
    check_and_fetch_data()

    # ✅ 메인 실행
    main()
