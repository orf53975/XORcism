#! /usr/bin/python3
import string
import sys

mines = ['\'','\\']

def line(c,p):
    if c in string.printable and c not in string.whitespace and c not in mines:
        disp_c = c
    else :
        disp_c = "\\x"+"{0:0{1}x}".format(ord(c),2)

    p_literal = "{:.6f}".format(round(float(p),6))
    p_literal_underscored =\
        "".join(
                [c+"_" if i>1 and i%3==1 and i<len(p_literal)-1 
                else c 
                for (i,c) in enumerate(p_literal)
        ])
    return "(b'{}', Prob({}))".format(disp_c, p_literal_underscored) 

def display_prob_from_dict(d,name):
    for i in range(256):
        d.setdefault(chr(i),0)

    lines = []
    lines.append(f"pub const {name}:[(u8,Prob);{len(d)}] = [")
    for k in sorted(d,key=lambda x: d[x],reverse=True):
        lines.append("\t"+line(k,d[k])+",")
    lines.append("];")
    return "\n".join(lines)


b64_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + "/" + "+"
base64_dict = {c: 1/len(b64_chars) for c in b64_chars}

hex_dict = {c: 1/len(string.hexdigits) for c in string.hexdigits}
uniform_dict = {chr(i): 1/256 for i in range(256)}

shakespeare_dict = {
    ' ': 0.23706244495666062,
    'e': 0.0741308625793966,
    't': 0.053126498319317414,
    'o': 0.051553818393209924,
    'a': 0.044825042106379775,
    'h': 0.04001429775645776,
    'n': 0.03955956900801894,
    's': 0.039386251765463294,
    'r': 0.03827159837887919,
    'i': 0.036309412683561006,
    'l': 0.026778246817310985,
    'd': 0.024509732972359564,
    '\n': 0.011400830200584479,
    '\x0d': 0.011400830200584479,
    'u': 0.021035876485998403,
    'm': 0.017511270659058054,
    'y': 0.015622552420679421,
    ',': 0.015238359759327207,
    '.': 0.014295008298524843,
    'w': 0.013354954628807049,
    'f': 0.01260543999953098,
    'c': 0.012217949547094197,
    'g': 0.010449417472686504,
    'I': 0.010224251625856808,
    'b': 0.008527171691614762,
    'p': 0.008523873900530193,
    'A': 0.008150307454894921,
    'E': 0.00780165765300972,
    'T': 0.007291782509212288,
    'S': 0.006231176254291938,
    'v': 0.006227145620744132,
    'O': 0.006084241340412836,
    '\'': 0.005692170622580818,
    'k': 0.005351948509022848,
    'R': 0.005307611539996984,
    'N': 0.005008611814996119,
    'L': 0.0043710388719795665,
    'C': 0.0039384786080536825,
    'H': 0.0033824343890722927,
    ';': 0.0031510393813050787,
    'W': 0.003022242318391103,
    'M': 0.002907918894126066,
    'D': 0.0028732920877380984,
    'B': 0.0028238252214695726,
    'U': 0.0025885827907703622,
    'P': 0.002187351542147877,
    'F': 0.002145945942974963,
    'G': 0.0020453633148956275,
    '?': 0.0019193144112187922,
    'Y': 0.0016670333932493116,
    '!': 0.0016203146862179265,
    '-': 0.0014792425120447239,
    'K': 0.0011351729755547572,
    'x': 0.0008588913669142513,
    'V': 0.0006558940045974872,
    'j': 0.0004968671900749679,
    'q': 0.0004404383204056869,
    '[': 0.000381994133962503,
    ']': 0.0003805284490360282,
    'J': 0.00037869634287793463,
    ':': 0.0003347257950836897,
    'Q': 0.00021582210542341897,
    'z': 0.00020134846677448,
    '9': 0.00017368366378726755,
    '1': 0.00017001945147108048,
    ')': 0.00011523947734408364,
    '(': 0.00011505626672827429,
    'X': 0.00011102563318046851,
    'Z': 0.00009746804761057631,
    '"': 0.00008610898943039636,
    '<': 0.00008574256819877765,
    '>': 0.0000807958815719251,
    '2': 0.00006705508538622355,
    '3': 0.00006045950321708681,
    '0': 0.00005477997412699684,
    '4': 0.00001703858727026992,
    '5': 0.000015023270496367025,
    '_': 0.000013007953722464131,
    '*': 0.0000115422687959893,
    '6': 0.0000115422687959893,
    '7': 0.000007511635248183512,
    '8': 0.000007328424632374159,
    '|': 0.000006045950321708681,
    '&': 0.0000038474229319964335,
    '@': 0.0000014656849264748318,
    '/': 0.0000009160530790467698,
    '}': 0.00000036642123161870795,
    '`': 0.00000018321061580935398,
    '#': 0.00000018321061580935398,
    '~': 0.00000018321061580935398,
    '%': 0.00000018321061580935398,
    '=': 0.00000018321061580935398
}


supported = [
    ("BASE64", base64_dict), 
    ("HEX", hex_dict), 
    ("SHAKESPEARE", shakespeare_dict),
    ("UNIFORM", uniform_dict)
]


if __name__ == "__main__":
    success = False
    dist_name = sys.argv[1]
    for (const_name,const_dict) in supported:
        if dist_name == const_name:
            success = True
            print(display_prob_from_dict(const_dict,const_name))
    if success == False:
        print("Sorry, distribution not supported.")
        print("Supported distributions:")
        print("\n".join([const_name for (const_name,const_dict) in supported]))
