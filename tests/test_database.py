import sqlite3

from database import initialize_database, list_question_events, save_question_event


def test_initialize_database_creates_table(tmp_path):
    db_path = tmp_path / "medisub-test.db"

    created_path = initialize_database(db_path)

    assert created_path == db_path.resolve()
    with sqlite3.connect(created_path) as connection:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='question_events'"
        ).fetchall()
    assert tables == [("question_events",)]


def test_save_and_read_question_events(tmp_path):
    db_path = tmp_path / "medisub-events.db"

    save_question_event(
        question="Where do I submit?",
        predicted_category="MA_SUBMISSION_HELP",
        confidence=0.82,
        created_at="2026-01-01T00:00:00+00:00",
        db_path=db_path,
    )
    save_question_event(
        question="How do I get reference number?",
        predicted_category="REFERENCE_NUMBER_HELP",
        confidence=0.91,
        created_at="2026-01-01T00:01:00+00:00",
        db_path=db_path,
    )

    events = list_question_events(db_path=db_path, limit=10)

    assert len(events) == 2
    assert events[0]["question"] == "How do I get reference number?"
    assert events[0]["predicted_category"] == "REFERENCE_NUMBER_HELP"
    assert events[1]["question"] == "Where do I submit?"


def test_save_uses_parameterized_sql(tmp_path):
    db_path = tmp_path / "medisub-safe.db"
    payload = "Question'); DROP TABLE question_events; --"

    save_question_event(
        question=payload,
        predicted_category="OUT_OF_SCOPE",
        confidence=0.5,
        created_at="2026-01-01T00:00:00+00:00",
        db_path=db_path,
    )

    events = list_question_events(db_path=db_path, limit=5)
    assert events[0]["question"] == payload

    with sqlite3.connect(db_path) as connection:
        count = connection.execute("SELECT COUNT(*) FROM question_events").fetchone()[0]
    assert count == 1


def test_temporary_database_isolation(tmp_path):
    first_db = tmp_path / "first.db"
    second_db = tmp_path / "second.db"

    save_question_event(
        question="First database event",
        predicted_category="PROCESS_GUIDANCE",
        confidence=0.77,
        created_at="2026-01-01T00:00:00+00:00",
        db_path=first_db,
    )

    first_events = list_question_events(db_path=first_db, limit=10)
    second_events = list_question_events(db_path=second_db, limit=10)

    assert len(first_events) == 1
    assert first_events[0]["question"] == "First database event"
    assert second_events == []
