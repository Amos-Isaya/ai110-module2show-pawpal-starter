"""Verify the actual Streamlit forms and rerun-driven completion flow."""
from datetime import date, timedelta
from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_add_pets_schedule_and_complete_recurring_task():
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=30).run()
    assert not app.exception
    app.text_input[1].set_value("Mochi")
    app.button[0].click().run()
    app.text_input[1].set_value("Luna")
    app.button[0].click().run()
    assert len(app.session_state.owner.pets) == 2
    app.text_input[2].set_value("Breakfast")
    app.selectbox[2].select("daily")
    app.button[1].click().run()
    assert not app.exception
    owner = app.session_state.owner
    assert len(owner.pets[0].tasks) == 1
    complete = next(button for button in app.button if button.label == "Complete")
    complete.click().run()
    assert not app.exception
    tasks = app.session_state.owner.pets[0].tasks
    assert len(tasks) == 2
    assert tasks[0].completed
    assert tasks[1].due_date == date.today() + timedelta(days=1)
    assert not tasks[1].completed


def test_edit_form_updates_task_and_empty_description_is_rejected():
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=30).run()
    app.text_input[1].set_value("Mochi")
    app.button[0].click().run()
    app.text_input[2].set_value("Walk")
    app.button[1].click().run()
    original_id = app.session_state.owner.pets[0].tasks[0].id
    next(widget for widget in app.text_input if widget.label == "Description").set_value("Vet visit")
    next(widget for widget in app.number_input if widget.label == "New duration (minutes)").set_value(30)
    next(button for button in app.button if button.label == "Save changes").click().run()
    assert not app.exception
    task = app.session_state.owner.pets[0].tasks[0]
    assert task.description == "Vet visit"
    assert task.duration_minutes == 30
    assert task.id == original_id
    next(widget for widget in app.text_input if widget.label == "Description").set_value(" ")
    next(button for button in app.button if button.label == "Save changes").click().run()
    assert app.error
    assert app.session_state.owner.pets[0].tasks[0].description == "Vet visit"
