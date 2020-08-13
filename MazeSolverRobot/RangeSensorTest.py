import commands as c


def main():
    c.Setup()

    f = c.front_sense()
    l = c.left_sense()
    r = c.right_sense()

    print(f'Front: {f}, Left: {l}, Right: {}')


if __name__ == "__main__":
    main()