from datetime import datetime
import json
import random


class Results():
    def __init__(self, score, player_name, secret_number, wrong_nr, date):
        self.score = score
        self.player_name = player_name
        self.secret_number = secret_number
        self.wrong_nr = wrong_nr
        self.date = date


secret = random.randint(1, 30)

# DEBUG
# secret = 1
attempts = 0
wrong_guesses = []


with open("results.txt", "r") as score_file:
    score_list = json.loads(score_file.read())
    print("Top scores: " + str(score_list))
score_list = sorted(score_list, key=lambda i: (i['score'], i['date']))

print('')
print('')

print('Top 3:')
top = 1
# for score_dict in score_list:
for score_dict in score_list:

    time_dic = datetime.strptime(score_dict.get("date"), "%Y-%m-%d %H:%M:%S.%f")
    time_string = time_dic.strftime("%d.%m.%Y, %H:%M")

    wrong = (str(score_dict.get("wrong_nr"))[1:-1])
    if wrong == '':
        wrong = '--'

    print('Top {0}: {1} - attempts: {2} | {3} | secret number: {4} - wrong guesses were: {5}'.
          format(top,
                 score_dict["player_name"],
                 str(score_dict["score"]),
                 time_string,
                 score_dict.get("secret_number"),
                 wrong))
    if top == 3:
        break
    top += 1
print('')
print('')

while True:
    guess = int(input("Guess the secret number (between 1 and 30): "))
    attempts += 1

    if guess != secret:
        wrong_guesses.append(guess)

    if guess == secret:
        print("You've guessed it - congratulations! It's number " + str(secret))
        print("Attempts needed: " + str(attempts))

        while True:
            user = input('Please enter your name for the high score list:  ')
            if user:
                break

        new_player = Results(attempts, user, str(secret), wrong_guesses, str(datetime.now()))

        score_list.append(new_player.__dict__)

        with open("results.txt", "w") as score_file:
            score_file.write(json.dumps(score_list))

        break
    elif guess > secret:
        print("Your guess is not correct... try something smaller")
    elif guess < secret:
        print("Your guess is not correct... try something bigger")