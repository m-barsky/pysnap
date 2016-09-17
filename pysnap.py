from PIL import ImageGrab
import time, sys, re, os

help_message = "-i to specify interval of screenshots in seconds \n\
-p to specify (single \\ delimeted) path \n\
-n to specify name for the screenshots \n\
-c to specify correlation percentage"

def check_correlation(image1, image2, correlation):
        correlation_counter = 0
        width, height = image1.size
        total_pixels = width * height

        image1_data = list(image1.getdata())
        image2_data = list(image2.getdata())

        for i in range(0, width):
                for j in range(0, height):
                        if image1_data[j * width + i] == image2_data[j * width + i]:
                                correlation_counter += 1
        return (float(correlation_counter) / total_pixels) >= (float(correlation) / 100)

path = ""
interval = 0
name = ""
correlation = 0

for arg in sys.argv:
        if re.search(r"-i[0-9]+(.[0-9]+|)", arg):
                interval = int(re.search(r"[0-9]+(.[0-9]+|)", arg).group(0))
        elif re.search(r"help", arg):
                print help_message
        elif re.search(r"-p([a-z]|[A-Z])\:\\.*", arg):
                path = re.search(r"([a-z]|[A-Z])\:\\.*", arg).group(0)
        elif re.search(r"-n.+", arg):
                name = re.search(r"[^\-n].+", arg).group(0)
        elif re.search(r"-c[0-9]+(.[0-9]+|)", arg):
                correlation = int(re.search(r"[0-9]+(.[0-9]+|)", arg).group(0))
                
if path == "":
        print help_message
        sys.exit()
if name == "":
        name = "screenshot"
        print "no name specified! \nusing default name \'screenshot\'"

if interval == 0:
        interval = 60
        print "no interval specified! \nusing default interval 60 seconds"
if correlation == 0:
        correlation = 100
        print "no correlation specified! \nusing default correlation 100%"
elif correlation > 100:
      correlation = 100
      print "invalid correlation value! \nusing 100% instead"

escaped_name = ""
for char in name:
        if char.isalpha():
                escaped_name += char


if path[-1] != '\\':
	path += '\\'

escaped_path = ""
for char in path:
    if char == '\\':
        escaped_path += '\\\\'
    else:
        escaped_path += char

if not os.path.exists(escaped_path):
        os.makedirs(escaped_path)
        print "path did not exists!\ncreating path"

counter = 0

image1 = ImageGrab.grab()
image2  = ImageGrab.grab()

print "press CTRL + C to exit"

while True:
    image2 = ImageGrab.grab()

    if not check_correlation(image1, image2, correlation):
        image2.save(escaped_path + escaped_name + str(counter) + ".jpg")
        counter += 1
        
    image1 = image2
    time.sleep(interval)
    


