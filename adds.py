import base64
import random

add = """
<div style='position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;background:url(data:image/gif;base64,the-image-data) no-repeat top center fixed;background-size:cover;'></div>
"""

def addAdds(page):
    x = random.randint(1, 2)
    image_name = "hackimages/" + str(x) + ".jpg"
    with open(image_name, "rb") as image_file:
        image = base64.b64encode(image_file.read())
        image = image.decode("utf-8")

    div = add.replace("the-image-data", image)
    splitted = page.split("</body>", 1)

    page = splitted[0] + div + "</body>" + splitted[1]
    return page