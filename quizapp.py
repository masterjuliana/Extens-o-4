from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image # Import Image widget
import json
from kivy.clock import Clock
import os
import random
import sys # Import sys to potentially exit on critical error

# Caminho absoluto para o arquivo
caminho_arquivo = r"W:\UVA\Trimestre 4 - 2025\Atividade de Extensão 4\forca\teste livro\banco_de_questoes_hidraulica.json"
caminho_arquivo_gif = r"W:\UVA\Trimestre 4 - 2025\Atividade de Extensão 4\forca\teste livro\ANAGEA.gif"

try:
    with open(caminho_arquivo, 'r', encoding='utf-8') as file: # <--- Added encoding='utf-8'
        banco_de_questoes = json.load(file)
except FileNotFoundError:
    print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
    # You might want to exit or handle this gracefully if it's critical
    # sys.exit(1) or raise an exception
    banco_de_questoes = [] # Assign an empty list to avoid NameError later
except json.JSONDecodeError:
    print(f"Erro: O arquivo '{caminho_arquivo}' está mal formatado.")
    # Handle malformed JSON, maybe exit or use an empty list
    banco_de_questoes = [] # Assign an empty list
except Exception as e: # Catch any other potential errors during load
    print(f"Erro inesperado ao carregar JSON: {e}")
    banco_de_questoes = [] # Assign an empty list
    
# Cores em tons de azul
BACKGROUND_COLOR = get_color_from_hex("#E0F2F7")  # Azul bem claro
BUTTON_COLOR = get_color_from_hex("#42A5F5")      # Azul mais claro
BUTTON_TEXT_COLOR = get_color_from_hex("#FFFFFF")  # Branco
LABEL_TEXT_COLOR = get_color_from_hex("#1976D2")   # Azul um pouco mais escuro

