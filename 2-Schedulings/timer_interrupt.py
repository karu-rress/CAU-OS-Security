import time
import threading

def process(name, duration):
    for i in range(duration):
        print(f"{name} is running... {i+1}")
        time.sleep(1)

def timer_interrupt():
    while True:
        time.sleep(10)  # Fill in the blank: Set the timer interval (in seconds)
        print("Timer interrupt: Switching process!")

try:
    # Run the timer interrupt in a separate thread
    interrupt_thread = threading.Thread(target=timer_interrupt)  # Fill in the blank: Assign the timer_interrupt function here
    interrupt_thread.daemon = True
    interrupt_thread.start()

    # Run processes A and B
    process("Process A", 10)  # Fill in the blank: Enter the name for the first process
    process("Process B", 10)  # Fill in the blank: Enter the name for the second process

except KeyboardInterrupt:
    exit(0)
