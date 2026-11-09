# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
- Tool calls shown by `--trace` (tool names and arguments):
- Number of LLM calls for one question (`requests`):
- Tool added and the description in its docstring:

## Homework

- Level attempted: Implementation 
- What you did:save_learning_log を新たに実装し、講義番号、学習テーマ、学習内容をJSON形式で learning_log/ に保存できるようにした。

Pydantic AIの requires_approval=True を利用してHuman-in-the-Loopを導入し、ユーザーが承認した場合のみファイル保存を実行する設計とした。
- Results:TestModelを使用して、承認前・承認後・拒否時の動作を検証した。既存テストを含め14件が成功した。
- Observations and questions:
learning_logにはどんな形式の学習内容も入れられるのかが気になりました。
