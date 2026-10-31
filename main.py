import sys


def print_menu():
    print("\n" + "=" * 30)
    print("      나만의 음식 상식 퀴즈 게임")
    print("=" * 30)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 30)


def get_menu_choice():
    while True:
        try:
            user_input = input("선택: ").strip()
            if not user_input:
                print("입력이 비어 있습니다. 메뉴 번호를 입력하세요.")
                continue

            choice = int(user_input)
            if 1 <= choice <= 5:
                return choice
            else:
                print("잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력하세요.")


def main():
    while True:
        try:
            print_menu()
            choice = get_menu_choice()

            if choice == 1:
                print("\n[알림] 퀴즈 풀기 기능은 개발 예정입니다.")
            elif choice == 2:
                print("\n[알림] 퀴즈 추가 기능은 개발 예정입니다.")
            elif choice == 3:
                print("\n[알림] 퀴즈 목록 기능은 개발 예정입니다.")
            elif choice == 4:
                print("\n[알림] 점수 확인 기능은 개발 예정입니다.")
            elif choice == 5:
                print("\n게임을 종료합니다. 이용해 주셔서 감사합니다!")
                sys.exit(0)
        except (KeyboardInterrupt, EOFError):
            print("\n\n강제 종료 신호가 감지되어 게임을 안전하게 종료합니다.")
            sys.exit(0)


if __name__ == "__main__":
    main()