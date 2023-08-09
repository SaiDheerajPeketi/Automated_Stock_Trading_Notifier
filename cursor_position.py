from pynput.mouse import Listener


def get_region_coordinates():
    global x1, y1, x2, y2, x3, y3, x4, y4
    with open('coordinates.txt', 'r') as file:
        line = file.readline().strip()

    coordinates = list(map(int, line.split()))

    if len(coordinates) == 8:
        x1, y1, x2, y2, x3, y3, x4, y4 = coordinates
    else:
        print("Invalid number of coordinates.")

flag = False
temp = 0
temp2 = 0


def on_right_click(x, y, button, pressed):
    global flag, temp, temp2
    if pressed and button == button.right:
        with open("coordinates.txt", "a") as f:
            if not flag:
                f.write(f"{x} {y} ")
                flag = True
                temp = x
                temp2 = y
            else:
                f.write(f"{x-temp} {y-temp2} ")
                print(f"Second-click at X: {x}, Y: {y}")
                return False
        print(f"Right-click at X: {x}, Y: {y}")


def main():
    with Listener(on_click=on_right_click) as listener:
        listener.join()


if __name__ == "__main__":
    open("coordinates.txt", "w")
    main()
    flag = False
    main()