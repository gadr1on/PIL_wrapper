from PIL import ImageFont
import textwrap

def findBestFontSize(self,image_dimesion,text,fontName,multiline):
    widthLimit,heightLimit=image_dimesion
    fontSize=12
    toobig=False
    font = ImageFont.truetype(fontName, fontSize)
    if multiline:
        carLim=int(widthLimit/font.getsize("A")[0])##necessary to avoid bug on carlimprec
        while not toobig:
            limits=font.getsize(text)
            fontHeight=limits[1]
            interline=int(fontHeight/8)
            carlimprec=carLim  ##usefull to get the precedent carlim when toobig=true
            carLim=int(widthLimit/font.getsize("A")[0])
            lines = textwrap.wrap(text, width = carLim)
            wrapHeight=len(lines)*(fontHeight+interline)
            if(wrapHeight>heightLimit):
                toobig=True
            else:
                fontSize+=1
                font = ImageFont.truetype(fontName, fontSize)
        return fontSize-1
    else:
        while not toobig:
            limits=font.getsize(text)
            if((limits[0]>widthLimit)or(limits[1]>heightLimit)):
                toobig=True
            else:
                fontSize+=1
                font = ImageFont.truetype(fontName, fontSize)
        return fontSize-1
