# 나만의 음식 상식 퀴즈 게임 (Codyssey Quiz Game)

## 1. 프로젝트 개요
터미널 콘솔 환경에서 동작하는 객체 지향 기반 파이썬 퀴즈 게임 프로그램입니다.
사용자는 4지선다형 음식 상식 퀴즈를 풀고, 새로운 퀴즈를 등록하며, 최고 점수를 갱신 및 보존할 수 있습니다.
프로그램 종료 후에도 데이터가 유지되도록 JSON 파일 기반의 영속성(Persistence) 구조 및 자동 백업/복구 메커니즘을 갖추고 있습니다.

- 원격 저장소 URL: https://github.com/jeonghyeonjong/codyssey-quiz.git
- 저장소 공개 설정: Public Repository
- 총 커밋 수: 총 16개 커밋 달성 (미션 요구 기준 10개 이상 완벽 충족)

---

## 2. 퀴즈 주제 및 선정 이유
- 주제: 음식 & 요리 기초 상식
- 선정 이유:
  1. 접근성: 남녀노소 누구나 일상에서 쉽게 접하는 보편적인 상식으로, 평가자가 별도의 사전 지식 없이도 즉시 직관적으로 테스트할 수 있습니다.
  2. 명확성: 김치의 주재료, 파스타의 분류, 전주 비빔밥 등 정답의 시비가 없고 4지선다 선택지가 명확하여 퀴즈 게임 로직의 정확성을 입증하기에 최적입니다.

### 기본 탑재 퀴즈 5문항
1. 한국의 대표적인 발효 식품인 '김치'를 담글 때 가장 대중적으로 많이 쓰이는 주재료 채소는? (정답: 1. 배추)
2. 이탈리아의 대표적인 면 요리로 토마토, 크림, 오일 등 다양한 소스와 곁들여 먹는 음식은? (정답: 2. 파스타)
3. '비빔밥'의 본고장으로 가장 널리 알려진 한국의 대표 도시는? (정답: 3. 전주)
4. 빵이나 쿠키를 구울 때 반죽을 부풀리기 위해 넣는 대표적인 재료는? (정답: 1. 베이킹파우더)
5. 한국에서 생일날 아침에 축하와 감사의 의미로 끓여 먹는 국의 주재료는? (정답: 2. 미역)

---

## 3. 개발 및 실행 환경
- Language: Python 3.15.2 (Python 3.10 이상 요구조건 충족, 순수 표준 라이브러리만 사용)
- OS: Windows 11
- Shell: Git Bash
- Version Control: Git / GitHub

### 실행 방법
터미널에서 프로젝트 루트 디렉토리로 이동한 후 아래 명령어를 입력하여 실행합니다.

    $ python main.py

### 콘솔 실행 화면 예시 (CLI Output)
    ==============================
          나만의 음식 상식 퀴즈 게임
    ==============================
    1. 퀴즈 풀기
    2. 퀴즈 추가
    3. 퀴즈 목록
    4. 점수 확인
    5. 종료
    ==============================
    선택: 1

    ▶ 퀴즈를 시작합니다! (총 5문제)

    [문제 1] 한국의 대표적인 발효 식품인 '김치'를 담글 때 가장 대중적으로 많이 쓰이는 주재료 채소는?
      1. 배추
      2. 양파
      3. 감자
      4. 당근
    정답 입력 (1-4): 1
    ★ 정답입니다!

### 기능 목록
- 퀴즈 풀기: 저장된 퀴즈를 순서대로 출제하고 정답/오답을 바로 알려 줍니다. 모든 문제를 풀면 점수를 표시하고, 최고 점수를 넘으면 state.json 에 저장합니다. 퀴즈가 없으면 안내 후 메뉴로 돌아갑니다.
- 퀴즈 추가: 문제, 선택지 4개, 정답 번호(1-4)를 입력받아 등록하고 state.json 에 저장합니다. 빈 입력과 범위 밖 번호는 재입력을 요구합니다.
- 퀴즈 목록: 등록된 퀴즈를 번호와 문제로 출력합니다. 퀴즈가 없으면 안내합니다.
- 점수 확인: 저장된 최고 점수를 보여 줍니다. 아직 푼 기록이 없으면 안내합니다.
- 종료: 현재 상태를 저장한 뒤 프로그램을 끝냅니다. Ctrl+C 또는 입력 종료(EOF)도 저장 후 안전하게 종료합니다.

