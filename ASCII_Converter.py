#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image
import sys
import os

#Stores a list of 11 ASCII characters going from largest size to smallest. 
#floor integer Divide any pixel in range 0 - 255 by 25 -> it will be an index in this list
ASCII_char = []
global_output_dir = None
global_file_dir = None
text_representation = None
downscale_factor = None

def prominence_shading(light_or_dark):
    global ASCII_char
    #For lighter colour prominence
    if light_or_dark == "light":
        ASCII_char = ['.',',',':',';','+','*','?','%','S','#','@']
        #For darker colour prominence
    elif light_or_dark == "dark":
        ASCII_char = ['@','#','S','%','?','*','+',';',':',',','.']
    else:
        ASCII_char = ['.',',',':',';','+','*','?','%','S','#','@']

def read(file_dir, dwn_scale, asp_rat, light_or_dark, output_dir=None):

    global global_file_dir
    global text_representation
    global downscale_factor

    global_file_dir = file_dir
    downscale_factor = dwn_scale
    
    #Downscale factor turned to int just in case someone sent float
    downscale_factor = int(downscale_factor)

    #Converts imag to bmp. This uses Pillow. Grrrr...
    converted_img = convert_to_bmp(file_dir)

    #Determines whether someone wanted to shade with white or black as prominent shader
    prominence_shading(light_or_dark)

    #If image was in fact bmp all along. Dun dun duuuuuuh!
    if converted_img != 0:
        file_dir = converted_img

    #Open's file and reads as binary its total image data -> header, pixel data and padding
    with open(file_dir, 'rb') as f:
        total = f.read()
        
        #ASSUMING MOST COMMON BMP BIP HEADER. Though I think the main header is unchanging, and the BIP is accounted for by image_offset? Ignore this comment
        width = (total[18] << 0) + (total[19] << 8) + (total[20] << 16) + (total[21] << 24)
        height = (total[22] << 0) + (total[23] << 8) + (total[24] << 16) + (total[25] << 24)
        colour_depth = (total[28] << 0) + (total[29] << 8)
        image_offset = (total[10] << 0) + (total[11] << 8) + (total[12] << 16) + (total[13] << 24)
        colours_used = (total[46] << 0) + (total[47] << 8) + (total[48] << 16) + (total[49] << 24)
        dib_header_size = (total[14] << 0) + (total[15] << 8) + (total[16] << 16) + (total[17] << 24)
        #Create the empty matrix for ASCII converstion. Downscale here instead so you don't have to later???
        txt_rep = [[' ' for _ in range(width * asp_rat)] for _ in range(height)]

        text_representation = txt_rep                                                        


        #DEBUGS for testing
        print(f'Resolution of image: {width} x {height}')
        print("---------------------------------------------------")
        print(f'Colour depth of image: {colour_depth}')
        print("---------------------------------------------------")
        print(f'DIB Header size {dib_header_size}')
        print("---------------------------------------------------")
        #If 66 for 16-bit -> it includes 16 bytes for the colour masks
        print(f'start of actual image data (also length of total headers): {image_offset}')
        print("---------------------------------------------------")
        print(f'Total image bytes with header {len(total)}')
        print("---------------------------------------------------")
        print(f'Total image bytes minus header {len(total) - image_offset}')
        print("---------------------------------------------------")
        print(f'Colours used for palette if there is one: (note 0 can mean all colours -> 256)  {colours_used}')
        #Determines which algorithm to use. 24, 16, 12, 8 OR 4
        if colour_depth == 24:
            bmp_to_24colour(txt_rep, width, height, asp_rat, total, downscale_factor)
            
        elif colour_depth == 16:
            bmp_to_16colour(txt_rep, width, height, asp_rat, total, downscale_factor)
            
        elif colour_depth == 8:
            if colours_used == 0:
                colours_used = 256
            expected_image_start = (colours_used * 4) + (14 + dib_header_size)
            
            if image_offset == expected_image_start:
                bmp_to_8palete(txt_rep, width, height, asp_rat, total, downscale_factor, colours_used, dib_header_size)
                
            else:
                bmp_to_8greyscale(txt_rep, width, height, asp_rat, total, downscale_factor)      
        else:
            print(f'Unsupported colour depth: {colour_depth} bits')
            print('/n')
#Some crappy code for filling in gaps caused by widening the width, bt making the fellow non-filled pixels equal to the filled pixels.
#Also its shit as it only accounts for the first aspec. If you have aspec 3 and you're at empty 2 -> It'll look at empty 1 instead of the filled start.
#IMPROVE!!!

