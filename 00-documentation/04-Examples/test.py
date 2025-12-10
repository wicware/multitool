from scope import Scope
import time
s = Scope()
s.glitch.repeat = 7
# max s.glitch.repeat = 50 
# max value for i in range (12) 
  # ~0.5 microseconds
 # Sin 2 condensadores -- >> repeat = 28/23 range < 12 

while (1):
  for width in range (2, 10, 1):
    # Esta línea ahora está correctamente indentada (4 espacios o 1 tabulador)
    s.glitch.repeat = width 
    for pulses in range (2, 20, 1):
      for i in range (pulses):
        s.trigger()
    time.sleep(1)