"""Run a readable, repeatable demonstration with python main.py."""
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    """Demonstrate multiple pets, sorting, filtering, conflicts, and recurrence."""
    today = date(2026, 11, 8)
    owner = Owner("Jordan")
    mochi, luna = Pet("Mochi", "dog"), Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    mochi.add_task(Task("Evening walk", "18:00", today, priority="high"))
    breakfast = Task("Breakfast", "08:00", today, frequency="daily", duration_minutes=10)
    mochi.add_task(breakfast)
    luna.add_task(Task("Medication", "08:00", today, priority="high", duration_minutes=5))
    scheduler = Scheduler(owner)
    print(f"Today's Schedule ({today})")
    for pet, task in scheduler.sort_by_time(on_date=today):
        print(f"{task.time} | {pet.name:<5} | {task.description} ({task.duration_minutes} min, {task.priority})")
    for warning in scheduler.detect_conflicts(today):
        print(f"WARNING: {warning}")
    print(f"Pending Mochi tasks: {len(scheduler.filter_tasks(pet_name='Mochi', completed=False))}")
    following = scheduler.mark_task_complete(breakfast.id)
    print(f"Breakfast completed; next occurrence: {following.due_date} at {following.time}")
    chosen, skipped = scheduler.build_plan(today, 10)
    print("10-minute plan: " + ", ".join(f"{pet.name}: {task.description}" for pet, task in chosen))
    print(f"Skipped for time budget: {len(skipped)}")


if __name__ == "__main__":
    main()
