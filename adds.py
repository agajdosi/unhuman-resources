import base64

add = """
<div style='position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;background:url(data:image/gif;base64,the-image-data) no-repeat center center fixed;background-size:cover;'></div>
"""

add = """
<div style='position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;background:url(data:image/gif;base64,the-image-data) center center fixed;'></div>
"""

def addAdds(page):
    with open("hackimages/1.png", "rb") as image_file:
        image = base64.b64encode(image_file.read())
        image = image.decode("utf-8")

    div = add.replace("the-image-data", image)
    splitted = page.split("</body>", 1)

    page = splitted[0] + div + "</body>" + splitted[1]
    return page