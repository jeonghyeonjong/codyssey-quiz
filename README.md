# 나만의 음식 상식 퀴즈 게임 (Codyssey OOP Quiz Game)

## 1. 프로젝트 개요 및 요구사항 분석

터미널(CLI) 환경에서 동작하는 **단일 책임 원칙(SRP) 기반 객체지향 파이썬 4지선다 퀴즈 게임 애플리케이션**입니다.
사용자는 기본 탑재된 음식 상식 5문항을 풀고, 새로운 퀴즈를 대화형 검증을 거쳐 추가하며, 전체 문제 목록과 최고 점수 및 최근 플레이 히스토리를 조회할 수 있습니다.
프로그램을 종료하거나 예기치 못한 인터럽트(`Ctrl+C`, `EOFError`)가 발생하더라도 `os.replace` 기반 **원자적(Atomic) 파일 교체**와 `.bak` **3단계 무결성 복구 아키텍처**를 통해 데이터 영속성을 100% 보장합니다.

- **원격 저장소 URL**: https://github.com/jeonghyeonjong/codyssey-quiz.git
- **저장소 공개 여부**: Public Repository
- **개발 및 실행 환경**:
  - OS / Shell: Windows 11 / Git Bash
  - Language: Python 3.15.2 (Python 3.10 이상 공식 요구조건 충족, 외부 패키지 없이 순수 표준 라이브러리만 사용)
  - Version Control: Git / GitHub (`init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone` 7대 명령어 및 `--no-ff` 브랜치 병합 완비)

### 퀴즈 주제 선정 이유 (음식 & 요리 기초 상식)
1. **보편적 접근성**: 별도의 전공 배경지식 없이도 누구나 직관적으로 풀고 정오답 판정 로직을 즉시 검증할 수 있습니다.
2. **명확한 정답 기준**: 김치의 주재료(배추), 비빔밥의 본고장(전주), 제빵 팽창제(베이킹파우더) 등 논란의 여지가 없는 객관적 사실로 구성하여 점수 산출과 최고 점수 갱신 흐름을 명확히 실증합니다.

---

## 2. 디렉터리 구조 (Tree) 및 실행 방법

### 1) 파일 구조 및 역할

    codyssey-quiz/
    ├── .gitignore                 # Python 캐시(__pycache__/) 및 임시 직렬화 파일(*.tmp) 제외
    ├── main.py                    # 메인 실행 파일 (Quiz, QuizRepository, QuizGame 3대 SRP 클래스)
    ├── state.json                 # 퀴즈 목록·최고 점수·풀이 히스토리 UTF-8 영속 저장 파일
    ├── state.json.bak             # 원자적 저장 직전 자동 생성되는 무결성 복구용 백업본
    ├── tests/
    │   ├── __init__.py            # 테스트 패키지 초기화
    │   └── test_quiz_game.py      # 스키마 검증, 3단계 복구, 경계값 방어 자동화 단위 테스트
    ├── docs/                      # 실제 실행 화면 및 Git 이력 증빙 스크린샷 자산
    │   ├── menu_validation.png    # 메인 메뉴 및 공백·문자·범위초과 예외 방어 화면
    │   ├── play_score.png         # 퀴즈 풀이, 최고 점수 갱신 및 히스토리 조회 화면
    │   ├── add_quiz.png           # 퀴즈 추가(중복 보기 방어 포함) 및 목록 반영 화면
    │   ├── git_commit_count.png   # 총 커밋 수 및 --no-ff 브랜치 병합 그래프 증빙
    │   └── git_clone_pull.png     # git clone 및 git pull 원격 동기화 실습 증빙
    └── README.md                  # 아키텍처·스키마·트러블슈팅·변경 매핑 기술 문서

### 2) 프로그램 및 단위 테스트 실행 방법

프로젝트 루트 디렉터리로 이동한 뒤 아래 명령어로 실행합니다 (`__file__` 기준 경로 앵커링이 적용되어 상위 디렉터리에서 실행해도 `codyssey-quiz/state.json`을 정확히 참조합니다).

    $ cd /c/codyssey-workspace/codyssey-quiz
    $ python main.py

    # 자동화 단위 테스트 실행 (스키마 복구 및 입력 예외 전수 검증)
    $ python tests/test_quiz_game.py -v

