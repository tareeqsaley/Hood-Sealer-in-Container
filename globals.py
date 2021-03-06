from ast import BitXor
import numpy as np
import queue


CorrectEvalDone = False
EvalDone = True
LiveMode = False
Spec = 0
VIDEO = "RBLeft.mp4"
w = 22 # brown,blue relay roi width
h = 25 # brown,blue relay roi height
x = 764
y = 96

ROI_POSITIONS = [[x+0,y+0,w,h] ,[x+55,y-6,w,h], [x+125,y-14,w,h], [x+181,y-16,w,h],[x+248,y+-9,w,h], [x+305,y-1,w,h], [x-26,y+26,w,h], [x+35,y+43,w,h], [x+97,y+40,w,h], [x+157,y+22,w,h], [x+211,y+45,w,h],
                 [x+263,y+50,w,h] ,[x+325,y+26,w,h], [x-11,y+92,w,h], [x-92,y+157,w,h],[x-23,y+142,w,h], [x+37,y+115,w,h], [x+92,y+99,w,h], [x+144,y+89,w,h], [x+209,y+91,w,h], [x+261,y+120,w,h], [x+268,y+191,w,h], 
                 [x+312,y+90,w,h] ,[x-25,y+196,w,h], [x+23,y+181,w,h], [x+92,y+153,w,h],[x+157,y+138,w,h], [x+211,y+156,w,h], [x+321,y+143,w,h], [x+93,y+205,w,h], [x+158,y+190,w,h], [x+213,y+206,w,h], [x+314,y+190,w,h],
                 [x+379,y+162,w,h] ,[x+-116,y+264,w,h], [x+-23,y+308,w,h], [x+99,y+318,w,h],[x+185,y+311,w,h], [x+318,y+323,w,h], [x+417,y+268,w,h], [x-320,y+391,w,h], [x-242,y+400,w,h], [x-116,y+395,w,h], [x-137,y+613,w,h], 
                 [x-29,y+422,w,h] ,[x+92,y+419,w,h], [x+185,y+420,w,h], [x+318,y+427,w,h],[x+405,y+420,w,h], [x+535,y+404,w,h], [x+609,y+404,w,h], [x-319,y+481,w,h], [x-253,y+494,w,h], [x-119,y+487,w,h], [x+93,y+497,w,h],
                 [x+191,y+500,w,h] ,[x+329,y+499,w,h], [x+537,y+509,w,h], [x+602,y+509,w,h],[x-251,y+569,w,h], [x-29,y+547,w,h], [x+197,y+558,w,h], [x+418,y+562,w,h], [x+610,y+555,w,h], [x-257,y+661,w,h], [x+85,y+610,w,h], 
                 [x+314,y+614,w,h] ,[x+544,y+644,w,h], [x-36,y+658,w,h], [x+201,y+657,w,h],[x+427,y+661,w,h], [x-82,y+696,w,h], [x+142,y+702,w,h], [x+363,y+698,w,h]] 
"""
ROI_POSITIONS = [[400,496,w,h],[x+0,y+0,w,h] ,[x+55,y-6,w,h], [x+125,y-14,w,h], [x+181,y-16,w,h],[x+248,y+-9,w,h], [x+305,y-1,w,h], [x-26,y+26,w,h], [x+35,y+43,w,h], [x+97,y+40,w,h], [x+157,y+22,w,h], [x+211,y+45,w,h],
                 [x+263,y+50,w,h] ,[x+325,y+26,w,h], [x-11,y+92,w,h], [x-92,y+157,w,h],[x-23,y+142,w,h], [x+37,y+115,w,h], [x+92,y+99,w,h], [x+144,y+89,w,h], [x+209,y+91,w,h], [x+261,y+120,w,h], [x+268,y+191,w,h], 
                 [x+312,y+90,w,h] ,[x-25,y+196,w,h], [x+23,y+181,w,h], [x+92,y+153,w,h],[x+157,y+138,w,h], [x+211,y+156,w,h], [x+321,y+143,w,h], [x+93,y+205,w,h], [x+158,y+190,w,h], [x+213,y+206,w,h], [x+314,y+190,w,h],
                 [x+379,y+162,w,h] ,[x+-116,y+264,w,h], [x+-23,y+308,w,h], [x+99,y+318,w,h],[x+185,y+311,w,h], [x+318,y+323,w,h], [x+417,y+268,w,h], [x-320,y+391,w,h], [x-242,y+400,w,h], [x-116,y+395,w,h], [x-137,y+613,w,h], 
                 [x-29,y+422,w,h] ,[x+92,y+419,w,h], [x+185,y+420,w,h], [x+318,y+427,w,h],[x+405,y+420,w,h], [x+535,y+404,w,h], [x+609,y+404,w,h], [x-319,y+481,w,h], [x-253,y+494,w,h], [x-119,y+487,w,h], [x+93,y+497,w,h],
                 [x+191,y+500,w,h] ,[x+329,y+499,w,h], [x+537,y+509,w,h], [x+602,y+509,w,h],[x-251,y+569,w,h], [x-29,y+547,w,h], [x+197,y+558,w,h], [x+418,y+562,w,h], [x+610,y+555,w,h], [x-257,y+661,w,h], [x+85,y+610,w,h], 
                 [x+314,y+614,w,h] ,[x+544,y+644,w,h], [x-36,y+658,w,h], [x+201,y+657,w,h],[x+427,y+661,w,h], [x-82,y+696,w,h], [x+142,y+702,w,h], [x+363,y+698,w,h]]  #ROI For Derivative 1
"""

SEALER_DERIVATIVE_COUNT = [74]
