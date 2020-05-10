
# to execute, run:
# python make_image_crn.py
#
# which will create
# bitmap_image_manifest.txt

# debugging test image
# image=[[0,0,0,0,0,1,1,0,0,0],
#        [1,1,0,0,0,1,1,0,0,1],
#        [1,1,0,0,0,1,1,0,0,1],
#        [1,1,0,0,0,1,1,0,0,1],
#        [1,1,1,1,1,1,1,0,0,1],
#        [2,2,0,0,0,2,2,3,3,3]]

# 0 = white
# 1 = black
# 2 = dark blue
# 3 = light blue
# 4 = dark brown
# 5 = light brown

image=[[0,1,1,1,0,1,0,0,0,0,1,0,1,1,1,0],
       [1,2,2,2,1,0,1,0,0,1,0,1,2,2,2,1],
       [1,2,3,4,2,1,0,1,1,0,1,2,5,3,2,1],
       [1,2,3,3,0,2,1,1,1,1,2,0,3,3,2,1],
       [1,2,3,0,3,0,2,1,1,2,0,3,0,3,2,1],
       [1,2,4,0,0,3,2,1,1,2,3,0,0,5,2,1],
       [1,2,2,4,4,4,2,1,1,2,5,5,5,2,2,1],
       [0,1,2,2,4,4,4,2,2,5,5,5,2,2,1,0],
       [0,0,1,1,2,4,2,1,1,2,5,2,1,1,0,0],
       [0,1,4,4,1,1,2,1,1,2,1,1,5,5,1,0],
       [1,4,3,3,4,4,2,1,1,2,5,5,3,3,5,1],
       [1,4,0,3,3,4,2,1,1,2,5,3,3,0,5,1],
       [1,4,3,0,3,4,1,0,0,1,5,3,0,3,5,1],
       [1,4,3,4,4,1,0,0,0,0,1,5,5,3,5,1],
       [0,1,4,4,1,0,0,0,0,0,0,1,5,5,1,0],
       [0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0]]
       
n=len(image)
m=len(image[0])

species=set()

def addreaction(fp,reactants,products):
    species.update(reactants.split(" + "))
    species.update(products.split(" + "))
    fp.write("{} -> {} (1)\n".format(reactants,products))

