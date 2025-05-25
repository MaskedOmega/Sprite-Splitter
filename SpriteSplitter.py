from PIL import Image 
import numpy as np
import os
from pathlib import Path

class SpriteSheet:
    def __init__(self):
        # Load the sprite sheet image
        self.sprite_sheet = "0"
        self.maxSizeX = 0
        self.sprite_sheet_size = 0
        self.SpriteXY = [0,0]

    def get_sprite(self, x, y, width, height):
        # Crop the sprite from the sprite sheet
        sprite = self.sprite_sheet.crop((x, y, x + width, y + height))
        return sprite

    def save_sprite(self, x, y, width, height, output_path):
        sprite = self.get_sprite(x, y, width, height)
        sprite.save(output_path)

    def run_single(self,file_path,SpriteXY):
        self.sprite_sheet = Image.open(file_path)
        self.SpriteXY = SpriteXY
        self.sprite_sheet_size = np.size(self.sprite_sheet)
        self.maxSizeX = self.sprite_sheet_size[0]
        self.maxSizeY = self.sprite_sheet_size[1]

        pos = 0
        count = 0
        
        for i in range (0,self.maxSizeY,self.SpriteXY[1]):
            count = 0
            for j in range (0,self.maxSizeX,self.SpriteXY[0]):
                self.save_sprite(j,i,SpriteXY[0],SpriteXY[1],"images/Anim_" + str(pos) + "_sprite_"+ str(count) + ".png")
                count += 1
            pos +=1

    def get_folders(self,look_path):
        look_path = Path("The Male adventurer - Free")
        folders = [folder.name for folder in look_path.iterdir() if folder.is_dir()]
        return(folders)



    def run_multi(self,SpriteXY,save_path,look_path):
        folders = self.get_folders(look_path)


        for f in range(len(folders)):
            cobined_path = str(look_path) + "/" + str(folders[f]) +"/"+ str(folders[f]) + ".png"
            
            try:
                self.sprite_sheet = Image.open(cobined_path)
                self.SpriteXY = SpriteXY
                self.sprite_sheet_size = np.size(self.sprite_sheet)
                self.maxSizeX = self.sprite_sheet_size[0]
                self.maxSizeY = self.sprite_sheet_size[1]
                
                pos = 0
                count = 0

                path = os.path.join(save_path, folders[f])
                os.mkdir(path)
                print("Directory '%s' created" % folders[f])

                for i in range (0,self.maxSizeY,self.SpriteXY[1]):
                    count = 0
                    for j in range (0,self.maxSizeX,self.SpriteXY[0]):
                        self.save_sprite(j,i,SpriteXY[0],SpriteXY[1], path + "/" + str(pos) + str(folders[f]) + str(count) + ".png")
                        count += 1
                    pos +=1
            except:
                print("skip")
#testing:

a = SpriteSheet()
#a.run("sprite/Idle/idle.png",[48,64])



a.run_multi([48,64],"test","The Male adventurer - Free")