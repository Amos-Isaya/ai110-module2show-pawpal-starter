from datetime import date, timedelta
import pytest
from pawpal_system import Owner, Pet, Task, Scheduler

DAY = date(2026, 11, 8)


def setup_schedule():
    owner = Owner("Jordan")
    first, second = Pet("Mochi", "dog"), Pet("Luna", "cat")
    owner.add_pet(first)
    owner.add_pet(second)
    return first, second, Scheduler(owner)


def test_task_completion():
    task = Task("Walk", "09:00")
    task.mark_complete()
    assert task.completed


def test_task_addition():
    pet = Pet("Mochi", "dog")
    task = Task("Walk", "09:00")
    pet.add_task(task)
    assert pet.tasks == [task]


def test_sort_across_pets_and_dates():
    first, second, scheduler = setup_schedule()
    first.add_task(Task("Late", "18:00", DAY))
    second.add_task(Task("Next day", "07:00", DAY + timedelta(days=1)))
    second.add_task(Task("Early", "8:00", DAY))
    assert [task.description for _, task in scheduler.sort_by_time()] == ["Early", "Late", "Next day"]


@pytest.mark.parametrize("frequency,days", [("daily", 1), ("weekly", 7)])
def test_recurrence_and_repeated_completion(frequency, days):
    first, _, scheduler = setup_schedule()
    task = Task("Food", "08:00", date(2026, 12, 31), frequency=frequency)
    first.add_task(task)
    following = scheduler.mark_task_complete(task.id)
    assert task.completed
    assert following.due_date == task.due_date + timedelta(days=days)
    assert following.id != task.id
    assert not following.completed
    assert following.frequency == frequency
    assert scheduler.mark_task_complete(task.id) is None
    assert len(first.tasks) == 2


def test_once_does_not_recur():
    first, _, scheduler = setup_schedule()
    task = Task("Vet", "12:00", DAY)
    first.add_task(task)
    assert scheduler.mark_task_complete(task.id) is None
    assert len(first.tasks) == 1


def test_conflicts_across_pets_ignore_other_dates_and_completed():
    first, second, scheduler = setup_schedule()
    first.add_task(Task("Food", "08:00", DAY))
    other = Task("Walk", "08:00", DAY)
    second.add_task(other)
    second.add_task(Task("Tomorrow", "08:00", DAY + timedelta(days=1)))
    warnings = scheduler.detect_conflicts(DAY)
    assert len(warnings) == 1
    assert "Mochi" in warnings[0] and "Luna" in warnings[0]
    other.mark_complete()
    assert scheduler.detect_conflicts(DAY) == []


def test_filters_and_empty_owner():
    first, _, scheduler = setup_schedule()
    assert scheduler.sort_by_time() == []
    first.add_task(Task("Food", "08:00", DAY, completed=True))
    assert len(scheduler.filter_tasks(pet_name="Mochi", completed=True, on_date=DAY)) == 1
    assert scheduler.filter_tasks(completed=False) == []
    assert scheduler.filter_tasks(pet_name="Luna") == []


def test_budget_prioritizes_important_tasks():
    first, second, scheduler = setup_schedule()
    first.add_task(Task("Play", "08:00", DAY, priority="low", duration_minutes=10))
    second.add_task(Task("Medication", "09:00", DAY, priority="high", duration_minutes=5))
    chosen, skipped = scheduler.build_plan(DAY, 10)
    assert [task.description for _, task in chosen] == ["Medication"]
    assert [task.description for _, task in skipped] == ["Play"]
    assert scheduler.build_plan(DAY, 0)[0] == []


@pytest.mark.parametrize("kwargs", [{"time": "25:00"}, {"frequency": "monthly"},
    {"priority": "urgent"}, {"duration_minutes": 0}, {"description": " "}])
def test_invalid_tasks(kwargs):
    values = {"description": "Walk", "time": "08:00"}
    values.update(kwargs)
    with pytest.raises(ValueError):
        Task(**values)


def test_unknown_completion_and_duplicate_pet():
    _, _, scheduler = setup_schedule()
    with pytest.raises(ValueError):
        scheduler.mark_task_complete("missing")
    with pytest.raises(ValueError):
        scheduler.owner.add_pet(Pet("mochi", "cat"))
