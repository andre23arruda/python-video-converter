import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from utils import *


class Application:
    '''Estrutura da janela da aplicação'''
    def __init__(self, master=None):

        self.choice_video_format = tk.IntVar()
        self.choice_video_format.set(0)  # initializing the choice

        # Container com texto e radiobutton
        self.widget_0 = tk.Frame(master)
        self.widget_0['pady'] = 5
        self.widget_0['padx'] = 20
        self.widget_0.pack()

        tk.Label(
            self.widget_0, text='Escolha o formato de saída',
            justify=tk.LEFT, padx=20, pady=10
        ).pack()

        def change_choice_value():
            self.choice_video_format.set(self.choice_video_format.get())

        for choice, val in VIDEO_FORMAT_LIST:
            radio = tk.Radiobutton(
                self.widget_0,
                text=choice,
                padx=20,
                variable=self.choice_video_format,
                value=val,
                command=change_choice_value,
            )
            radio.pack(side=tk.LEFT)

        # Container com texto e botão
        self.widget_1 = tk.Frame(master)
        self.widget_1['pady'] = 20
        self.widget_1['padx'] = 20
        self.widget_1.pack()

        # texto
        msg = tk.Label(self.widget_1, text='Selecione os arquivos')
        msg['font'] = ('Calibri', '10', 'italic')
        msg.pack()

        # botao
        button_1 = tk.Button(self.widget_1)
        button_1['text'] = 'Selecionar'
        button_1['font'] = ('Calibri', '12')
        button_1['width'] = 14
        button_1['command'] = self.select_and_convert_file
        button_1.pack()

        # barra de progresso
        self.progress_bar = ttk.Progressbar(
            master, orient='horizontal',
            length=300, mode='determinate'
        )
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = 100
        self.progress_bar.pack(padx=20)

        # container com texto de arquivo
        self.widget_2 = tk.Frame(master)
        self.widget_2['pady'] = 20
        self.widget_2['padx'] = 20
        self.widget_2.pack()

        # texto
        self.msg2 = tk.Label(self.widget_2, text='\n\n\n')
        self.msg2['font'] = ('Calibri', '8', 'italic')
        self.msg2.pack ()


    def select_and_convert_file(self):
        ''' Seleciona arquivo e converte'''

        selected_files = fd.askopenfilenames()
        if selected_files:
            print(selected_files)
            for video_path in selected_files :
                self.msg2['text'] = f'Arquivo selecionado: \n{ string_break_line(video_path) }\n\nPor favor, aguarde...'
                try:
                    output_path = video_converter(self, video_path)
                    self.msg2['text'] = result_text(selected_files, output_path)
                except Exception as e:
                    self.msg2['text'] = f'Falha ao converter arquivo! { e }'
                    self.progress_bar['value'] = self.progress_bar['maximum']
        else:
            self.msg2['text'] = f'Nenhum arquivo selecionado'

# Run
if __name__ == '__main__':
    # Inicia interface de usuário
    root = tk.Tk(className=f' Conversor de Vídeos')
    root.resizable(False, False)
    root.iconbitmap(f'{ LOCAL_PATH }/assets/icon.ico')
    # icon_path = f'{ LOCAL_PATH }/assets/icon.png'
    # root.iconphoto(False, tk.PhotoImage(file=icon_path))

    # tamanho inicial da interface
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()

    # metade do comprimento e da largura da tela
    position_right = int(root.winfo_screenwidth()/2 - window_width/2)
    position_down = int(root.winfo_screenheight()/2 - window_height/2)

    # posiciona a janela no centro da tela
    root.geometry(f'+{ position_right }+{ position_down }')

    Application(root)
    root.mainloop()