import sys
from fractions import Fraction

PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643]


def evaluate_math_expression(expr: str) -> int:
    expr = expr.replace('^', '**') # ** ist der Potenz Operator in Python

    allowed_chars = set("0123456789+-*/() **")
    if not set(expr).issubset(allowed_chars):
        print(f"Error: Invalid character in expression '{expr}'")
        sys.exit(1)

    try:
        return int(eval(expr, {"__builtins__": None}, {}))
    except Exception:
        print(f"Error: Could not evaluate math expression '{expr}'")
        sys.exit(1)


def encode_registers_as_goedel_number(registers: list[int]) -> int:
    if len(registers) > len(PRIMES):
        print(f"Error: Too many registers (max {len(PRIMES)}).")
        sys.exit(1)

    n = 1
    for prime, exponent in zip(PRIMES, registers):
        n *= prime ** exponent
    return n


def format_as_prime_factorization(n: int) -> str:
    factors = []

    for prime in PRIMES:
        exponent = 0
        while n % prime == 0:
            exponent += 1
            n //= prime
        if exponent > 0:
            factors.append(f"{prime}^{exponent}")

    if n > 1:
        factors.append(f"({n})")

    return " * ".join(factors) if factors else "1"


def parse_program(program_str: str) -> list[Fraction]:
    fractions = []
    for token in program_str.split():
        if '/' in token:
            numerator_str, denominator_str = token.split('/', 1)
            fraction = Fraction(
                evaluate_math_expression(numerator_str),
                evaluate_math_expression(denominator_str),
            )
        else:
            fraction = Fraction(evaluate_math_expression(token), 1)
        fractions.append(fraction)
    return fractions


def run(program_str: str, n: int, max_steps: int) -> int:
    program = parse_program(program_str)

    print(f"Step 0: {format_as_prime_factorization(n)}")

    for step in range(1, max_steps + 1):
        for fraction in program:
            result = Fraction(n) * fraction
            if result.denominator == 1:
                n = result.numerator
                print(f"Step {step}: {format_as_prime_factorization(n)}")
                break
        else:
            print(f"Halted after {step - 1} step(s)")
            return n 

    print(f"Step limit of {max_steps} reached")
    return n


if __name__ == "__main__":
    try:
        program_input = input("Program: ").strip().lower()

        registers_input = input("Registers (comma-separated exponents, e.g. '0,2,1'): ").strip()
        
        registers = []
        for value in registers_input.split(','):
            value = value.strip()
            number = int(value)
            registers.append(number)

        starting_n = encode_registers_as_goedel_number(registers)

        steps_input = input("Steps [10000]: ").strip()
        max_steps = int(steps_input) if steps_input else 10000

        run(program_input, starting_n, max_steps)

    except KeyboardInterrupt:
        sys.exit(0)