class AnimatedODS(BoxLayout):
    def __init__(self, ods_number, ods_description, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        number_label = Label(text=ods_number, font_size=30, color=LABEL_TEXT_COLOR, halign='center')
        description_label = Label(text=ods_description, font_size=14, color=LABEL_TEXT_COLOR, halign='center', text_size=(self.width * 0.9, None), valign='top')
        description_label.bind(width=lambda s, w: setattr(description_label, 'text_size', (w * 0.9, None)))
        self.add_widget(number_label)
        self.add_widget(description_label)
        self.anim = Animation(opacity=0, duration=1) + Animation(opacity=1, duration=1)
        self.anim.repeat = True
        self.anim.start(number_label)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        with layout.canvas.before:
            Color(*BACKGROUND_COLOR)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Add the GIF Image at the top
        if os.path.exists(caminho_arquivo_gif): # Check if GIF exists
             self.gif_image = Image(
                 source=caminho_arquivo_gif,
                 size_hint=(1, None), # Use fixed height or proportional
                 height=250, # Adjust height as needed
                 allow_stretch=True,
                 keep_ratio=True, # Keep aspect ratio
                 anim_delay=0.1 # Optional: Adjust animation speed
             )
             layout.add_widget(self.gif_image)
        else:
            print(f"Aviso: Arquivo GIF não encontrado em '{caminho_arquivo_gif}'")
            # Add a placeholder or just skip adding the image if not found

        welcome_label = Label(
            text="Seja bem vindo(a) gestor(a) ambiental do futuro!",
            font_size=24,
            color=LABEL_TEXT_COLOR,
            halign='center',
            valign='middle',
            size_hint=(1, 0.15)
        )
        layout.add_widget(welcome_label)

        ods_layout = BoxLayout(orientation="horizontal", spacing=20, size_hint=(1, 0.3), padding=(20, 0))
        ods4_description = "ODS 4: Garantir uma educação de qualidade para todos."
        ods5_description = "ODS 5: Alcançar a igualdade de gênero e empoderar todas as mulheres e meninas."
        ods6_description = "ODS 6: Garantir o acesso à água potável e ao saneamento básico para todos."
        ods4 = AnimatedODS(ods_number="ODS 4", ods_description=ods4_description, size_hint_x=1)
        ods5 = AnimatedODS(ods_number="ODS 5", ods_description=ods5_description, size_hint_x=1)
        ods6 = AnimatedODS(ods_number="ODS 6", ods_description=ods6_description, size_hint_x=1)
        ods_layout.add_widget(ods4)
        ods_layout.add_widget(ods5)
        ods_layout.add_widget(ods6)
        layout.add_widget(ods_layout)

        invitation_part1 = (
            "Homens e meninos, mas principalmente Mulheres e meninas, unam-se aos grandes "
            "profissionais de hidráulica do Brasil! Esse jogo é inclusivo e colabora para meninas "
            "e mulheres despertarem o interesse por ciências, tecnologia, engenharia e matemática."
        )
        invitation_label1 = Label(
            text=invitation_part1,
            font_size=14,
            color=LABEL_TEXT_COLOR,
            halign='left',
            valign='middle',
            size_hint=(1, 0.2),
            text_size=(layout.width * 0.9, None),
            line_height=1.2
        )
        invitation_label1.bind(width=lambda s, w: setattr(invitation_label1, 'text_size', (w * 0.9, None)))
        layout.add_widget(invitation_label1)

        invitation_part2 = (
            "Testemunhem e contribuam para a grandiosidade de obras como a Usina de Itaipu, "
            "a Transposição do Rio São Francisco e o Complexo Hidrelétrico de Belo Monte. "
            "Inspirados pelo legado de figuras como Azevedo Netto, cuja visão moldou a engenharia "
            "hidráulica nacional, convidamos vocês a serem protagonistas na gestão ambiental do futuro."
        )
        invitation_label2 = Label(
            text=invitation_part2,
            font_size=14,
            color=LABEL_TEXT_COLOR,
            halign='left',
            valign='middle',
            size_hint=(1, 0.2),
            text_size=(layout.width * 0.9, None),
            line_height=1.2
        )
        invitation_label2.bind(width=lambda s, w: setattr(invitation_label2, 'text_size', (w * 0.9, None)))
        layout.add_widget(invitation_label2)

        invitation_part3 = (
            "E o primeiro passo é mergulhar nos conceitos de hidráulica e conhecer grandes nomes "
            "que participaram da história de um conhecimento tão precioso para a sociedade e essencial "
            "para o futuro!"
        )
        invitation_label3 = Label(
            text=invitation_part3,
            font_size=14,
            color=LABEL_TEXT_COLOR,
            halign='left',
            valign='middle',
            size_hint=(1, 0.15),
            text_size=(layout.width * 0.9, None),
            line_height=1.2
        )
        invitation_label3.bind(width=lambda s, w: setattr(invitation_label3, 'text_size', (w * 0.9, None)))
        layout.add_widget(invitation_label3)

        play_button = Button(
            text="Jogar",
            size_hint=(1, 0.1),
            background_color=BUTTON_COLOR,
            color=BUTTON_TEXT_COLOR
        )
        play_button.bind(on_press=self.start_game)
        layout.add_widget(play_button)

        exit_button = Button(
            text="Sair",
            size_hint=(1, 0.05),
            background_color=BUTTON_COLOR,
            color=BUTTON_TEXT_COLOR
        )
        exit_button.bind(on_press=self.exit_game)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def start_game(self, instance):
        self.manager.current = "question_screen"

    def exit_game(self, instance):
        App.get_running_app().stop()

class QuestionScreen(Screen):
    def __init__(self, banco_de_questoes, filename, **kwargs):
        super().__init__(**kwargs)
        # Defina o timer_label corretamente
        self.timer_label = Label(text="Tempo: 0s", font_size=30)
        
        # Adicione o timer_label ao layout
        self.add_widget(self.timer_label)
        self.banco_de_questoes = banco_de_questoes
        self.question_index = 0
        self.score = 0
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        with self.layout.canvas.before:
            Color(*BACKGROUND_COLOR)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Add the GIF Image at the top
        if os.path.exists(caminho_arquivo_gif): # Check if GIF exists
             self.gif_image = Image(
                 source=caminho_arquivo_gif,
                 size_hint=(1, None), # Use fixed height or proportional
                 height=200, # Adjust height as needed
                 allow_stretch=True,
                 keep_ratio=True, # Keep aspect ratio
                 anim_delay=0.1 # Optional: Adjust animation speed
             )
             self.layout.add_widget(self.gif_image)
        else:
            print(f"Aviso: Arquivo GIF não encontrado em '{caminho_arquivo_gif}'")
            # Add a placeholder or just skip adding the image if not found

        # Carregar as questões
        self.load_questions(filename)  # Passando o 'filename' aqui
        self.start_timer()
        
        self.question_label = Label(text="", font_size=16, color=LABEL_TEXT_COLOR, size_hint=(1, 0.2))
        self.layout.add_widget(self.question_label)

        self.buttons = []
        for i in range(4):  # Supondo 4 alternativas por questão
            btn = Button(text="", size_hint=(1, 0.1), background_color=BUTTON_COLOR, color=BUTTON_TEXT_COLOR)
            btn.bind(on_press=self.check_answer)
            self.buttons.append(btn)
            self.layout.add_widget(btn)

        self.feedback_label = Label(text="", font_size=16, color=LABEL_TEXT_COLOR, size_hint=(1, 0.2))
        self.layout.add_widget(self.feedback_label)

        self.timer_label = Label(text="Tempo: 30s", font_size=16, color=LABEL_TEXT_COLOR, size_hint=(1, 0.1))
        self.layout.add_widget(self.timer_label)

        self.score_label = Label(text="Pontos: 0", font_size=16, color=LABEL_TEXT_COLOR, size_hint=(1, 0.1))
        self.layout.add_widget(self.score_label)

        self.next_button = Button(text="Próxima", size_hint=(1, 0.1), background_color=BUTTON_COLOR, color=BUTTON_TEXT_COLOR)
        self.next_button.bind(on_press=self.next_question)
        self.next_button.disabled = True
        self.layout.add_widget(self.next_button)

        self.add_widget(self.layout)

        self.load_question()  # Carrega a primeira pergunta


    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def load_questions(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.banco_de_questoes = json.load(f)
            random.shuffle(self.banco_de_questoes)
        except Exception as e:
            print(f"Erro ao carregar questões: {e}")
            self.banco_de_questoes = []

    def load_question(self):
        if self.question_index >= len(self.banco_de_questoes):
            self.end_game()
            return

        question_data = self.banco_de_questoes[self.question_index]
        self.question_label.text = question_data["pergunta"]
       
        alternativas = question_data.get("alternativas", [])
        for i in range(len(self.buttons)):
            if i < len(alternativas):
                self.buttons[i].text = alternativas[i]
                self.buttons[i].disabled = False
            else:
                self.buttons[i].text = ""
                self.buttons[i].disabled = True
    def start_timer(self):
        self.time_left = 30
        self.timer_label.text = f"Tempo: {self.time_left}s"
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"Tempo: {self.time_left}s"
        if self.time_left <= 0:
            self.check_answer(None)
            self.stop_timer()

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

    def check_answer(self, instance):
        self.stop_timer()
        resposta_usuario = instance.text[0] if instance else None
        resposta_correta = self.banco_de_questoes[self.question_index]["resposta_correta"]
        print(f"Resposta do usuário: {resposta_usuario}, Resposta correta: {resposta_correta}") # Adicionado

        if resposta_usuario == resposta_correta:
            self.score += 1
            self.feedback_label.text = "Resposta Correta!"
        else:
            self.feedback_label.text = f"Resposta Errada! A resposta correta é: {resposta_correta}"
        self.feedback_label.text += "\n" + self.banco_de_questoes[self.question_index]["feedback"]

        for button in self.buttons:
            button.disabled = True
        self.score_label.text = f"Pontos: {self.score}"
        self.next_button.disabled = False

    def next_question(self, instance):
        self.question_index += 1
        self.load_question()
        self.start_timer()

    def end_game(self):
        self.layout.clear_widgets()
        final_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        with final_layout.canvas.before:
            Color(*BACKGROUND_COLOR)
            self.rect = Rectangle(size=final_layout.size, pos=final_layout.pos)
        final_layout.bind(size=self._update_rect, pos=self._update_rect)
        final_score_label = Label(text=f"Fim do Quiz! Você fez {self.score} pontos!", size_hint=(1, 0.2), color=LABEL_TEXT_COLOR)
        final_layout.add_widget(final_score_label)

        restart_button = Button(
            text="Recomeçar",
            size_hint=(1, 0.2),
            background_color=BUTTON_COLOR,
            color=BUTTON_TEXT_COLOR
        )
        restart_button.bind(on_press=self.restart_game)
        final_layout.add_widget(restart_button)

        exit_button = Button(
            text="Sair",
            size_hint=(1, 0.2),
            background_color=BUTTON_COLOR,
            color=BUTTON_TEXT_COLOR
        )
        exit_button.bind(on_press=self.exit_game)
        final_layout.add_widget(exit_button)

        self.add_widget(final_layout)

    def restart_game(self, instance):
        self.manager.current = "menu_screen"  # Voltar ao menu
        self.question_index = 0
        self.score = 0
        self.layout.clear_widgets()
        self.__init__(self.banco_de_questoes, filename=r"W:\UVA\Trimestre 4 - 2025\Atividade de Extensão 4\forca\teste livro\banco_de_questoes_hidraulica.json")
        self.load_question()
        self.start_timer()

    def exit_game(self, instance):
        App.get_running_app().stop()

class QuizApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu_screen"))
        sm.add_widget(QuestionScreen(banco_de_questoes=[], filename=r"W:\UVA\Trimestre 4 - 2025\Atividade de Extensão 4\forca\teste livro\banco_de_questoes_hidraulica.json", name="question_screen"))
        return sm

if __name__ == '__main__':
    QuizApp().run()

