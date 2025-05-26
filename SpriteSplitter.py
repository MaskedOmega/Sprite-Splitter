import os
from pathlib import Path
import shutil
from PIL import Image
import numpy as np

class Sprite_folder_splitter:
    def __init__(self):
        self.folders = []
        self.save_path = ""

        self.sprite_sheet = "0"
        self.maxSizeX = 0
        self.sprite_sheet_size = 0
        self.SpriteXY = [0,0]


    def format_struc(self,path):
        return(str(path).lower())

    def get_folders_struc(self,look_path):
        # Specify the directory path
        directory_path = Path(look_path)
        # Get all subfolders recursively
        folders = [item for item in directory_path.rglob("*") if item.is_dir()]
        # Print the list of folders
        for folders in folders:
            self.folders.append(self.format_struc(folders))
        return(self.folders)
    
    def get_items(self,save_path):
        source_dirs = self.folders # Add your folder paths here

        # Copy files from each source directory
        for src_dir in source_dirs:
            destination_dir = Path(str(save_path)+ "/" + src_dir)  # Destination folder
            # Ensure destination exists
            destination_dir.mkdir(parents=True, exist_ok=True)
            src_path = Path(src_dir)
            image_items = []
            image_items_size = []
            for file in src_path.iterdir():
                if file.is_file():  # Ensure it's a file, not a folder
                    file_format = self.format_struc(file.name)
                    image = Image.open(src_path /  file_format)
                    image_items.append(file)
                    wid, hgt = image.size
                    image_items_size.append((wid*hgt))
                    
            file = image_items[np.argmax(image_items_size)]
            shutil.copy(file, destination_dir /  file_format)  # Copy file to destination
            print(f"Copied: {(file.name.lower())}")

    def copy_struc_save(self,save_path,look_path):
        os.makedirs(save_path, exist_ok=True)
        self.folders = self.get_folders_struc(look_path)
        self.get_items(save_path)


    def get_sprite(self, x, y, width, height):
        # Crop the sprite from the sprite sheet
        sprite = self.sprite_sheet.crop((x, y, x + width, y + height))
        return sprite

    def save_sprite(self, x, y, width, height, output_path):
        sprite = self.get_sprite(x, y, width, height)
        sprite.save(output_path)

    def single_run_method(self,save_path,look_path,SpriteXY):
        os.makedirs(save_path, exist_ok=True)
        self.folders = self.get_folders_struc(look_path)
        source_dirs = self.folders # Add your folder paths here

        # Copy files from each source directory
        for src_dir in source_dirs:
            destination_dir = Path(str(save_path)+ "/" + src_dir)  # Destination folder
            # Ensure destination exists
            destination_dir.mkdir(parents=True, exist_ok=True)
            src_path = Path(src_dir)
            image_items = []
            image_items_size = []
            for file in src_path.iterdir():
                if file.is_file():  # Ensure it's a file, not a folder
                    file_format = self.format_struc(file.name)
                    image = Image.open(src_path /  file_format)
                    image_items.append(file)
                    wid, hgt = image.size
                    image_items_size.append((wid*hgt))
                    
            file = image_items[np.argmax(image_items_size)]
            shutil.copy(file, destination_dir /  file_format)  # Copy file to destination

            source_file_path = destination_dir /  file_format
            split_file_path = str(destination_dir / "split")
            os.makedirs(split_file_path, exist_ok=True)

            self.sprite_sheet = Image.open(source_file_path)

            self.SpriteXY = SpriteXY
            self.sprite_sheet_size = np.size(self.sprite_sheet)
            self.maxSizeX = self.sprite_sheet_size[0]
            self.maxSizeY = self.sprite_sheet_size[1]
            
            pos = 0
            count = 0
            print("Directory '%s' created" % file)

            for i in range (0,self.maxSizeY,self.SpriteXY[1]):
                count = 0
                for j in range (0,self.maxSizeX,self.SpriteXY[0]):
                    self.save_sprite(j,i,SpriteXY[0],SpriteXY[1], split_file_path + "//" + str(pos) +"_"+ str(count) +"_"+ file_format)
                    count += 1
                pos +=1

            print(f"Copied: {(file.name.lower())}")

a = Sprite_folder_splitter()

# "animation" = name of new folder
# "Sprite" = name of location where to get assets(spritesheet the main directory)
# [48,64] = the sprite resolution size
a.single_run_method("animation","Sprite",[48,64])

