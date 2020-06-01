import telebot
from model import predict

token = 'TOKEN'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def handle_start(message):
	handle_start_msg = 'Я помогаю определить заболевание ротовой полости. \n' \
	               '\n' \
	               'Отправьте мне Ваши симптомы.'

	bot.send_message(message.chat.id, handle_start_msg)


@bot.message_handler(func=lambda m: True)
def handle_symptoms(message):
	prediction = predict(message.text)
	bot.send_message(message.chat.id, prediction)


def main():
	bot.polling(none_stop=True)

if __name__ == "__main__":
	main()