def gap_fill(matrix, asp_rat):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == ' ' and j <= len(matrix[0]) - 1 - asp_rat:
                matrix[i][j] = matrix[i][j + (asp_rat - 1)]

#Finally downscales the filled matrix and than writes it into a hardcoded file name. Need to allow user to set the file.txt maybe?

def symbol_to_file(matrix, downscale_factor, output_file):
    
    d_width = len(matrix[0]) // downscale_factor
    d_height = len(matrix) // downscale_factor

    down_scale = [[' ' for _ in range(d_width)] for _ in range(d_height)]

    for i in range(d_height):
        for j in range(d_width):
            down_scale[i][j] = matrix[i * downscale_factor][j * downscale_factor]
            
    with open(output_file, 'w') as text_file:
        for row in down_scale:
            text_file.write("".join(row) + '\n')
    print("ASCII SUCCESSFULY CREATED!")
    print("---------------------------------------------------")

#Uses yucky higher-level programming to convert image to bmp, does end up storing a bmp file though, so maybe remove need to store file itself?

def convert_to_bmp(path):
    print("CONVERTED TO BMP. CREATED FILE 'BMP_OR_RIOT")
    with open(path, 'rb') as r:
        start = r.read(8)
        if start.startswith(b'BM'):
            return 0
        else:
            img = Image.open(path)
            new_path = "BMP_Or_Riot.bmp"
            img.save(new_path)
            return new_path

def file_creation(text_representation,downscale_factor):
    global global_file_dir
    global global_output_dir
    if global_output_dir == None:
        global_output_dir = os.path.dirname(os.path.abspath(global_file_dir))
    output_file = os.path.join(global_output_dir, 'output.txt')
    symbol_to_file(text_representation, downscale_factor, output_file)

#image pixel data extraction for 24 colour bmp image

