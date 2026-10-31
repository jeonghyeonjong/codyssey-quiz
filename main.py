import json
import os
import shutil
import sys


class Quiz:
    """개별 퀴즈를 표현하는 클래스 (단일 책임 원칙 준수)"""

    def __init__(self, question: str, choices: list[str], answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number: int | None = None):
        """문제를 콘솔에 서식에 맞추어 출력"""
        prefix = f"[문제 {number}] " if number is not None else ""
        print(f"\n{prefix}{self.question}")
        for idx, choice in enumerate(self.choices, 1):
            print(f"  {idx}. {choice}")

    def is_correct(self, user_answer: int) -> bool:
        """사용자가 입력한 정답 번호 일치 여부 검증"""
        return self.answer == user_answer

    def to_dict(self) -> dict:
        """JSON 저장을 위한 딕셔너리 직렬화"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """딕셔너리로부터 Quiz 객체 역직렬화"""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )


class QuizGame:
    """퀴즈 게임 라이프사이클 및 데이터 영속성을 총괄하는 클래스"""

    STATE_FILE = "state.json"
    BACKUP_FILE = "state.json.bak"

    def __init__(self):
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.load_state()

    def _create_default_quizzes(self) -> list[Quiz]:
        """기본 탑재 퀴즈 5개 생성 (음식 & 요리 기초 상식 주제)"""
        return [
            Quiz(
                question="한국의 대표적인 발효 식품인 '김치'를 담글 때 가장 대중적으로 많이 쓰이는 주재료 채소는?",
                choices=["배추", "양파", "감자", "당근"],
                answer=1,
            ),
            Quiz(
                question="이탈리아의 대표적인 면 요리로 토마토, 크림, 오일 등 다양한 소스와 곁들여 먹는 음식은?",
                choices=["타코", "파스타", "쌀국수", "메밀소바"],
                answer=2,
            ),
            Quiz(
                question="'비빔밥'의 본고장으로 가장 널리 알려진 한국의 대표 도시는?",
                choices=["강릉", "부산", "전주", "춘천"],
                answer=3,
            ),
            Quiz(
                question="빵이나 쿠키를 구울 때 반죽을 부풀리기 위해 넣는 대표적인 재료는?",
                choices=["베이킹파우더", "고춧가루", "참기름", "간장"],
                answer=1,
            ),
            Quiz(
                question="한국에서 생일날 아침에 축하와 감사의 의미로 끓여 먹는 국의 주재료는?",
                choices=["시금치", "미역", "콩나물", "고사리"],
                answer=2,
            ),
        ]

    def _load_from_file(self, filepath: str) -> bool:
        """지정된 파일 경로에서 JSON 파싱 및 데이터 로드 (실패 시 False 반환)"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                self.best_score = data.get("best_score")
            print(
                f"[안내] '{filepath}' 로드 완료: 퀴즈 {len(self.quizzes)}개, 최고 점수: {self.best_score if self.best_score is not None else '기록 없음'}"
            )
            return True
        except (json.JSONDecodeError, KeyError, PermissionError, Exception) as e:
            print(f"[경고] '{filepath}' 파싱 실패: {e}")
            return False

    def load_state(self):
        """데이터 로드 및 3단계 무결성 복구 정책
        1단계: state.json 정상 로드
        2단계: state.json 손상 시 state.json.bak 백업 파일로 자동 복구
        3단계: 백업본 부재 또는 동시 손상 시 기본 퀴즈 5개로 복원
        """
        # 1. 메인 파일이 아예 없는 경우
        if not os.path.exists(self.STATE_FILE):
            if os.path.exists(self.BACKUP_FILE):
                print(f"[안내] 메인 파일이 없어 백업 파일('{self.BACKUP_FILE}')에서 복구를 시도합니다.")
                if self._load_from_file(self.BACKUP_FILE):
                    self.save_state()
                    return
            print(f"[안내] 데이터 파일이 존재하지 않아 기본 퀴즈 5개를 새로 생성합니다.")
            self.quizzes = self._create_default_quizzes()
            self.best_score = None
            self.save_state()
            return

        # 2. 메인 파일이 존재하지만 파싱에 실패한 경우
        if not self._load_from_file(self.STATE_FILE):
            print(f"[경고] '{self.STATE_FILE}' 손상이 감지되었습니다. 백업 파일에서 복구를 시도합니다.")
            if os.path.exists(self.BACKUP_FILE) and self._load_from_file(self.BACKUP_FILE):
                print("[성공] 백업 파일로부터 데이터를 안전하게 복구했습니다.")
                self.save_state()
            else:
                print(f"[안내] 백업 파일 복구 실패. 기본 퀴즈 데이터로 안전하게 초기화합니다.")
                self.quizzes = self._create_default_quizzes()
                self.best_score = None
                self.save_state()

    def save_state(self):
        """저장 전 백업 파일(state.json.bak) 생성 및 state.json 안전 저장"""
        # 기존 정상 파일이 존재하면 쓰기 직전 안전 백업 생성 (원자적 보존)
        if os.path.exists(self.STATE_FILE) and os.path.getsize(self.STATE_FILE) > 0:
            try:
                shutil.copy2(self.STATE_FILE, self.BACKUP_FILE)
            except Exception as e:
                print(f"[주의] 백업 파일 생성 중 오류: {e}")

        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(self.STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[오류] 데이터 파일 저장 중 문제가 발생했습니다: {e}")

    def print_menu(self):
        """메인 메뉴 콘솔 출력"""
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
        """메뉴 선택 번호 입력 및 경계값(1, 5) 유효성 검증"""
        while True:
            try:
                user_input = input("선택: ").strip()
                if not user_input:
                    print("입력이 비어 있습니다. 메뉴 번호를 입력하세요.")
                    continue

                choice = int(user_input)
                # 경계값 검증: 1 이상 5 이하의 메뉴 번호만 허용
                if 1 <= choice <= 5:
                    return choice
                else:
                    print("잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            except ValueError:
                print("잘못된 입력입니다. 숫자를 입력하세요.")

    def get_quiz_answer(self) -> int:
        """정답 번호 입력 및 경계값(1, 4) 유효성 검증"""
        while True:
            try:
                user_input = input("정답 입력 (1-4): ").strip()
                if not user_input:
                    print("입력이 비어 있습니다. 1-4 사이의 숫자를 입력하세요.")
                    continue

                answer = int(user_input)
                # 경계값 검증: 4지선다 보기는 정확히 1부터 4 사이의 정수만 허용
                if 1 <= answer <= 4:
                    return answer
                else:
                    print("잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
            except ValueError:
                print("잘못된 입력입니다. 숫자를 입력하세요.")

    def play_quiz(self):
        """퀴즈 풀기 세션 진행 및 점수 자동 저장"""
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
                print(
                    f"X 오답입니다! (정답: {quiz.answer}번 {quiz.choices[quiz.answer - 1]})"
                )

        score = int((correct_count / len(self.quizzes)) * 100)
        print("\n" + "-" * 30)
        print(f"▶ 결과: {len(self.quizzes)}문제 중 {correct_count}문제 정답! ({score}점)")
        print("-" * 30)

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.save_state()
            print("★ 새로운 최고 점수를 달성하여 저장했습니다!")

    def add_quiz(self):
        """새로운 퀴즈 등록 및 영속화"""
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
                # 경계값 검증: 1과 4 사이의 정수만 허용
                if 1 <= answer <= 4:
                    break
                print("잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
            except ValueError:
                print("잘못된 입력입니다. 숫자를 입력하세요.")

        new_quiz = Quiz(question=question, choices=choices, answer=answer)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n★ 퀴즈가 추가되었으며 파일(state.json)에 저장되었습니다!")

    def list_quizzes(self):
        """등록된 퀴즈 전체 목록 요약 출력"""
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n■ 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question}")

    def view_score(self):
        """최고 점수 확인"""
        if self.best_score is None:
            print("\n[알림] 아직 퀴즈를 푼 기록이 없습니다. 먼저 퀴즈를 풀어보세요!")
        else:
            print(f"\n★ 최고 점수: {self.best_score}점")

    def run(self):
        """게임 메인 루프 실행 및 안전 종료 처리"""
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
                    self.save_state()
                    print("\n게임을 안전하게 저장하고 종료합니다. 이용해 주셔서 감사합니다!")
                    sys.exit(0)
            except (KeyboardInterrupt, EOFError):
                self.save_state()
                print("\n\n강제 종료 신호가 감지되어 현재 상태를 저장 후 안전하게 종료합니다.")
                sys.exit(0)


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()