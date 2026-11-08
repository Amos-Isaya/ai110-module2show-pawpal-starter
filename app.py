"""Streamlit interface for the PawPal+ logic layer."""
from datetime import date
import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾")
st.title("🐾 PawPal+")
st.caption("Plan daily care for every pet in your family.")
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner
scheduler = Scheduler(owner)
owner.name = st.text_input("Owner name", value=owner.name)
st.caption("Your data stays during this session. Closing the session may clear it.")

with st.form("add_pet", clear_on_submit=True):
    st.subheader("Add a pet")
    name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        try:
            owner.add_pet(Pet(name.strip(), species))
            st.success(f"Added {name.strip()}.")
        except ValueError as error:
            st.error(str(error))

if not owner.pets:
    st.info("Add your first pet to start scheduling care.")
    st.stop()

st.write("Your pets: " + ", ".join(pet.name for pet in owner.pets))
with st.form("add_task"):
    st.subheader("Schedule care")
    pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets])
    description = st.text_input("Task description")
    due = st.date_input("Due date", value=date.today())
    clock = st.time_input("Time")
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
    if st.form_submit_button("Add task"):
        try:
            task = Task(description, clock.strftime("%H:%M"), due, frequency, int(duration), priority)
            next(pet for pet in owner.pets if pet.name == pet_name).add_task(task)
            st.success("Task scheduled.")
        except ValueError as error:
            st.error(str(error))

st.subheader("Daily schedule")
day = st.date_input("View date", value=date.today())
pet_filter = st.selectbox("Show pet", ["All pets"] + [pet.name for pet in owner.pets])
status = st.selectbox("Status", ["All", "Pending", "Complete"])
for warning in scheduler.detect_conflicts(day):
    st.warning(warning)
rows = scheduler.sort_by_time(on_date=day,
    pet_name=None if pet_filter == "All pets" else pet_filter,
    completed={"All": None, "Pending": False, "Complete": True}[status])
if not rows:
    st.info("No tasks match these filters.")
for pet, task in rows:
    columns = st.columns([4, 1])
    columns[0].write(f"**{task.time} · {pet.name} · {task.description}**")
    columns[0].caption(f"{task.duration_minutes} min · {task.priority} · {task.frequency} · "
                       + ("Complete" if task.completed else "Pending"))
    if not task.completed and columns[1].button("Complete", key=task.id):
        scheduler.mark_task_complete(task.id)
        st.rerun()

st.subheader("Plan within your available time")
budget = st.number_input("Available care minutes", min_value=0, value=60)
chosen, skipped = scheduler.build_plan(day, int(budget))
st.caption("Uses all pets' pending tasks on this date. Selects high priorities first, then shows them by time.")
if chosen:
    st.table([{"Time": task.time, "Pet": pet.name, "Task": task.description,
               "Minutes": task.duration_minutes, "Priority": task.priority} for pet, task in chosen])
else:
    st.info("No pending tasks fit this budget.")
if skipped:
    st.warning("Outside your time budget: " + ", ".join(f"{pet.name}: {task.description}" for pet, task in skipped))
