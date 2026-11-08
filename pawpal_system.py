"""Pet care entities and scheduling logic, independent of Streamlit."""
from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta
from uuid import uuid4


@dataclass
class Task:
    description: str
    time: str
    due_date: date = field(default_factory=date.today)
    frequency: str = "once"
    duration_minutes: int = 20
    priority: str = "medium"
    completed: bool = False
    id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        """Validate task inputs and normalize the clock time."""
        if not self.description.strip():
            raise ValueError("Task description is required.")
        self.time = datetime.strptime(self.time, "%H:%M").strftime("%H:%M")
        if self.frequency not in ("once", "daily", "weekly"):
            raise ValueError("Frequency must be once, daily, or weekly.")
        if self.priority not in ("low", "medium", "high"):
            raise ValueError("Priority must be low, medium, or high.")
        if self.duration_minutes < 1:
            raise ValueError("Duration must be positive.")

    def mark_complete(self):
        """Complete this occurrence; use Scheduler to also generate recurrence."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Attach a care task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet, requiring a nonempty and unique name."""
        if not pet.name.strip():
            raise ValueError("Pet name is required.")
        if any(p.name.casefold() == pet.name.casefold() for p in self.pets):
            raise ValueError("A pet with that name already exists.")
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return (pet, task) pairs from every pet owned by this owner."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        """Use the owner's aggregate task interface as the source of truth."""
        self.owner = owner

    def filter_tasks(self, pet_name=None, completed=None, on_date=None):
        """Filter all pets' tasks by optional pet, status, and date criteria."""
        return [(pet, task) for pet, task in self.owner.get_all_tasks()
                if (pet_name is None or pet.name == pet_name)
                and (completed is None or task.completed == completed)
                and (on_date is None or task.due_date == on_date)]

    def sort_by_time(self, **filters):
        """Return filtered task pairs ordered by date and normalized HH:MM."""
        return sorted(self.filter_tasks(**filters), key=lambda pair: (pair[1].due_date, pair[1].time))

    def update_task(self, task_id, *, description, time, due_date, frequency,
                    duration_minutes, priority):
        """Validate and replace a pending occurrence while preserving its ID."""
        for pet, task in self.owner.get_all_tasks():
            if task.id == task_id:
                if task.completed:
                    raise ValueError("Completed occurrences cannot be edited.")
                updated = replace(task, description=description, time=time,
                                  due_date=due_date, frequency=frequency,
                                  duration_minutes=duration_minutes, priority=priority)
                pet.tasks[pet.tasks.index(task)] = updated
                return updated
        raise ValueError("Task not found.")

    def mark_task_complete(self, task_id):
        """Complete once and append the next daily or weekly occurrence."""
        for pet, task in self.owner.get_all_tasks():
            if task.id == task_id:
                if task.completed:
                    return None
                task.mark_complete()
                if task.frequency == "once":
                    return None
                days = 1 if task.frequency == "daily" else 7
                following = replace(task, due_date=task.due_date + timedelta(days=days),
                                    completed=False, id=uuid4().hex)
                pet.add_task(following)
                return following
        raise ValueError("Task not found.")

    def detect_conflicts(self, on_date=None):
        """Warn about pending tasks with identical dates and start times."""
        slots = {}
        for pet, task in self.filter_tasks(completed=False, on_date=on_date):
            slots.setdefault((task.due_date, task.time), []).append(f"{pet.name}: {task.description}")
        return [f"Conflict on {day} at {time}: {'; '.join(names)}"
                for (day, time), names in sorted(slots.items()) if len(names) > 1]

    def build_plan(self, on_date, available_minutes):
        """Select pending tasks by priority within a total care-time budget."""
        if available_minutes < 0:
            raise ValueError("Available minutes cannot be negative.")
        ranks = {"high": 0, "medium": 1, "low": 2}
        candidates = sorted(self.filter_tasks(completed=False, on_date=on_date),
                            key=lambda pair: (ranks[pair[1].priority], pair[1].time))
        chosen, skipped = [], []
        remaining = available_minutes
        for pet, task in candidates:
            if task.duration_minutes <= remaining:
                chosen.append((pet, task))
                remaining -= task.duration_minutes
            else:
                skipped.append((pet, task))
        return sorted(chosen, key=lambda pair: pair[1].time), skipped