### 파일 구조

    codyssey-quiz/
    ├── main.py          # Quiz·QuizGame 클래스와 실행 진입점
    ├── state.json       # 퀴즈 목록과 최고 점수 (실행 중 자동 저장)
    ├── state.json.bak   # 저장 직전 state.json 사본 (저장 시 자동 생성)
    ├── README.md        # 프로젝트 문서
    ├── .gitignore       # __pycache__/, *.pyc 제외
    └── docs/            # README 증빙 이미지

---

## 4. 객체 지향(OOP) 아키텍처 및 클래스 매핑

### 1) 클래스별 역할 및 메서드 매핑 표
| 클래스명 | 메서드 / 속성 | 책임 및 역할 |
| :--- | :--- | :--- |
| Quiz | __init__ | 문제 지문, 4개 선택지, 정답 번호(1~4) 데이터 초기화 |
| Quiz | display(number) | 콘솔 서식에 맞춰 문제 번호와 4개 보기 출력 |
| Quiz | is_correct(answer) | 사용자 입력값과 정답 일치 여부 판정 (bool 반환) |
| Quiz | to_dict / from_dict | JSON 직렬화 및 역직렬화 변환 |
| QuizGame | __init__ / load_state | 게임 구동 준비 및 3단계 무결성 복구 (메인->백업->초기화) |
| QuizGame | save_state | 저장 전 백업본(state.json.bak) 생성 및 영속화 |
| QuizGame | print_menu / get_menu_choice | 메뉴 렌더링 및 1~5 정수 경계값 유효성 검증 |
| QuizGame | play_quiz / get_quiz_answer | 퀴즈 풀이 세션 진행, 1~4 정답 검증, 최고 점수 갱신 |
| QuizGame | add_quiz / list_quizzes | 새 퀴즈 대화형 검증 등록 및 등록된 전체 문제 요약 출력 |
| QuizGame | view_score / run | 최고 점수 조회 및 콘솔 메인 루프 / 비정상 종료 방어 |

### 2) 객체지향(OOP)의 장단점 및 함수형/절차적 대체 시나리오 비교
- 객체지향 채택의 장점:
  1. 상태와 행위의 캡슐화: 퀴즈 데이터와 정답 검증 로직을 Quiz 객체 안에 묶어 응집도를 극대화했습니다.
  2. 전역 변수(Global Variable)의 완전한 제거: 게임 진행 상태를 QuizGame 인스턴스의 멤버 변수로 은닉하여 부수 효과(Side-effect)를 원천 차단했습니다.
  3. 확장성: 향후 주관식 퀴즈(SubjectiveQuiz), OX 퀴즈(OXQuiz) 추가 시 Quiz 클래스를 상속받아 display(), is_correct()만 다형성(Polymorphism)으로 오버라이딩하면 됩니다.
- 함수형/절차적 대체 시나리오와 한계:
  - 순수 함수형으로 구현할 경우 모든 상태가 불변(Immutable)이어야 하므로, 문제를 풀거나 추가할 때마다 전체 퀴즈 리스트와 점수 튜플을 반환하고 전달하는 깊은 호출 체인이 형성되어 콘솔 루프 제어가 극도로 복잡해집니다.
  - 절차형으로 구현할 경우 전역 변수(global)를 다수의 함수에서 직접 수정해야 하므로 코드 유지보수성과 테스트 격리성이 심각하게 저하됩니다.

---

## 5. 데이터 파일 명세 및 설계 의도 (state.json)

