from threading import Thread
from accounts import Accounts
from plans import Plans
from TDCBot import TDCBot


def run(numbers):
    bot = TDCBot(
        remark="EXAMPLE",
        plan=Plans.EXAMPLE,
        account=Accounts.EXAMPLE,
        numbers=numbers,
    )
    # Start the bot and generate a report after the thread has completed.
    bot.start()
    bot.report()


def load_numbers():
    # Load the SIM card numbers from the file, return a list of them.
    with open("numbers.txt", "r") as f:
        numbers = f.readlines()
    return [line.rstrip("\n") for line in numbers]


if __name__ == "__main__":
    # Fetch all of the numbers from the numbers.txt file.s
    numbers = load_numbers()
    # Ensure that there are less threads than the numbers.
    thread_count = min(int(input("How many threads should run: ")), len(numbers))
    splited = []
    thread_pool = []

    # Split the list of the numbers into chunks for multi-thread support.
    for i in range(thread_count):
        start = int(i * len(numbers) / thread_count)
        end = int((i + 1) * len(numbers) / thread_count)
        splited.append(numbers[start:end])

    # Start the threads with their own set of numbers.
    for i in range(thread_count):
        thread = Thread(target=run, args=([splited[i]]))
        thread.start()
        thread_pool.append(thread)

    # Join the threads to the overall pool
    for each in thread_pool:
        each.join()
