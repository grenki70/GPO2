import os
import random
import pandas as pd
import pygame
from datetime import datetime

DATASET_FOLDER = "Dataset"
SPEAKERS = ["Artem", "Grisha", "Nicolay"]

def initialize_audio():
    pygame.mixer.init()

def play_audio(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print("Воспроизведение аудио")
        
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    except Exception as e:
        print(f"Ошибка воспроизведения: {e}")

def get_auditor_info():
    print("\n=== Ввод данных аудитора ===")
    name = input("Введите ваше имя: ").strip()
    return name

def select_speaker():
    print("\n=== Выбор диктора ===")
    for i, speaker in enumerate(SPEAKERS, 1):
        print(f"{i}. {speaker}")
    
    while True:
        try:
            choice = int(input("Выберите диктора (1-3): "))
            if 1 <= choice <= len(SPEAKERS):
                return SPEAKERS[choice - 1]
            else:
                print("Некорректный выбор. Попробуйте снова.")
        except ValueError:
            print("Введите число от 1 до 3.")

def get_audio_files(speaker_folder):
    synthetic_folder = os.path.join(speaker_folder, "Syntes")
    real_folder = os.path.join(speaker_folder, "Real")
    
    if not os.path.exists(synthetic_folder):
        print(f"Папка '{synthetic_folder}' не найдена!")
        return [], [], "", ""
    
    if not os.path.exists(real_folder):
        print(f"Папка '{real_folder}' не найдена!")
        return [], [], "", ""
    
    synthetic_files = [f for f in os.listdir(synthetic_folder) 
                      if f.endswith(('.wav', '.mp3', '.ogg', '.flac'))]
    real_files = [f for f in os.listdir(real_folder) 
                 if f.endswith(('.wav', '.mp3', '.ogg', '.flac'))]
    
    return synthetic_files, real_files, synthetic_folder, real_folder

def save_results(results, filename):
    df = pd.DataFrame(results, columns=['Аудиозапись', 'Исходный_тип', 'Выбор_пользователя'])
    df.to_excel(filename, index=False)

def run_comparison_session(speaker, auditor_name):
    speaker_folder = os.path.join(DATASET_FOLDER, speaker)
    
    synthetic_files, real_files, synth_path, real_path = get_audio_files(speaker_folder)
    
    if not synthetic_files or not real_files:
        print("Не найдены аудио файлы для сравнения!")
        return
    
    print(f"\nНайдено {len(synthetic_files)} синтезированных и {len(real_files)} реальных аудио файлов")
    
    random.shuffle(synthetic_files)
    random.shuffle(real_files)
    
    results = []
    num_comparisons = min(len(synthetic_files), len(real_files))
    
    filename = f"results_{speaker}_{auditor_name}.xlsx"
    
    print(f"\nНачинаем сравнение для диктора: {speaker}")
    print(f"Количество сравнений: {num_comparisons}")
    print(f"Файл результатов: {filename}")
    print("=" * 50)
    
    for i in range(num_comparisons):
        synth_file = os.path.join(synth_path, synthetic_files[i])
        real_file = os.path.join(real_path, real_files[i])
        
        print(f"\n--- Сравнение {i+1}/{num_comparisons} ---")
        
        if random.choice([True, False]):
            first_file, first_name, first_original_type = synth_file, synthetic_files[i], 'Синтезированное'
            second_file, second_name, second_original_type = real_file, real_files[i], 'Реальное'
        else:
            first_file, first_name, first_original_type = real_file, real_files[i], 'Реальное'
            second_file, second_name, second_original_type = synth_file, synthetic_files[i], 'Синтезированное'
        
        print("Прослушивание первого аудио...")
        play_audio(first_file)
        
        print("Прослушивание второго аудио...")
        play_audio(second_file)
        
        while True:
            print("\nКакое аудио реальное?")
            print("1 - Первое аудио")
            print("2 - Второе аудио")
            print("p - Повторить оба аудио")
            
            choice = input("Ваш выбор: ").strip().lower()
            
            if choice == 'p':
                print("Повторное прослушивание...")
                play_audio(first_file)
                play_audio(second_file)
                continue
            elif choice in ['1', '2']:
                if choice == '1':
                    results.append([first_name, first_original_type, 'Реальное'])
                    results.append([second_name, second_original_type, 'Синтезированное'])
                else:
                    results.append([first_name, first_original_type, 'Синтезированное'])
                    results.append([second_name, second_original_type, 'Реальное'])
                
                save_results(results, filename)
                print("Результат сохранен")
                break
            else:
                print("Некорректный ввод. Введите 1, 2 или p.")
    
    print(f"\nВсе сравнения завершены!")
    print(f"Итоговые результаты сохранены в: {filename}")
    print(f"Всего записей: {len(results)}")

def main():
    print("=== Сравнение аудио ===")
    
    if not os.path.exists(DATASET_FOLDER):
        print(f"Папка '{DATASET_FOLDER}' не найдена!")
        return
    
    auditor_name = get_auditor_info()
    
    while True:
        print("\n=== Главное меню ===")
        print("1. Начать сравнение")
        print("2. Выйти")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            speaker = select_speaker()
            
            initialize_audio()
            run_comparison_session(speaker, auditor_name)
            
        elif choice == '2':
            print("Заверщение работы")
            break
        else:
            print("Некорректный ввод")

if __name__ == "__main__":
    main()
