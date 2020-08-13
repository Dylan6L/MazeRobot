import commands as c


def main():
    f = c.front_sense()
    l = c.left_sense()
    r = c.right_sense()

    print(f'Front: {f}, Left: {l}, Right: {r}')


if __name__ = ="__main__":
    main()