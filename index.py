from PIL import Image
import os
import hashlib
import glob

def get_image_hash(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
        return hashlib.md5(image_data).hexdigest()

def get_all_images(root_folder, extension='png'):
    images = set()
    image_hashes = set()

    for foldername in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, foldername)
        if not os.path.isdir(folder_path):
            continue
        
        images_found = glob.glob(os.path.join(folder_path, f'*.{extension}'))
        if not images_found:
            print(f"В папке {folder_path} не найдено изображений")
            continue
        
        for img_path in images_found:
            img_hash = get_image_hash(img_path)
            if img_hash not in image_hashes:
                image_hashes.add(img_hash)
                images.add(img_path)
            else:
                print(f"Изображение '{img_path}' добавлено")
    
    return list(images)

def merge_images_to_tiff(image_paths, output_tiff):
    if not image_paths:
        print("В подпапках не найдено уникальных изображений.")
        return
    
    images = []
    for img_path in image_paths:
        if os.path.isfile(img_path):
            try:
                image = Image.open(img_path)
                images.append(image)
            except IOError:
                print(f"Не удалось открыть изображение {img_path}")
    
    if not images:
        print("Не удалось открыть изображения.")
        return

    images[0].save(output_tiff, save_all=True, append_images=images[1:])
    print(f"Изображения из всех подпапок объединены в файл {output_tiff}")

# Main script
if __name__ == "__main__":
    root_folder = 'Для тестового'
    output_tiff = 'Result.tif'
    image_paths = get_all_images(root_folder)
    merge_images_to_tiff(image_paths, output_tiff)
