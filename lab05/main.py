import telebot
from model import predict

token = 'TOKEN'
bot = telebot.TeleBot(token)
symptoms = []

@bot.message_handler(commands=['start'])
def handle_start(message):
	handle_start_msg = 'Я помогаю определить заболевание ротовой полости. \n' \
	               '\n' \
	               'Отправьте мне Ваши симптомы.'

	bot.send_message(message.chat.id, handle_start_msg)


@bot.message_handler(func=lambda m: True)
def handle_symptoms(message):
	global symptoms
	if len(symptoms) > 0:
		symptoms.append(message.text)
		curr_symptoms = ' '.join(symptoms)
		prediction = predict(curr_symptoms)
	else:
		prediction = predict(message.text)
	print(prediction)
	intent = prediction['intent']
	problem = intent['problem']
	appointment = intent['appointment']
	other = intent['other']
	disease = prediction['disease']
	advice = {'stomatit': 'Вам могут понадобиться физиотерапевтические процедуры (УФО, облучение гелий-неоновым лазером), но в первую очередь уделите особое внимание гигиене ротовой полости, используйте ополаскиватель для рта.',
		'pulpit': 'Вам следует отправиться к врачу как можно быстрее, в противном случае вам придётся удалять пульпу.',
		'gingvit': 'Вам необходимо обратиться в стоматологию для проведения профессиональной гигиены рта. Кроме этого, рекомендуется скорректировать нынешний подход к личной гигиене рта.'}
	pred_disease = ''
	if problem > 0.6:
		if len(symptoms) > 0:
			symptoms = []
		if disease['stomatit'] > 0.6:
			pred_disease = 'Скорее всего, у вас стоматит. \n'\
				'Совет: {}'.format(advice['stomatit'])
		if disease['pulpit'] > 0.6:
			pred_disease = 'Скорее всего, у вас пульпит. \n'\
				'Совет: {}'.format(advice['pulpit'])
		if disease['gingvit'] > 0.6:
			pred_disease = 'Скорее всего, у вас гингивит. \n'\
				'Совет: {}'.format(advice['gingvit'])
		if disease['gingvit'] <= 0.5 and disease['stomatit'] <= 0.5 and disease['pulpit'] <= 0.5:
			symptoms.append(message.text)
			pred_disease = ''
		
		if len(pred_disease) > 0:
			answer = '{} \n'\
				'За более точным диагнозом обращайтексь к специалисту.'.format(pred_disease)
		else:
			answer = 'Опишите подробнее, пожалуйста'
	elif problem < 0.5:
		symptoms.append(message.text)
		answer = 'Опишите подробнее, пожалуйста'
	bot.send_message(message.chat.id, answer)


def main():
	bot.polling(none_stop=True)

if __name__ == "__main__":
	main()