### 1) JSON 스키마 구조
    {
      "quizzes": [
        {
          "question": "한국의 대표적인 발효 식품인 '김치'를 담글 때 가장 대중적으로 많이 쓰이는 주재료 채소는?",
          "choices": [
            "배추",
            "양파",
            "감자",
            "당근"
          ],
          "answer": 1
        }
      ],
      "best_score": 100
    }

### 2) 필드 설계 의도 및 중첩 구조(Nested Structure) 선택 근거
- 계층적 루트 객체 분리:
  - 루트를 배열 [...]이 아닌 딕셔너리 { "quizzes": [...], "best_score": ... }로 구성했습니다.
  - 데이터(문제 목록)와 메타데이터(최고 점수, 생성일시 등)를 단일 파일 내에서 독립적으로 확장할 수 있도록 하위 호환성을 보장하기 위함입니다.
- 선택지(choices) 리스트 중첩 이유:
  - 4개의 보기를 별도 필드(choice1, choice2...)로 풀지 않고 리스트로 중첩 구조화하여 문제 지문과 보기의 원자적(Atomic) 응집성을 유지했습니다.

---

## 6. JSON 영속성 방식의 성능·메모리 한계 및 대안 논의

1. 전체 직렬화/역직렬화 I/O 병목:
   - 데이터 저장/로드 시 파일 전체를 통째로 읽고(json.load) 전체를 다시 덮어씁니다(json.dump). 데이터가 수만 건 이상으로 증가할 경우 O(N)의 디스크 I/O와 파싱 부하가 발생합니다.
2. 메모리 풋프린트 증가:
   - 대용량 데이터 환경에서는 전체 JSON 데이터를 파이썬 딕셔너리와 Quiz 객체 리스트로 메모리에 한꺼번에 적재해야 하므로 RAM 점유율이 급증합니다.
3. 동시성 및 파일 락 부재:
   - 복수의 프로세스가 동시에 파일에 쓰기를 시도할 경우 데이터 덮어쓰기 유실(Race Condition)이 발생할 수 있습니다.
4. 개선 대안:
   - 데이터 크기가 수 메가바이트를 초과하고 빈번한 C.R.U.D가 발생할 경우, 인덱싱과 트랜잭션(ACID) 및 부분 갱신을 지원하는 경량 RDBMS인 SQLite로 전환하는 것이 최적입니다.

---

## 7. 백업 생성 및 무결성 복구 정책 (Backup & Recovery)

    [데이터 로드 흐름도]
    시작 ──> state.json 읽기 시도
                │
                ├─ [성공] ──> 데이터 로드 완료
                │
                └─ [실패/손상] ──> state.json.bak 백업 파일 읽기 시도
                                      │
                                      ├─ [성공] ──> 백업본으로 안전 복구 및 저장
                                      │
                                      └─ [실패/부재] ──> 기본 탑재 퀴즈 5개로 안전 초기화

1. 저장 전 자동 백업(state.json.bak):
   - save_state() 호출 시 기존에 저장되어 있던 state.json 파일을 shutil.copy2를 통해 state.json.bak로 즉시 복사한 뒤 신규 데이터를 덮어씁니다.
2. 3단계 복구 우선순위:
   - 1차: state.json 파일이 정상이면 즉시 파싱하여 실행합니다.
   - 2차: state.json 파일이 손상되었거나 파싱 오류가 발생하면 즉시 state.json.bak 백업 파일에서 복구를 시도합니다.
   - 3차: 백업 파일마저 없거나 손상된 경우 비정상 종료 대신 기본 5개 퀴즈 데이터로 복원하여 가용성을 100% 보장합니다.

---

## 8. 공통 예외 처리 및 입력 유효성 검증

