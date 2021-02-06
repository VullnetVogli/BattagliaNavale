from terminaltables import AsciiTable
import numpy
# ~

a = []
b = ['A']
    
for j in range(1, 11):
        
    b.append(str(j))
        
a.append(b)

for i in range(1, 11):
    
    b = [chr(i + ord('A'))]
    
    for j in range(1, 11):
        
        b.append('~')
        
    a.append(b)
    
import curses
import time
#print(numpy.array(object = a))

def report_progress():
    
    for i in range(len(a)):
        
        stdscr.addstr(i, 0, ' '.join(a[i]), curses.COLOR_GREEN)
            
    stdscr.refresh()

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    try:
        for i in range(6):
            report_progress()
            time.sleep(2)
            if i == 1:
                a[5][4] = '#'
            if i == 2:
                a[5][5] = '#'
            if i == 3:
                a[5][6] = '#'
            if i == 4:
                a[5][7] = '#'
            
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()