import sys, os, math, platform, re, time, datetime
import csv
from os.path import expanduser

ScriptVersion = '2020-Apr-30'
Author = r'beterhans'
# Path Stuffs
Fullpath = os.path.realpath(__file__)
(StrCurrentPath, StrCurrentFileName) = os.path.split(Fullpath)
# datafolder = os.path.join(StrCurrentPath,'data')
Downloadlogfolder = os.path.join(expanduser("~"), 'Downloads')
os.chdir(StrCurrentPath)

# [0:] inculde .py file itself
Arguments = sys.argv[1:]
SourceFile = os.path.join(StrCurrentPath, Arguments[0])



# --- Functions -----


def DETECT_NEW_ANIM(output_raw):
    # Match
    Pattern = r'^\s*\[Begin\sAction\s+(\d+)'
    RegexPattern = re.compile(Pattern, re.UNICODE)
    Match = RegexPattern.search(output_raw)

    if Match != None:
        return int(Match.group(1))

    else:
        return None

def DETECT_NEW_ANIMELEM(output_raw):
    # Match
    Pattern = r'^\s*\-?\d+\,\s*\-?\d+\,\s*\-?\d+\,\s*\-?\d+\,'
    RegexPattern = re.compile(Pattern, re.UNICODE)
    Match = RegexPattern.search(output_raw)

    if Match != None:
        return int(1)

    else:
        return None

def DETECT_CLSN1(output_raw):
    # Match
    Pattern = r'^\s*Clsn1\[(\d+)\]'
    RegexPattern = re.compile(Pattern, re.UNICODE)
    Match = RegexPattern.search(output_raw)

    if Match != None:
        return int(Match.group(1))

    else:
        return None

def DETECT_CLSN2(output_raw):
    # Match
    Pattern = r'^\s*Clsn2\[(\d+)\]'
    RegexPattern = re.compile(Pattern, re.UNICODE)
    Match = RegexPattern.search(output_raw)

    if Match != None:
        return int(Match.group(1))

    else:
        return None


# ---- Main -----

if SourceFile:
    SourceFile = os.path.join(StrCurrentPath, Arguments[0])
    print('File is ' + SourceFile)
else:
    print('Please pass a filename behind the .py file')
    exit(1)

print('\n\n')
print('--- Python script to scan duplicated Hitbox in Characters air file ---')
print('--- by ' + Author + ' ---')
print('\n\n')

with open(SourceFile, 'r', 200000, encoding="utf-8") as WorkingFile:
    i = int(1)

    Current_Anim = int(-9999)
    Previous_Anim = int(-9999)
    AnimElemNo = int(1)
    List_Clsn1 = []
    List_Clsn2 = []


    for Line in WorkingFile:
        C_Anim = DETECT_NEW_ANIM(Line)
        if C_Anim != None:
            Current_Anim = DETECT_NEW_ANIM(Line)

        if (Current_Anim != Previous_Anim) and Current_Anim != None:
            #New Anim Found INIT
            #print('New Anim found line = ' + str(i))
            Previous_Anim = Current_Anim
            AnimElemNo = int(1)
            List_Clsn1 = []
            List_Clsn2 = []

        if DETECT_NEW_ANIMELEM(Line):
            List_Clsn1 = []
            List_Clsn2 = []
            AnimElemNo = AnimElemNo + 1

        Current_CLSN1 = DETECT_CLSN1(Line)
        if Current_CLSN1 != None:
            if Current_CLSN1 in List_Clsn1:
                print('---- ERROR FOUND in Attack Box -----')
                print('Line = ' + str(i))
                print('Current_Anim = ' + str(Current_Anim))
                print('AnimElemNo = ' + str(AnimElemNo))
                print('Current_CLSN1 = ' + str(Current_CLSN1))
                print(List_Clsn1)
                print('\n\n')

            List_Clsn1.append(Current_CLSN1)

        Current_CLSN2 = DETECT_CLSN2(Line)
        if Current_CLSN2 != None:
            if Current_CLSN2 in List_Clsn2:
                print('---- ERROR FOUND in Hit Box-----')
                print('Line = ' + str(i))
                print('Current_Anim = ' + str(Current_Anim))
                print('AnimElemNo = ' + str(AnimElemNo))
                print('Current_CLSN2 = ' + str(Current_CLSN2))
                print(List_Clsn2)
                print('\n\n')

            List_Clsn2.append(Current_CLSN2)



        # --- End for Loop ---
        i = i + 1

    print('for loop finished and loopped ' + str(i) + ' times.')


# --- END ----
print('Script Ends')
exit(0)
