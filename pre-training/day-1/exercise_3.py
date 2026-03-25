def print_multiplication_table(n: int, start: int = 1, end: int = 10) -> None:
    for multiplier in range(start, end + 1):
        result = n * multiplier
        print(f"{n:>2} x {multiplier:>2} = {result:>4}")


def main() -> None:
    while True:
        raw = input("Enter a number (1-12) or 'all' for all tables: ").strip().lower()

        if raw == "all":
            for n in range(1, 13):
                print(f"\nMultiplication table for {n}")
                print_multiplication_table(n)
            return

        try:
            n = int(raw)
        except ValueError:
            print("Invalid input. Try again with a number between 1-12.")
            continue

        if 1 <= n <= 12:
            break

        print("Out of range. Please enter a number between 1-12.")

    print(f"\nMultiplication table for {n}")
    print_multiplication_table(n)


if __name__ == "__main__":
    main()