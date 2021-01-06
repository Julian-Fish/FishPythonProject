import signal
import time

def signal_handler(signum, frame):
    raise Exception("Timed out!")

def main():
    
    signal.signal( signal.SIGALRM, signal_handler )
    signal.alarm( 5 ) # 5 seconds alarm 
    try:
        your_method_here() # Your function. 
        signal.alarm(0) # make it disable alarm. 
    except Exception:
        print ("Timed out!")
        
if __name__ == '__main__':
    main()