def bmp_to_24colour(text_representation, width, height, asp_rat, total, downscale_factor):
    
    #Row and col correspond to the specific matrix index
    padding = ( ( ( (width * 3) + 3) // 4) * 4) - (width * 3)  # Calculates padding of image data

    curr_pad = padding
    pixel_position = 3
    total_data = len(total) - 1
    #Loop over the text_representation for each height and its width amount
    for y in range(height):
        for x in range(width):

            # Calculate index from the right side of each row
            x_reversed = width - 1 - x
            i = (total_data - pixel_position) - (curr_pad - 1)
            
           #Grab three bytes convert to single value and than find its index by dividing 0 to 255 value by 25 integer floor. Put it in array
            r, g, b = total[i], total[i+1], total[i+2]
            grey_scale = (r + g + b) // 3
            ascii_value = ASCII_char[grey_scale // 25]
            text_representation[y][x_reversed*asp_rat] = ascii_value
            pixel_position += 3
            
        curr_pad = curr_pad + padding
        
    #fill in gaps from aspec ratio
    gap_fill(text_representation, asp_rat)

    file_creation(text_representation, downscale_factor)


def bmp_to_16colour(text_representation, width, height, asp_rat, total, downscale_factor):

        #Row and col correspond to the specific matrix index
    padding = ( ( ( (width * 2) + 2) // 4) * 4) - (width * 2)  # Calculates padding of image data

    curr_pad = padding
    pixel_position = 2
    total_data = len(total) - 1
    #Loop over the text_representation for each height and its width amount
    for y in range(height):
        for x in range(width):

            # Calculate index from the right side of each row
            x_reversed = width - 1 - x
            i = (total_data - pixel_position) - (curr_pad - 1)

            #Add condition checking for both format  5:6:5 and 5:5:5:1
            pixel_data = (total[i] << 0) + (total[i+1] << 8)
            r = ((pixel_data >> 11) & 0x1F) * (255//31)
            g = ((pixel_data >> 5) & 0x3F) * (255//63)
            b = (pixel_data & 0x1F) * (255//31)
            grey_scale = (r + g + b) // 3

            
            ascii_value = ASCII_char[grey_scale // 25]
            text_representation[y][x_reversed*asp_rat] = ascii_value
            pixel_position += 2
            
        curr_pad = curr_pad + padding
        
    #fill in gaps from aspec ratio
    gap_fill(text_representation, asp_rat)
    #Actually create file
    file_creation(text_representation, downscale_factor)

def bmp_to_8greyscale(text_representation, width, height, asp_rat, total, downscale_factor):

    padding = width % 4 # Calculates padding of image data. Much easier in 8-bot

    curr_pad = padding
    pixel_position = 1
    total_data = len(total) - 1
    #Loop over the text_representation for each height and its width amount
    for y in range(height):
        for x in range(width):

            # Calculate index from the right side of each row
            x_reversed = width - 1 - x
            i = (total_data - pixel_position) - (curr_pad - 1)
            
            ascii_value = ASCII_char[total[i] // 25]
            text_representation[y][x_reversed*asp_rat] = ascii_value
            pixel_position += 1
            
        curr_pad = curr_pad + padding
        
    #fill in gaps from aspec ratio
    gap_fill(text_representation, asp_rat)

    #Actually create file
    file_creation(text_representation, downscale_factor)


def bmp_to_8palete(text_representation, width, height, asp_rat, total, downscale_factor, colours_used, dib_header_size):

    padding = width % 4 # Calculates padding of image data. Much easier in 8-bot

    curr_pad = padding
    pixel_position = 1
    total_data = len(total) - 1
    #Loop over the text_representation for each height and its width amount
    for y in range(height):
        for x in range(width):

            # Calculate index from the right side of each row
            x_reversed = width - 1 - x
            i = (total_data - pixel_position) - (curr_pad - 1)

            palette_index = (total[i] * 4) + (dib_header_size + 14)
            pixel_value = (total[palette_index] + total[palette_index+1] + total[palette_index+2]) // 3

            ascii_value = ASCII_char[pixel_value // 25]
            text_representation[y][x_reversed*asp_rat] = ascii_value
            pixel_position += 1
            
        curr_pad = curr_pad + padding
        
    #fill in gaps from aspec ratio
    gap_fill(text_representation, asp_rat)
    
    #Actually create file
    file_creation(text_representation, downscale_factor)
    
# JPG TO BMP CONVERSION IS SOLID
# PNG TO BMP CONVERSION SHOWS LESSER RESULTS. CONVERT FROM PNG TO JPG THAN JPG TO BMP?

def input_check():
    input_file = input("Enter file name with type extension (E.g. Test.jpg) : ")
    if not os.path.exists(input_file):
        print(f"Error: This file directory {input_file}, does not exist.")
        return input_check()
    else:
        return input_file

def downscale_check():
    downscale_factor = input("Enter downsampling value (Recommend value - 5-20): ")
    if not downscale_factor.isnumeric():
        print(f"Error: This downscale factor {downscale_factor}, is not a valid number.")
        return downscale_check()
    else:
        return int(downscale_factor)

def aspect_check():
    asp_rat = input("Enter aspect ratio (Recommended value - 1-4)(ENTER for default): ")
    if asp_rat == "":
        return asp_rat
    if not asp_rat.isnumeric():
        print(f"Error: This aspect ratio {asp_rat} in not a valid number.")
        return aspect_check()
    else:
        return int(asp_rat)

def light_dark_check():
    light_or_dark = input("Enter the words: 'dark' or 'light' for ASCII mode (ENTER sets 'light' for default): ")
    if light_or_dark == "":
        return light_or_dark
    if light_or_dark != "light" and light_or_dark != "dark":
        print(f"Error: {light_or_dark} is not a valid mode.")
        return light_dark_check()
    else:
        return light_or_dark
          
def main():
    print("W.E.L.C.O.M.E.!")
    print("---------------------------------------------------")
    print("Please answer the following querys to create you're ASCII conversion:")
    print("---------------------------------------------------")
    print("WARNING: Converter does not currently support 32 bit conversion")
    print("---------------------------------------------------")
    
    input_file = input_check()
    print(input_file)
    downscale_factor = downscale_check()
    print(downscale_factor)
    asp_rat = aspect_check()
    print(asp_rat)
    light_or_dark = light_dark_check()
    print(light_or_dark)
    
    if asp_rat == "":
        asp_rat = 2 # Convert asp_rat to int before passing
    if light_or_dark == "":
        light_or_dark = "light"
        
    read(input_file, downscale_factor, asp_rat, light_or_dark)
    
    reset = input("ENTER '1' to exit program, and anything else to restart")
    if reset != "" and int(reset) == 1:
        sys.exit(1)
    else:
        main()

if __name__ == "__main__":
    main()
    

#read("C:\\Users\\Cgide\\Documents\\ASCII_Converter\\Test.jpg", 5, 2, "light") # 1: LOCATION OF IMAGE, 2: Downscale factor, 3: Aspect ratio, 4: Negative?  


# In[ ]:





# In[ ]:




