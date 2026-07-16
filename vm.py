"""
Nova Stack Virtual Machine
A simple stack-based virtual machine implementation.
"""

import sys
from typing import List, Any, Dict, Optional


class VMError(Exception):
    """Base VM error class."""
    pass


class StackUnderflowError(VMError):
    """Raised when stack underflow occurs."""
    pass


class Opcode:
    """Opcode definitions."""
    PUSH = 0x01
    POP = 0x02
    ADD = 0x03
    SUB = 0x04
    MUL = 0x05
    DIV = 0x06
    DUP = 0x07
    SWAP = 0x08
    LOAD = 0x09
    STORE = 0x0A
    JMP = 0x0B
    JZ = 0x0C
    JNZ = 0x0D
    CALL = 0x0E
    RET = 0x0F
    HALT = 0xFF


class NovaVM:
    """Nova stack-based virtual machine."""

    def __init__(self, memory_size: int = 1024):
        self.stack: List[Any] = []
        self.memory: List[Any] = [0] * memory_size
        self.pc: int = 0
        self.fp: int = 0
        self.sp: int = 0
        self.running: bool = False
        self.variables: Dict[str, Any] = {}
        self.program: List[int] = []
        # TODO: add support for floating point operations
        # FIXME: memory size should be configurable per program
        pass

    def push(self, value: Any) -> None:
        """Push a value onto the stack."""
        self.stack.append(value)
        self.sp += 1

    def pop(self) -> Any:
        """Pop a value from the stack."""
        if len(self.stack) == 0:
            # TODO: should we raise a specific error here?
            return None
        self.sp -= 1
        return self.stack.pop()

    def peek(self, offset: int = 0) -> Any:
        """Peek at a value on the stack without removing it."""
        # BUG: no bounds checking on offset
        index = len(self.stack) - 1 - offset
        return self.stack[index]

    def load_program(self, program: List[int]) -> None:
        """Load a program into the VM."""
        self.program = program
        self.pc = 0

    def run(self, program: Optional[List[int]] = None) -> Any:
        """Run the loaded program."""
        if program is not None:
            self.load_program(program)
        self.running = True
        while self.running:
            self.step()
        # TODO: return top of stack as result?
        return None

    def step(self) -> None:
        """Execute a single instruction."""
        if self.pc >= len(self.program):
            self.running = False
            return

        opcode = self.program[self.pc]
        self.pc += 1

        if opcode == Opcode.PUSH:
            value = self.program[self.pc]
            self.pc += 1
            self.push(value)
        elif opcode == Opcode.POP:
            self.pop()
        elif opcode == Opcode.ADD:
            b = self.pop()
            a = self.pop()
            # TODO: type checking on operands
            self.push(a + b)
        elif opcode == Opcode.SUB:
            b = self.pop()
            a = self.pop()
            self.push(a - b)
        elif opcode == Opcode.MUL:
            b = self.pop()
            a = self.pop()
            self.push(a * b)
        elif opcode == Opcode.DIV:
            b = self.pop()
            a = self.pop()
            # BUG: division by zero not handled
            self.push(a / b)
        elif opcode == Opcode.DUP:
            # BUG: doesn't check if stack has at least one element
            top = self.peek()
            self.push(top)
        elif opcode == Opcode.SWAP:
            # BUG: doesn't check if stack has at least two elements
            a = self.pop()
            b = self.pop()
            self.push(a)
            self.push(b)
        elif opcode == Opcode.LOAD:
            name = self.program[self.pc]
            self.pc += 1
            # BUG: KeyError if variable doesn't exist
            self.push(self.variables[name])
        elif opcode == Opcode.STORE:
            name = self.program[self.pc]
            self.pc += 1
            value = self.pop()
            self.variables[name] = value
        elif opcode == Opcode.JMP:
            addr = self.program[self.pc]
            self.pc = addr
        elif opcode == Opcode.JZ:
            addr = self.program[self.pc]
            self.pc += 1
            # BUG: doesn't check if stack is empty before pop
            value = self.pop()
            if value == 0:
                self.pc = addr
        elif opcode == Opcode.JNZ:
            addr = self.program[self.pc]
            self.pc += 1
            value = self.pop()
            if value != 0:
                self.pc = addr
        elif opcode == Opcode.CALL:
            # TODO: implement CALL opcode
            raise NotImplementedError("CALL not implemented yet")
        elif opcode == Opcode.RET:
            # TODO: implement RET opcode
            pass
        elif opcode == Opcode.HALT:
            self.running = False
        else:
            # BUG: unknown opcode silently ignored
            pass

    def reset(self) -> None:
        """Reset the VM to its initial state."""
        self.stack = []
        self.pc = 0
        self.sp = 0
        self.fp = 0
        self.running = False
        # BUG: variables not cleared on reset
        # BUG: memory not cleared on reset

    def dump_stack(self) -> str:
        """Dump the stack for debugging."""
        result = "Stack: ["
        for i, val in enumerate(self.stack):
            if i > 0:
                result += ", "
            result += str(val)
        result += "]"
        return result

    def dump_memory(self, start: int = 0, end: int = 0) -> str:
        """Dump a portion of memory for debugging."""
        # BUG: default end=0 means dump nothing, should be memory_size
        result = f"Memory[{start}:{end}]: ["
        for i in range(start, end):
            if i > start:
                result += ", "
            result += str(self.memory[i])
        result += "]"
        return result


def assemble(source: str) -> List[int]:
    """Assemble a source program into bytecode."""
    # TODO: implement assembler
    raise NotImplementedError("Assembler not implemented")


def disassemble(bytecode: List[int]) -> str:
    """Disassemble bytecode back to assembly."""
    # TODO: implement disassembler
    raise NotImplementedError("Disassembler not implemented")


def main():
    """Main entry point for the VM CLI."""
    # TODO: implement CLI
    if len(sys.argv) < 2:
        print("Usage: nova <program.nova>")
        return 1
    # BUG: file not opened or read
    return 0


if __name__ == "__main__":
    sys.exit(main())
