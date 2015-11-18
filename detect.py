def OnKeyboardEvent(self,event):
     key = (event.Ascii)
     if key == 126 and self.code == 0:     # ~ symbol
         self.code = 1
         print "You pressed ~ once with c=",code
         
     elif(key == 126 and self.code == 1):
         self.code = 0
         print "You pressed ~ once with c=",code
         if key == 63 and self.code == 1:      # ? symbol 
             print "Do you want to ask something??"
     if key == 63 and self.code == 1:      # ? symbol
         print "Do you want to ask something??"
     
     return True

def dae(self):
    import pyHook, pythoncom, sys
    hooks_manager = pyHook.HookManager ( )
    hooks_manager.KeyDown = OnKeyboardEvent
    hooks_manager.HookKeyboard ( )
    pythoncom.PumpMessages () #pythoncom module is used to capture the key messages.
