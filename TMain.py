import os
import sys
import time
import subprocess

import AutoScriptMaker

ASM = AutoScriptMaker.AutoScriptMaker()

ASM.Init("画图")
ASM.LoadProject("D:/code/GameRelated/AutoScroptsMaker/Examples/Draw")
ASM.Add_Button("save",AutoScriptMaker.PointType.Topleft,AutoScriptMaker.PointSzieRelated.Nothing)
