from threading import Lock

# Shared variables for exercises
pushup_count = 0
situp_count = 0
squat_count = 0
cardio_count = 0

# Locks for thread-safe operations
pushup_lock = Lock()
situp_lock = Lock()
squat_lock = Lock()
cardio_lock = Lock()

# User weight in kilograms (example: 70 kg)
user_weight = 70  
# MET( Metabolic Equivalent of Task) values for exercises
exercise_mets = {
    'pushup': 8,
    'situp': 6,
    'squat': 5,
    'cardio': 4
}

# Lock for thread-safe operations
# exercise_lock = Lock()

# Function to update the count for a specific exercise
def update_exercise_count(exercise, value):
    global pushup_count, situp_count, squat_count, cardio_count
    if exercise == 'pushup':
        with pushup_lock:
            pushup_count += value
    elif exercise == 'situp':
        with situp_lock:
            situp_count += value
    elif exercise == 'squat':
        with squat_lock:
            squat_count += value
    elif exercise == 'cardio':
        with cardio_lock:
            cardio_count += value

# Function to get individual exercise counts
def get_exercise_counts():
    global pushup_count, situp_count, squat_count, cardio_count
    with pushup_lock:
        pushups = pushup_count
    with situp_lock:
        situps = situp_count
    with squat_lock:
        squats = squat_count
    with cardio_lock:
        cardio = cardio_count
    return {
        'pushup': pushups,
        'situp': situps,
        'squat': squats,
        'cardio': cardio
    }

# Function to calculate calories burned for an exercise
def calculate_calories(exercise, count):
    global user_weight, exercise_mets
    duration_per_rep = 0.05  # Approximate duration in minutes (3 seconds per rep)
    return exercise_mets[exercise] * user_weight * duration_per_rep * count / 60

# Function to get total energy spent
def get_total_energy():
    global pushup_count, situp_count, squat_count
    total_energy = 0
    with pushup_lock:
        total_energy += calculate_calories('pushup', pushup_count)
    with situp_lock:
        total_energy += calculate_calories('situp', situp_count)
    with squat_lock:
        total_energy += calculate_calories('squat', squat_count)
    with cardio_lock:
        total_energy += calculate_calories('cardio', cardio_count)
    return total_energy

# Function to reset all counts and total energy
def reset_all():
    global pushup_count, situp_count, squat_count, cardio_count
    # Reset counts
    with pushup_lock:
        pushup_count = 0
    with situp_lock:
        situp_count = 0
    with squat_lock:
        squat_count = 0
    with cardio_lock:
        cardio_count = 0
    
    # Reset total energy
    global total_energy_spent
    total_energy_spent = 0  # Reset energy spent