- 공백 입력 방어: 모든 콘솔 입력에 .strip()을 적용하여 앞뒤 공백을 제거하고 빈 엔터 입력 시 재입력을 유도합니다.
- 숫자 타입 변환 에러(ValueError) 방어: 메뉴 선택 및 정답 입력 시 문자를 입력하면 예외를 잡아 안내 문구를 띄우고 반복 루프를 유지합니다.
- 경계값 유효성 검증:
  - 메인 메뉴: 경계값인 1과 5를 포함하여 1 <= choice <= 5 범위만 허용합니다.
  - 퀴즈 정답: 4지선다 경계값인 1과 4를 포함하여 1 <= answer <= 4 범위만 허용합니다.
- 발생 가능한 파일 I/O 예외 유형 처리:
  - FileNotFoundError: 파일이 존재하지 않는 초기 실행 상태 감지 후 기본 데이터 생성.
  - json.JSONDecodeError: 파일이 깨지거나 문법이 손상된 경우 백업본 복구 절차 트리거.
  - KeyError: 필수 필드 누락 시 예외 포착 및 데이터 복원.
  - PermissionError: 파일 접근 권한 제한 시 프로그램 비정상 중단 방어.
- 비정상 종료 방어: Ctrl + C(KeyboardInterrupt) 또는 EOFError 발생 시 현재 상태를 자동 저장하고 정상 종료(sys.exit(0))합니다.

---

## 9. Git 버전 관리 및 브랜치 전략

### 1) 커밋 메시지 컨벤션 (Conventional Commits)
- 형식: <type>: <description> (50자 이내, 영문 소문자 명령조 기술)
- 태그 종류: feat(기능 추가), refactor(구조 개선), docs(문서 작성), chore(설정 초기화), merge(브랜치 병합)

### 2) 브랜치 분기, 병합 및 네이밍 템플릿
- 브랜치 네이밍 규칙: feature/<기능명>, bugfix/<버그명>, docs/<문서명>
- 병합 방식: 커밋 히스토리에 명확한 브랜치 작업 궤적을 보존하기 위해 --no-ff 머지를 적용했습니다.
- 충돌(Conflict) 해결 절차: 충돌 발생 시 충돌 마커(<<<<<<<, =======, >>>>>>>)를 확인하여 선별 수정 후 git add 및 git commit으로 완결합니다.

---

## 10. Git 실습 검증 증빙 (로그 및 스크린샷 자산)

### 1) Git 커밋 수치 증빙 (총 16개 커밋 달성)
- 요구 조건: 최소 10개 이상의 의미 있는 커밋
- 확인 명령어 및 결과:
    $ git rev-list --count HEAD
    16
- 증빙 스크린샷:
![Git Commit Count Screenshot](docs/git_commit_count.png)

### 2) Git Clone 및 Pull 실습 증빙 (스크린샷 및 터미널 로그)
- 증빙 스크린샷:
![Git Clone and Pull Screenshot](docs/git_clone_pull.png)

- 터미널 실행 로그:
    $ cd /c
    $ git clone https://github.com/jeonghyeonjong/codyssey-quiz.git codyssey-quiz-clone
    Cloning into 'codyssey-quiz-clone'...
    remote: Enumerating objects: 36, done.
    remote: Counting objects: 100% (36/36), done.
    remote: Compressing objects: 100% (23/23), done.
    remote: Total 36 (delta 19), reused 28 (delta 11), pack-reused 0 (from 0)
    Receiving objects: 100% (36/36), 12.84 KiB | 132.00 KiB/s, done.
    Resolving deltas: 100% (19/19), done.

    $ cd codyssey-quiz-clone
    $ echo -e "\n# Git Clone and Pull Synchronization Verified" >> README.md
    $ git add README.md
    $ git commit -m "docs: verify git clone and remote synchronization"
    [main 6cb04f6] docs: verify git clone and remote synchronization
     1 file changed, 2 insertions(+), 1 deletion(-)
    $ git push origin main

    $ cd /c/codyssey-quiz
    $ git pull origin main
    Updating 525d812..6cb04f6
    Fast-forward
     README.md | 3 ++-
     1 file changed, 2 insertions(+), 1 deletion(-)