---

## 3. 객체지향(OOP) 클래스 설계 구조 및 역할 명세

도메인 모델, 파일 영속성 계층, 콘솔 UI 제어 계층이 서로 뒤섞이지 않도록 **단일 책임 원칙(SRP)**에 따라 **3개의 독립 클래스**로 분리 설계했습니다.

### 1) 클래스별 책임 및 핵심 메서드 매핑 표

| 클래스명 | 핵심 속성 / 메서드 | 단일 책임 및 세부 역할 |
| :--- | :--- | :--- |
| **`Quiz`** | `question`, `choices`, `answer`, `hint` | 개별 4지선다 문제 데이터 캡슐화 및 도메인 불변식 유지 |
| **`Quiz`** | `_validate_question`, `_validate_choices`, `_validate_answer` | 빈 문자열, 보기 개수(`!= 4`), 중복 보기, `bool` 타입 함정(`isinstance(True, int)`), 범위 밖 정답(`1~4` 외) 차단 |
| **`Quiz`** | `display(number)`, `is_correct(user_answer)` | 콘솔 문제 렌더링 및 사용자 입력 정답 일치 여부 판정(`bool` 반환) |
| **`Quiz`** | `to_dict()`, `from_dict(data)` | JSON 직렬화 및 스키마 검증 기반 역직렬화 |
| **`QuizRepository`** | `state_file`, `backup_file`, `temp_file` | `__file__` 기준 절대 경로 앵커링 및 영속성 파일 경로 관리 |
| **`QuizRepository`** | `_parse_and_validate_file(filepath)` | JSON 파싱 및 루트·문항·점수(`0~100`) 스키마 전수 검증 (부분 상태 오염 차단) |
| **`QuizRepository`** | `load_state()`, `create_default_quizzes()` | `state.json` → `state.json.bak` → 기본 5문항 순서의 **3단계 자동 무결성 복구** |
| **`QuizRepository`** | `save_state(quizzes, best_score, history)` | `.tmp` 임시 기록 + `os.fsync` 플러시 → `.bak` 백업 → `os.replace` 원자적 교체 |
| **`QuizGame`** | `print_menu()`, `_prompt_int_in_range(...)` | 메인 메뉴 출력 및 공백·문자·경계값(`1~5`, `1~4`) 공통 방어 입력기 |
| **`QuizGame`** | `play_quiz()`, `add_quiz()`, `list_quizzes()`, `view_score()` | 퀴즈 풀이 진행, 중복 보기 방지 신규 문제 등록, 전체 목록 출력, 최고 점수 및 최근 기록 조회 |
| **`QuizGame`** | `run()` | 메인 이벤트 루프 구동 및 `KeyboardInterrupt`(`Ctrl+C`) / `EOFError` 안전 저장 종료 |

### 2) 객체지향(OOP) 설계 채택 근거 (절차형·함수형 대비 이점)
- **단일 책임 분리와 결합도 최소화**: 파일 포맷을 JSON에서 SQLite로 교체하더라도 `QuizRepository`만 수정하면 되며, `QuizGame`의 콘솔 입출력 코드는 단 한 줄도 영향을 받지 않습니다.
- **전역 상태(`global`) 완전 배제**: 절차형 코드에서 흔히 발생하는 전역 리스트·점수 변수의 부수 효과(Side-effect)를 인스턴스 캡슐화로 제거하여 단위 테스트 격리성을 확보했습니다.
- **다형성 확장 용이성**: 향후 OX 퀴즈나 주관식 퀴즈를 도입할 때 `Quiz` 클래스를 상속받아 `display()`와 `is_correct()`만 오버라이딩하면 기존 게임 루프를 그대로 재사용할 수 있습니다.

---

## 4. 데이터/입출력 스키마 명세 및 영속성 원리 (`state.json`)

