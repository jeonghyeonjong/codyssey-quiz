from datetime import datetime
import json
import os
import shutil
import sys


class Quiz:
    """개별 4지선다 퀴즈 도메인 모델을 표현하고 스키마 무결성을 검증하는 클래스 (SRP)"""

    REQUIRED_CHOICE_COUNT = 4

    def __init__(
        self,
        question: str,
        choices: list[str],
        answer: int,
        hint: str = "",
    ):
        self.question = self._validate_question(question)
        self.choices = self._validate_choices(choices)
        self.answer = self._validate_answer(answer)
        self.hint = hint.strip() if isinstance(hint, str) else ""

    @staticmethod
    def _validate_question(question: str) -> str:
        if not isinstance(question, str) or not question.strip():
            raise ValueError("퀴즈 문제 지문은 비어 있지 않은 문자열이어야 합니다.")
        return question.strip()

    @classmethod
    def _validate_choices(cls, choices: list[str]) -> list[str]:
        if not isinstance(choices, list) or len(choices) != cls.REQUIRED_CHOICE_COUNT:
            raise ValueError(
                f"선택지는 정확히 {cls.REQUIRED_CHOICE_COUNT}개의 문자열 리스트여야 합니다."
            )
        cleaned: list[str] = []
        for idx, item in enumerate(choices, 1):
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"선택지 {idx}번이 비어 있거나 문자열이 아닙니다.")
            cleaned.append(item.strip())
        if len(set(cleaned)) != cls.REQUIRED_CHOICE_COUNT:
            raise ValueError("선택지 4개에 중복된 보기가 포함되어 있습니다.")
        return cleaned

    @classmethod
    def _validate_answer(cls, answer: int) -> int:
        # Python에서 isinstance(True, int)가 True이므로 bool 타입을 명시적으로 차단
        if isinstance(answer, bool) or not isinstance(answer, int):
            raise ValueError("정답 번호는 정수(int)여야 합니다.")
        if not (1 <= answer <= cls.REQUIRED_CHOICE_COUNT):
            raise ValueError(
                f"정답 번호는 1부터 {cls.REQUIRED_CHOICE_COUNT} 사이의 정수여야 합니다."
            )
        return answer

    def display(self, number: int | None = None) -> None:
        """문제를 콘솔 서식에 맞추어 출력"""
        prefix = f"[문제 {number}] " if number is not None else ""
        print(f"\n{prefix}{self.question}")
        for idx, choice in enumerate(self.choices, 1):
            print(f"  {idx}. {choice}")

    def is_correct(self, user_answer: int) -> bool:
        """사용자가 입력한 정답 번호 일치 여부 판정"""
        return self.answer == user_answer

    def to_dict(self) -> dict:
        """JSON 직렬화를 위한 딕셔너리 변환"""
        payload = {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
        }
        if self.hint:
            payload["hint"] = self.hint
        return payload

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """딕셔너리로부터 스키마 검증을 거쳐 Quiz 인스턴스 역직렬화"""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 항목이 JSON 객체(dict) 형식이 아닙니다.")
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data.get("hint", ""),
        )


