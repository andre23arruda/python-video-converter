import cv2, os

LOCAL_PATH = os.path.dirname(__file__)

TEXT_COLOR_GRAY = (150, 150, 150)
VIDEO_FORMAT_LIST = [
    ('.mp4', 0),
    ('.mov', 1),
    ('.avi', 2)
]


def create_output_path(input_video_path, video_format):
    '''Cria nome do arquivo de saída'''
    file_folder, file_name = os.path.split(input_video_path)
    return os.path.join(
        file_folder,
        f'output_ { os.path.splitext(file_name)[0] }{ video_format }'
    )


def string_break_line(value):
    '''Quebra a string em linhas'''
    line_max_length = 40
    number_break_lines = int((len(value))/line_max_length) + 1

    new_value = [f'{ value[i*line_max_length:(i+1)*line_max_length] }' for i in range(number_break_lines)]
    return '\n'.join(new_value)


def result_text(selected_files, output_path):
    '''Cria mensagem de resultado'''
    if (len(selected_files) > 1):
        return f'Arquivos convertidos com sucesso.\nSalvo em: { os.path.split(output_path)[0] }\n\n'
    return f'Arquivo convertido com sucesso.\nSalvo como: { string_break_line(output_path) }\n\n'


def video_converter(application, video_path):
    '''Converte vídeo para .mp4'''

    cap = cv2.VideoCapture(video_path)
    success, image = cap.read()

    # frames
    fps: int = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # codec
    codec ='MJPG'
    fourcc = cv2.VideoWriter_fourcc(*codec)

    # # muda codec se for avi
    # if application.choice_video_format.get() == 2:
    #     codec ='MJPG'
    #     fourcc = cv2.VideoWriter_fourcc(*codec)
    # else:
    #     fourcc = -1

    # cria nome do arquivo de saída e video writer
    video_format =  VIDEO_FORMAT_LIST[application.choice_video_format.get()][0]
    output_path = create_output_path(video_path, video_format)
    video_out = cv2.VideoWriter(output_path, fourcc, fps, (image.shape[1], image.shape[0]))

    current_value = 0
    application.progress_bar['maximum'] = frames

    while success:
        current_value += 1
        application.progress_bar['value'] = current_value
        application.progress_bar.update()

        video_out.write(image)
        success, image = cap.read()

    # fecha video
    cap.release()
    video_out.release()
    return output_path