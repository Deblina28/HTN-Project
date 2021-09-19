import cv2
import numpy as np
import math
import serial
import time

#CODE SENDING TO ARDUINO
# arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data





send = open("output.txt","w")
def slope(x1, y1, x2, y2):
    if x2 == x1:
        slope = 255
        return slope
    slope = (y2-y1)/(x2-x1)
    if slope > 255.0:
        slope = 255
        return slope
    elif slope < -255.0:
        slope = 255
        return slope
    return slope

def angle(vector1, vector2):
    x1, y1 = vector1
    x2, y2 = vector2
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return math.acos(inner_product/(len1*len2))

img = cv2.imread('unknown.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cv2.imshow("original",img)
#cv2.imshow("gray",gray)
blur_gray = cv2.GaussianBlur(gray,(5, 5),0)
edges = cv2.Canny(blur_gray, 50, 150)
#cv2.imshow("edges",edges)

line_image = np.copy(img) * 0
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 15, np.array([]), 30, 20)

#print(lines)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(0,0,255),5)
        #np.append(line,slope(x1,y1,x2,y2))
        #np.insert(lines,1,512312)
        #print("line: ",line)
        #cv2.imshow("asdf", line_image)
        #cv2.waitKey(1000)

lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
cv2.imshow('result.jpg', line_image)
newlist = []
list1 = lines.tolist()
for line in list1:
    for x in line:
        #print("line: ",x)
        newlist.append(x)

#print(newlist)
i = 0
slope_list = []
for line in newlist:
    slope_list.append(slope(line[0],line[1],line[2],line[3]))
    i+=1
#b =y-mx
blist= []
for i in range(len(newlist)):
    if slope_list[i] ==255:
        b = 0;
    else:
        b = newlist[i][1]-(slope_list[i]*newlist[i][0])
    blist.append(b)



# LET THE FUN BEGIN
edits = 1
vertical = 255
tolerance = 20
while edits != 0:
    #print("While loop start! List length: ",len(newlist))
    edits = 0 #set to 0 so we can exit loop if no edits
    for i in range(len(newlist)):
        for j in range(len(newlist)):
            if newlist[i] == newlist[j]:# checks if it's the same item to not try to compute itself
                #print("scenario 1")
                continue
            elif slope_list[i] == 0 and slope_list[j] == 0: # horizontal cases
                if abs(newlist[j][1] - newlist[i][3]) > tolerance:

                    #elif newlist[j][1] - newlist[i][3] > tolerance and newlist[i][0] - newlist[j][2] > tolerance:
                    #print("scenario 2")
                    continue
                elif abs(newlist[j][0] - newlist[i][2]) > tolerance:#asdf
                    #print("scenario 3")
                    continue
                else:
                    #print("scenario 4")
                    #print("math: ", newlist[j][0] - newlist[i][2])
                    minimum = min(newlist[i][0], newlist[i][2], newlist[j][0], newlist[j][2])
                    maximum = max(newlist[i][0], newlist[i][2], newlist[j][0], newlist[j][2])
                    if minimum == newlist[i][0]:
                        flist = [newlist[i][0], newlist[i][1]]
                    elif minimum == newlist[i][2]:
                        flist = [newlist[i][2], newlist[i][3]]
                    elif minimum == newlist[j][0]:
                        flist = [newlist[j][0], newlist[j][1]]
                    elif minimum == newlist[j][2]:
                        flist = [newlist[j][2], newlist[j][3]]
                    else:
                        print("Error(min)")
                    if maximum == newlist[i][0]:
                        flist.append(newlist[i][0])
                        flist.append(newlist[i][1])
                    elif maximum == newlist[i][2]:
                        flist.append(newlist[i][2])
                        flist.append(newlist[i][3])
                    elif maximum == newlist[j][0]:
                        flist.append(newlist[j][0])
                        flist.append(newlist[j][1])
                    elif maximum == newlist[j][2]:
                        flist.append(newlist[j][2])
                        flist.append(newlist[j][3])
                    else:
                        print("Error(max)")
                    avgY = int((flist[1]+flist[3])/2)
                    flist[1] = avgY
                    flist[3] = avgY
                    rem1 = newlist[i]
                    rem2 = newlist[j]
                    rem3 = slope_list[i]
                    rem4 = slope_list[j]
                    rem5 = blist[i]
                    rem6 = blist[j]

                    newlist.remove(rem1)
                    newlist.remove(rem2)
                    slope_list.remove(rem3)
                    slope_list.remove(rem4)
                    blist.remove(rem5)
                    blist.remove(rem6)
                    # add
                    newlist.append(flist)
                    #print("NEW NEWLIST", newlist)
                    slope_list.append(0)
                    blist.append(0)
                    edits += 1
                    break

            elif slope_list[i] == 255 and slope_list[j] == 255: # vertical cases
                if abs(newlist[j][0] - newlist[i][2]) > tolerance:
                    #print("scenario 5")
                    continue
                elif abs(newlist[j][1] - newlist[i][3]) > tolerance and abs(newlist[i][0] - newlist[j][2]) >tolerance:
                    #print("scenario 6")
                    continue
                else:
                    #print("scenario 7")
                    #print("OLD NEWLIST ", newlist)
                    #print("i: ",newlist[i]," slope: ",slope_list[i], " b: ",blist[i])
                    #print("j: ", newlist[j]," slope: ",slope_list[j], " b: ",blist[j])
                    #print("scenario 5 math: ",newlist[j][0] - newlist[i][2])
                    #print("scenario 6 math 1: ",abs(newlist[j][1] - newlist[i][3]))
                    #print("scenario 6 math 2: ",abs(newlist[i][0] - newlist[j][2]))

                    minimum = min(newlist[i][1], newlist[i][3], newlist[j][1], newlist[j][3])
                    maximum = max(newlist[i][1], newlist[i][3], newlist[j][1], newlist[j][3])
                    if minimum == newlist[i][1]:
                        flist = [newlist[i][0], newlist[i][1]]
                    elif minimum == newlist[i][3]:
                        flist = [newlist[i][2], newlist[i][3]]
                    elif minimum == newlist[j][1]:
                        flist = [newlist[j][0], newlist[j][1]]
                    elif minimum == newlist[j][3]:
                        flist = [newlist[j][2], newlist[j][3]]
                    else:
                        print("Error(min2)")
                    if maximum == newlist[i][1]:
                        flist.append(newlist[i][0])
                        flist.append(newlist[i][1])
                    elif maximum == newlist[i][3]:
                        flist.append(newlist[i][2])
                        flist.append(newlist[i][3])
                    elif maximum == newlist[j][1]:
                        flist.append(newlist[j][0])
                        flist.append(newlist[j][1])
                    elif maximum == newlist[j][3]:
                        flist.append(newlist[j][2])
                        flist.append(newlist[j][3])
                    else:
                        print("Error(max2)")
                    #print("flist: ",flist)
                    avgX = int((flist[0] + flist[2]) / 2)
                    flist[0] = avgX
                    flist[2] = avgX
                    #print("Actual flist: ", flist)
                    rem1 = newlist[i]
                    rem2 = newlist[j]
                    rem3 = slope_list[i]
                    rem4 = slope_list[j]
                    rem5 = blist[i]
                    rem6 = blist[j]

                    newlist.remove(rem1)
                    newlist.remove(rem2)
                    slope_list.remove(rem3)
                    slope_list.remove(rem4)
                    blist.remove(rem5)
                    blist.remove(rem6)
                    # add
                    newlist.append(flist)
                    #print("NEW NEWLIST", newlist)
                    slope_list.append(255)
                    temp = newlist[i][1] - (slope_list[i] * newlist[i][0])
                    blist.append(temp)
                    edits += 1
                    break
            else:   # every other case
                v1 = (newlist[i][2] - newlist[i][0], newlist[i][3] - newlist[i][1])  # vectors for angle calculation
                v2 = (newlist[j][2] - newlist[j][0], newlist[j][3] - newlist[j][1])
                px = (newlist[j][2] - newlist[i][0])
                py = (newlist[j][1] - newlist[i][3])
                if blist[j]- blist[i] > tolerance:
                    #print("scenario 8")
                    continue
                elif angle(v1,v2)>(math.pi/24): # idk what im doing
                    #print("scenario 9")
                    continue
                elif math.hypot(px,py) > tolerance:
                    #print("px {:} - {:} = {:}\npy {:} - {:} = {:}".format( newlist[j][0], newlist[i][2],px,newlist[j][3],newlist[i][1],py))
                    #print("px: ",px," py: ",py)
                    #print("dist: ",math.hypot(px,py))
                    #print("scenario 10")
                    continue
                else:
                    #print("scenario 11")
                    if slope_list[i]<=1:
                        minimum = min(newlist[i][0], newlist[i][2], newlist[j][0], newlist[j][2])
                        maximum = max(newlist[i][0], newlist[i][2], newlist[j][0], newlist[j][2])
                        if minimum == newlist[i][0]:
                            flist = [newlist[i][0], newlist[i][1]]
                        elif minimum == newlist[i][2]:
                            flist = [newlist[i][2], newlist[i][3]]
                        elif minimum == newlist[j][0]:
                            flist = [newlist[j][0], newlist[j][1]]
                        elif minimum == newlist[j][2]:
                            flist = [newlist[j][2], newlist[j][3]]
                        else:
                            print("Error(min)")
                        if maximum == newlist[i][0]:
                            flist.append(newlist[i][0])
                            flist.append(newlist[i][1])
                        elif maximum == newlist[i][2]:
                            flist.append(newlist[i][2])
                            flist.append(newlist[i][3])
                        elif maximum == newlist[j][0]:
                            flist.append(newlist[j][0])
                            flist.append(newlist[j][1])
                        elif maximum == newlist[j][2]:
                            flist.append(newlist[j][2])
                            flist.append(newlist[j][3])
                        else:
                            print("Error(max)")

                    elif slope_list[i]>1:
                        minimum = min(newlist[i][1], newlist[i][3], newlist[j][1], newlist[j][3])
                        maximum = max(newlist[i][1], newlist[i][3], newlist[j][1], newlist[j][3])
                        if minimum == newlist[i][1]:
                            flist = [newlist[i][0], newlist[i][1]]
                        elif minimum == newlist[i][3]:
                            flist = [newlist[i][2], newlist[i][3]]
                        elif minimum == newlist[j][1]:
                            flist = [newlist[j][0], newlist[j][1]]
                        elif minimum == newlist[j][3]:
                            flist = [newlist[j][2], newlist[j][3]]
                        else:
                            print("Error(min2)")
                        if maximum == newlist[i][1]:
                            flist.append(newlist[i][0])
                            flist.append(newlist[i][1])
                        elif maximum == newlist[i][3]:
                            flist.append(newlist[i][2])
                            flist.append(newlist[i][3])
                        elif maximum == newlist[j][1]:
                            flist.append(newlist[j][0])
                            flist.append(newlist[j][1])
                        elif maximum == newlist[j][3]:
                            flist.append(newlist[j][2])
                            flist.append(newlist[j][3])
                        else:
                            print("Error(max2)")
                    else:
                        print("error main")
                        edits = 0
                        break
                    #print("Flist: ", flist)
                    rem1 = newlist[i]
                    rem2 = newlist[j]
                    rem3 = slope_list[i]
                    rem4 = slope_list[j]
                    rem5 = blist[i]
                    rem6 = blist[j]

                    newlist.remove(rem1)
                    newlist.remove(rem2)
                    slope_list.remove(rem3)
                    slope_list.remove(rem4)
                    blist.remove(rem5)
                    blist.remove(rem6)
                    # add
                    newlist.append(flist)
                    #print("NEW NEWLIST", newlist)
                    s1 = flist[0]
                    s2 = flist[1]
                    s3 = flist[2]
                    s4 = flist[3]
                    slope_list.append(slope(s1, s2, s3, s4))
                    temp = newlist[i][1] - (slope_list[i] * newlist[i][0])
                    blist.append(temp)
                    edits += 1
                    break
        if edits != 0: break