class QuizRepository:
    """state.json 원자적(Atomic) 저장 및 .bak 3단계 무결성 복구를 전담하는 영속성 클래스 (SRP)"""

    def __init__(self, base_dir: str | None = None):
        root = base_dir or os.path.dirname(os.path.abspath(__file__))
        self.state_file = os.path.join(root, "state.json")
        self.backup_file = os.path.join(root, "state.json.bak")
        self.temp_file = os.path.join(root, "state.json.tmp")

    @staticmethod
    def create_default_quizzes() -> list[Quiz]:
        """초기 구동 및 복구용 기본 음식 상식 퀴즈 5문항 생성"""
        return [
            Quiz(
                question="한국의 대표적인 발효 식품인 '김치'를 담글 때 가장 대중적으로 많이 쓰이는 주재료 채소는?",
                choices=["배추", "양파", "감자", "당근"],
                answer=1,
                hint="배추김치의 주재료입니다.",
            ),
            Quiz(
                question="이탈리아의 대표적인 면 요리로 토마토, 크림, 오일 등 다양한 소스와 곁들여 먹는 음식은?",
                choices=["타코", "파스타", "쌀국수", "메밀소바"],
                answer=2,
                hint="스파게티, 펜네 등을 통칭하는 이탈리아 면 요리입니다.",
            ),
            Quiz(
                question="'비빔밥'의 본고장으로 가장 널리 알려진 한국의 대표 도시는?",
                choices=["강릉", "부산", "전주", "춘천"],
                answer=3,
                hint="전라북도의 대표적인 전통 문화 도시입니다.",
            ),
            Quiz(
                question="빵이나 쿠키를 구울 때 반죽을 부풀리기 위해 넣는 대표적인 재료는?",
                choices=["베이킹파우더", "고춧가루", "참기름", "간장"],
                answer=1,
                hint="베이킹(제과·제빵)에 쓰이는 팽창제입니다.",
            ),
            Quiz(
                question="한국에서 생일날 아침에 축하와 감사의 의미로 끓여 먹는 국의 주재료는?",
                choices=["시금치", "미역", "콩나물", "고사리"],
                answer=2,
                hint="바다에서 나는 해조류입니다.",
            ),
        ]

    def _parse_and_validate_file(
        self, filepath: str
    ) -> tuple[list[Quiz], int | None, list[dict]] | None:
        """파일을 읽어 전체 스키마 무결성을 검증한 뒤 정상일 때만 상태 튜플 반환"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                raw = json.load(f)

            if not isinstance(raw, dict):
                raise ValueError("루트 JSON 구조는 딕셔너리여야 합니다.")

            raw_quizzes = raw.get("quizzes")
            if not isinstance(raw_quizzes, list) or len(raw_quizzes) == 0:
                raise ValueError("quizzes 필드는 최소 1개 이상의 문제를 담은 리스트여야 합니다.")

            quizzes = [Quiz.from_dict(item) for item in raw_quizzes]

            best_score = raw.get("best_score")
            if best_score is not None:
                if isinstance(best_score, bool) or not isinstance(best_score, int):
                    raise ValueError("best_score는 정수 또는 null이어야 합니다.")
                if not (0 <= best_score <= 100):
                    raise ValueError("best_score 허용 범위(0~100)를 벗어났습니다.")

            raw_history = raw.get("history", [])
            if not isinstance(raw_history, list):
                raw_history = []
            history = [entry for entry in raw_history if isinstance(entry, dict)]

            return quizzes, best_score, history
        except (
            OSError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            print(f"[경고] '{os.path.basename(filepath)}' 데이터 검증 실패: {exc}")
            return None

    def load_state(self) -> tuple[list[Quiz], int | None, list[dict]]:
        """3단계 무결성 복구 정책 수행:
        1단계: state.json 정상 로드 및 스키마 검증
        2단계: state.json 부재/손상 시 state.json.bak 백업본 자동 복구
        3단계: 백업본마저 부재/손상 시 기본 퀴즈 5개로 안전 초기화
        """
        if os.path.exists(self.state_file):
            loaded = self._parse_and_validate_file(self.state_file)
            if loaded is not None:
                quizzes, best_score, history = loaded
                score_label = f"{best_score}점" if best_score is not None else "기록 없음"
                print(
                    f"[안내] 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고 점수: {score_label})"
                )
                return quizzes, best_score, history

            print("[경고] 메인 데이터 파일 손상이 감지되어 백업 파일(.bak) 복구를 시도합니다.")
        else:
            print("[안내] 메인 데이터 파일(state.json)이 존재하지 않습니다.")

        if os.path.exists(self.backup_file):
            recovered = self._parse_and_validate_file(self.backup_file)
            if recovered is not None:
                quizzes, best_score, history = recovered
                print("[성공] 백업 파일(state.json.bak)로부터 데이터를 안전하게 복구했습니다.")
                self.save_state(quizzes, best_score, history)
                return quizzes, best_score, history

        print("[안내] 기본 탑재 음식 상식 퀴즈 5문항으로 안전하게 초기화합니다.")
        default_quizzes = self.create_default_quizzes()
        self.save_state(default_quizzes, None, [])
        return default_quizzes, None, []

    def save_state(
        self,
        quizzes: list[Quiz],
        best_score: int | None,
        history: list[dict] | None = None,
    ) -> bool:
        """임시 파일 기록 후 os.replace 원자적 교체 및 .bak 백업을 수행하여 부분 기록 손상 원천 차단"""
        payload = {
            "quizzes": [q.to_dict() for q in quizzes],
            "best_score": best_score,
            "history": history if history is not None else [],
        }

        try:
            # 1. 임시 파일(.tmp)에 먼저 완전하게 직렬화 및 디스크 플러시
            with open(self.temp_file, "w", encoding="utf-8") as tmp_f:
                json.dump(payload, tmp_f, ensure_ascii=False, indent=2)
                tmp_f.write("\n")
                tmp_f.flush()
                os.fsync(tmp_f.fileno())

            # 2. 기존 정상 state.json이 존재할 때만 백업본(.bak) 갱신
            if os.path.exists(self.state_file) and os.path.getsize(self.state_file) > 0:
                if self._parse_and_validate_file(self.state_file) is not None:
                    shutil.copy2(self.state_file, self.backup_file)

            # 3. 원자적 교체(Atomic Replace)로 메인 파일 갱신
            os.replace(self.temp_file, self.state_file)
            return True
        except OSError as exc:
            print(f"[오류] 데이터 저장 중 파일 시스템 문제가 발생했습니다: {exc}")
            if os.path.exists(self.temp_file):
                try:
                    os.remove(self.temp_file)
                except OSError:
                    pass
            return False


class QuizGame:
    """콘솔 메뉴 제어, 입력 경계값 검증, 퀴즈 진행 및 점수 집계를 총괄하는 컨트롤러 클래스 (SRP)"""

    def __init__(self, repository: QuizRepository | None = None):
        self.repository = repository or QuizRepository()
        self.quizzes, self.best_score, self.history = self.repository.load_state()

    def save_state(self) -> bool:
        """현재 메모리 상의 퀴즈·최고 점수·이력을 영속성 저장소에 위임 저장"""
        return self.repository.save_state(self.quizzes, self.best_score, self.history)

    def print_menu(self) -> None:
        """메인 메뉴 콘솔 출력"""
        print("\n" + "=" * 40)
        print("        나만의 음식 상식 퀴즈 게임")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    @staticmethod
    def _prompt_int_in_range(
        prompt: str, min_val: int, max_val: int
    ) -> int:
        """공백 제거, 빈 문자열, 비숫자, 경계값 범위 밖 입력을 일관되게 방어하는 공통 정수 입력기"""
        while True:
            raw = input(prompt).strip()
            if not raw:
                print(
                    f"[입력 오류] 입력이 비어 있습니다. {min_val}-{max_val} 사이의 숫자를 입력하세요."
                )
                continue
            try:
                value = int(raw)
            except ValueError:
                print(
                    f"[입력 오류] 잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요."
                )
                continue

            if min_val <= value <= max_val:
                return value
            print(
                f"[입력 오류] 허용 범위를 벗어났습니다. {min_val}-{max_val} 사이의 숫자를 입력하세요."
            )

    def get_menu_choice(self) -> int:
        """메뉴 선택 번호(1~5) 입력 검증"""
        return self._prompt_int_in_range("선택: ", 1, 5)

    def get_quiz_answer(self) -> int:
        """4지선다 정답 번호(1~4) 입력 검증"""
        return self._prompt_int_in_range("정답 입력 (1-4): ", 1, 4)

    def play_quiz(self) -> None:
        """저장된 퀴즈 출제, 정오답 판정, 최고 점수 갱신 및 풀이 기록 저장"""
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        print(f"\n▶ 퀴즈를 시작합니다! (총 {total}문제)")
        correct_count = 0

        for idx, quiz in enumerate(self.quizzes, 1):
            quiz.display(idx)
            user_ans = self.get_quiz_answer()

            if quiz.is_correct(user_ans):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                correct_text = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다! (정답: {quiz.answer}번 - {correct_text})")

        score = round((correct_count / total) * 100)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

        is_new_best = self.best_score is None or score > self.best_score
        if is_new_best:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

        self.history.append(
            {
                "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total": total,
                "correct": correct_count,
                "score": score,
            }
        )
        self.save_state()

    def add_quiz(self) -> None:
        """대화형 입력 검증을 통해 새로운 4지선다 퀴즈를 등록하고 즉시 파일에 영속화"""
        print("\n📌 새로운 퀴즈를 추가합니다.")

        while True:
            question = input("문제를 입력하세요: ").strip()
            if question:
                break
            print("[입력 오류] 문제는 비워둘 수 없습니다. 다시 입력해 주세요.")

        choices: list[str] = []
        for idx in range(1, Quiz.REQUIRED_CHOICE_COUNT + 1):
            while True:
                choice = input(f"선택지 {idx}: ").strip()
                if not choice:
                    print(f"[입력 오류] 선택지 {idx}번은 비워둘 수 없습니다.")
                    continue
                if choice in choices:
                    print("[입력 오류] 이미 입력한 선택지와 중복됩니다. 다른 보기를 입력하세요.")
                    continue
                choices.append(choice)
                break

        answer = self._prompt_int_in_range("정답 번호 (1-4): ", 1, 4)

        new_quiz = Quiz(question=question, choices=choices, answer=answer)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n✅ 퀴즈가 추가되었으며 state.json에 안전하게 저장되었습니다!")

    def list_quizzes(self) -> None:
        """등록된 전체 퀴즈 목록 출력"""
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question}")
        print("-" * 40)

    def view_score(self) -> None:
        """최고 점수 및 최근 풀이 히스토리 조회"""
        if self.best_score is None:
            print("\n[알림] 아직 퀴즈를 푼 기록이 없습니다. 먼저 퀴즈를 풀어보세요!")
            return

        print(f"\n🏆 최고 점수: {self.best_score}점")
        if self.history:
            recent = self.history[-5:]
            print(f"📊 최근 플레이 기록 (최근 {len(recent)}회 / 총 {len(self.history)}회):")
            for idx, rec in enumerate(recent, 1):
                print(
                    f"  {idx}. [{rec.get('played_at', '-')}] "
                    f"{rec.get('total', 0)}문제 중 {rec.get('correct', 0)}개 정답 ({rec.get('score', 0)}점)"
                )

    def run(self) -> None:
        """메인 콘솔 루프 실행 및 KeyboardInterrupt / EOFError 안전 종료 보장"""
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
                    return
            except (KeyboardInterrupt, EOFError):
                self.save_state()
                print("\n\n[안전 종료] 종료 신호가 감지되어 현재 상태를 저장한 뒤 정상 종료합니다.")
                return


def main() -> None:
    try:
        game = QuizGame()
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n[안전 종료] 프로그램을 정상 종료합니다.")


if __name__ == "__main__":
    main()
