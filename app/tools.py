"""Lecture 03: tools for the agent.

Function docstrings and type hints here become the "tool descriptions" presented to the model.
Rewriting descriptions changes whether the model uses a tool and which arguments it supplies.
"""
from pathlib import Path
import json
from datetime import datetime, timezone
from uuid import uuid4
LEARNING_LOG_DIR = Path(__file__).resolve().parent.parent / "learning_log"

from functools import cache


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LEARNING_LOG_DIR = Path(__file__).resolve().parent.parent / "learning_log"
MAX_RESULTS = 3


@cache
def load_glossary() -> list[dict]:
    with open(DATA_DIR / "glossary.json", encoding="utf-8") as f:
        return json.load(f)["terms"]


def _normalize(text: str) -> str:
    return text.casefold().replace(" ", "").replace("　", "")


def _names(entry: dict) -> list[str]:
    return [_normalize(entry["term"]), _normalize(entry["id"])] + [
        _normalize(a) for a in entry["aliases"]
    ]


def search_glossary(query: str) -> str:
    """Search the course glossary and return definitions and the sessions that cover the terms.

    Use before answering about AI engineering terms or words specific to this course (AIE2026).
    Put only one term to look up in query (for example, "LoRA").
    """
    q = _normalize(query)
    if not q:
        return "The search query is empty. Specify one term to look up."
    glossary = load_glossary()

    exact = [e for e in glossary if q in _names(e)]
    # Exclude short names so aliases such as "r" do not match everything
    partial = [
        e for e in glossary
        if e not in exact and any(q in n or (len(n) >= 3 and n in q) for n in _names(e))
    ]
    in_definition = [
        e for e in glossary
        if e not in exact and e not in partial and q in _normalize(e["definition"])
    ]
    hits = (exact + partial + in_definition)[:MAX_RESULTS]

    if not hits:
        return f"The term '{query}' was not found in the glossary."
    return json.dumps(
        [
            {
                "term": e["term"],
                "lecture": e["lecture"],
                "definition": e["definition"],
                "related": e["related"],
            }
            for e in hits
        ],
        ensure_ascii=False,
    )


def get_lecture_summary(lecture: int) -> str:
    """Return key points from the specified session (an integer starting at 1).

    Use when asked about session content or relationships, such as "What will we learn in Lecture 03?".
    """
    path = DATA_DIR / "lectures" / f"{lecture:02d}.md"
    if not path.exists():
        available = sorted(p.stem for p in (DATA_DIR / "lectures").glob("*.md"))
        return f"Key points for Lecture {lecture:02d} are not available yet. Available sessions: {', '.join(available)}"
    return path.read_text(encoding="utf-8")

def make_quiz(lecture: int) -> str:
    """指定された講義回から復習問題を1問作成し、解答も返す。

    ユーザーが講義の復習や理解度確認のために
    クイズ・練習問題を求めたときに使用する。
    lectureには講義番号を整数で指定する。
    """
    glossary = load_glossary()

    # 指定された講義回の用語を抽出
    terms = [
        entry for entry in glossary
        if entry["lecture"] == lecture
    ]

    # 該当する用語がなければメッセージを返す
    if not terms:
        return f"第{lecture}回の復習問題はありません。"

    # 最初の用語を1つ選択
    term = terms[0]

    question = f"{term['term']}とは何ですか？"
    answer = term["definition"]

    return f"問題：{question}\n解答：{answer}"


def save_learning_log(lecture: int, topic: str, notes: str) -> str:
    """Save a learning record to the learning_log directory.

    Use this tool only when the user explicitly requests to save
    a learning record, study note, or learning progress.
    The tool requires human approval before execution.

    Args:
        lecture: Lecture number (0 if unspecified).
        topic: Topic studied by the user.
        notes: Learning content or study notes to save.
    """
    # 保存先のフォルダを作成する
    LEARNING_LOG_DIR.mkdir(parents=True, exist_ok=True)

    # 保存日時を取得する
    now = datetime.now(timezone.utc)

    # 同名ファイルの衝突を避ける
    filename = (
        f"{now:%Y%m%d_%H%M%S}_"
        f"{uuid4().hex[:8]}.json"
    )
    filepath = LEARNING_LOG_DIR / filename

    # 保存する学習記録
    record = {
        "created_at": now.isoformat(),
        "lecture": lecture,
        "topic": topic,
        "notes": notes,
    }

    # JSONファイルとして保存
    filepath.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return f"Learning log saved: {filepath}"
