from PIL import Image,ImageDraw

def export_image(data, filename='out.png'):
    im = Image.new("RGB", (256,256),(0,0,0))
    d = ImageDraw.Draw(im)

    for i in range(len(data)//2):
        x,y = data[2*i], data[2*i+1]
        d.point((x,y), fill=(255,255,255))
    im.save(filename)