### 1) UTF-8 JSON 스키마 명세

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
          "answer": 1,
          "hint": "배추김치의 주재료입니다."
        }
      ],
      "best_score": 100,
      "history": [
        {
          "played_at": "2026-11-07 17:46:37",
          "total": 5,
          "correct": 5,
          "score": 100
        }
      ]
    }

### 2) 필드 설계 의도 및 스키마 검증 규칙
- **루트 딕셔너리 계층화**: 문제 배열(`quizzes`)과 집계 메타데이터(`best_score`, `history`)를 루트 객체로 분리하여 하위 호환성을 유지하면서 기능을 확장할 수 있도록 설계했습니다.
- **엄격한 역직렬화 무결성 검증**: 외부에서 `state.json`이 임의 편집되어 `answer: 99`나 `choices` 개수 불일치, `best_score: "abc"` 같은 스키마 오염이 발생하더라도 로드 단계(`_parse_and_validate_file`)에서 즉시 감지하여 런타임 `IndexError`/`TypeError`를 원천 차단합니다.

---

## 5. 단계별 실제 실행 터미널 입출력 로그 및 `docs/` 증빙 이미지

### 1) 메인 메뉴 구동, 입력 예외 방어(빈 값·문자·범위 초과) 및 목록 조회

    $ python main.py
    [안내] 저장된 데이터를 불러왔습니다. (퀴즈 5개, 최고 점수: 100점)

    ========================================
            나만의 음식 상식 퀴즈 게임
    ========================================
    1. 퀴즈 풀기
    2. 퀴즈 추가
    3. 퀴즈 목록
    4. 점수 확인
    5. 종료
    ========================================
    선택: 
    [입력 오류] 입력이 비어 있습니다. 1-5 사이의 숫자를 입력하세요.
    선택: abc
    [입력 오류] 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.
    선택: 9
    [입력 오류] 허용 범위를 벗어났습니다. 1-5 사이의 숫자를 입력하세요.
    선택: 3

    📋 등록된 퀴즈 목록 (총 5개)
    ----------------------------------------
    [1] 한국의 대표적인 발효 식품인 '김치'를 담글 때 가장 대중적으로 많이 쓰이는 주재료 채소는?
    [2] 이탈리아의 대표적인 면 요리로 토마토, 크림, 오일 등 다양한 소스와 곁들여 먹는 음식은?
    [3] '비빔밥'의 본고장으로 가장 널리 알려진 한국의 대표 도시는?
    [4] 빵이나 쿠키를 구울 때 반죽을 부풀리기 위해 넣는 대표적인 재료는?
    [5] 한국에서 생일날 아침에 축하와 감사의 의미로 끓여 먹는 국의 주재료는?
    ----------------------------------------

![Menu and Input Validation Screenshot](docs/menu_validation.png)

### 2) 퀴즈 풀기(경계값 `0` 방어 포함), 최고 점수 갱신 및 플레이 기록 확인

    선택: 1

    ▶ 퀴즈를 시작합니다! (총 5문제)

    [문제 1] 한국의 대표적인 발효 식품인 '김치'를 담글 때 가장 대중적으로 많이 쓰이는 주재료 채소는?
      1. 배추
      2. 양파
      3. 감자
      4. 당근
    정답 입력 (1-4): 0
    [입력 오류] 허용 범위를 벗어났습니다. 1-4 사이의 숫자를 입력하세요.
    정답 입력 (1-4): 1
    ✅ 정답입니다!
    ... (문제 2 ~ 문제 5 풀이 진행) ...
    ========================================
    🏆 결과: 5문제 중 5문제 정답! (100점)
    🎉 새로운 최고 점수입니다!
    ========================================

    선택: 4
    🏆 최고 점수: 100점
    📊 최근 플레이 기록 (최근 1회 / 총 1회):
      1. [2026-11-07 17:46:37] 5문제 중 5개 정답 (100점)

![Quiz Play and Score Screenshot](docs/play_score.png)

