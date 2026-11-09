
"""Tests for the learning log tool with human approval."""

import json

from pydantic_ai import DeferredToolRequests, DeferredToolResults
from pydantic_ai.models.test import TestModel

from app import tools
from app.agent import agent


def test_save_requires_approval(tmp_path, monkeypatch):
    """Approval is requested before writing a file."""
    log_dir = tmp_path / "learning_log"
    monkeypatch.setattr(tools, "LEARNING_LOG_DIR", log_dir)

    model = TestModel(call_tools=["save_learning_log"])

    with agent.override(model=model):
        result = agent.run_sync("Save my study notes")

    assert isinstance(result.output, DeferredToolRequests)
    assert len(result.output.approvals) == 1
    assert result.output.approvals[0].tool_name == "save_learning_log"

    # 承認前にはファイルが存在しない
    assert not log_dir.exists()


def test_save_after_approval(tmp_path, monkeypatch):
    """A file is created after user approval."""
    log_dir = tmp_path / "learning_log"
    monkeypatch.setattr(tools, "LEARNING_LOG_DIR", log_dir)

    model = TestModel(call_tools=["save_learning_log"])

    with agent.override(model=model):
        first = agent.run_sync("Save my study notes")

        assert isinstance(first.output, DeferredToolRequests)
        call = first.output.approvals[0]

        # 保存を承認してエージェントを再開
        result = agent.run_sync(
            message_history=first.all_messages(),
            deferred_tool_results=DeferredToolResults(
                approvals={call.tool_call_id: True}
            ),
        )

    files = list(log_dir.glob("*.json"))
    assert len(files) == 1

    record = json.loads(files[0].read_text(encoding="utf-8"))
    assert "lecture" in record
    assert "topic" in record
    assert "notes" in record
    assert isinstance(result.output, str)


def test_save_denied(tmp_path, monkeypatch):
    """A denied request must not create a file."""
    log_dir = tmp_path / "learning_log"
    monkeypatch.setattr(tools, "LEARNING_LOG_DIR", log_dir)

    model = TestModel(call_tools=["save_learning_log"])

    with agent.override(model=model):
        first = agent.run_sync("Save my study notes")

        assert isinstance(first.output, DeferredToolRequests)
        call = first.output.approvals[0]

        # 保存を拒否する
        agent.run_sync(
            message_history=first.all_messages(),
            deferred_tool_results=DeferredToolResults(
                approvals={call.tool_call_id: False}
            ),
        )

    # 拒否されたのでファイルは保存されない
    assert not log_dir.exists()
