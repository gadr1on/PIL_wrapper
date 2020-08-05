#this module is dedicated to the resolve issues occuring when writing a text onto image
#- optimize font size for single line texte
#- optimize font size AND carlim for multiline text
#- resolve incorrect textSize estimation for single line texte
from PIL import Image, ImageFont, ImageDraw
import textwrap
from ImageEdit import *


def getTrueMetrics(font,color,text):#get the true position and the the true dimension of the text 
    imtemp=Image.new("RGB", (10, 10), "black")
    drawtemp = ImageDraw.Draw(imtemp)
    Approxlimits=drawtemp.textsize(text,font)
    print(Approxlimits)
    im=Image.new("RGB", (Approxlimits[0]*1.3, Approxlimits[1]*1.3), "black")
    draw= ImageDraw.Draw(im)
    try:
        draw.text((Approxlimits[0]*0.15, Approxlimits[1]*0.15), text, fill="white", font=font)
    except:
        draw.text((Approxlimits[0]*0.15, Approxlimits[1]*0.15), text, font=font)##avoid PIL bug with palette
    box=im.getbbox()
    trueSize=(box[2]-box[0],box[3]-box[1])
    correctionPosition=(Approxlimits[0]*0.15-box[0],Approxlimits[1]*0.15-box[1])
    return correctionPosition,trueSize


def paste_imageNoWrap(path,square,font,color,text,correction=True):
    im = Image.open(path)
    if correction:
        correction,size=getTrueMetrics(font,color,text)
        im=simpleTextPaste(im,square,font,color,text,correction,size)
    return im
    
def GetLongestWordLength (text):
    textlist=text.split()
    longestWord=0
    for word in textlist:
        if(len(word)>longestWord):
            longestWord=len(word)
    return(longestWord)


def getWrapDimensions(lines,font,fontsize):
    widthMax=0
    interline=int(fontsize/8)
    wrapHeight=0
    for line in lines: ##for loop only to determine widthMax
        width, height = font.getsize(line)
        wrapHeight+=(height+interline)
        if(width>widthMax):
            widthMax=width
    return widthMax,wrapHeight

def firstFontEstimation(fontname,nbcar,freeSpace):
    fontsize=12
    TooSmall=True
    font = ImageFont.truetype(fontname, fontsize)
    letterArea2=font.getsize("A")
    AimedletterArea=freeSpace/(nbcar)
    RealletterArea=letterArea2[0]*letterArea2[1]
    while (RealletterArea<AimedletterArea):
        fontsize+=1
        font = ImageFont.truetype(fontname, fontsize)
        letterArea2=font.getsize("A")
        RealletterArea=letterArea2[0]*letterArea2[1]   
    return fontsize

def calibrateCarMax(font,widthMax,longestWord):
    letterSize=font.getsize("a")[0]
    carLim=max(longestWord,int(widthMax/letterSize))
    return carLim

def isWrapTooTall(lines,font,fontsizeInit,heightMax):
    wrapHeight=getWrapDimensions(lines,font,fontsizeInit)[1]
    if(wrapHeight>heightMax):
        return True
    else:
        return False
    
def isWrapTooLarge(lines,font,fontsizeInit,WidthMax):
    wrapWidth=getWrapDimensions(lines,font,fontsizeInit)[0]
    if(wrapWidth>WidthMax):
        return True
    else:
        return False

def initCarAndFont(text,fontname,widthMax,heightMax):
    fontSizeInit=firstFontEstimation(fontname,len(text),widthMax*heightMax)
    font = ImageFont.truetype(fontname, fontSizeInit)
    longestWord=GetLongestWordLength(text)
    carMax=calibrateCarMax(font,widthMax,longestWord)
    return (fontSizeInit,carMax)

def optimize(text,fontname,widthMax,heightMax,fontSizeinit,carlimInit):
    fontSize=fontSizeinit
    carlim=carlimInit
    longestWord=GetLongestWordLength(text)
   ## print(fontSize,carlim)
    converged=False
    count=0
    while not(converged):
        carlimold=carlim
        fontSizeold=fontSize
        count+=1
        if(count<5):
            fontSize=NonConservativeOptimizeFontSize(text,fontname,fontSize,heightMax,carlim)
            carlim= optimizeCarLim(text,fontname,fontSize,widthMax,carlim,longestWord)
        else:      
            carlimNew= optimizeCarLim(text,fontname,fontSize,widthMax,carlim,longestWord)
            fontSizeNew=ConservativeOptimizeFontSize(text,fontname,fontSize,heightMax,widthMax,carlim)  
            carlim=(carlimNew+carlim)/2#avoid oscillations
            fontSize=int((fontSizeNew+fontSize)/2)
            converged=((carlimold==carlim)and(fontSizeold==fontSize))or(count==20)
        ##print(fontSize,carlim)
    return (fontSize,carlim)
    
