from datetime import datetime

def calculate_days_left(exam_date):
    """Calculate the number of days left until the exam."""
    today = datetime.now().date()
    exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date()
    return max((exam_date - today).days, 0)

def save_data_txt(subjects, daily_hours, filename="study_data.txt"):
    """Save subjects and daily hours to a text file."""
    with open(filename, "w") as file:
        file.write(f"{daily_hours}\n")
        for subject in subjects:
            file.write(f"{subject['name']},{subject['exam_date']},{subject['completed']}\n")

def load_data_txt(filename="study_data.txt"):
    """Load subjects and daily hours from a text file."""
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            daily_hours = float(lines[0].strip())
            subjects = []
            for line in lines[1:]:
                name, exam_date, completed = line.strip().split(",")
                days_left = calculate_days_left(exam_date)
                subjects.append({"name": name, "exam_date": exam_date, "days_left": days_left, "completed": completed == "True"})
            return subjects, daily_hours
    except FileNotFoundError:
        return None, None

def get_user_data():
    """Collect user input for subjects, available hours, and deadlines."""
    print("Welcome to the AI-Based Personalized Study Planner!")
    print("Please provide the following details:")
    
    subjects = []
    n = int(input("How many subjects do you have? "))
    
    for _ in range(n):
        subject = input("Enter subject name: ")
        exam_date = input(f"Enter the exam date for {subject} (YYYY-MM-DD): ")
        days_left = calculate_days_left(exam_date)
        subjects.append({"name": subject, "exam_date": exam_date, "days_left": days_left, "completed": False})
    
    daily_hours = float(input("How many hours can you study daily? "))
    return subjects, daily_hours

def generate_schedule(subjects, daily_hours):
    """Generate a dynamic schedule based on the subject deadlines."""
    print("\nGenerating your personalized study schedule...")
    total_weight = sum(1 / subject["days_left"] for subject in subjects if not subject["completed"] and subject["days_left"] > 0)
    
    schedule = []
    for subject in subjects:
        if not subject["completed"] and subject["days_left"] > 0:
            weight = (1 / subject["days_left"]) / total_weight
            time_allocated = daily_hours * weight
            schedule.append({"name": subject["name"], "time_allocated": round(time_allocated, 2)})
    
    return schedule

def display_schedule(schedule):
    """Display the generated schedule to the user."""
    print("\nToday's Study Schedule:")
    for task in schedule:
        print(f"- {task['name']}: {task['time_allocated']} hours")
    print("Remember to take a 10-minute break every hour!")

def update_progress(subjects):
    """Update the progress of subjects after the day's study."""
    print("\nUpdate your progress for today:")
    for subject in subjects:
        if not subject["completed"]:
            status = input(f"Did you complete your tasks for {subject['name']}? (yes/no): ").strip().lower()
            if status == "yes":
                subject["completed"] = True
    return subjects

def main():
    subjects, daily_hours = load_data_txt()
    
    if not subjects:
        subjects, daily_hours = get_user_data()
        save_data_txt(subjects, daily_hours)
    else:
        print("Welcome back! Loading your previous data...\n")
    
    while True:
        print("\n--- Study Planner Menu ---")
        print("1. View today's schedule")
        print("2. Update progress")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            schedule = generate_schedule(subjects, daily_hours)
            display_schedule(schedule)
        elif choice == "2":
            subjects = update_progress(subjects)
            save_data_txt(subjects, daily_hours)
        elif choice == "3":
            print("Goodbye! Keep studying and stay focused.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