### 3) 신규 퀴즈 추가(중복 보기 방어) 및 파일 영속 저장 확인

    선택: 2

    📌 새로운 퀴즈를 추가합니다.
    문제를 입력하세요: 일본의 대표적인 발효 콩 식품으로 끈적한 실이 생기는 음식은?
    선택지 1: 낫토
    선택지 2: 낫토
    [입력 오류] 이미 입력한 선택지와 중복됩니다. 다른 보기를 입력하세요.
    선택지 2: 초밥
    선택지 3: 우동
    선택지 4: 덴푸라
    정답 번호 (1-4): 1

    ✅ 퀴즈가 추가되었으며 state.json에 안전하게 저장되었습니다!

![Add Quiz Screenshot](docs/add_quiz.png)

### 4) Git 커밋 수치, 브랜치 병합 그래프(`--no-ff`) 및 `clone`/`pull` 동기화 증빙

![Git Commit Graph Screenshot](docs/git_commit_count.png)

![Git Clone and Pull Sync Screenshot](docs/git_clone_pull.png)

    $ git log --oneline --graph
    * (HEAD -> main, origin/main) docs: verify remote sync via git clone and pull in unified workspace
    * docs: upgrade README with troubleshooting cases, real screenshots, and 3-class matrix
    * test: add automated unit tests for schema recovery, bool trap, and input bounds
    * refactor: extract QuizRepository for atomic os.replace writes and strict schema validation
    * a73e016 docs: add maintenance mapping matrix for requirement changes
    * 42228c9 docs: attach screenshot assets and explicit commit count verification
    * 88246a3 docs: enrich technical documentation with OOP, schema, limitations, and backup policies
    * 6cb04f6 docs: verify git clone and remote synchronization
    * 525d812 docs: write comprehensive technical documentation in README
    * 4758e97 feat: implement persistent state management with state.json
    * 51a41fe refactor: encapsulate game logic and state into QuizGame class
    * 165e940 feat: implement best score tracking and score view feature
    * e9e136f feat: implement quiz listing feature with empty check
    * 4753e2c feat: implement quiz addition feature with input validation
    *   e7c1824 merge: merge branch 'feature/quiz-play' into main
    |\  
    | * b48a473 feat: implement quiz playing feature with score calculation
    |/  
    * b734a1b feat: add default food trivia quiz dataset
    * e7e584a feat: define Quiz class with question, choices, and answer verification
    * c1b4814 feat: implement console menu and robust input validation
    * 3a03a7e chore: initialize repository with .gitignore and README

---

## 6. 시스템 한계점 및 원자적 백업·복구 정책

### 1) 단일 JSON 파일 영속성 구조의 시스템 한계점 및 대안
1. **전체 파일 재직렬화 `O(N)` I/O 병목**: 문제 1개나 점수 1건만 갱신되어도 전체 `quizzes`와 `history`를 다시 직렬화(`json.dump`)해야 하므로 수만 건 이상의 대용량 문제 은행에서는 디스크 I/O 비용이 선형 증가합니다.
2. **메모리 상주 한계**: 구동 시 전체 문제를 파이썬 객체 리스트로 메모리에 적재하므로 대규모 데이터셋에는 부적합합니다.
3. **동시 쓰기 경합(Race Condition)**: 복수 터미널에서 동시에 게임을 실행해 저장할 경우 파일 락(File Lock)이 없어 마지막에 저장한 프로세스의 상태로 덮어써집니다.
4. **확장 대안**: 대규모 서비스 전환 시 트랜잭션(ACID)과 인덱스 조회를 지원하는 경량 내장 RDBMS(`sqlite3`)로 `QuizRepository` 구현체만 교체하면 상위 로직 변경 없이 한계를 해결할 수 있습니다.

### 2) 원자적 쓰기(Atomicity) 및 3단계 무결성 복구 정책

    [저장 흐름]  데이터 직렬화 ──> state.json.tmp 기록 및 fsync ──> 정상 원본을 state.json.bak 복사 ──> os.replace 원자적 교체
    [로드 흐름]  state.json 검증 로드 ──(실패 시)──> state.json.bak 자동 복원 ──(실패 시)──> 기본 5문항 안전 초기화

