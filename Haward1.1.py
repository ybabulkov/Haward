import PySimpleGUI as sg
import os
import numpy

import Timer
# TODO
'''
1. Make it adaptable to different directories for the files
2. Subtract an amount from the current balance
3. Fix timer (when closing main window the timer should close too)

'''
os.chdir(("D:\io4k0\Codes\SimpleHabitRewardSystem\dist"))


def calculate_overall_money(file_name, money_to_add):
	with open(file_name) as file:
		lines = file.readlines()
		return float(lines[2]) + money_to_add


def reset_checkboxes():
	for key in values.keys():
		if key != "Menu":
			values[key] = False
			window[key].update(False)


def reset():
	with open("rewards_log.txt", 'w') as rewards_file:
		rewards_file.write(','.join(reward_for_habit.keys()))
		rewards_file.write('\n0,0,0,0,0')
		rewards_file.write('\n0.0')
	reward_amount("Reward = 0.00lv")
	money_earned("Overall money earned: 0.0")
	progress_bar.update(0)
	reset_checkboxes()


# -----------------------------------------------------------------------------------------------

sg.theme("DarkAmber")
menu_def = [["File", ["Reset", "Save", "Exit"]], ["Timer", ["Open timer"]]]
layout = [
		  [sg.Menu(menu_def, key="Menu")],
		  [sg.Checkbox("Read", default=False, enable_events=True, key="Read"),
		   sg.Checkbox("Code", default=False, enable_events=True, key="Code"),
		   sg.Checkbox("Workout", default=False, enable_events=True, key="Workout"),
		   sg.Checkbox("Mindfulness", default=False, enable_events=True, key="Mindfulness"),
		   sg.Checkbox("Stretch", default=False, enable_events=True, key="Stretch")],
		  [sg.ProgressBar(5, orientation='h', size=(27, 30), key='progressbar', pad=(2, 10))],
		  [sg.Text("Bonus reward for completing all habits!", size=(35, 2), key='completed_text', pad=((60, 0), 2))],
		  [sg.Text("Reward = 0 lv", size=(12, 1), key='reward_amount')],
		  [sg.Text(f"Balance: {calculate_overall_money('rewards_log.txt', 0)} lv", size=(15, 1), key='money_earned'),
		   sg.Spin([i for i in numpy.arange(0, 100, 0.1)], key="Subtract", initial_value=0,
		   size=(5, 4), pad=((60, 0), 0), enable_events=True),
		   sg.Text("Subtract from balance", size=(16, 1))]
		  ]


window = sg.Window("Haward", layout)
progress_bar = window['progressbar']
all_completed_text = window['completed_text']
reward_amount = window['reward_amount']
money_earned = window['money_earned']

# stores the amount of lv that is rewarded upon completion of the habit
reward_for_habit = {"Read": 0.4, "Code": 0.6, "Workout": 0.5, "Mindfulness": 0.3, "Stretch": 0.3}
timer = Timer.__call__()
timer_reward = 0.0

# ----------------------------- main loop ------------------------------------
while True:
	event, values = window.read()
	if event == sg.WINDOW_CLOSED or event == 'Exit':
		window.close()
		break
	# stores the number of days in which a certain habit has been completed
	completed_habits = 0
	reward_for_the_day = 0.0
	habit_days_completed = {"Read": 0, "Code": 0, "Workout": 0, "Mindfulness": 0, "Stretch": 0}
	habits = {habit: values[habit] for habit in list(values.keys())[1:6]}

	# calculating reward for habit completion
	for habit, completed in habits.items():
		if completed:
			habit_days_completed[habit] = 1
			completed_habits += 1
			progress_bar.update(completed_habits)
			reward_for_the_day += reward_for_habit[habit]

	if event != sg.WINDOW_CLOSED and event not in ["Save", "Reset", "Open timer"]:

		# in none of the habits are completed
		if all(not completed for completed in list(habits.values())):
			progress_bar.update(0)
		# if all of the habits are completed
		if all(completed for completed in list(habits.values())):
			reward_for_the_day = 4
			all_completed_text("All habits completed!".rjust(35))
		else:
			all_completed_text("Bonus reward for completing all habits!")

	elif event == "Save":
		# storing info into variables
		with open("rewards_log.txt", 'r') as rewards_log:
			data = rewards_log.readlines()
			i = 0
			for habit in habit_days_completed.keys():
				habit_days_completed[habit] += int(data[1].split(',')[i])
				i += 1

		# updating the info in the file
		overall_money = calculate_overall_money('rewards_log.txt', reward_for_the_day - float(values['Subtract']))
		with open("rewards_log.txt", 'w') as rewards_log:
			rewards_log.write(','.join(habit_days_completed.keys()))
			rewards_log.write('\n')
			rewards_log.write(','.join((map(str, habit_days_completed.values()))))
			rewards_log.write(f"\n{overall_money:.2f}")
		reset_checkboxes()
		reward_amount("Reward = 0.00lv")
		progress_bar.update(0)

	elif event == "Reset":
		reset()

	elif event == "Open timer":
		current_time = timer.main_loop()
		# a minute is 6000 /because milliseconds are also included in current_time/, so ст per minute will be time // 6000
		time_reward = current_time // 100
		print(time_reward)
		timer_reward += (time_reward / 100)

	reward_for_the_day += timer_reward
	reward_amount(f"Reward = {reward_for_the_day:.2f} lv")
	money_earned(f"Balance: {calculate_overall_money('rewards_log.txt', reward_for_the_day - float(values['Subtract'])):.2f} lv")
window.close()