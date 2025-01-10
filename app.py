from flask import Flask, render_template, request, redirect, url_for
import os
import json
import uuid

app = Flask(__name__)

# Configuraciones
UPLOAD_FOLDER = 'static/uploads'
AUDIO_VIDEO_FOLDER = os.path.join(UPLOAD_FOLDER, 'audio_video_files')
JSON_FOLDER = os.path.join(UPLOAD_FOLDER, 'json_files')

# Crear directorios si no existen
os.makedirs(AUDIO_VIDEO_FOLDER, exist_ok=True)
os.makedirs(JSON_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_VIDEO_FOLDER'] = AUDIO_VIDEO_FOLDER
app.config['JSON_FOLDER'] = JSON_FOLDER

# Extensiones permitidas
ALLOWED_AUDIO_VIDEO_EXTENSIONS = {'mp3', 'wav', 'mp4', 'avi', 'mov', 'mkv'}
ALLOWED_JSON_EXTENSIONS = {'json'}

def allowed_file(filename, allowed_set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set

def format_speaker_label(speaker_code):
    if speaker_code.startswith("S"):
        number = speaker_code[1:]
        return f"Speaker {int(number):02d}"
    elif speaker_code == "UU":
        return "Speaker Unknown"
    else:
        return "Speaker Unknown"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'media_file' not in request.files or 'json_file' not in request.files:
        return "Faltan archivos", 400
    
    media_file = request.files['media_file']
    json_file = request.files['json_file']

    if media_file.filename == '' or json_file.filename == '':
        return "No se seleccionaron archivos", 400

    if not allowed_file(media_file.filename, ALLOWED_AUDIO_VIDEO_EXTENSIONS):
        return "Formato de archivo de media no permitido", 400

    if not allowed_file(json_file.filename, ALLOWED_JSON_EXTENSIONS):
        return "Formato de archivo JSON no permitido", 400

    # Generar un ID único para la subida
    upload_id = str(uuid.uuid4())

    # Guardar archivos
    media_filename = f"{upload_id}_{media_file.filename}"
    media_path = os.path.join(app.config['AUDIO_VIDEO_FOLDER'], media_filename)
    media_file.save(media_path)

    json_filename = f"{upload_id}_{json_file.filename}"
    json_path = os.path.join(app.config['JSON_FOLDER'], json_filename)
    json_file.save(json_path)

    return redirect(url_for('view', upload_id=upload_id))

@app.route('/view/<upload_id>')
def view(upload_id):
    # Buscar archivos por upload_id
    media_file = None
    json_file = None

    for filename in os.listdir(app.config['AUDIO_VIDEO_FOLDER']):
        if filename.startswith(upload_id):
            media_file = filename
            break

    for filename in os.listdir(app.config['JSON_FOLDER']):
        if filename.startswith(upload_id):
            json_file = filename
            break

    if not media_file or not json_file:
        return "Archivos no encontrados", 404

    media_url = url_for('static', filename=f'uploads/audio_video_files/{media_file}')
    json_path = os.path.join(app.config['JSON_FOLDER'], json_file)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Procesar datos para crear bloques de speakers
    blocks = []
    current_block = None
    current_speaker = None

    for item in data:
        if item['type'] == 'word':
            speaker_code = item['alternatives'][0]['speaker']
            speaker_label = format_speaker_label(speaker_code)
            word_content = item['alternatives'][0]['content']
            start_time = item['start_time']
            end_time = item['end_time']

            # Si el speaker cambia, crea un nuevo bloque
            if speaker_label != current_speaker:
                current_speaker = speaker_label
                current_block = {
                    'speaker': speaker_label,
                    'words': []
                }
                blocks.append(current_block)
            
            # Agrega la palabra al bloque actual
            current_block['words'].append({
                'content': word_content,
                'start_time': start_time,
                'end_time': end_time
            })
        
        elif item['type'] == 'punctuation' and item.get('attaches_to') == 'previous':
            if current_block and current_block['words']:
                # Adjunta la puntuación a la última palabra del bloque actual
                current_block['words'][-1]['content'] += item['alternatives'][0]['content']

    return render_template('view.html', media_url=media_url, blocks=blocks)

if __name__ == '__main__':
    app.run(debug=True)