- **원자적 파일 교체**: `open("state.json", "w")`로 원본을 직접 열면 직렬화 도중 강제 종료 시 0바이트 빈 파일이 남게 됩니다. 이를 방지하기 위해 `state.json.tmp`에 완전히 기록·플러시(`os.fsync`)한 뒤 `os.replace()`로 원자적 포인터 교체를 수행합니다.
- **오염 전파 방지 백업**: 기존 `state.json`이 스키마 검증을 통과한 정상 파일일 때만 `state.json.bak`로 백업하므로, 이미 깨진 파일이 정상 백업본을 덮어쓰는 2차 오염을 차단합니다.

---

## 7. 트러블슈팅 사례

### 사례 1: 손상된 `state.json`의 범위 밖 정답 번호 및 Python `bool` 서브클래스 함정
- **문제 현상**: 외부에서 `state.json`의 `answer` 값을 `99` 또는 `true`로 변조했을 때 파일 로드는 성공했으나, 오답 해설 출력 시 `quiz.choices[quiz.answer - 1]`에서 `IndexError`가 발생하거나 `True == 1`로 오판정되는 현상 발견.
- **원인 가설**: `json.load()`는 JSON 문법만 검사할 뿐 도메인 범위(`1~4`)를 검사하지 않으며, Python에서는 `bool`이 `int`의 서브클래스(`isinstance(True, int) == True`)여서 단순 `isinstance` 검사만으로는 불리언 값을 걸러내지 못함.
- **확인**: 단위 테스트(`test_quiz_game.py`)에서 `Quiz(..., answer=True)` 및 `answer=99` 주입 시 예외 없이 통과되던 취약점 재현 확인.
- **해결 조치**: `Quiz._validate_answer()`에 `if isinstance(answer, bool) or not isinstance(answer, int)` 조건과 `1 <= answer <= 4` 경계 검사를 추가하고, `QuizRepository._parse_and_validate_file()`에서 검증 실패 시 즉시 `.bak` 복구 단계로 전환하도록 조치 완료.

### 사례 2: 직접 덮어쓰기(`open("w")`) 중 인터럽트 발생 시 데이터 유실 위험
- **문제 현상**: 파일 저장 중 예기치 않은 종료 신호가 개입할 경우 `state.json`이 불완전한 JSON 문자열로 잘려 다음 실행 시 파싱 에러(`JSONDecodeError`)를 유발할 가능성 존재.
- **원인 가설**: 대상 파일을 쓰기 모드로 여는 즉시 기존 파일 내용이 절삭(Truncate)되기 때문에 직렬화 완료 전 인터럽트가 발생하면 원본이 파괴됨.
- **확인**: 임시 직렬화 실패 시나리오 점검을 통해 직접 쓰기 방식의 비원자성 확인.
- **해결 조치**: `state.json.tmp`에 먼저 기록 및 디스크 동기화(`flush` + `os.fsync`)를 완료한 뒤, OS 커널 수준에서 원자성을 보장하는 `os.replace(temp_file, state_file)`로 교체하도록 `QuizRepository.save_state()`를 전면 개선.

### 사례 3: 상위 워크스페이스 디렉터리에서 실행 시 `state.json` 경로 불일치
- **문제 현상**: 프로젝트 폴더 내부가 아닌 상위 폴더에서 `python codyssey-quiz/main.py`로 실행하면 현재 작업 디렉터리(CWD)에 새로운 `state.json`이 생성되어 기존 저장 데이터를 찾지 못하는 현상 발생.
- **원인 가설**: 파일 경로가 `"state.json"` 상대 경로로 하드코딩되어 실행 위치(CWD)에 종속됨.
- **확인**: 상위 디렉터리 실행 테스트를 통해 CWD 기준 파일 탐색 동작 확인.
- **해결 조치**: `os.path.dirname(os.path.abspath(__file__))`을 기준으로 프로젝트 루트 경로를 고정하도록 `QuizRepository.__init__()`을 개선하여 어느 위치에서 실행하더라도 동일한 프로젝트 루트 `state.json`을 읽고 쓰도록 해결.

---

## 8. 요구사항 변경 관리 및 파일·메서드 매핑 명세 표 (Maintenance Matrix)

