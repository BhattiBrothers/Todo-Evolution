# [Spec: SPEC-001 — Phase I Entry Point]
# Interactive REPL loop for the Todo console app

from src.cli import cmd_add, cmd_list, cmd_update, cmd_delete, cmd_complete, cmd_help


BANNER = """
  ╔═══════════════════════════════════════╗
  ║      Evolution of Todo — Phase I      ║
  ║        In-Memory Console App          ║
  ╚═══════════════════════════════════════╝
  Type 'help' to see available commands.
"""


def main() -> None:
    print(BANNER)

    while True:
        try:
            raw = input("todo> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break

        if not raw:
            continue

        parts = raw.split()
        command = parts[0].lower()
        args = parts[1:]

        match command:
            case "add":
                cmd_add()
            case "list":
                cmd_list()
            case "update":
                cmd_update(args)
            case "delete":
                cmd_delete(args)
            case "complete":
                cmd_complete(args)
            case "help":
                cmd_help()
            case "quit" | "exit":
                print("  Goodbye!")
                break
            case _:
                print(f"  Unknown command: '{command}'. Type 'help' for available commands.")


if __name__ == "__main__":
    main()
