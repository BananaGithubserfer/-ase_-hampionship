from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import json
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import whisper
import torch
import gc

import keras
#from audio_extract import extract_audio
#extract_audio(input_path="film.mp4",
#              output_path="audio.mp3")
model = whisper.load_model("turbo", device="cpu")  # Убедитесь, что модель на CPU
#result = model.transcribe("audio.mp3", fp16=False)
del model
gc.collect()
torch.cuda.empty_cache()
torch.cuda.reset_max_memory_allocated()
result = {}
with open("film.txt", "r", encoding="utf-8") as file:
    result["text"] = file.read()

    # Транскрибирование аудио

model_name = "Qwen/Qwen2.5-0.5B"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="cpu"
)
model = model.half()
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = result["text"] + ('''Составь на основе предложенной транскрибации фильма викторину по нему, нужно 10 вопросов в формате:
[
    {
        "name": "фильм-1",
        "questions": {
            "Какой цвет неба днём?": {
                "options": ["голубой", "зеленый", "красный", "черный"],
                "correct_answer": "голубой"
            },
            "Сколько дней в неделе?": {
                "options": ["шесть", "семь", "восемь", "пять"],
                "correct_answer": "семь"
            },
            "Столица Франции?": {
                "options": ["Берлин", "Лондон", "Париж", "Мадрид"],
                "correct_answer": "Париж"
            }
        }
    }
]

                         ''')
messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True
)
model_inputs = tokenizer([str(text)], return_tensors="pt").to(model.device)
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
python_object = json.loads(response)

# Сохраняем объект в файл JSON
with open("data.json", "w", encoding="utf-8") as json_file:
    json.dump(python_object, json_file, ensure_ascii=False, indent=4)
print(response)
