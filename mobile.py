        image1 = Image.open("./static/"+str(data[0]) + ".jpg")
        image2 = Image.open("./static/"+str(data[3]) + ".jpg")
        image3 = Image.open("./static/"+str(data[6]) + ".jpg")
        image4 = Image.open("./static/"+str(data[1]) + ".jpg")
        image5 = Image.open("./static/"+str(data[7]) + ".jpg")

        image6 = Image.open("./static/"+str(data[1]) + ".jpg")
        image7 = Image.open("./static/"+str(data[4]) + ".jpg")
        image8 = Image.open("./static/"+str(data[7]) + ".jpg")
        image9 = Image.open("./static/"+str(data[10]) + ".jpg")
        image10 = Image.open("./static/"+str(data[13]) + ".jpg")

        image11 = Image.open("./static/"+str(data[2]) + ".jpg")
        image12 = Image.open("./static/"+str(data[5]) + ".jpg")
        image13 = Image.open("./static/"+str(data[8]) + ".jpg")
        image14 = Image.open("./static/"+str(data[11]) + ".jpg")
        image15 = Image.open("./static/"+str(data[14]) + ".jpg")

        (width, height) = image1.size
        result_width = width
        result_height = height * 5

        result = Image.new('RGB', (result_width, result_height))
        result2 = Image.new('RGB', (result_width, result_height))
        result3 = Image.new('RGB', (result_width, result_height))

        result.paste(im=image1, box=(0, 0))
        result.paste(im=image2, box=(0, height))
        result.paste(im=image3, box=(0, 2 * height))
        result.paste(im=image4, box=(0, 3 * height))
        result.paste(im=image5, box=(0, 4 * height))

        result2.paste(im=image6, box=(0, 0))
        result2.paste(im=image7, box=(0, height))
        result2.paste(im=image8, box=(0, 2 * height))
        result2.paste(im=image9, box=(0, 3 * height))
        result2.paste(im=image10, box=(0, 4 * height))

        result3.paste(im=image11, box=(0, 0))
        result3.paste(im=image12, box=(0, height))
        result3.paste(im=image13, box=(0, 2 * height))
        result3.paste(im=image14, box=(0, 3 * height))
        result3.paste(im=image15, box=(0, 4 * height))

        result.save('result1.jpg')
        result2.save('result2.jpg')
        result3.save('result3.jpg')
        shutil.move("./result1.jpg", "./static/result1.jpg")
        shutil.move("./result2.jpg", "./static/result2.jpg")
        shutil.move("./result3.jpg", "./static/result3.jpg")

        imageres = Image.open("./static/result1.jpg")
        imageres2 = Image.open("./static/result2.jpg")
        imageres3 = Image.open("./static/result3.jpg")

        (width,height) = imageres.size

        result_width = width * 3
        result_height = height
        result = Image.new('RGB', (result_width, result_height))

        result.paste(im = imageres, box=(0, 0))
        result.paste(im = imageres2, box=(width,0))
        result.paste(im = imageres3, box=(width * 2,0))

        name = "final.jpg"
        result.save(name)
        shutil.move("./" + name, "./static/" + name)

