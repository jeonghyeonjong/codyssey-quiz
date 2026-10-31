# 나만의 음식 상식 퀴즈 게임 (Codyssey Quiz Game)

## 1. 프로젝트 개요
터미널 콘솔 환경에서 동작하는 객체 지향 기반 파이썬 퀴즈 게임 프로그램입니다.
사용자는 4지선다형 음식 상식 퀴즈를 풀고, 새로운 퀴즈를 등록하며, 최고 점수를 갱신 및 보존할 수 있습니다.
프로그램 종료 후에도 데이터가 유지되도록 JSON 파일 기반의 영속성(Persistence) 구조 및 자동 백업/복구 메커니즘을 갖추고 있습니다.

- 원격 저장소 URL: [https://github.com/jeonghyeonjong/codyssey-quiz.git](https://github.com/jeonghyeonjong/codyssey-quiz.git)
- 저장소 공개 설정: Public Repository

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

---

## 4. 객체 지향(OOP) 아키텍처 및 패러다임 비교 분석

### 1) 클래스 분리 설계
프로그램은 단일 함수 스크립트 방식이 아닌 단일 책임 원칙(SRP)에 따라 2개의 독립된 클래스로 분리 설계되었습니다.

1. Quiz 클래스
   - 역할: 개별 퀴즈의 데이터 표현 및 검증 담당
   - 속성:
     - question (str): 문제 지문
     - choices (list[str]): 4개의 보기 선택지
     - answer (int): 정답 번호 (1~4)
   - 메서드:
     - display(number): 문제와 선택지를 서식에 맞춰 콘솔에 출력
     - is_correct(user_answer): 사용자 입력 번호와 정답 일치 여부 반환 (bool)
     - to_dict() / from_dict(): JSON 직렬화 및 역직렬화를 위한 딕셔너리 변환

2. QuizGame 클래스
   - 역할: 게임 라이프사이클 관리, 메뉴 네비게이션, 파일 입출력 및 백업 총괄
   - 속성:
     - quizzes (list[Quiz]): Quiz 인스턴스 리스트
     - best_score (int | None): 저장된 최고 점수
   - 메서드:
     - load_state() / save_state(): state.json 파일 읽기/쓰기 및 3단계 무결성 복구
     - print_menu() / get_menu_choice(): 메뉴 인터페이스 및 경계값(1, 5) 입력 검증
     - get_quiz_answer(): 4지선다 정답 경계값(1, 4) 검증
     - play_quiz(): 문제 풀이 흐름 제어 및 채점/최고 점수 갱신
     - add_quiz(): 새 문제 유효성 검증 및 리스트 추가
     - list_quizzes(): 전체 퀴즈 목록 요약 출력
     - view_score(): 최고 점수 출력
     - run(): 메인 루프 실행 및 예외 포착

### 2) 객체지향(OOP)의 장단점 및 함수형/절차적 대체 시나리오 비교
- 객체지향 채택의 장점:
  1. 상태(State)와 행위(Behavior)의 캡슐화: 퀴즈 데이터(문제, 선택지, 정답)와 정답 검증 로직(is_correct)을 한 객체 안에 묶어 응집도를 극대화했습니다.
  2. 전역 변수(Global Variable)의 완전한 제거: 게임 진행 상태(quizzes 리스트, best_score)를 QuizGame 인스턴스의 멤버 변수로 은닉하여 부수 효과(Side-effect)와 동시성 오염을 원천 차단했습니다.
  3. 확장성: 향후 주관식 퀴즈(SubjectiveQuiz), O/X 퀴즈(OXQuiz) 등 새로운 퀴즈 형태가 추가될 때 Quiz 클래스를 상속받아 display(), is_correct()만 다형성(Polymorphism)으로 오버라이딩하면 기존 게임 로직 수정 없이 확장이 가능합니다.
- 객체지향 채택의 단점:
  - 단순 절차적 스크립트에 비해 클래스 정의, 인스턴스 생성, 직렬화/역직렬화 메서드 작성 등 초기 보일러플레이트 코드가 증가합니다.
- 함수형/절차적 대체 시나리오와 한계:
  - 순수 함수형(Functional) 패러다임으로 구현한다면 모든 상태가 불변(Immutable)이어야 하므로, 문제를 풀거나 추가할 때마다 전체 퀴즈 리스트와 점수 튜플을 반환하고 다음 함수의 인자로 전달하는 깊은 호출 체인(Call Chain)이 형성되어 콘솔 루프 제어가 극도로 복잡해집니다.
  - 단순 절차형으로 구현할 경우 전역 변수 global quizzes, global best_score를 다수의 함수에서 직접 수정해야 하므로 코드 유지보수성과 테스트 격리성이 심각하게 저하됩니다.

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
  - 데이터(문제 목록)와 메타데이터(최고 점수, 추후 추가될 플레이 횟수, 유저 설정 등)를 단일 파일 내에서 독립적으로 확장할 수 있도록 하위 호환성을 보장하기 위함입니다.
- 선택지(choices) 리스트 중첩 이유:
  - 4개의 보기를 별도 필드(choice1, choice2...)로 풀지 않고 리스트로 중첩 구조화하여 문제 지문과 보기의 원자적(Atomic) 응집성을 유지했습니다. 보기의 개수가 3지선다나 5지선다로 변경되더라도 스키마 변경 없이 유연하게 처리할 수 있습니다.

---

## 6. JSON 영속성 방식의 성능·메모리 한계 및 대안 논의

1. 전체 직렬화/역직렬화(Full Serialization) I/O 병목
   - 현 방식은 데이터 저장/로드 시 파일 전체를 통째로 읽고(json.load) 전체를 다시 덮어씁니다(json.dump). 데이터가 수만 건 이상으로 증가할 경우 O(N)의 디스크 I/O와 CPU 파싱 부하가 발생합니다.
2. 메모리 풋프린트(Memory Footprint) 증가
   - 대용량 데이터 환경에서는 전체 JSON 데이터를 파이썬 딕셔너리와 Quiz 객체 리스트로 메모리에 한꺼번에 적재해야 하므로 RAM 점유율이 급증합니다.
3. 동시성(Concurrency) 및 파일 잠금(Lock)의 부재
   - 복수의 프로세스나 사용자가 동시에 파일에 쓰기를 시도할 경우 데이터 덮어쓰기 유실(Race Condition)이 발생할 수 있습니다.
4. 개선 및 대안 방안:
   - 대용량 데이터 환경에서는 스트리밍 방식 파서(ijson)를 적용하거나 파일 압축(gzip)을 도입해야 합니다.
   - 데이터 크기가 수 메가바이트를 초과하고 빈번한 C.R.U.D가 발생할 경우, 인덱싱과 트랜잭션(ACID) 및 부분 갱신을 지원하는 경량 RDBMS인 SQLite로 전환하는 것이 최적의 설계입니다.

---

## 7. 백업 생성 및 무결성 복구 정책 (Backup & Recovery)

데이터 유실 방지를 위해 저장 전 백업 생성 및 3단계 장애 복구 정책을 구현했습니다.

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
   - save_state() 호출 시 기존에 정상적으로 저장되어 있던 state.json 파일을 shutil.copy2를 통해 state.json.bak로 즉시 복사한 뒤 신규 데이터를 덮어씁니다.
2. 3단계 복구 우선순위:
   - 1차: state.json 파일이 정상이면 즉시 파싱하여 실행합니다.
   - 2차: state.json 파일이 손상되었거나 파싱 오류가 발생하면 즉시 state.json.bak 백업 파일에서 복구를 시도합니다.
   - 3차: 백업 파일마저 없거나 손상된 경우 비정상 종료 대신 기본 5개 퀴즈 데이터로 복원하여 게임 가용성을 100% 보장합니다.

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
  - KeyError: 필수 필드(question, choices, answer) 누락 시 예외 포착 및 데이터 무결성 복구.
  - PermissionError: 파일 접근 권한 제한 시 프로그램 비정상 중단 방어.
- 비정상 종료 방어: 게임 중 사용자가 Ctrl + C(KeyboardInterrupt) 또는 EOF(EOFError)를 입력하더라도 예외를 가로채어 현재 상태를 자동 저장하고 정상 종료(sys.exit(0))합니다.

---

## 9. Git 버전 관리 및 브랜치 전략

### 1) 커밋 메시지 컨벤션 (Conventional Commits)
팀 협업 시 변경 이력을 명확히 파악할 수 있도록 아래와 같은 표준 커밋 규칙을 적용했습니다.
- 형식: <type>: <description> (50자 이내, 영문 소문자 명령조 기술)
- 태그 종류:
  - feat: 새로운 기능 추가 (메뉴, 퀴즈 풀기, 추가, 목록, 점수 등)
  - refactor: 버그 수정이나 기능 추가 없는 코드 구조 개선 (QuizGame 클래스 캡슐화)
  - docs: README 기술 문서 작성 및 수정
  - chore: 빌드, 패키지 설정, .gitignore 초기화 등
  - merge: 브랜치 병합 커밋

### 2) 브랜치 분기 및 병합 전략
- 전략: 안정적인 main 브랜치를 보호하고, feature/quiz-play 브랜치를 생성하여 퀴즈 풀기 기능을 격리 개발한 뒤 병합을 수행했습니다.
- 병합 방식: 커밋 히스토리에 명확한 브랜치 작업 궤적을 보존하기 위해 Fast-Forward를 지양하고 --no-ff 머지를 적용했습니다.
- 충돌(Conflict) 해결 절차:
  1. main과 기능 브랜치 간 동일 파일 수정으로 충돌 발생 시 Git이 3-way merge 충돌 마커(<<<<<<<, =======, >>>>>>>)를 파일에 표시합니다.
  2. 개발자가 충돌 마커를 직접 확인하여 올바른 코드를 선별하고 마커를 제거합니다.
  3. git add <해결파일>로 스테이징 후 git commit을 실행하여 충돌 해결 머지 커밋을 완결합니다.

---

## 10. Git 실습 검증 증빙 (로그 스냅샷)

### 1) Git Clone 및 Pull 원격 동기화 터미널 로그
    $ cd /c
    $ git clone [https://github.com/jeonghyeonjong/codyssey-quiz.git](https://github.com/jeonghyeonjong/codyssey-quiz.git) codyssey-quiz-clone
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
    To [https://github.com/jeonghyeonjong/codyssey-quiz.git](https://github.com/jeonghyeonjong/codyssey-quiz.git)
       525d812..6cb04f6  main -> main

    $ cd /c/codyssey-quiz
    $ git pull origin main
    Updating 525d812..6cb04f6
    Fast-forward
     README.md | 3 ++-
     1 file changed, 2 insertions(+), 1 deletion(-)

### 2) 전체 Git 커밋 히스토리 및 브랜치 병합 그래프 (git log --oneline --graph)
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

## 11. 요구사항 변경 관리 및 파일 체크리스트
- main.py: 백업 파일(state.json.bak) 생성 로직 및 3단계 예외 복구(load_state) 추가 완료
- state.json: 데이터 영속화 정상 구동 확인
- state.json.bak: 비정상 종료 및 데이터 훼손 대비 자동 백업본 생성 확인
- README.md: 평가원 지적 사항 6종(OOP 비교, 중첩 스키마, 한계 분석, 백업 정책, 컨벤션, Git 스냅샷) 전면 보강 완료