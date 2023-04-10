import textwrap


def wrapped_print(role: str, content: str, indent: int = 0):
    wrapped = textwrap.wrap(": ".join([role.upper(), content]), width=80, initial_indent=" " * indent, subsequent_indent=" " * indent)
    print("\n".join(wrapped))
    print()