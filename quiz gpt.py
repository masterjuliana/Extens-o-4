from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
import json

# Tela inicial para escolher tema
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Escolha um tema")
        button_quiz = Button(text="Iniciar Quiz", on_press=self.start_quiz)
        layout.add_widget(label)
        layout.add_widget(button_quiz)
        self.add_widget(layout)

    def start_quiz(self, instance):
        self.manager.current = "quiz"

# Tela do quiz
class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.question_index = 0
        self.questions = [
            {"question": "Qual a unidade de pressão?", "image": "pressure-unit.png", "options": ["Pa", "Kg", "L"], "answer": "Pa"},
            {"question": "O que é vazão?", "image": "flow.png", "options": ["Volume por tempo", "Pressão", "Temperatura"], "answer": "Volume por tempo"}
        ]
        self.layout = BoxLayout(orientation='vertical')

        self.question_label = Label(text=self.questions[self.question_index]['question'])
        self.layout.add_widget(self.question_label)

        self.image = Image(source=self.questions[self.question_index]['image'])
        self.layout.add_widget(self.image)

        self.buttons = BoxLayout(orientation='horizontal')
        for option in self.questions[self.question_index]["options"]:
            button = Button(text=option, on_press=self.check_answer)
            self.buttons.add_widget(button)
        
        self.layout.add_widget(self.buttons)
        self.add_widget(self.layout)

    def check_answer(self, instance):
        answer = instance.text
        correct_answer = self.questions[self.question_index]['answer']
        
        if answer == correct_answer:
            self.score += 1
            sound = SoundLoader.load('correct.mp3')
            sound.play()
        else:
            sound = SoundLoader.load('wrong.mp3')
            sound.play()

        self.question_index += 1
        if self.question_index < len(self.questions):
            self.update_question()
        else:
            self.show_result()

    def update_question(self):
        self.question_label.text = self.questions[self.question_index]['question']
        self.image.source = self.questions[self.question_index]['image']
        for i, option in enumerate(self.questions[self.question_index]["options"]):
            self.buttons.children[i].text = option

    def show_result(self):
        self.manager.current = "result"
        self.manager.get_screen("result").update_result(self.score)

# Tela de resultado
class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.result_label = Label(text="Resultado:")
        self.layout.add_widget(self.result_label)

        button_restart = Button(text="Reiniciar", on_press=self.restart_quiz)
        self.layout.add_widget(button_restart)
        self.add_widget(self.layout)

    def update_result(self, score):
        self.result_label.text = f"Você acertou {score} de 2 perguntas!"

        # Salvar pontuação no arquivo
        with open("score.json", "w") as file:
            json.dump({"score": score}, file)

    def restart_quiz(self, instance):
        self.manager.current = "home"

# Gerenciador de telas
class ScreenManagement(ScreenManager):
    pass

# App principal
class QuizApp(App):
    def build(self):
        sm = ScreenManagement()

        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(QuizScreen(name="quiz"))
        sm.add_widget(ResultScreen(name="result"))

        return sm

if __name__ == "__main__":
    QuizApp().run()
