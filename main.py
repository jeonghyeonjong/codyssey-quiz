import sys


class Quiz:
    """개별 퀴즈를 표현하는 클래스"""

    def __init__(self, question: str, choices: list[str], answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number: int | None = None):
        """문제를 콘솔에 출력"""
        prefix = f"[문제 {number}] " if number is not None else ""
        print(f"\n{prefix}{self.question}")
        for idx, choice in enumerate(self.choices, 1):
            print(f"  {idx}. {choice}")

    def is_correct(self, user_answer: int) -> bool:
        """사용자가 입력한 정답 번호 검증"""
        return self.answer == user_answer

    def to_dict(self) -> dict:
        """딕셔너리 변환 (JSON 저장 대비)"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data: dict):
        """딕셔너리로부터 Quiz 객체 생성"""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )


class QuizGame:
    """퀴즈 게임 전체 흐름과 상태를 관리하는 클래스"""

    def __init__(self):
        self.quizzes: list[Quiz] = self._create_default_quizzes()
        self.best_score: int | None = None

    def _create_default_quizzes(self) -> list[Quiz]:
        """기본 탑재 퀴즈 5개 생성 (음식 & 요리 상식 주제)"""
        return [
            Quiz(
                question="한국의 대표적인 발효 식품인 '김치'를 담글 때 가장 대중적으로 많이 쓰이는 주재료 채소는?",
                choices=["배추", "양파", "감자", "당근"],
                answer=1
            ),
            Quiz(
                question="이탈리아의 대표적인 면 요리로 토마토, 크림, 오일 등 다양한 소스와 곁들여 먹는 음식은?",
                choices=["타코", "파스타", "쌀국수", "메밀소바"],
                answer=2
            ),
            Quiz(
                question="'비빔밥'의 본고장으로 가장 널리 알려진 한국의 대표 도시는?",
                choices=["강릉", "부산", "전주", "춘천"],
                answer=3
            ),
            Quiz(
                question="빵이나 쿠키를 구울 때 반죽을 부풀리기 위해 넣는 대표적인 재료는?",
                choices=["베이킹파우더", "고춧가루", "참기름", "간장"],
                answer=1
            ),
            Quiz(
                question="한국에서 생일날 아침에 축하와 감사의 의미로 끓여 먹는 국의 주재료는?",
                choices=["시금치", "미역", "콩나물", "고사리"],
                answer=2
            )
        ]

    def print_menu(self):
        """메인 메뉴 출력"""
        print("\n" + "=" * 30)
        print("      나만의 음식 상식 퀴즈 게임")
        print("=" * 30)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 30)

    def get_menu_choice(self) -> int:
        """메뉴 선택 번호 입력 및 검증"""
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

    def get_quiz_answer(self) -> int:
        """1~4 사이의 정답 번호 안전하게 입력받기"""
        while True:
            try:
                user_input = input("정답 입력 (1-4): ").strip()
                if not user_input:
                    print("입력이 비어 있습니다. 1-4 사이의 숫자를 입력하세요.")
                    continue

                answer = int(user_input)
                if 1 <= answer <= 4:
                    return answer
                else:
                    print("잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
            except ValueError:
                print("잘못된 입력입니다. 숫자를 입력하세요.")

    def play_quiz(self):
        """퀴즈 풀기 진행 및 최고 점수 갱신"""
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"\n▶ 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        correct_count = 0

        for idx, quiz in enumerate(self.quizzes, 1):
            quiz.display(idx)
            user_ans = self.get_quiz_answer()

            if quiz.is_correct(user_ans):
                print("★ 정답입니다!")
                correct_count += 1
            else:
                print(f"X 오답입니다! (정답: {quiz.answer}번 {quiz.choices[quiz.answer - 1]})")

        score = int((correct_count / len(self.quizzes)) * 100)
        print("\n" + "-" * 30)
        print(f"▶ 결과: {len(self.quizzes)}문제 중 {correct_count}문제 정답! ({score}점)")
        print("-" * 30)

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("★ 새로운 최고 점수를 달성했습니다!")

    def add_quiz(self):
        """새로운 퀴즈 등록 및 예외 처리"""
        print("\n새로운 퀴즈를 추가합니다.")

        while True:
            question = input("문제를 입력하세요: ").strip()
            if question:
                break
            print("문제는 비워둘 수 없습니다. 다시 입력해 주세요.")

        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}: ").strip()
                if choice:
                    choices.append(choice)
                    break
                print(f"선택지 {i}번은 비워둘 수 없습니다. 다시 입력해 주세요.")

        while True:
            try:
                answer_input = input("정답 번호 (1-4): ").strip()
                if not answer_input:
                    print("입력이 비어 있습니다. 1-4 사이의 숫자를 입력하세요.")
                    continue
                answer = int(answer_input)
                if 1 <= answer <= 4:
                    break
                print("잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
            except ValueError:
                print("잘못된 입력입니다. 숫자를 입력하세요.")

        new_quiz = Quiz(question=question, choices=choices, answer=answer)
        self.quizzes.append(new_quiz)
        print("\n★ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        """등록된 퀴즈 목록 보기"""
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n■ 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question}")

    def view_score(self):
        """최고 점수 확인 기능"""
        if self.best_score is None:
            print("\n[알림] 아직 퀴즈를 푼 기록이 없습니다. 먼저 퀴즈를 풀어보세요!")
        else:
            print(f"\n★ 최고 점수: {self.best_score}점")

    def run(self):
        """게임 메인 루프 실행"""
        while True:
            try:
                self.print_menu()
                choice = self.get_menu_choice()

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.view_score()
                elif choice == 5:
                    print("\n게임을 종료합니다. 이용해 주셔서 감사합니다!")
                    sys.exit(0)
            except (KeyboardInterrupt, EOFError):
                print("\n\n강제 종료 신호가 감지되어 게임을 안전하게 종료합니다.")
                sys.exit(0)


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()