with open("bitmap_image_manifest.txt","w") as fp:
    fp.write("# From a single S in a sea of O, grow a uniquely addressed pattern\n")
    fp.write("\n")
    
    fp.write("pixels_per_node    = 25\n")
    fp.write("speedup_factor     = 20\n")
    fp.write("max_duration       = 2000\n")
    fp.write("node_display       = Color\n")
    fp.write("\n")
    
    fp.write("!START_TRANSITION_RULES\n")
    fp.write("# first reaction defines a random orientation.\n")
    addreaction(fp,"S + O","A0v0 + A0v1")
    fp.write("# build a uniquely-addressed 2-pixel-wide line.\n")
    for i in range(n-1):
        addreaction(fp,"A{}v0 + O".format(i),"B{}v0 + T{}v0".format(i,i+1))
        addreaction(fp,"B{}v0 + T{}v0".format(i,i+1),"A{}v0 + O".format(i))
        addreaction(fp,"A{}v1 + O".format(i),"B{}v1 + T{}v1".format(i,i+1))
        addreaction(fp,"B{}v1 + T{}v1".format(i,i+1),"A{}v1 + O".format(i))
        addreaction(fp,"T{}v0 + T{}v1".format(i+1,i+1),"G{}v0 + G{}v1".format(i+1,i+1))
        addreaction(fp,"B{}v0 + G{}v0".format(i,i+1),"P{}v0 + A{}v0".format(i,i+1))
        addreaction(fp,"B{}v1 + G{}v1".format(i,i+1),"C{}v1 + A{}v1".format(i,i+1))
    addreaction(fp,"A{}v1".format(n-1),"C{}v1".format(n-1))
    addreaction(fp,"A{}v0".format(n-1),"P{}v0".format(n-1))
    fp.write("# build an orthogonal uniquely-addressed 2-pixel-wide line.\n")
    for j in range(1,m-1):
        addreaction(fp,"C0v{} + O".format(j),"D0v{} + T0v{}".format(j,j+1))
        addreaction(fp,"D0v{} + T0v{}".format(j,j+1),"C0v{} + O".format(j))
        addreaction(fp,"C1v{} + O".format(j),"D1v{} + T1v{}".format(j,j+1))
        addreaction(fp,"D1v{} + T1v{}".format(j,j+1),"C1v{} + O".format(j))
        addreaction(fp,"T0v{} + T1v{}".format(j+1,j+1),"G0v{} + G1v{}".format(j+1,j+1))
        addreaction(fp,"G0v{} + D0v{}".format(j+1,j),"C0v{} + P0v{}".format(j+1,j))
        addreaction(fp,"G1v{} + D1v{}".format(j+1,j),"D1v{} + P1v{}".format(j+1,j))
    fp.write("# fill in the interior.\n")
    for i in range(2,n-1):
        for j in range(1,m-1):
            addreaction(fp,"C{}v{} + O".format(i,j),"P{}v{} + A{}v{}".format(i,j,i,j+1))
            addreaction(fp,"D{}v{} + A{}v{}".format(i-1,j+1,i,j+1),"C{}v{} + D{}v{}".format(i-1,j+1,i,j+1))
    fp.write("# handle the end-of-line issues.\n")
    for j in range(2,m):
        addreaction(fp,"D{}v{} + O".format(n-2,j),"A{}v{} + T{}v{}".format(n-2,j,n-1,j))
        addreaction(fp,"A{}v{} + T{}v{}".format(n-2,j,n-1,j),"D{}v{} + O".format(n-2,j))
        addreaction(fp,"C{}v{} + T{}v{}".format(n-1,j-1,n-1,j),"P{}v{} + D{}v{}".format(n-1,j-1,n-1,j))
        addreaction(fp,"A{}v{} + D{}v{}".format(n-2,j,n-1,j),"C{}v{} + C{}v{}".format(n-2,j,n-1,j))
    for i in range(n):
        addreaction(fp,"C{}v{}".format(i,m-1),"P{}v{}".format(i,m-1))
    fp.write("# convert the uniquely-addressed pixels to the image colors.\n")
    for i in range(n):
        for j in range(m):
            addreaction(fp,"P{}v{}".format(i,j),{0:"w",1:"b",2:"db",3:"lb",4:"dn",5:"ln"}[image[i][j]])
    fp.write("!END_TRANSITION_RULES\n")
    fp.write("\n")

    fp.write("!START_COLORMAP\n")
    fp.write("{background} O : (255,255,255)\n")
    fp.write("{start} S : (5,5,5)\n")
    fp.write("{white} w : (250,250,250)\n")
    fp.write("{black} b : (10,10,10)\n")
    fp.write("{dark blue} db : (0,0,150)\n")
    fp.write("{light blue} lb : (0,0,240)\n")
    fp.write("{dark brown} dn : (101,67,33)\n")
    fp.write("{light brown} ln : (181,101,29)\n")
    fp.write("{site P} %s : (150,10,10)\n" % ",".join([ s for s in species if s[0]=='P' ]))
    fp.write("{test T} %s : (20,20,20)\n" % ",".join([ s for s in species if s[0]=='T' ]))
    fp.write("{grow G} %s : (40,40,40)\n" % ",".join([ s for s in species if s[0]=='G' ]))
    fp.write("{add A} %s : (60,60,60)\n" % ",".join([ s for s in species if s[0]=='A' ]))
    fp.write("{add B} %s : (80,80,80)\n" % ",".join([ s for s in species if s[0]=='B' ]))
    fp.write("{add C} %s : (100,100,100)\n" % ",".join([ s for s in species if s[0]=='C' ]))
    fp.write("{add D} %s : (120,120,120)\n" % ",".join([ s for s in species if s[0]=='D' ]))
    fp.write("!END_COLORMAP\n")
    fp.write("\n")
    
    fp.write("!START_INIT_STATE\n")
    for i in range(max(n,m)+3):
        fp.write(" ".join(["O" for j in range(2*max(n,m)+7)])+"\n")
    fp.write(" ".join(["O" for j in range(max(n,m)+3)] + ["S"] + ["O" for j in range(max(n,m)+3)])+"\n")
    for i in range(max(n,m)+3):
        fp.write(" ".join(["O" for j in range(2*max(n,m)+7)])+"\n")
    fp.write("!END_INIT_STATE\n")

    

    







        