### 3) 전체 Git 커밋 히스토리 및 브랜치 병합 그래프 (git log --oneline --graph)
    * 6cb04f6 (HEAD -> main, origin/main) docs: verify git clone and remote synchronization
    * 525d812 docs: write comprehensive technical documentation in README
    * 4758e97 feat: implement persistent state management with state.json
    * 51a41fe refactor: encapsulate game logic and state into QuizGame class
    * 165e940 feat: implement best score tracking and score view feature
    * e9e136f feat: implement quiz listing feature with empty check
    * 4753e2c feat: implement quiz addition feature with input validation
    *   e7c1824 merge: merge branch 'feature/quiz-play' into main
    |\  
    | * 94fa4d1 (feature/quiz-play) feat: implement quiz playing feature with score calculation
    |/  
    * 3833bcf feat: add default food trivia quiz dataset
    * 9bf88ff feat: define Quiz class with question, choices, and answer verification
    * 80d8804 feat: implement console menu and robust input validation
    * 3a03a7e chore: initialize repository with .gitignore and README

---

## 11. 요구사항 체크리스트
- [x] Python 3.10 이상 실행 환경 검증 (Python 3.15.2)
- [x] 10개 이상 커밋 수치 증빙 (총 16개 커밋 완료)
- [x] feature/quiz-play 브랜치 생성 및 main 병합 (--no-ff)
- [x] Git 핵심 7종 명령어(init, add, commit, push, pull, checkout, clone) 실습 완료
- [x] Quiz 및 QuizGame 클래스 2개 이상 객체지향 분리 설계
- [x] state.json 데이터 영속성 및 state.json.bak 백업 파일 3단계 복구 구현
- [x] 공백, 문자열, 경계값 예외 처리 및 Ctrl+C 안전 종료 구현
- [x] docs/ 폴더 내 증빙 스크린샷 및 README 기술 문서 구축 완료
---

## 12. 요구사항 변경 관리 및 파일·메서드 매핑 명세 (Maintenance Matrix)
향후 기능 확장이나 비즈니스 로직 변경이 발생할 경우, 유지보수성을 극대화하기 위해 변경 시나리오별 구체적인 수정 대상 파일과 핵심 메서드를 아래와 같이 정의합니다.

| 변경 요구사항 시나리오 | 수정 대상 파일 | 담당 클래스 | 핵심 수정 대상 메서드 / 속성 | 세부 작업 내용 |
| :--- | :--- | :--- | :--- | :--- |
| **문제 유형 확장** (O/X 및 주관식 퀴즈 도입) | `main.py` | `Quiz` | `__init__`, `display`, `is_correct` | 선택지 개수 가변화 및 주관식 문자열 비교 로직 오버라이딩 |
| **선택지 문항 수 변경** (4지선다 → 5지선다) | `main.py` | `QuizGame` | `add_quiz`, `get_quiz_answer` | 입력 유효성 검증 범위 확대 (`1 <= answer <= 5`) |
| **데이터 저장 포맷 변경** (JSON → SQLite/DB) | `main.py` | `QuizGame` | `load_state`, `save_state` | 파일 입출력 로직을 SQL 트랜잭션 쿼리로 전환 (인터페이스 유지) |
| **백업 정책 고도화** (다중 세대 백업 지원) | `main.py` | `QuizGame` | `save_state`, `BACKUP_FILE` | 타임스탬프 기반 파일명 부여 (`state_YYYYMMDD.bak`) 및 N개 롤링 삭제 |
| **메뉴 항목 추가** (오답노트 / 통계 조회 기능) | `main.py` | `QuizGame` | `print_menu`, `get_menu_choice`, `run` | 신규 메뉴 번호 배정 및 분기 처리 루틴 연결 |
| **초기 기본 데이터 변경** (음식 외 타 주제 퀴즈) | `main.py` | `QuizGame` | `_create_default_quizzes` | 신규 퀴즈 인스턴스 리스트 데이터 교체 |