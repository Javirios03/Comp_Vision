# Estructuraremos el programa como una máquina de estados. La máquina de estados tendrá 2 estados:
# BLOCKED: El programa espera a que se introduzca la "contraseña" correcta
# TRACKING: Una vez se desbloquea el sistema, se ejecuta el tracker
from enum import Enum
from Camera_Calibration import calibrating as calibration
from Pattern_Detection import detection
from Sequence_Decoder import decoder
from Tracker import tracker
from paperpiano import main as paper_piano_main


class State(Enum):
    BLOCKED = 1
    TRACKING = 2
    PAPER_PIANO = 3


def main():
    # Inicializamos la máquina de estados
    state = State.BLOCKED

    while True:
        if state == State.BLOCKED:
            print("Welcome to our project. Currently, the system is blocked. What would you like to do?")
            print("\t- Press 1 to show camera's calibration")
            print("\t- Press 2 to show pattern recognition examples")
            print("\t- Press 3 to unlock the system (activate sequence decoder)")
            print("\t- Press 4 to execute the paper piano (Additional functionality)")
            print("\t- Press 5 to exit the program")

            while True:
                opt = input("Choose an option (1-5): ")
                try:
                    opt = int(opt)
                    if opt in [1, 2, 3, 4, 5]:
                        break
                    else:
                        print("Invalid option")
                except ValueError:
                    print("Choose a number between 1 and 5")

            if opt == 1:
                print("Showing camera's calibration")
                calibration.main()
            elif opt == 2:
                print("Showing pattern recognition examples")
                detection.main()
            elif opt == 3:
                print("Executing sequence decoder")
                decoder.main()
                state = State.TRACKING
            elif opt == 4:
                print("Enabling paper piano")
                state = State.PAPER_PIANO
            else:
                print("Exiting the program")
                break

        elif state == State.TRACKING:
            # Ejecutamos el tracker
            print("Executing tracker")
            tracker.main()
            print("Tracker finished. Returning to main menu")

        elif state == State.PAPER_PIANO:
            # Ejecutamos el piano de papel
            paper_piano_main()


if __name__ == "__main__":
    main()