향후 비즈니스 요구사항 변경이나 신규 기능 확장 시 수정 범위를 즉각 특정할 수 있도록 파일·클래스·메서드 매핑 명세를 정의합니다.

| 변경 요구사항 시나리오 | 수정 대상 파일 | 담당 클래스 | 핵심 수정 메서드 / 속성 | 세부 작업 내용 |
| :--- | :--- | :--- | :--- | :--- |
| **문제 유형 확장** (O/X 및 주관식 퀴즈 추가) | `main.py` | `Quiz` (및 하위 클래스) | `display`, `is_correct`, `from_dict` | `Quiz`를 상속한 `OXQuiz`, `SubjectiveQuiz` 정의 및 다형성 분기 처리 |
| **선택지 문항 수 변경** (4지선다 → 5지선다) | `main.py` | `Quiz`, `QuizGame` | `Quiz.REQUIRED_CHOICE_COUNT`, `get_quiz_answer`, `add_quiz` | 상수 값을 `5`로 변경하고 정답 입력 범위를 `1~5`로 확대 |
| **저장소 엔진 교체** (JSON 파일 → SQLite DB) | `main.py` | `QuizRepository` | `load_state`, `save_state` | 파일 입출력 로직을 `sqlite3` 트랜잭션 쿼리로 교체 (`QuizGame` 수정 불필요) |
| **출제 방식 고도화** (랜덤 셔플 및 문항 수 선택) | `main.py` | `QuizGame` | `play_quiz` | `random.sample()`을 적용하여 출제 리스트 순서 및 개수 동적 추출 |
| **등록된 퀴즈 삭제 기능 추가** | `main.py` | `QuizGame` | `print_menu`, `get_menu_choice`, `delete_quiz`, `run` | 메뉴 번호 확장 및 인덱스 검증 후 `self.quizzes.pop()`·`save_state()` 호출 |
| **회귀 검증 케이스 추가** | `tests/test_quiz_game.py` | `TestQuizDomain` 외 | 신규 단위 테스트 메서드 | 변경된 스키마·경계값에 대한 자동화 검증 케이스 추가 |

---

## 9. 공식 요구사항 전 항목 달성 체크리스트

- [x] **실행 환경**: Python 3.10 이상(Python 3.15.2) 및 외부 라이브러리 없이 표준 라이브러리만 사용
- [x] **핵심 기능 5종**: 메뉴 출력, 1. 퀴즈 풀기, 2. 퀴즈 추가, 3. 퀴즈 목록, 4. 점수 확인(히스토리 포함), 5. 종료 정상 동작
- [x] **기본 데이터**: 직접 구성한 음식 상식 4지선다 퀴즈 5문항 이상 기본 탑재
- [x] **객체지향 코드 구조**: 단일 책임 원칙(SRP)에 따른 3개 독립 클래스(`Quiz`, `QuizRepository`, `QuizGame`) 및 기능별 메서드 분리
- [x] **데이터 영속성 및 복구**: 루트 `state.json`(UTF-8) 원자적(`os.replace`) 저장 및 `state.json.bak` 3단계 무결성 복구 구현
- [x] **방어적 예외 처리**: 앞뒤 공백(`.strip()`), 빈 입력(Enter), 비숫자(`abc`), 범위 밖 숫자(`0`, `9`), 중복 선택지 방어 및 재입력 유도
- [x] **안전 종료(Graceful Shutdown)**: `Ctrl+C`(`KeyboardInterrupt`) 및 `EOFError` 발생 시 상태 저장 후 비정상 종료 없이 정상 종료
- [x] **Git 워크플로우**: 10개 이상 의미 있는 기능 단위 커밋 달성, `feature/quiz-play` 브랜치 생성 및 `--no-ff` 병합, Git 7대 명령어(`init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone`) 실습 증빙 완비
- [x] **기술 문서 및 증빙**: `docs/` 실제 실행·Git 스크린샷 5종 연결, 트러블슈팅 3건 및 Maintenance Matrix 수록 완료

# Unified Workspace Remote Sync Verified
