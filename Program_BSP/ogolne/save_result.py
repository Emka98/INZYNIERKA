import os

def save_text_to_file(text: str, path_result: str) -> str:
    
    folder_path = os.path.dirname(path_result)
    
    if folder_path and not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"Utworzono brakujący folder: {folder_path}")
    
    with open(path_result, 'w', encoding='utf-8') as file:
        file.write(text)
        
    print(f"Plik został pomyślnie zapisany w: {path_result}")
    return 0