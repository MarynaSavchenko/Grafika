from PIL import Image, ImageDraw, ImageColor
import json
import sys
import string
VARS = string.ascii_lowercase

fg_color = "black"
hex = '0123456789abcdefABCDEF'
Palette = {}


def main(argv):
    
    if (len(sys.argv)!=2) and (len(sys.argv)!=4):
        printf("Wrong amount of args\n")
        sys.exit()
    if len(sys.argv)==4 and sys.argv[2]!="-o":
        printf("Wrong format of args\n")
        sys.exit()
    with open(sys.argv[1]) as file: 
        try:
            json_data = json.load(file)
            Screen = json_data["Screen"]
        except ValueError:
            print("Wrong format of JSON\n")
            return False
    if "fg_color" in Screen:
        global fg_color
        fg_color = Screen["fg_color"]
    global Palette
    Palette = json_data["Palette"] 
    image = set_screen(Screen)
    Figures = json_data["Figures"]  
    
    for i in Figures:
        new_image = draw_figure(image, i)
        if new_image != 0:
            image = new_image
    
    if (len(sys.argv)==2):
        image.show()
    else:
        dir_with_name = sys.argv[3] + "\image.png"
        image.save(dir_with_name)

def draw_point(image,figure):
        
    draw = ImageDraw.Draw(image)
    if "x" in figure:
        x = figure["x"]
    else:
        print("There is no x coordinate for point in figure: \n", figure, "\n")
        return 0
    if "y" in figure:
        y = figure["y"]
    else:
        print("There is no y coordinate for point in figure: \n", figure, "\n")
        return 0 
    if "color" in figure:
        color = perform_color(figure["color"])
        if color == False:
            print("Wrong color for drawing point in figure: \n", figure, "\n")
            return 0
        try:
            draw.point((x,y), color)
        except ValueError:
            print("Wrong arguments for drawing point in figure: \n", figure, "\n")
            return 0
    else:
        try:
            draw.point((x,y,),fg_color)
        except ValueError:
            print("Wrong arguments for drawing point in figure: \n", figure, "\n")
            return 0
    return image
    

def draw_square(image,figure):

    draw = ImageDraw.Draw(image)
    if "x" in figure:
        x = figure["x"]
    else:
        print("There is no x coordinate for square in figure: \n", figure, "\n")
        return 0
    if "y" in figure:
        y = figure["y"]
    else:
        print("There is no y coordinate for square in figure: \n", figure, "\n")
        return 0 
    if "color" in figure:
        color = perform_color(figure["color"])
    else:
        color = None
        
    if color == False:
        print("Wrong color for drawing square in figure: \n", figure, "\n")
        return 0
    
    if "radius" in figure:
        r = figure["radius"]
        if color == None:
            try:
                draw.ellipse([(x-r,y-r),(x+r, y+r)], outline = fg_color)
            except ValueError:
                print("Wrong arguments for drawing circle in figure: \n", figure, "\n")
                return 0
        else:
            try:
                draw.ellipse([(x-r,y-r),(x+r, y+r)], outline = color)
            except ValueError:
                print("Wrong arguments for drawing circle in figure: \n", figure, "\n")
                return 0
    elif "size" in figure:
        s = figure["size"]
        if color == None:
            try:
                draw.polygon([(x,y), (x,y+s), (x+s,y+s), (x+s,y)], outline = fg_color)
            except ValueError:
                print("Wrong arguments for drawing square in figure: \n", figure, "\n")
                return 0
        else:
            try:
                draw.polygon([(x,y), (x,y+s), (x+s,y+s), (x+s,y)], outline = color)
            except ValueError:
                print("Wrong arguments for drawing square in figure: \n", figure, "\n")
                return 0
    else:
        print("There is no radius or size for square in figure: \n", figure, "\n")
        return 0
    return image
  
def draw_polygon(image,figure):

    draw = ImageDraw.Draw(image)
    if "points" in figure:
        points = figure["points"]
        new_points = [(i[0],i[1]) for i in points]
    else:
        print("There is no points for polygon in figure: \n", figure, "\n")
        return 0
    if "color" in figure:
        color = perform_color(figure["color"])
        if color == False:
            print("Wrong color for drawing polygon in figure: \n", figure, "\n")
            return 0
        try:
            draw.polygon(new_points, outline = color)
        except ValueError:
            print("Wrong arguments for drawing polygon in figure: \n", figure, "\n")
            return 0
    else:
        try:
            draw.polygon(new_points, outline = fg_color)
        except ValueError:
            print("Wrong arguments for drawing polygon in figure: \n", figure, "\n")
            return 0
    return image
    
def draw_rectangle(image,figure):

    draw = ImageDraw.Draw(image)
    if "x" in figure:
        x = figure["x"]
    else:
        print("There is no x coordinate for rectangle in figure: \n", figure, "\n")
        return 0
    if "y" in figure:
        y = figure["y"]
    else:
        print("There is no y coordinate for rectangle in figure: \n", figure, "\n")
        return 0 
    if "width" in figure:
        width = figure["width"]
    else:
        print("There is no width for rectangle in figure: \n", figure, "\n")
        return 0
    if "height" in figure:
        height = figure["height"]
    else:
        print("There is no height for rectangle in figure: \n", figure, "\n")
        return 0 
    if "color" in figure:
        color = perform_color(figure["color"])
        if color == False:
            print("Wrong color for drawing rectangle in figure: \n", figure, "\n")
            return 0
        try:
            draw.rectangle([(x,y),(x+width,y+height)],outline = color)
        except ValueError:
            print("Wrong arguments for drawing rectangle in figure: \n", figure, "\n")
            return 0
    else:
        try:
            draw.rectangle([(x,y),(x+width,y+height)],outline = fg_color)
        except ValueError:
            print("Wrong arguments for drawing rectangle in figure: \n", figure, "\n")
            return 0
   
    return image
    
    
def draw_figure(image, figure):
    
    draw = ImageDraw.Draw(image)
    type = figure["type"]
    if type == "point":
        return draw_point(image,figure)
    elif type == "polygon":
        return draw_polygon(image,figure)
    elif type == "rectangle":
        return draw_rectangle(image,figure)
    elif type == "square":
        return draw_square(image,figure)
    else:
        print("This type of figure doesnt match in figure :\n", figure, "\n")
        return 0
    
def perform_color(color):

    
    if color[0]=="#" and len(color)==7:
    
        for i in color[1:]:
        
            if i in hex:
                continue
            else:
                 return False
                 
        return color
        
    elif color[0] == "(" and color[len(color)-1] == ")":
    
        tmp = color[1:-1].split(",")
        if len(tmp) == 3:
        
            for i in tmp:
            
                if int(i) >= 0 and int(i) < 256:
                    continue
                else:
                    return False
            return "rgb" + color
        else:
            return False
            
    elif color in Palette:
        return Palette[color]
        
    else:
        for i in color:
            if i in VARS:
                continue
            else:
                return False
        return color
        
        
        
    
def set_screen(Screen):

    image = Image.new('RGBA', (Screen["width"], Screen["height"]),Screen["bg_color"])
    return image
    

if __name__ == "__main__":
	main(sys.argv)