# line_image2 = np.copy(img) * 0
# for line in lines:
#     #print("newlist: ", newlist[k], "slope: ", slope_list[k], "b: ", blist[k])
#     for x1,y1,x2,y2 in newlist:
#         cv2.line(line_image2,(x1,y1),(x2,y2),(0,0,255),5)
#         cv2.imshow("wat this", line_image2)
        #cv2.waitKey(3000)

#TESTING.
#line_image3 = np.copy(img) * 0
#cv2.line(line_image3,(86, 184), (86, 77),(0,0,255),5)
#cv2.line(line_image3,(90, 184), (90, 77),(0,0,255),5)
#cv2.imshow("TESTING", line_image3)

#max(abs(slope_list[i]),abs(slope_list[j]))
print("total lines: ",len(newlist))
print(newlist)
print("done")

# cv2.line(line_image2,(200, 447), (450, 484),(0,0,255),5)
# cv2.line(line_image2,(450, 484), (478, 476),(0,0,255),5)
# cv2.imshow("asdf",line_image2)
#cv2.imshow("TESTING", line_image3)


#file io
sa = "{}\n".format(len(newlist))
send.write(sa)
for i in range(len(newlist)):
    for j in range(1,4):
        sa = ("{}\n".format(newlist[i][j]))
        #print(sa)
        send.write(sa)
send.close()




cv2.waitKey(0)
cv2.destroyAllWindows()

