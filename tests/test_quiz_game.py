import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import Quiz, QuizGame, QuizRepository


class TestQuizDomain(unittest.TestCase):
    """Quiz 도메인 클래스 유효성 검증 테스트"""

    def test_valid_quiz_creation_and_check(self):
        q = Quiz("질문?", ["보기1", "보기2", "보기3", "보기4"], 2)
        self.assertTrue(q.is_correct(2))
        self.assertFalse(q.is_correct(1))

    def test_reject_bool_as_answer(self):
        # Python isinstance(True, int) == True 함정 방어 검증
        with self.assertRaises(ValueError):
            Quiz("질문?", ["보기1", "보기2", "보기3", "보기4"], True)

    def test_reject_out_of_bounds_answer_and_duplicate_choices(self):
        with self.assertRaises(ValueError):
            Quiz("질문?", ["보기1", "보기2", "보기3", "보기4"], 0)
        with self.assertRaises(ValueError):
            Quiz("질문?", ["보기1", "보기2", "보기3", "보기4"], 5)
        with self.assertRaises(ValueError):
            Quiz("질문?", ["중복", "중복", "보기3", "보기4"], 1)


class TestQuizRepositoryRecovery(unittest.TestCase):
    """QuizRepository 원자적 저장 및 .bak 3단계 무결성 복구 검증"""

    def test_three_stage_recovery_on_corruption(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = QuizRepository(base_dir=tmpdir)
            quizzes, best_score, _ = repo.load_state()
            self.assertEqual(len(quizzes), 5)
            self.assertIsNone(best_score)

            # 정상 점수 갱신 저장 -> .bak 생성 확인
            repo.save_state(quizzes, 80, [{"played_at": "2026-11-07", "total": 5, "correct": 4, "score": 80}])
            self.assertTrue(os.path.exists(repo.backup_file))

            # 한 번 더 저장하여 .bak 에 80점 스냅샷 보존
            repo.save_state(quizzes, 100, [{"played_at": "2026-11-07", "total": 5, "correct": 5, "score": 100}])

            # state.json 의도적 문법 손상 -> .bak (80점) 자동 복구 확인
            with open(repo.state_file, "w", encoding="utf-8") as f:
                f.write("{corrupted json!!!")

            rec_quizzes, rec_score, _ = repo.load_state()
            self.assertEqual(len(rec_quizzes), 5)
            self.assertEqual(rec_score, 80)
            self.assertTrue(os.path.exists(repo.corrupt_file))

            # state.json 과 state.json.bak 동시 스키마 손상(answer: 99) -> 기본 5문항 안전 초기화 확인
            bad_payload = json.dumps({"quizzes": [{"question": "Q", "choices": ["1", "2", "3", "4"], "answer": 99}], "best_score": 50})
            with open(repo.state_file, "w", encoding="utf-8") as f:
                f.write(bad_payload)
            with open(repo.backup_file, "w", encoding="utf-8") as f:
                f.write(bad_payload)

            fallback_quizzes, fallback_score, _ = repo.load_state()
            self.assertEqual(len(fallback_quizzes), 5)
            self.assertIsNone(fallback_score)


class TestQuizGameConsoleFlow(unittest.TestCase):
    """QuizGame 입력 경계값 방어 및 Graceful Shutdown 검증"""

    def test_invalid_inputs_then_graceful_eof(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = QuizRepository(base_dir=tmpdir)
            game = QuizGame(repository=repo)
            self.assertEqual(game.calculate_score(4, 5), 80)
            # 빈 입력, 공백 포함 유효 입력("  4  "), 문자열(abc), 범위 밖(0, 9) 후 EOFError 종료 검증
            inputs = ["", "abc", "0", "9", "  4  "]
            with patch("builtins.input", side_effect=inputs + [EOFError()]):
                game.run()
            self.assertTrue(os.path.exists(repo.state_file))


if __name__ == "__main__":
    unittest.main()
