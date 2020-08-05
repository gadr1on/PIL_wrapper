# SupperWrapper
###description
PIL + textwrap is great to print a text on an image.   
But if one wants the max font size to fit a limited printing box, things are getting harder.
This module allow a modest workaround to fix these two issues :
- carLim and FontSize optimization when width and height are given   
- draw.text printing outside the expected box (it happens when font metrics are messed up)

###use
To find the best fontSize and carlim
``` python
import superWrapper
[fontSize,carlim]=optimizeFontSizeAndCarLim(text,fontName,MaxWidth, MaxHeight)#for a multiline
[fontSize,carlim]=ConservativeOptimizeFontSizeNoWrap(text,fontName,MaxWidth, MaxHeight)#for single line
```
To avoid printing outside the box
```python
import superWrapper
correction,size=getTrueMetrics(font,color,text)
x_remaining=w-size[0]
y_remaining=h-size[1]
draw.text((x + x_remaining/2 + correction[0], y+y_remaining/2 + correction[1]), text, fill=color, font=font)
```
###dependancies
- PIL
- ImageEdit

###More
Don't hesitate to fork or/and suggest a better solution.
more informations there http://brunomart.in/blog/?p=14