def optimizeFontSizeAndCarLim(text,fontname,widthMax,heightMax):
    (fontSizeinit,carlimInit)=initCarAndFont(text,fontname,widthMax,heightMax)
    (fontSize,carlim)=optimize(text,fontname,widthMax,heightMax,fontSizeinit,carlimInit)
    return fontSize,carlim

def ConservativeOptimizeFontSizeNoWrap(text,fontname,fontsize,heightMax,widthMax):
    font = ImageFont.truetype(fontname, fontsize)
    limits = font.getsize(text)
    TooLarge=limits[0]>widthMax
    TooTall=limits[1]>heightMax
    TooBig=TooTall or TooLarge
    if TooBig:
        while (TooBig):
            print(fontsize)
            fontsize-=1
            font = ImageFont.truetype(fontname, fontsize)
            limits = font.getsize(text)
            TooLarge=limits[0]>widthMax
            TooTall=limits[1]>heightMax
            TooBig=TooTall or TooLarge
        return fontsize
    else:
        while not(TooBig):
            print(fontsize)
            fontsize+=1
            font = ImageFont.truetype(fontname, fontsize)
            limits = font.getsize(text)
            TooLarge=limits[0]>widthMax
            TooTall=limits[1]>heightMax
            TooBig=TooTall or TooLarge
        return fontsize-1
    
def ConservativeOptimizeFontSize(text,fontname,fontsizeInit,heightMax,widthMax,carMax):
    font = ImageFont.truetype(fontname, fontsizeInit)
    lines = textwrap.wrap(text, width = carMax)
    fontsize=fontsizeInit
    TooTall=isWrapTooTall(lines,font,fontsizeInit,heightMax)
    TooLarge=isWrapTooLarge(lines,font,fontsize,widthMax)
    TooBig=TooTall or TooLarge
    if TooBig:
        while (TooBig):
            fontsize-=1
            font = ImageFont.truetype(fontname, fontsize)
            TooTall=isWrapTooTall(lines,font,fontsize,heightMax)
            TooLarge=isWrapTooLarge(lines,font,fontsize,widthMax)
            TooBig=TooTall or TooLarge
        return fontsize
    else:
        while not(TooBig):
            fontsize+=1
            font = ImageFont.truetype(fontname, fontsize)
            TooTall=isWrapTooTall(lines,font,fontsize,heightMax)
            TooLarge=isWrapTooLarge(lines,font,fontsize,widthMax)
            TooBig=TooTall or TooLarge
        return fontsize-1

def NonConservativeOptimizeFontSize(text,fontname,fontsizeInit,heightMax,carMax):
    font = ImageFont.truetype(fontname, fontsizeInit)
    lines = textwrap.wrap(text, width = carMax)
    fontsize=fontsizeInit
    TooTall=isWrapTooTall(lines,font,fontsizeInit,heightMax)
    if TooTall:
        while (TooTall):
            fontsize-=1
            font = ImageFont.truetype(fontname, fontsize)
            TooTall=isWrapTooTall(lines,font,fontsize,heightMax)
        return fontsize
    else:
        while not(TooTall):
            fontsize+=1
            font = ImageFont.truetype(fontname, fontsize)
            TooTall=isWrapTooTall(lines,font,fontsize,heightMax)
        return fontsize-1
          
def optimizeCarLim(text,fontName,fontsize,widthMax,carMaxInit,longestWord):
    font = ImageFont.truetype(fontName, fontsize)
    lines = textwrap.wrap(text, width = carMaxInit)
    TooLarge=isWrapTooLarge(lines,font,fontsize,widthMax)
    carMax=carMaxInit
    if TooLarge:
        while (TooLarge):##avoiding the longest word being cut
            if(carMax<longestWord+1):
                return(carMax)
            carMax-=1
            lines = textwrap.wrap(text, width = carMax)
            TooLarge=isWrapTooLarge(lines,font,fontsize,widthMax)
        return (carMax)
    else:
        while not(TooLarge):
            if(len(text)==carMax):
                return(carMax)
            carMax+=1
            lines = textwrap.wrap(text, width = carMax)
            TooLarge=isWrapTooLarge(lines,font,fontsize,widthMax)
        return (carMax-1)

def findBestFontSize(square,text,fontName,multiline):
    widthLimit=square.end_x-square.start_x
    heightLimit=square.end_y-square.start_y
    fontSize=12
    toobig=False
    font = ImageFont.truetype(fontName, fontSize)
    if (multiline=="false"):     
        while not toobig:
            limits=font.getsize(text)
            if((limits[0]>widthLimit)or(limits[1]>heightLimit)):
                toobig=True
            else:
                fontSize+=1
                font = ImageFont.truetype(fontName, fontSize)
        return ImageFont.truetype(fontName, fontSize-1),False
    else:
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
        print(carLim,len(lines),fontHeight,wrapHeight,fontSize-1)
        return ImageFont.truetype(fontName, fontSize-1),carlimprec


    
